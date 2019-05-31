import time
import uuid
import random
import numpy as np

from funguauniverse.utils.web.serviceclient import ServiceClient
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression

class MemoryRegressorClient(ServiceClient):
    def initialize(self, query, **kwargs):
        # You should put the settings of the regressor into kwargs. This would be things like the length of memory
        # The memory should be short for non-stationary predictions
        res = self._send({
            "command": "initialize",
            "args": [query],
            "kwargs": kwargs
        })
        return res


    def train(self, query, X, y):
        trained_response = self._send({
            "command": "train",
            "args": [query, X, y],
            "kwargs": {}
        })
        return trained_response
    
    def score(self, query, X, y):
        model_score = self._send({
            "command": "score",
            "args": [query, X, y],
            "kwargs": {}
        })
        return model_score
    
    def predict(self, query, X):
        prediction = self._send({
            "command": "predict",
            "args": [query, X],
            "kwargs": {}
        })
        return prediction


if __name__ == "__main__":
    client = MemoryRegressorClient()
    base_fake_model = query_obj = {
        "type": "fakemodel",
        "coin": "BTC_USD",
        "eid": uuid.uuid4().hex
    }

    start = time.time()
    for _ in range(5):
    
        X, y = make_regression(n_features=4, n_samples=1000, random_state=1)
        splitsX = np.split(X, 4)
        splitsy = np.split(y, 4)
        client.initialize(base_fake_model)

        for _ in range(len(splitsX)):
            _X = splitsX[_]
            _y = splitsy[_]
            X_train, X_test, y_train, y_test = train_test_split(
                _X, _y, test_size=0.1, random_state=0)
            client.train(base_fake_model, X_train, y_train)
            score = client.score(base_fake_model, X_test, y_test)
            # print(score)

            prediction = client.predict(base_fake_model, X_test)
            print(prediction.get("data", None))
    end = time.time()
    print(end-start)