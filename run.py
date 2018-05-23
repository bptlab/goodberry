import sys
from device import Device
from connector import ChangeServer
import logging
import utils
from setup import main as setup


class Run:
    def __init__(self):
        try:
            self.device = Device()
        except Exception:
            sys.exit(1)
        self.device.load_settings()
        self.watcher = ChangeServer(self)
        self.observer = self.device.get_observers()
        self.actions = self.device.get_actions()
        logging.info("Loaded " + str(len(self.observer)) + " observer(s) and " + str(len(self.actions)) + " action(s).")

    def run(self):
        self.start_observers()
        self.start_watcher()

    def start_observers(self):
        logging.info("Starting observers...")
        for observer_name, observer_object in self.observer.items():
            logging.info("Starting " + observer_name + " observer in background.")
            observer_object.start_observe()

    def start_watcher(self):
        logging.info("Start watching input...")
        self.watcher.start_watching()

    def handle_change(self, event_data):
        if not event_data["device_id"] == self.device.id:
            logging.info("Message not relevant for this device.")
            return

        feature = event_data["feature"]
        value = event_data["value"]
        logging.info("Value updated: changed {} to {}".format(feature, value))

        self.run_action(feature, value)

    def run_action(self, action_name, value):
        try:
             self.actions[action_name].start_action(value=value)
        except KeyError as e:
             logging.error("Device", e.args[0], "not configured.")


if __name__ == "__main__":
    if not utils.settings_exist():
        setup()
    Run().run()
