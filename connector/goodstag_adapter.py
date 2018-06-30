import datetime
import json
import requests
from json import JSONDecodeError

from connector.STOMP.stomp_client import STOMPClient
from connector.websocket_wrapper import WebsocketWrapper

C_HTTPS_PREFIX = "https://"
C_WSS_PREFIX = "wss://"
C_URI_ACCESS_TOKEN_PARAMETER = "/ws?access_token="
C_URI_NOTIFICATIONS_PATH = "/notifications"
C_URI_SUBSCRIPTION_PATH = "/subscribe"
C_TOKEN_ROUTE = "/oauth/token"
C_DEVICE_ID_SEPARATOR = " "

C_NFC_UNKNOWN_TAG_SCAN_NAME = "NFCUnknownTagScan"
C_NFC_UNMAPPED_TAG_SCAN_NAME = "NFCUnmappedTagScan"
C_NFC_USER_SCAN_NAME = "NFCUserScan"
C_NFC_BOOK_SCAN_NAME = "NFCBookScan"

C_GOODSTAG_CARDSCAN = "cardscan"
C_GOODSTAG_BOOKSCAN = "bookscan"

class GoodstagAdapter:
	goodstag_url = ""
	goodstag_username = ""
	goodstag_password = ""
	goodstag_device_ids = ""
	goodstag_access_token = ""
	refresh_access_token = datetime.datetime.now()
	websocket_client = None
	stomp_client = None
	notifications_subscriptions = None
	processed_execution_results = []

	def __init__(self, device, name):
		self.name = name
		self.device = device

		self.read_goodstag_url()
		self.read_goodstag_username()
		self.read_goodstag_password()
		self.read_goodstag_device_ids()

	def read_goodstag_url(self):
		self.goodstag_url = self.device.settings["goodstag"]["url"]

		if not self.goodstag_url:
			raise RuntimeError("GoodsTag uri is not configured. please check your config.")
		
	def read_goodstag_username(self):
		self.goodstag_username = self.device.settings["goodstag"]["username"]

		if not self.goodstag_username:
			raise RuntimeError("GoodsTag username is not configured. please check your config.")
	
	def read_goodstag_password(self):
		self.goodstag_password = self.device.settings["goodstag"]["password"]

		if not self.goodstag_password:
			raise RuntimeError("GoodsTag password is not configured. please check your config.")

	def read_goodstag_device_ids(self):
		ids = self.device.settings["goodstag"]["device-ids"]

		if not ids:
			raise RuntimeError("GoodsTag device ids are not configured. please check your config.")

		self.goodstag_device_ids = ids.split(C_DEVICE_ID_SEPARATOR)

	def disconnect(self):
		if not self.websocket_client or not self.websocket_client.is_connected():
			return
		self.websocket_client.close()

	def authenticate(self):
		now = datetime.datetime.now()

		# check whether we already have a access token and if it is still valid
		if self.goodstag_access_token and now < self.refresh_access_token:
			return self.goodstag_access_token

		url = C_HTTPS_PREFIX + self.goodstag_url + C_TOKEN_ROUTE

		params = {
			"grant_type": "password",
			"username": self.goodstag_username,
			"password": self.goodstag_password,
			"client_id": "gt-user"
		}

		try:
			r = requests.post(url, data=params)
			if r.status_code != 200:
				print("cannot authenticate at '%s'.", url)
				return ""

			response = r.json()
		except IOError as e:
			print("cannot send authentication request to GoodsTag!")
			raise RuntimeError(e)
		except JSONDecodeError as e:
			print("cannot parse GoodsTag authentication response!")
			raise RuntimeError(e)

		access_token = ""
		validity_duration = 0

		try:
			access_token = response["access_token"]
			validity_duration = int(response["expires_in"])

		except KeyError:
			print("cannot read 'access_token' from GoodsTag authentication response")

		self.refresh_access_token= datetime.datetime.now() + datetime.timedelta(seconds=validity_duration)


		return access_token

	def connect(self):
		self.goodstag_access_token = self.authenticate()

		if not self.goodstag_access_token:
			raise RuntimeError("cannot connect to GoodsTag: access_token not granted!")

		uri = C_WSS_PREFIX + self.goodstag_url + C_URI_ACCESS_TOKEN_PARAMETER + self.goodstag_access_token

		try:
			# close existing connection
			self.disconnect()

			self.websocket_client = WebsocketWrapper(uri)

		except RuntimeError as e:
			print("cannot connect to GoodsTag: web socket webSocketClient connection was refused")
			raise e

		self.stomp_client = STOMPClient(C_WSS_PREFIX + self.goodstag_url, self.websocket_client, self.websocket_client)
		self.stomp_client.connect(self)

	def subscribe_to_device(self, device_id):
		headers = {
			"content-type": "application/json"
		}

		message = {
			"type": "eventSubscribe",
			"eventType": "device.tag.detect",
			"source": "urn:device:%s" % device_id
		}

		try:
			self.stomp_client.send(C_URI_SUBSCRIPTION_PATH, str(message), headers)

		except JSONDecodeError:
			print("cannot create subscription message for GoodsTag web socket!")

	@staticmethod
	def raise_error(execution_result):
		error_message = execution_result["errorMessage"]
		if error_message:
			raise RuntimeError(error_message)

	@staticmethod
	def get_english_translation(execution_result):
		translations = execution_result["translations"]

		if not translations:
			raise RuntimeError("Cannot get english translation from GoodsTag event!")

		for translation in translations:
			if not translation["language"].lower() == "en":
				continue
			return translation
		raise RuntimeError("Cannot get english translation from GoodsTag event!")

	def parse_goodstag_event(self, goodstag_event):
		timestamp = goodstag_event["time"]

		execution_result = goodstag_event["executionResult"]

		self.raise_error(execution_result)

		# check, whether this event was processed already
		# this might happen, if the user holds the tag too close to the scanner for too long
		if execution_result["id"] in self.processed_execution_results:
			return

		self.processed_execution_results.append(execution_result["id"])

		result = execution_result["result"]
		type = result["type"]

		if type.lower() == C_GOODSTAG_BOOKSCAN:
			self.parse_bookscan_event(timestamp, result, goodstag_event)
		elif type.lower() == C_GOODSTAG_CARDSCAN:
			self.parse_cardscan_event(timestamp, result, goodstag_event)
		else:
			raise RuntimeError("Unknown GoodsTag event type: '%s'", type)

	def parse_bookscan_event(self, timestamp, execution_result, goodstag_event):
		pass

	def parse_cardscan_event(self, timestamp, execution_result, goodstag_event):
		epc = goodstag_event["data"]["epc"]
		translation = self.get_english_translation(execution_result)

		event_values = {
			"NFCID": epc,
			"UserId": execution_result["card-id"],
			"Name": translation["name"]
			# "Mail": translation["mail"]
		}

		print("*** NEW GOODSTAG CARD SCAN EVENT ***")
		print(event_values)

	def start_watching(self):
		# check, whether our webSocketClient connection was closed.
		if self.websocket_client and self.websocket_client.is_connected():
			return

		# if so, initialize a new connection
		self.connect()

	def stop_watching(self):
		self.disconnect()

	def message_received(self, dispatcher, message):
		if dispatcher != self.notifications_subscriptions:
			print("GoodsTag adapter received message from unknown subscription!")
			return

		print("GoodsTag event received: '%s'", message.get_body())

		if not message.contains_header("content-type") or not message.get_header("content-type").lower() ==  "application/json":
			print("GoodsTag event does not contain a JSON body. This is not supported (yet)!")
			return

		try:
			json_body = json.loads(message.get_body())
			self.parse_goodstag_event(json_body)

		except JSONDecodeError as e:
			print("Cannot parse GoodsTag event to JSON object: %s" % str(e))
		except RuntimeError as e:
			print("Cannot parse GoodsTag event: %s" % str(e))

	def connect_finished(self, sender, connectionSucceeded):
		if sender != self.stomp_client:
			print("GoodsTag adapter received 'connection finished' from unknown STOMP client!")
			return

		if not connectionSucceeded:
			return

		self.notifications_subscriptions= self.stomp_client.subscribe(C_URI_NOTIFICATIONS_PATH)
		self.notifications_subscriptions.add_message_receiver(self)

		for device_id in self.goodstag_device_ids:
			self.subscribe_to_device(device_id)