import os
import requests
from utils import get_logger


class Connector:
    def __init__(self):
        self.logger = get_logger(__name__)

    def update_property(self, device_id, feature_name, property_name, value):
        self.logger.info("Updating property on device", device_id, "feature", feature_name, "property_name", property_name, "value", value)

    def update_feature(self, device_id, feature_name, value):
        self.logger.info("Updating feature on device", device_id, "feature", feature_name, "value", value)

    def reset_action(self, device_id, action_name, is_boolean=True):
        value = "false"
        if not is_boolean:
            value = ""
        self.logger.info("Resetting action on device", device_id, "action", action_name, "value", value)

    def put(self, data):
        pass
        # TODO: fire request