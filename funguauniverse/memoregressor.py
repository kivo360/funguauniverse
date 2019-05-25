# Create a memorization for the general sklearn regressor type
# Use to run multiple sessions of regression at once
import time
import uuid
import random
import numpy as np
from multiprocessing.managers import BaseManager

from funguauniverse import MemoizeAndOperate
from sklearn.linear_model import PassiveAggressiveRegressor

from sklearn.datasets import make_regression


class MemoryPassiveRegressor(MemoizeAndOperate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize(self, query:dict, regressor_type="regressor"):
        existing_model = self.load(query)
        if existing_model is None:
            self.set_item(query, PassiveAggressiveRegressor(
                max_iter=100), overwrite=False)
        else:
            print("Loaded Model")
            self.set_item(query, existing_model, overwrite=False)
            

    def train(self, query: dict, X, y):
        # Partially train the passive aggressive regressor
        try:
            regressor = self.get_item(query)
            regressor.partial_fit(X, y)
            self.set_item(query, regressor, overwrite=True)
        except Exception as e:
            print(str(e))
            pass
        
    
    def predict(self, query:dict, X):
        # Predict the score of the regression algorithm for the data `x`
        try:
            regressor = self.get_item(query)
            prediction = regressor.predict(X)
            return prediction
        except Exception as e:
            return []
        

    def score(self, query, X, y):
        # Generate the score for the model in X and Y
        try:
            regressor = self.get_item(query)
            score = regressor.score(X, y)
            return score
        except Exception as e:
            print(e)
            return 0.0
    
    def background_operation(self):
        reg_keys = list(self.reg_dict.keys())
        for rk in reg_keys:
            latest_update = time.time()
            self.timestamp_record[rk] = latest_update
            b64key = self.b64_to_dict(rk)
            self.save(b64key, self.reg_dict[rk])
            time.sleep(0.5)
            # self.load(b64key)
            print("Saving Models")
            # We would use this dict to load the most recent model.
            # logger.info(f"Processing Keys: {rk}", enqueue=True)
    def save(self, query:dict, obj):
        with self.space as space:
            space.store(obj, query=query, current_time=True)

    def load(self, query:dict):
        try:
            with self.space as space:
                item = space.load(query=query)
                return item
        except Exception:
            return None
        

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


class MyManager(BaseManager):
    pass



if __name__ == "__main__":
    
    # mem_regressor.initialize()
    # mem_regressor.train(query, trainX, trainY) # Assume the default is PassiveAggressiveRegressor
    # mem_regressor.test(query, textX, testY)
    # mem_regressor.predict(query, data)
    from sklearn.model_selection import train_test_split
    base_fake_model = query_obj = {
        "type": "fakemodel",
        "coin": "BTC_USD",
        "eid": uuid.uuid4().hex
    }
    mem_regressor = MemoryPassiveRegressor()
    MyManager.register('Maths', MemoryPassiveRegressor)
    with MyManager() as manager:
        maths = manager.Maths()
        print(maths)

    mem_regressor.initialize(base_fake_model)
    # index = 0
    X, y = make_regression(n_features=4, n_samples=1000, random_state=1)
    
    splitsX = np.split(X, 4)
    splitsy = np.split(y, 4)
    # print(splitsX)

    for _ in range(len(splitsX)):
        _X = splitsX[_]
        _y = splitsy[_]
        X_train, X_test, y_train, y_test = train_test_split(
            _X, _y, test_size=0.1, random_state=0)
        mem_regressor.train(base_fake_model, X_train, y_train)
        score = mem_regressor.score(base_fake_model, X_test, y_test)
        # print(score)
        
        prediction = mem_regressor.predict(base_fake_model, X_test)
        print(prediction)
        # print(y_train)

    
    # 
    

    # for i in range(len(X_train)):
    #     _X = X_train[i]
    #     _y = y_train[i]
    #     mem_regressor.train(
    #         base_fake_model, (_X.reshape(-1, 1)), _y)
        
    # mem_regressor.train(base_fake_model, X_train, y_train)
    # score = mem_regressor.score(base_fake_model, X_test, y_test)


    
    # print(score)

    # while index < 10000:
    #     pct = random.uniform(0, 1)
    #     if pct > 0.98:
    #         new_hex = uuid.uuid4().hex
    #         query_obj = {
    #             "type": "fakemodel",
    #             "coin": "BTC_USD",
    #             "eid": new_hex
    #         }
    #         mem_regressor.initialize(query_obj)
    #         print("Created Model")
    #         # print(new_hex)
    #     # print(pct)
    #     print("Step Completed")
    #     time.sleep(0.5)
    #     index += 1
