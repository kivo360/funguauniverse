from featman import Features


class StoreItem(object):
    """
        # StoreItem
        ---
        Save and load an item with dynamic programming
    """
    def __init__(self, *args, **kwargs):
        pass


    def save(self, id, obj):
        # Save the item
        raise NotImplementedError
    
    def load(self, id):
        raise NotImplementedError



