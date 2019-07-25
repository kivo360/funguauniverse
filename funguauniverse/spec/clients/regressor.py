import json
from loguru import logger

from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession



class PriceService(object):
    def __init__(self, host="0.0.0.0", port=8500):
        self.call_variable = f"http://{host}:{port}"
        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))

    def get_single(self, pair, episode=None, is_live=False):
        """ Returns the latest price for a pair"""
        print("Get the single latest price")
        try:
            return self._send({
                "call": "price/get_single",
                "data": {
                    "coinname": pair,
                    "episode": episode,  # Will try grabbing from live if it's None
                    "limit": 250,
                    "is_live": is_live
                }
            })
        except Exception:
            logger.error("Call Failed - get_single")
            return {
                "data": {}
            }

    def get_single_before(self, pair, episode=None, is_live=False):
        """ Returns the latest price for a pair"""
        print("Get the latest prices")
        try:
            return self._send({
                "call": "price/get_single_before",
                "data": {
                    "coinname": pair,
                    "episode": episode,  # Will try grabbing from live if it's None
                    "limit": 250,
                    "is_live": is_live
                }
            })
        except Exception:
            logger.error("Call Failed - get_single_before")
            return {
                "data": {}
            }

    def get_multi(self, pair, episode=None, is_live=False):
        # get_multi
        try:
            # Will try grabbing from live if it's None
            return self._send({
                "call": "price/get_multi",
                "data": {
                    "coinname": pair,
                    "episode": episode,
                    "limit": 250,
                    "is_live": is_live
                }
            })
            
        except Exception:
            logger.error("Call Failed - get_multiple_prices")
            return {
                "data": {}
            }

    def add_single(self, pair, price_bar, episode=None, is_live=False):
        try:
            return self._send({
                "call": "price/set_single",
                "data": {
                    "single": {
                        "coinname": pair,
                        "bar": price_bar
                    },
                    "episode": episode,  # Will try grabbing from live if it's None
                    "is_live": is_live
                }
            })
        except Exception:
            logger.error("Call Failed - multiple_prices")
            return {
                "data": {}
            }

    def add_multi(self, pair, price_bars, episode=None, is_live=False):
        try:
            return self._send({
                "call": "price/set_multi",
                "data": {
                    "multi": {
                        "coinname": pair,
                        "bars": price_bars
                    },
                    "episode": episode,  # Will try grabbing from live if it's None
                    "is_live": is_live
                }
            })
        except Exception:
            logger.error("Call Failed - add_multiple_prices")
            return {
                "data": {}
            }

    def _send(self, call_info: dict):
        call = call_info.get("call")
        data = call_info.get("data")
        assert call is not None
        assert data is not None

        concatenated_call = self.call_variable + f"/{call}"
        call_params_json = json.dumps(data)
        resp = self.session.post(concatenated_call, json=call_params_json)
        return resp
