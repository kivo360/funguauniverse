import json
import time
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from loguru import logger



class MemoryService(object):
    def __init__(self, host="0.0.0.0", port=8500, is_ssl=False):
        protocol = "http"
        if is_ssl == True:
            protocol = "https"
        self.call_variable = f"{protocol}://{host}:{port}"
        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=100))

    def store_action(self, percentage, decision, price, pair, episode=None, setid=None, is_live=False):
        """ Returns the latest price for a pair"""
        
        logger.info(f"Storing action for coin: {pair}")
        try:
            return self._send({
                "call": "basic/store/actions",
                "data": {
                    "percentage": percentage,
                    "decision": decision,  # Will try grabbing from live if it's None
                    "price": price,
                    "spec": {
                        "pair": pair,
                        "live": is_live,
                        "episode": episode,
                        "setid": setid
                    }
                    
                }
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }

    def store_reward(self, reward, entity, pair, episode=None, setid=None, is_live=False):
        """ Returns the latest price for a pair"""
        logger.info(f"Storing reward for coin: {pair} -- with entity: {entity}")
        try:
            return self._send({
                "call": "basic/store/rewards",
                "data": {
                    "reward": reward,
                    "entity": entity,
                    "spec": {
                        "pair": pair,
                        "live": is_live,
                        "episode": episode,
                        "setid": setid
                    }
                }
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }
    

    def query_reward(self, entity, pair, episode=None, setid=None, is_live=False):
        """ Returns the latest price for a pair"""
        print("Get the single latest price")
        try:
            return self._send({
                "call": "basic/query/rewards",
                "data": {
                    "entity": entity,
                    "spec": {
                        "pair": pair,
                        "live": is_live,
                        "episode": episode,
                        "setid": setid
                    }
                    
                }
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }


    def query_action(self, pair, episode=None, setid=None, is_live=False):
        """ Returns the latest price for a pair"""
        print("Get the single latest price")
        try:
            return self._send({
                "call": "basic/query/actions",
                "data": {
                    "spec": {
                        "pair": pair,
                        "live": is_live,
                        "setid": setid,
                        "episode": episode
                    }
                    
                }
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }


    def log_counterfactual(self, covariate, instrument, treatment, pair, bartime=time.time(), episode=None, setid=None, is_live=False):
        counterfactual_json = {
            "covariance": covariate,
            "instruments": instrument,
            "treatment": treatment,
            "bartime": bartime,
            "spec": {
                "pair": pair,
                "live": is_live,
                "setid": setid,
                "episode": episode
            }
        }

        try:
            return self._send({
                "call": "counterfact/store",
                "data": counterfactual_json
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }

    def log_outcome(self, outcome, entity, pair, bartime=time.time(), episode=None, setid=None, is_live=False):
        counterfactual_json = {
            "outcome": outcome,
            "entity": entity,
            "bartime": bartime,
            "spec": {
                "pair": pair,
                "live": is_live,
                "setid": setid,
                "episode": episode
            }
        }

        try:
            return self._send({
                "call": "counterfact/store/outcome",
                "data": counterfactual_json
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }
    
    def query_outcome(self, entity, pair, max_num=50, episode=None, setid=None, is_live=False):
        outcome_json = {
            "entity": entity,
            "max_num": max_num,
            "spec": {
                "pair": pair,
                "live": is_live,
                "setid": setid,
                "episode": episode
            }
        }

        try:
            return self._send({
                "call": "counterfact/query/all",
                "data": outcome_json
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }

    def _send(self, call_info: dict):
        call = call_info.get("call")
        data = call_info.get("data")
        assert call is not None
        assert data is not None

        concatenated_call = self.call_variable + f"/{call}"
        
        resp = self.session.post(concatenated_call, json=data)
        return resp