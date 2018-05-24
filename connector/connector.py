import os
import requests
from utils import get_logger


class Connector:
    def __init__(self):
        self.logger = get_logger(__name__)
        try:
            self.BASE_URL = os.environ["CONNECTOR_URL"]
            self.AUTH_TOKEN = os.environ["AUTH_TOKEN"]
        except KeyError as e:
            self.logger.error("Environment variables not set. Set CONNECTOR_URL and AUTH_TOKEN.")
            raise e

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
        # return r

"""
    @staticmethod
    def get_response_message(request, artifact_name):
        if request.status_code == requests.codes.created:
            return "Successfully created the " + artifact_name
        if request.status_code == requests.codes.no_content:
            return "Updated or deleted the " + artifact_name
        return request.reason + "\n" + request.text
"""