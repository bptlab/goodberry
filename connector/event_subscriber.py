import uuid
from http import HTTPStatus

import requests
import sys

from utils import get_logger


class EventSubscriber:
	def __init__(self, device):
		self.logger = get_logger(__name__)
		self.device = device
		self.event_source = self.device.settings["eventSource"]
		self.host = self.device.settings['host']
		self.ssl_enabled = self.device.settings['sslEnabled']
		self.port = self.device.settings['port']

	def subscribe(self):
		event_types = self.device.event_types
		for event_type in event_types:
			if "registered" not in event_types[event_type].keys():
				event_query = "Select * from %s" % event_type
				id = uuid.uuid4().hex

				callback_address = "http"
				if self.ssl_enabled:
					callback_address += "s"
				callback_address += "//" + self.host + ":" + str(self.port) + "/api/v1/events/" + id
				if self.send_subscription(event_query, callback_address):
					event_types[event_type]["registered"] = True
					event_types[event_type]["id"] = id
		self.device.settings["eventTypes"] = event_types
		self.device.write_settings()

	def send_subscription(self, event_query, callback_address):
		self.logger.info("Subscribing to '%s' on '%s', callback: %s" % (event_query, self.event_source, callback_address))

		url = self.event_source + "/webapi/REST/EventQuery/REST"
		post_data = {
			"notificationPath": callback_address,
			"queryString": event_query
		}
		response = requests.post(url=url, json=post_data)
		if response.status_code == HTTPStatus.OK:
			self.logger.info("Subscribed to event source with query: '%s'." % event_query)
			return True
		else:
			self.logger.warn("Could not subscribe to event source with query: '%s'." % event_query)
			return False
