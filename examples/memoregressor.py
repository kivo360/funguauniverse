import time
import uuid
import random
import numpy as np
from copy import copy

from funguauniverse import MemoizeAndOperate
from funguauniverse import start_service
from sklearn.linear_model import PassiveAggressiveRegressor

from sklearn.datasets import make_regression


class MemoryPassiveRegressor(MemoizeAndOperate):
    """ A class for online learning using the passive aggressive regressor """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize(self, query:dict, **kwargs):
        existing_model = self.load(query)
        if existing_model is None:
            self.set_item(query, PassiveAggressiveRegressor(
                max_iter=1000), overwrite=False)
        else:
            self.set_item(query, existing_model, overwrite=False)
    
    def check_and_load(self, query):
        q = copy(query)
        _hash = self.hash_dict(q)
        _keys = list(self.reg_dict.keys())
        if _hash not in _keys:
            self.initialize(query)

    def train(self, query: dict, X, y, **kwargs):
        # Partially train the passive aggressive regressor
        # print(self.hash_dict)
        self.check_and_load(query)
        try:
            regressor = self.get_item(query)
            regressor.partial_fit(X, y)
            self.set_item(query, regressor, overwrite=True)
            return "DONE"
        except Exception as e:
            print(str(e))
            pass
        
    
    def predict(self, query:dict, X, **kwargs):
        # Predict the score of the regression algorithm for the data `x`
        print(self.query_lookup_table)
        self.check_and_load(query)
        try:
            regressor = self.get_item(query)
            prediction = regressor.predict(X)
            return prediction
        except Exception as e:
            return []
        
    def score(self, query, X, y, **kwargs):
        # Generate the score for the model in X and Y
        # print(self.query_lookup_table)
        self.check_and_load(query)
        try:
            regressor = self.get_item(query)
            score = regressor.score(X, y)
            return score
        except Exception as e:
            print(str(e))
            return 0.0
    
    def background_operation(self):
        reg_keys = list(self.reg_dict.keys())
        for rk in reg_keys:
            latest_update = time.time()
            
            hash_query = self.query_by_hash(rk)
            self.save(hash_query, self.reg_dict[rk])
            time.sleep(0.05)
    
    # TODO: Add prune example

    # def prune(self):
    #     # Prune the latest keys
    #     self.timestamp_record
    #     pass

    def save(self, query:dict, obj):
        q = copy(query)
        with self.space as space:
            space.store(obj, query=q, current_time=True)

    def load(self, query:dict):
        q = copy(query)
        try:
            with self.space as space:
                item = space.load(query=q)
                return item
        except Exception:
            return None
        



if __name__ == "__main__":
    memes = MemoryPassiveRegressor()
    print(memes)
    start_service(memes, "localhost", 5581)



