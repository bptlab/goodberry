from connector.connector import Connector
from datetime import datetime


class Component:
    def __init__(self, device_id, **kwargs):
        self.device_id = device_id
        self.connector = Connector()

    @staticmethod
    def get_timestamp():
        return str(datetime.now())
