import requests
import pickle
from loguru import logger



class ServiceClient(object):
    """ Call the HTTP Service directly """
    def __init__(self, **kwargs):
        self.host = kwargs.get("address", "localhost")
        self.port = kwargs.get("port", 5581)
        self._address = f"http://{self.host}:{self.port}"

    def _send(self, data):
        payload = pickle.dumps(data)
        response = requests.post(self._address, data=payload)
        if response.status_code != 200:
            logger.error("Request failed {}: {}".format(response.text, data))
        response.raise_for_status()
        parsed = pickle.loads(response.content)
        return parsed

if __name__ == "__main__":
    serve_command = ServiceClient()
