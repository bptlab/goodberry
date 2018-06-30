import websockets as websockets


class WebsocketWrapper:
	def is_connected(self):
		return self.is_connected

	def get_close_reason(self):
		return self.close_reason

	def __init__(self, server_uri):
		self.session = None
		self.close_reason = None
		self.is_connected = False
		self.receivers = []

		try:
			websockets.connect(server_uri, ssl=True)
		except Exception as e:
			raise RuntimeError(e)

	def close(self):
		if not self.is_connected:
			return
		try:
			self.session.close()
		except IOError:
			# empty, since we don't need to handle this exception
			pass

		self.is_connected = False
		self.session = None

	# todo: no usage
	def on_open(self, session):
		self.is_connected = True
		self.session = session

	# todo: no usage
	def on_close(self, session, close_reason):
		self.is_connected = False
		self.close_reason = close_reason
		self.session = None

	# todo: no usage
	def on_message(self, message):
		if not len(self.receivers):
			print("web socket client received message ('%s'), but has no message handlers", message)
			return

		for receiver in self.receivers:
			receiver.message_received(self, message)

	def can_send(self):
		return self.is_connected

	def send_message(self, message):
		if not self.is_connected or not self.session:
			return False

		# Todo Java -> Python! Send message to server
		self.session.getAsyncRemote().sendText(message, self)
		return True

	# Todo: no usage
	def on_result(self, send_result):
		if not send_result.isOK():
			print("cannot send WebSocket message: %s" % str(send_result))

	def can_receive(self):
		return self.is_connected

	def add_message_receiver(self, receiver):
		self.receivers.append(receiver)

	def remove_message_receiver(self, receiver):
		self.receivers.remove(receiver)