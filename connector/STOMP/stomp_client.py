import uuid

from connector.STOMP import STOMPServerCommand, C_VERSION_HEADER, C_SUBSCRIPTION_HEADER
from connector.STOMP.stomp_client_message_factory import STOMPClientMessageFactory
from connector.STOMP.stomp_server_message import STOMPServerMessage
from connector.STOMP.stomp_subscription import STOMPSubscription


class STOMPClient:
	def __init__(self, host, sender, dispatcher):
		self.host = host
		self.sender = sender
		self.dispatcher = dispatcher
		self.dispatcher.add_message_dispatcher(self)
		self.connected = False
		self.subscriptions = {}

	def get_message_sender(self):
		return self.sender

	def get_message_dispatcher(self):
		return self.dispatcher

	def subscribe(self, destination):
		if not self.connected:
			raise RuntimeError("Cannot subscribe to STOMP server: STOMP client is not connected!")

		while True:
			id = uuid.uuid4()
			if id not in self.subscriptions:
				break

		subscription = STOMPSubscription(self, destination, id)
		self.subscriptions[id] = subscription

		return subscription

	def send(self, destination, body, headers):
		if not self.connected:
			raise RuntimeError("Cannot send to STOMP server: STOMP client is not connected!")

		if not self.sender.can_send():
			return False

		message = STOMPClientMessageFactory.send(destination, body, headers)
		return self.sender.send_message(message)

	def send(self, destination, body):
		return self.send(destination, body, {})

	def message_received(self, dispatcher, message):
		if dispatcher != self.dispatcher:
			raise RuntimeError("STOMP Client received message from unknown message dispatcher!")

		stomp_message = STOMPServerMessage.parse(message)

		if not stomp_message.isValid():
			print("STOMP Client received invalid message: '%s'", message)
			return

		if stomp_message.getServerCommand() == STOMPServerCommand.CONNECTED:
			self.process_connected(stomp_message)
			return
		if stomp_message.getServerCommand() == STOMPServerCommand.MESSAGE:
			self.process_message(stomp_message)
			return
		if stomp_message.getServerCommand() == STOMPServerCommand.RECEIPT:
			self.process_receipt(stomp_message)
			return

		if stomp_message.getServerCommand() == STOMPServerCommand.ERROR:
			self.process_error(stomp_message)
			return

		print("STOMP message command unknown: '%s'", message)

	def connect(self, connect_handler):
		self.connect_handler = connect_handler

		if self.connected:
			self.connection_finished()
			return

		if not self.sender.can_send():
			self.connected = False
			self.connection_finished()
			return

		message = STOMPClientMessageFactory.connect(self.host)
		self.sender.send_message(message)

	def process_connected(self, message):
		try:
			serverVersion = message.getHeader(C_VERSION_HEADER)

			if not serverVersion == "1.2":
				print("STOMP server version does not equal '1.2'!")
				return

			self.connected = True
			self.connection_finished()

		except RuntimeError as e:
			self.connected = False
			self.connection_finished()
			print("Cannot process STOMP CONNECTED: '%s'", str(e))

	def connection_finished(self):
		if not self.connect_handler:
			print("STOMP client has no connect handler!")
			return

		self.connect_handler.connect_finished(self, self.connected)

	def process_message(self, message):
		try:
			subscription_id = message.get_header(C_SUBSCRIPTION_HEADER)

			if not self.subscriptions[subscription_id]:
				raise RuntimeError("Cannot find subscription for received STOMP message")

			subscription = self.subscriptions.get(subscription_id)
			subscription.consume_message(message)

		except RuntimeError as e:
			print("Cannot process STOMP MESSAGE: '%s'", str(e))

	def process_receipt(self, message):
		try:
			pass
		except RuntimeError as e:
			print("Cannot process STOMP RECEIPT: '%s'", str(e))

	def process_error(self, message):
		try:
			pass
		except RuntimeError as e:
			print("Cannot process STOMP ERROR: '%s'", str(e))