from connector.STOMP import C_ENTRY_SEPARATOR, C_HEADER_SEPARATOR, C_MESSAGE_END, C_ACCEPT_VERSION_HEADER, \
	C_HOST_HEADER, C_HEARTBEAT_HEADER, STOMPServerCommand, STOMPClientCommand, C_DESTINATION_HEADER, C_ID_HEADER, \
	C_ACKNOWLEDGE_HEADER, STOMPSubscriptionAcknowledgement, C_TRANSACTION_HEADER, C_RECEIPT_HEADER


class STOMPClientMessageFactory:

	@staticmethod
	def set_header(headers, header, value):
		if header in headers:
			return

		headers[header] = value

	@staticmethod
	def new_message(command, body, headers):
		message = ""

		message += str(command).upper()
		message += C_ENTRY_SEPARATOR

		for key, value in headers:
			message += key + C_HEADER_SEPARATOR + value + C_ENTRY_SEPARATOR 

		# separate header-section from body section
		message += C_ENTRY_SEPARATOR

		message += body
		message += C_MESSAGE_END

		return message

	@staticmethod
	def new_message(command, body):
		return STOMPClientMessageFactory.new_message(command, body, {})

	@staticmethod
	def connect(host):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ACCEPT_VERSION_HEADER, "1.2")
		STOMPClientMessageFactory.set_header(headers, C_HOST_HEADER, host)
		STOMPClientMessageFactory.set_header(headers, C_HEARTBEAT_HEADER, "0,0") # we don't support heart-beat

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.CONNECT, "", headers)

	@staticmethod
	def send(destination, body, headers):
		STOMPClientMessageFactory.set_header(headers, C_DESTINATION_HEADER, destination)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.SEND, body, headers)

	@staticmethod
	def send(destination, body):
		return STOMPClientMessageFactory.send(destination, body, {})
	
	@staticmethod
	def subscribe(destination, subscription_id, client_acknowledgement):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, subscription_id)
		STOMPClientMessageFactory.set_header(headers, C_DESTINATION_HEADER, destination)
		STOMPClientMessageFactory.set_header(headers, C_ACKNOWLEDGE_HEADER, str(client_acknowledgement).lower())

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.SUBSCRIBE, "", headers)

	@staticmethod
	def subscribe(destination, subscription_id):
		return STOMPClientMessageFactory.subscribe(destination, subscription_id, STOMPSubscriptionAcknowledgement.AUTO)
	
	@staticmethod
	def unsubscribe(subscription_id):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, subscription_id)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.UNSUBSCRIBE, "", headers)
	
	@staticmethod
	def ack(message_id, transaction_name):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, message_id)
		STOMPClientMessageFactory.set_header(headers, C_TRANSACTION_HEADER, transaction_name)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.ACK, "", headers)

	@staticmethod
	def ack(message_id):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, message_id)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.ACK, "", headers)
	
	@staticmethod
	def nack(message_id, transaction_name):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, message_id)
		STOMPClientMessageFactory.set_header(headers, C_TRANSACTION_HEADER, transaction_name)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.NACK, "", headers)

	@staticmethod
	def nack(message_id):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_ID_HEADER, message_id)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.NACK, "", headers)

	@staticmethod
	def begin(transaction_name):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_TRANSACTION_HEADER, transaction_name)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.BEGIN, "", headers)

	@staticmethod
	def commit(transaction_name):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_TRANSACTION_HEADER, transaction_name)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.COMMIT, "", headers)

	@staticmethod
	def abort(transaction_name):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_TRANSACTION_HEADER, transaction_name)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.ABORT, "", headers)

	@staticmethod
	def disconnect(receipt_id):
		headers = {}

		STOMPClientMessageFactory.set_header(headers, C_RECEIPT_HEADER, receipt_id)

		return STOMPClientMessageFactory.new_message(STOMPClientCommand.DISCONNECT, "", headers)