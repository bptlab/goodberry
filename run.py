import sys
from http.server import HTTPServer

from threading import Thread

from connector.event_listener import EventListener
from connector.event_subscriber import EventSubscriber
from device import Device
import utils
from setup import main as setup


class Run:
    def __init__(self):
        self.logger = utils.get_logger(__name__)
        try:
            self.device = Device()
        except Exception:
            sys.exit(1)
        self.device.load_settings()
        self.observer = self.device.get_observers()
        self.actions = self.device.get_actions()
        self.logger.info("Loaded " + str(len(self.observer)) + " observer(s) and " + str(len(self.actions)) + " action(s).")

    def run(self):
        self.start_observers()
        EventSubscriber(self.device).subscribe()
        self.start_event_listener_wrapper()

    def start_observers(self):
        self.logger.info("Starting observers...")
        for observer_name, observer_object in self.observer.items():
            self.logger.info("Starting " + observer_name + " observer in background.")
            observer_object.start_observe()

    def start_event_listener_wrapper(self):
        self.logger.info("Starting Event Listener ...")
        thread = Thread(target=self.start_event_listener)
        thread.daemon = False
        thread.start()
        self.logger.info("Event listener running")

    def start_event_listener(self):
        def handler(*args):
            EventListener(self, *args)

        host = self.device.settings["host"]
        port = self.device.settings["port"]
        event_listener = HTTPServer((host, port), handler)
        event_listener.serve_forever()

    def handle_change(self, feature, value):
        self.logger.info("Value updated: changed {} to {}".format(feature, value))

        self.run_action(feature, value)

    def run_action(self, action_name, value):
        try:
            self.actions[action_name].start_action(value=value)
        except KeyError as e:
            self.logger.error("Device", e.args[0], "not configured.")


if __name__ == "__main__":
    if not utils.settings_exist():
        setup()
    Run().run()
