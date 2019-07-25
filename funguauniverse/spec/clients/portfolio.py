import random
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import json
import dask.bag as db
import numpy as np
import pandas as pd



from requests_futures.sessions import FuturesSession











class PortfolioClient(object):
    """ 
        # Portfolio Client
        ---
        This is a single portfolio client. 
        We use it to test the flow through the pipeline.


        After the first trial, work to move multi-users.

        ### The Official Order
        ---
        **Create User** -> **Determine Order** -> **Send Order** -> **(Get User Stats | Get Performance)** -> **Update Context Service** -> **Get Context For Reward**
    """
    def __init__(self, host="0.0.0.0", port=9005):
        # self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))
        self.session = FuturesSession(ThreadPoolExecutor(max_workers=1000))
        self.address = f"http://{host}:{port}"

    def create_user(self, userid, exchange="baseexchange", is_live=False, episode=None):
        create_call = "/portfolio/create"
        call_loc = f"{self.address}{create_call}"

        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            }
        }
        call_params_json = json.dumps(call_params)
        self.session.post(call_loc, data=call_params_json)



    def get_user(self, userid, exchange="baseexchange", is_live=False, episode=None):
        create_call = "/portfolio/get"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            }
        }

        call_params_json = json.dumps(call_params)

        response = self.session.post(call_loc, data=call_params_json)
        return response.result()
    

    def get_performance(self, userid, exchange="baseexchange", is_live=False, episode=None):
        create_call = "/portfolio/performance"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            }
        }

        call_params_json = json.dumps(call_params)

        response = self.session.post(call_loc, data=call_params_json)
        return response.result()
    

    def update_user(self, userid, exchange="baseexchange", is_live=False, episode=None, timestamp=time.time()):
        create_call = "/portfolio/update"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            },
            "timestamp": timestamp
        }

        call_params_json = json.dumps(call_params)

        response = self.session.post(call_loc, data=call_params_json)
        return response
        


    def get_user_stats(self, userid, exchange="baseexchange", is_live=False, episode=None):
        create_call = "/portfolio/stats"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            }
        }
        call_params_json = json.dumps(call_params)

        response = self.session.post(call_loc, data=call_params_json)
        return response.result()
    

    def send_order(self, 
            userid:int, percentage:float, order_type:str,
            base:str, trade:str, price:float, exchange="baseexchange", 
            is_live=False, episode=None, timestamp=time.time()):
        """
            print(userid)
            print(percentage)
            print(order_type)
            print(base)
            print(trade)
            print(price)
            print(exchange)
            print(is_live)
            print(episode)
            print(timestamp)
        """
        create_call = "/order/send"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "base": base,
            "trade": trade,
            "exchange": exchange,
            "pct": percentage,
            "action": order_type,
            "price": price,
            "spec": {
                "episodeid": episode,
                "live": is_live
            },
            "timestamp": timestamp
        }
        call_params_json = json.dumps(call_params)
        self.session.post(call_loc, data=call_params_json)

    def user_allocation(self, userid, assets, exchange="baseexchange", is_live=False, episode=None):
        
        create_call = "/portfolio/allocate"
        call_loc = f"{self.address}{create_call}"
        call_params = {
            "userid": userid,
            "exchange": exchange,
            "spec": {
                "episodeid": episode,
                "live": is_live
            },
            "assets": assets
        }
        call_params_json = json.dumps(call_params)
        self.session.post(call_loc, data=call_params_json)
    # TODO: Get coin status for a given user
    # We can use that for 5-10 users concurrently
    # The switch from there will be integrating with the existing calls we have
    # Test the environment with one user first. Prepare to add other users into the mix as well
    # After you get the portoflio and context manager worked out, move forward

if __name__ == "__main__":
    # Test Calls
    episode_eid = uuid.uuid4().hex
    userid = 6000
    portfolio_client = PortfolioClient()
    for _ in range(1000):
        portfolio_client.create_user(_, is_live=False, episode=episode_eid)
        # user = portfolio_client.get_user(_, is_live=False, episode=episode_eid)
        # performance = portfolio_client.get_performance(_, is_live=False, episode=episode_eid)
        order_type = random.choice(["BUY", "HOLD", "SELL"])
        random_price = random.uniform(100, 1000)
        portfolio_client.send_order(
            userid=_,
            percentage=random.uniform(0, 1),
            order_type=order_type,
            base="USD",
            trade="BTC",
            price=random_price,
            exchange="backtest",
            is_live=False,
            episode=episode_eid
        )
        
        # stats = portfolio_client.get_user_stats(userid, is_live=False, episode=episode_eid)
        # print(stats.json())
    # print(user.json())
    # print(performance.json())
    # print("----------")
    # print("----------")
    # print(stats.json())
    
    
