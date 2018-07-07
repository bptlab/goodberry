from datetime import datetime


class Component:
    def __init__(self, device_id, **kwargs):
        self.device_id = device_id

    @staticmethod
    def get_timestamp():
        return str(datetime.now())
