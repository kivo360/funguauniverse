import random
import uuid

from featman import Features

class StoreItem(object):
    """
        # StoreItem
        ---
        Allow the user to consistently save and load features with abstractions
    """
    def __init__(self, *args, **kwargs):
        self.features = Features()
    
    def save(self, id, obj):
        # Save the item
        raise NotImplementedError
    
    def load(self, id):
        raise NotImplementedError
