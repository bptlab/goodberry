import asyncio
import logging
import json
import time

class ChangeServer:
    def __init__(self, runner):
        self.runner = runner

    def start_watching(self):
        asyncio.get_event_loop().run_until_complete(self.watch())

    async def watch(self):
        # TODO: implement webserver that waits for input
        i = 0
        while True:
            i += 1
            time.sleep(5)
            logging.info("{'name': 'test', 'device_id': 'default:TestDevice', 'feature': 'nfcwriter', 'property': 'nfcwriter', 'value': 'Test'}")
            self.handle_message('{"name": "test", "device_id": "default:TestDevice", "feature": "nfcwriter", "property": "nfcwriter", "value": "Test"}')

    def handle_message(self, message):
        """
        In case it is an update event for the current device,
        the handle_change method is invoked.
        :param message: a string containing the received event
        :return: (path, value) or None
        """
        try:
            event_data = json.loads(message)
            self.runner.handle_change(event_data)
        except json.JSONDecodeError as e:
            print(e)
            logging.warning("ERROR: {}".format(e.msg))
