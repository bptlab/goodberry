from enum import Enum, auto

C_ENTRY_SEPARATOR = "\r\n"
C_HEADER_SEPARATOR = ":"
C_MESSAGE_END = '\0'

C_ACCEPT_VERSION_HEADER = "accept-version"
C_HOST_HEADER = "host"
C_HEARTBEAT_HEADER = "heart-beat"
C_DESTINATION_HEADER = "destination"
C_ID_HEADER = "id"
C_ACKNOWLEDGE_HEADER = "ack"
C_TRANSACTION_HEADER = "transaction"
C_RECEIPT_HEADER = "receipt"

C_VERSION_HEADER = "version"
C_SUBSCRIPTION_HEADER = "subscription"


class STOMPSubscriptionAcknowledgement(Enum):
	AUTO = auto()
	CLIENT = auto()
	CLIENT_INDIVIDUAL = auto()


class STOMPServerCommand(Enum):
	CONNECTED = auto()
	MESSAGE = auto()
	RECEIPT = auto()
	ERROR = auto()
	INVALID_COMMAND = auto()


class STOMPClientCommand(Enum):
	CONNECT = auto()
	SEND = auto()
	SUBSCRIBE = auto()
	UNSUBSCRIBE = auto()
	BEGIN = auto()
	COMMIT = auto()
	ABORT = auto()
	ACK = auto()
	NACK = auto()
	DISCONNECT = auto()
