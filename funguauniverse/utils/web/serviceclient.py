import requests
from concurrent.futures import ProcessPoolExecutor
from requests_futures.sessions import FuturesSession
import pickle
from loguru import logger
from requests import Session



class ServiceClient(object):
    """ Call the HTTP Service directly """
    def __init__(self, **kwargs):
        self.host = kwargs.get("address", "localhost")
        self.port = kwargs.get("port", 5581)
        self._address = f"http://{self.host}:{self.port}"
        self.session = FuturesSession(executor=ProcessPoolExecutor(max_workers=10),
                         session=Session())

    def _send(self, data, blocking=True):
        payload = pickle.dumps(data)
        
        response = self.session.post(self._address, data=payload)
        if blocking == True:
            response = response.result()
            if response.status_code != 200:
                logger.error("Request failed {}: {}".format(response.text, data))
            try:
                response.raise_for_status()
                parsed = pickle.loads(response.content)
                return parsed
            except:
                return {}
        else:
            logger.info("async-call", enqueue=True)
        


if __name__ == "__main__":
    serve_command = ServiceClient()
