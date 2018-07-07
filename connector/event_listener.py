import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

import re

from utils import get_logger


class EventListener(BaseHTTPRequestHandler):
	def __init__(self, runner, *args):
		self.logger = get_logger(__name__)
		self.runner = runner
		self.settings = self.runner.device.settings
		BaseHTTPRequestHandler.__init__(self, *args)
		self.server_version = "Goodberry/1.0.0"

	def do_GET(self):
		if self.path == "/api/v1/configuration":
			response = json.dumps({
				'server_version': self.server_version,
				'settings': self.settings
			}).encode()
			self.send_response(HTTPStatus.OK)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			self.wfile.write(response)
			return

		if self.path == "/api/v1/health":
			self.send_response_only(HTTPStatus.OK)
			self.end_headers()
			return

		else:
			self.send_response_only(HTTPStatus.NOT_FOUND)
			self.end_headers()

	def do_POST(self):
		event_types = self.settings["eventTypes"]
		allowed_ids = [event_types[event_type]["id"] for event_type in event_types]
		match = re.search('/api/v1/event/(?P<id>[0-9a-f]{32})\Z', self.path)
		if match:
			if not match.group('id') in allowed_ids:
				self.send_bad_request("One of the allowed event IDs", "Event ID: %s" % match.group('id'))
				return

			content_type = self.headers['Content-Type']
			if content_type == 'application/json':
				content_length = int(self.headers['Content-Length'])
				post_data = self.rfile.read(content_length).decode("utf-8")
				try:
					event = json.loads(post_data)
					self.handle_event(match.group('id'), event)
					self.send_response_only(HTTPStatus.CREATED)
					self.end_headers()
				except json.JSONDecodeError as e:
					self.send_bad_request("Valid JSON", "Decoding error: %s" % e.msg)
				except AttributeError as e:
					self.send_bad_request("All required attributes are filled.", e.args[0])
				return

			else:
				response = json.dumps({
					"excepted": "Content-Type: appplication/json",
					"actual": "Content-Type: %s" % content_type
				}).encode()
				self.send_response(HTTPStatus.BAD_REQUEST)
				self.send_header("Content-Type", "application/json")
				self.end_headers()
				self.wfile.write(response)
				return

		else:
			self.send_response_only(HTTPStatus.NOT_FOUND)
			self.end_headers()
		return

	def send_bad_request(self, expected, actual):
		self.logger.warning("ERROR: {}".format(actual))
		response = json.dumps({
			"expected": expected,
			"actual": actual
		}).encode()
		self.send_response(HTTPStatus.BAD_REQUEST)
		self.send_header("Content-Type", "application/json")
		self.end_headers()
		self.wfile.write(response)

	def handle_event(self, id, event):
		"""
		In case it is an update event for the current device,
		the handle_change method is invoked.
		:param id: event type id
		:param event: a string containing the received event
		:return: (path, value) or None
		"""
		required_attributes = []
		event_types = self.settings["eventTypes"]
		for event_type in event_types:
			if event_types[event_type]["id"] == id:
				required_attributes = event_types[event_type]["requiredAttributes"]
		if not required_attributes:
			raise AttributeError("Not defined required attributes for this id: '%s'" % id)
		missing_attributes = set(required_attributes) - set(event.keys())
		if missing_attributes:
			raise AttributeError("Not all required attributes are set: %s" % missing_attributes)

		values = [event[attribute] for attribute in required_attributes]
		device_name = ""
		for action in self.settings["actions"]:
			device_name = self.settings["actions"][action]["config"]["type"] == "Device"
		if not device_name:
			raise KeyError("No display configured. Cannot display.")
		self.runner.handle_change(device_name, values)
