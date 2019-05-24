# Create a memorization for the general sklearn regressor type
# Use to run multiple sessions of regression at once
import time
import uuid
import random

from funguauniverse import MemoizeAndOperate
from sklearn.linear_model import PassiveAggressiveRegressor

class MemoryPassiveRegressor(MemoizeAndOperate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initialize(self, query:dict, regressor_type="regressor"):
        existing_model = self.load(query)
        if existing_model is None:
            self.set_item(query, PassiveAggressiveRegressor(), overwrite=False)
        else:
            print("Loaded Model")
            self.set_item(query, existing_model, overwrite=False)
            

    def train(self, query: dict, X, y):
        # Partially train the passive aggressive regressor
        try:
            regressor = self.get_item(query)
            regressor.partial_fit(X, y)
            self.set_item(query, regressor, overwrite=True)
        except Exception:
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
        except Exception:
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
        
if __name__ == "__main__":
    
    # mem_regressor.initialize()
    # mem_regressor.train(query, trainX, trainY) # Assume the default is PassiveAggressiveRegressor
    # mem_regressor.test(query, textX, testY)
    # mem_regressor.predict(query, data)
    base_fake_model = query_obj = {
        "type": "fakemodel",
        "coin": "BTC_USD",
        "eid": '15a42a0c43a3412a904aefade93e172e'
    }
    index = 0
    mem_regressor = MemoryPassiveRegressor()
    mem_regressor.initialize(base_fake_model)
    while index < 10000:
        pct = random.uniform(0, 1)
        if pct > 0.98:
            new_hex = uuid.uuid4().hex
            query_obj = {
                "type": "fakemodel",
                "coin": "BTC_USD",
                "eid": new_hex
            }
            mem_regressor.initialize(query_obj)
            print("Created Model")
            # print(new_hex)
        # print(pct)
        print("Step Completed")
        time.sleep(0.5)
        index += 1
