import sys
import ast
import uuid
import time
import base64
import threading
from funguauniverse import StoreItem
from loguru import logger
from spaceman import Spaceman
from hashlib import sha1
config = {
    "handlers": [
        {"sink": sys.stdout, "format": "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"},
    ],
    "extra": {"user": "someone"}
}
logger.configure(**config)


class MemoizeAndOperate(StoreItem, threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.interval = kwargs.get("interval", 3)
        self.mongo_host = kwargs.get("mongo_host")
        self.is_lock = kwargs.get("is_lock", True)
        self.reg_dict = {}
        self.timestamp_record = {}
        self.query_lookup_table = {}
        self.bgprocess = threading.Thread(
            target=self._run, name='bgprocess', daemon=True)
        self.bgprocess.start()
        self.space = Spaceman(mongo_host=self.mongo_host)
        self.daemon = True

    def filter_query(self, query: dict):
        assert query.get("type") is not None
        assert isinstance(query['type'], str)

    def set_item(self, query: dict, item, **kwargs):
        self.filter_query(query)
        if self.is_lock == True:
            with self.lock:
                is_overwrite = kwargs.get("overwrite", False)
                storage_string = self.hash_dict(query)
                # Add feature to check if we should overwrite
                if is_overwrite == True:
                    self.reg_dict[storage_string] = item
                    return

                if self.reg_dict.get(storage_string, None) is None:
                    self.reg_dict[storage_string] = item
        else:
            is_overwrite = kwargs.get("overwrite", False)
            storage_string = self.hash_dict(query)
            # Add feature to check if we should overwrite
            if is_overwrite == True:
                self.reg_dict[storage_string] = item
                return

            if self.reg_dict.get(storage_string, None) is None:
                self.reg_dict[storage_string] = item

    def get_item(self, query_dict: dict):
        self.filter_query(query_dict)
        if self.is_lock == True:
            with self.lock:
                storage_string = self.hash_dict(query_dict)
                item = self.reg_dict.get(storage_string, None)
                # Set that an item was touched

                self.timestamp_record[storage_string] = time.time()
                return item
        else:
            storage_string = self.hash_dict(query_dict)
            item = self.reg_dict.get(storage_string, None)
            self.timestamp_record[storage_string] = time.time()
            return item

    def hash_dict(self, query_dict: dict):
        # Updated hash for consistency between runs
        qhash = sha1(repr(sorted(query_dict.items())).encode()).hexdigest()
        self.query_lookup_table[qhash] = query_dict
        return qhash

    def query_by_hash(self, _hash):
        query_dict = self.query_lookup_table.get(_hash, None)
        return query_dict

    def dict_to_b64(self, query_dict: dict):
        qstring = str(query_dict)
        encoded = qstring.encode()
        byteb64 = base64.b64encode(encoded)
        return byteb64.decode("utf-8")

    def b64_to_dict(self, bstring: str):
        bstring_decoded = bstring.encode()
        decoded_base = base64.b64decode(bstring_decoded)
        decoded_string = decoded_base.decode()
        return ast.literal_eval(decoded_string)

    def background_operation(self):
        reg_keys = list(self.reg_dict.keys())
        for rk in reg_keys:
            latest_update = time.time()
            # self.timestamp_record[rk] = latest_update
            b64key = self.b64_to_dict(rk)
            # We would use this dict to load the most recent model.
            logger.info(f"Processing Keys: {rk}", enqueue=True)

    def _run(self):
        while True:
            self.background_operation()
            time.sleep(self.interval)

    def save(self):
        raise NotImplementedError(
            "Ensure to use this function to save the model")

    def load(self):
        raise NotImplementedError(
            "Ensure to implement this function to load the models you have")


if __name__ == "__main__":
    memop = MemoizeAndOperate(interval=0.07)
    latest_hex = uuid.uuid4().hex
    for i in range(100):
        memop.set_item({"eid": latest_hex}, 1)
        latest = memop.get_item({"eid": latest_hex})
        latest += 1
        memop.set_item({"eid": latest_hex}, latest, overwrite=True)
        print(latest)
        time.sleep(0.01)
