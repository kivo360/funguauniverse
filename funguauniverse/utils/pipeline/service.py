import json
import random
import threading
import time
from multiprocessing import Queue


from loguru import logger
import pandas as pd
import numpy as np

"""
    Acceptable Log Type
"""

class BaseService(object):
    """ 
        # Base Service 
        ---
        Here we run a base service. All services that inherit the class should work on the following methods to make it individualized:
            - `process`: Any
                - the `process` method takes the latest item added to the queue and does work on it. 
                This method is empty. Generally, you'd want to do all of the heavy lifting here.

            - `process_condition`: bool
                - The `process_condition` checks to see if a given condition has been met before processing the given variable. 
                This is good for the times when theres dependencies on previous processes that need to be syncronized
    """
    def __init__(self, result_queue, *args, **kwargs):
        self.main_queue = Queue()
        self.result_queue = result_queue
        
        # OPTIONAL VARIABLES (through kwargs)
        self.interval = kwargs.get("interval", 0.005)
        self.is_event_queue = kwargs.get("is_event_queue", False)
        self.event_queue = kwargs.get("event_queue", None)
        self.next_event_type = kwargs.get("next_ev_type", None)
        is_immediate = kwargs.get("is_immediate", True)

        
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True                            # Daemonize thread
        
        
        if is_immediate:
            self.thread.start()  # Start the execution

    

    def set_settings(self, **kwargs):
        """
            # Change Settings
            ---
            Optionally have the opprotunity to change any of the required variables for the class
        """
        _event_queue = kwargs.get("event_queue", None)
        _is_event_queue = kwargs.get("is_event_queue", None)
        _interval = kwargs.get("interval", None)
        _next_event_type = kwargs.get("next_ev_type", None)

        if self.crt(_event_queue, [Queue]):
            self.event_queue = _event_queue
        
        if self.crt(_is_event_queue, [bool]):
            self.is_event_queue = _event_queue
        
        if self.crt(_interval, [int, float]):
            self.interval = _interval
        
        if self.crt(_next_event_type, [str]):
            self.next_event_type = _next_event_type





    def push(self, item):
        """
            Push an item with the acceptable types into the main queue to be processed.

            Most specifically, we should have a blacklist of types to add
        """
        if item is None:
            logger.debug("We don't accept None types inside of the queue. ")
        
        self.main_queue.put(item)
        
    def process(self):
        """ 
            # Generic Processing
            ---
            It pulls from the main queue then processes everything that we'll need inside of the given activity.
            Keep the components of processing.

            Ensure to overload this with each run.
        """
        
        # logger.info("SUCK DICK BITCH")
        # print("Is it working?")

    def process_condititon(self):
        return True

    def run(self):
        while True:
            # item = self.__get_latest_from_queue()
            self.process()
            # logger.error(item)
            time.sleep(self.interval)

    def start(self):
        """
            Start thread if it's not immediate
        """
        if not self.thread.isAlive():
            self.thread.start()

    def get_latest_from_queue(self):
        """ Get the latest item from the message queue """
        is_empty = self.main_queue.empty()
        if not is_empty:
            __i = self.main_queue.get()
            # logger.error(__i)
            return __i
        return None

    def __check_none(self, item):
        if item is None:
            return False
        return True

    def __check_event_queue(self):
        if (self.is_event_queue == True) and (self.event_queue is None):
            return False
        elif (self.is_event_queue == True) and (self.event_queue is not None):
            return True
        elif (self.is_event_queue == False):
            return True
    
    def crt(self, item, types_list: list):
        """
            # Check Required Types
            ---
            Check the required types for the given variable

        """
        if item is None:
            return False

        item_type = type(item)
        if item_type in types_list:
            return True
        return False
