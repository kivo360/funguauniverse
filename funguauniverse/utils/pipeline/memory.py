from abc import ABC
import redis
import ray
# from redis import Redis

class MemoryInterface(ABC):
    def save(self, k, v, overwrite=False):
        raise NotImplementedError("You need to have a way to save information")
    
    def load(self, k):
        raise NotImplementedError("You need to have a way to load information")
    
    def remove(self, k):
        raise NotImplementedError("You need to remove keys")

    def get_keys(self):
        raise NotImplementedError("get_keys must be implemented")

class LocalMemory(MemoryInterface):
    def __init__(self, *args, **kwargs):
        self.local_dict = {}

    def save(self, k, v, overwrite=False):
        self.local_dict[k] = v
    
    def load(self, k):
        if k in self.local_dict:
            return self.local_dict[k]
        raise AttributeError(f"The key {k} doesn't exist")
    
    def remove(self, k):
        if k in self.local_dict:
            del self.local_dict[k]
        raise AttributeError(f"The key {k} doesn't exist")

    def get_keys(self):
        return list(self.local_dict.keys())

class RedisMemory(MemoryInterface):
    def __init__(self, redis_instance:redis.Redis, list_key_name="key_lists", *args, **kwargs):
        self.redis_instance = redis_instance
        self.key_list_name = list_key_name
    
    def save(self, key, val, overwrite=True):
        is_exist = self.redis_instance.get(key)
        if is_exist is not None and overwrite == False:
            return 0
        
        self.redis_instance.set(key, val)
        self.redis_instance.sadd(self.key_list_name, key)
        return 1
    def load(self, key):
        item = self.redis_instance.get(key)
        
        if item is None:
            raise AttributeError("The item does not exist in redis")
        return item
    
    def remove(self, key):
        self.redis_instance.delete(key)
        self.redis_instance.srem(self.key_list_name, key)

    def get_keys(self):
        keys = self.redis_instance.smembers(self.key_list_name)
        if keys is None:
            return []
        return [str(x) for x in keys]

class RemoteMemory(MemoryInterface):
    def __init__(self, remote_obj, *args, **kwargs):
        # The ray remote object should be a memory type. 
        self.ray_remote = remote_obj.remote()
    
    def save(self, k, v, overwrite=False):
        self.ray_remote.save.remote(k, v, overwrite)
    
    def load(self, key):
        return ray.get(self.ray_remote.load.remote(key))

    def remove(self, key):
        self.ray_remote.remove.remote(key)

    def get_keys(self):
        return ray.get(self.ray_remote.get_keys.remote())


if __name__ == "__main__":
    pass