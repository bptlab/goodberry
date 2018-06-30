from connector.STOMP import C_MESSAGE_END, STOMPServerCommand, C_HEADER_SEPARATOR, C_ENTRY_SEPARATOR


class STOMPServerMessage:
	def __init__(self, command, body, headers):
		self.command = command
		self.body = body
		self.headers = headers

	@staticmethod
	def invalid_message():
		return STOMPServerMessage(STOMPServerCommand.INVALID_COMMAND, "", {})

	@staticmethod
	def parse(message):
		if not message or message[len(message) - 1] != C_MESSAGE_END:
			print("Cannot parse STOMP message: message was null, empty or did not end with ^0!")
			return STOMPServerMessage.invalid_message()


		message_lines = list(reversed(message.split("\r?\n")))

		if not message_lines:
			print("Cannot parse STOMP message: message has no lines!")
			return STOMPServerMessage.invalid_message()

		command = STOMPServerCommand.INVALID_COMMAND
		headers = {}
		body = ""

		# parse command
		command_text = message_lines.pop()
		for c in STOMPServerCommand.values():
			if not command_text.lower() == str(c):
				continue

			command = c
			break

		if command == STOMPServerCommand.INVALID_COMMAND:
			print("Cannot parse STOMP message: unrecognized command '%s'", command_text)
			return STOMPServerMessage.invalid_message()

		# parse headers
		while message_lines:
			line = message_lines.pop()

			if line == "":
				# found empty line ==> separator for headers and body
				break

			header = line.split(C_HEADER_SEPARATOR)

			if len(header) != 2:
				# invalid header
				print("Cannot parse STOMP message: invalid header format!")
				return STOMPServerMessage.invalid_message()

			STOMPServerMessage.set_header(headers, header[0], header[1])

		# parse body
		while message_lines:
			body += message_lines.pop() + C_ENTRY_SEPARATOR

		return STOMPServerMessage(command, body, headers)

	@staticmethod
	def set_header(headers, header, value):
		if headers[header.lower()]:
			return
		headers[header.lower()] = value.lower()

	def is_valid(self):
		return self.command != STOMPServerCommand.INVALID_COMMAND

	def get_server_command(self):
		return self.command

	def get_body(self):
		return self.body

	def get_headers(self):
		return self.headers

	def contains_header(self, header):
		return self.headers[header.lower()]

	def get_header(self, header):
		if not self.contains_header(header):
			raise RuntimeError("STOMP message does not contain header '" + header + "'")

		return self.headers[header.lower()]

	def get_header(self, header, default_value):
		if not self.contains_header(header):
			return default_value

		return self.get_header(header)