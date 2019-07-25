import uuid
import requests
import pandas as pd
import sys
from funguauniverse import ServiceClient
from loguru import logger

config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time} - {message}"},
        {"sink": "file.log", "serialize": True},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)


class PreprocessingClient(ServiceClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def ta_prices(self, episode_id, coin, price:pd.DataFrame):
        price_dict = price.to_json(orient='index')
        response = self._gsend("/preprocess/prices", {
            "episode": episode_id,
            "coin": coin,
            "data": price_dict
        })
        return response

    def _gsend(self, route, data):
        """ General Send """
        address = self._address+route
        response = requests.post(address, json=data)
        if response.status_code != 200:
            logger.error("Request failed {}".format(response.text))
        parsed = response.content
        return parsed

if __name__ == "__main__":
    pass
    # assert action.get("pct", None) is not None
    # assert action.get("price", None) is not None
    # assert action.get("coin", None) is not None
    # assert action.get("decision", None) is not None
    # import random
    # import time
    # current_eid = '1dd20719728b49148441bb23c0ff84d7'
    # client = ContextualAwareness(host="localhost", port=9847)
    # client.initialize(current_eid)
    # action = {"pct": 0.2, "price": 270 *
    #           random.normalvariate(0.5, 0.2), "coin": "ETH", "decision": 0.5}
    # timestamp = time.time()
    # client.log_action(current_eid, action, timestamp)

    # start = time.time()
    # index = 0

    # for i in range(1000):
    #     client.log_reward(current_eid, "portfolio", random.normalvariate(
    #         12000, 2000), time.time() + (index * 60))
    # end = time.time()

    # print(end-start)

# eyd0eXBlJzogJ2NvbnRleHQnLCAnZWlkJzogJzA3MjA3M2UxNTcyYzRlOTViNWQ5NTY4MjAxN2NlZjc5J30=
# eyd0eXBlJzogJ2NvbnRleHQnLCAnZWlkJzogJ2MyMzVjZjRlMmIwYjQxZGQ4YjE5ZDBiMDIyMTZkMzY5J30=
