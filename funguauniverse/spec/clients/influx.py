import time
from influxdb import InfluxDBClient

class InfluxDBBuilder(object):
    def __init__(self, host="localhost", port=8086, precision='s', user="root", password="root"):
        self.host = host
        self.port = port
        self.precision = precision
        self.set_flag = False
        self.user = user
        self.password = password
        self.current_tag_list = {}
        self.database = "example"
        self.measurement = "measurement"
        self.client = None
    
    def reset_tags(self):
        self.current_tag_list = {}
    
    def reset(self):
        """ Reset the host for the influxdb """
        self.set_flag = True
        
        self.client = InfluxDBClient(self.host, self.port, self.user, self.password)
        self.client.create_database(self.database)
        return self
    
    

    def check_set(self):
        """Calls the reset option if it hasn't been set yet"""
        if self.set_flag == False:
            self.reset()
        self.client.switch_database(self.database)
        return self
    
    def set_user_information(self, user="root", password="root"):
        self.user = user
        self.password = password
        return self
    
    def set_db(self, name="database"):
        self.database = name
        return self
    
    def set_measurement(self, measurement="metric_name"):
        """Add a measurement name"""
        self.measurement = measurement
        return self
    
    def add_tag(self, key, value):
        self.current_tag_list[key] = value
        return self
    
    def json_builder(self, fields:dict, timestamp:float):
        return [{
            "measurement": self.measurement,
            "tags": self.current_tag_list,
            "time": int(timestamp),
            "fields": fields
        }]
    
    def write(self, fields, timestamp=None):
        if timestamp is None:
            timestamp=time.time()
        self.check_set()
        save_json = self.json_builder(fields=fields, timestamp=timestamp)
        self.client.write_points(save_json, time_precision=self.precision)
        return self
    
    def query(self, search_string):
        self.check_set()
        return self.client.query(search_string)