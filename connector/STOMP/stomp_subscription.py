from connector.STOMP import STOMPSubscriptionAcknowledgement
from connector.STOMP.stomp_client_message_factory import STOMPClientMessageFactory


class STOMPSubscription:
	def __init__(self, client, destination, id, acknowledgement):
		self.client = client
		self.destination = destination
		self.id = id
		self.acknowledgement = acknowledgement
		self.message_receivers = []

		self.send()

	def __init__(self, client, destination, id):
		self.__init__(client, destination, id, STOMPSubscriptionAcknowledgement.AUTO)

	def send(self):
		message = STOMPClientMessageFactory.subscribe(self.destination, self.id, self.acknowledgement)
		self.client.get_message_sender().send_message(message)

	def can_receive(self):
		return self.client.get_message_dispatcher().can_receive()

	def consume_message(self, message):
		for receiver in self.message_receivers:
			receiver.message_received(self, message)

	def add_message_receiver(self, receiver):
		self.message_receivers.append(receiver)

	def remove_message_receiver(self, receiver):
		self.message_receivers.remove(receiver)