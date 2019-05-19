import threading



class GenericHub(object):
    """ Hubs help create conditional locks. Use as a form of dynamic programming """
    def __init__(self, *args, **kwargs):
        self.action_log = {}
        self.lock = threading.Lock()

    def create(self, _id: str):
        with self.lock:
            self.action_log[_id] = []

    def push(self, _id: str, state_name: str):
        if isinstance(state_name, str):
            with self.lock:
                self.action_log[_id].append(_id)

    def get(self, _id: str):
        hub_obj = self.action_log.get(_id, None)
        if hub_obj is None:
            raise AttributeError(f"Item With Id: {_id} doesn't exist")
        
        return hub_obj
    
    def get_last(self, _id: str):
        hub_obj = self.action_log.get(_id, None)
        if hub_obj is None:
            raise AttributeError(f"Item With Id: {_id} doesn't exist")

        if len(hub_obj) == 0:
            raise IndexError(f"Item with Id: {_id}. Doesn't have any items. ")

        return hub_obj[-1]




# threading.active_count() 
# 
