import uuid
import threading
from threading import Lock


class Event(object):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.get("_type", "MARKET")
        self.eid = kwargs.get("eid", str(uuid.uuid4()))
        self.start_number = 1
        

    
    def set_vars(self, **kwargs):
        """
            # Set Variables
            Set important variables for the user. 
            Key Variables:
                - type: This is the main variable for events
        """
        _type = kwargs.get("_type")
        
        if _type is not None:
            self.type = _type
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
