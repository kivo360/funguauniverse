from abc import ABC
import redis
import ray
import maya
# from redis import Redis

class MemoryInterface(ABC):
    def save(self, k, v, overwrite=False):
        raise NotImplementedError("You need to have a way to save information")
    
    def load(self, k):
        raise NotImplementedError("You need to have a way to load information")
    
    def remove(self, k):
        raise NotImplementedError("You need to remove keys")
    
    def get_latest_time(self, k):
        raise NotImplementedError(f"You need to be able to get the latest time of the given {k}")
    
    def set_query_by_hash(self, k, query):
        raise NotImplementedError("You need to set an access query by hash")
    

    def get_query_by_hash(self, k):
        raise NotImplementedError("You need to get an access query by hash")

    def get_keys(self):
        raise NotImplementedError("get_keys must be implemented")

class LocalMemory(MemoryInterface):
    def __init__(self, *args, **kwargs):
        self.local_dict = {}
        self.timestamp_dict = {}
        self.query_lookup_table = {}

    def save(self, k, v, overwrite=False):
        is_exist = self.local_dict.get(k, None)
        current_epoch = maya.now().epoch
        if overwrite:
            self.local_dict[k] = v
            self.timestamp_dict[k] = current_epoch
            return 1
        else:
            if is_exist is None:
                self.local_dict[k] = v
                self.timestamp_dict[k] = current_epoch
                return 1
        return 0
    
    def load(self, k):
        if k in self.local_dict:
            current_epoch = maya.now().epoch
            self.timestamp_dict[k] = current_epoch
            return self.local_dict[k]
        raise AttributeError(f"The key {k} doesn't exist")
    
    
    def get_latest_time(self, k):
        if k in self.timestamp_dict:
            return self.timestamp_dict[k]
        raise AttributeError(f"The key {k} doesn't exist")


    def remove(self, k):
        if k in self.local_dict:
            del self.local_dict[k]
            del self.timestamp_dict[k]
        raise AttributeError(f"The key {k} doesn't exist")


    def get_keys(self):
        return list(self.local_dict.keys())


    def set_query_by_hash(self, k, query:dict):
        self.query_lookup_table[k] = query
    
    
    def get_query_by_hash(self, k):
        return self.query_lookup_table.get(k, None)

class RedisMemory(MemoryInterface):
    def __init__(self, redis_instance:redis.Redis, list_key_name="key_lists", *args, **kwargs):
        self.redis_instance = redis_instance
        self.key_list_name = list_key_name
    
    def save(self, key, val, overwrite=True):
        is_exist = self.redis_instance.get(key)
        if is_exist is not None and overwrite == False:
            return 0
        
        current_epoch = maya.now().epoch
        self.redis_instance.set(key, val)
        self.redis_instance.set(f"{key}:timestamp", current_epoch)
        self.redis_instance.sadd(self.key_list_name, key)
        return 1
    def load(self, key):
        current_epoch = maya.now().epoch
        item = self.redis_instance.get(key)
        self.redis_instance.set(f"{key}:timestamp", current_epoch)
        if item is None:
            raise AttributeError("The item does not exist in redis")
        return item
    


    def remove(self, key):
        self.redis_instance.delete(key)
        self.redis_instance.delete(f"{key}:timestamp")
        self.redis_instance.srem(self.key_list_name, key)

    def get_keys(self):
        keys = self.redis_instance.smembers(self.key_list_name)
        if keys is None:
            return []
        return [str(x) for x in keys]

    def get_latest_time(self, key):
        item = self.redis_instance.get(f"{key}:timestamp")
        if item is None:
            raise AttributeError("The item does not exist in redis")
        return item
    
    def set_query_by_hash(self, k, query:dict):
        self.redis_instance.set(f"{k}:query", query)
    
    def get_query_by_hash(self, k):
        return self.redis_instance.get(k)

class RemoteMemory(MemoryInterface):
    def __init__(self, remote_obj, *args, **kwargs):
        # The ray remote object should be a memory type. 
        # The ray remote memory should have roughly the same interface as the LocalMemory
        self.ray_remote = remote_obj.remote()
    
    def save(self, k, v, overwrite=False):
        self.ray_remote.save.remote(k, v, overwrite)
    
    def load(self, key):
        return ray.get(self.ray_remote.load.remote(key))

    def remove(self, key):
        self.ray_remote.remove.remote(key)

    def get_keys(self):
        return ray.get(self.ray_remote.get_keys.remote())
    
    def get_latest_time(self, key):
        return ray.get(self.ray_remote.get_latest_time.remote())

    def set_query_by_hash(self, k, query:dict):
        ray.get(self.ray_remote.set_query_by_hash.remote(k, query))
    
    def get_query_by_hash(self, k):
        return ray.get(self.ray_remote.get_query_by_hash.remote())

if __name__ == "__main__":
    pass