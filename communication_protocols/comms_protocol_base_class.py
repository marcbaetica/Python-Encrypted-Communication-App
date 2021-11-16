from abc import ABC, abstractmethod


class BaseCommsProtocolHandler(ABC):
    @abstractmethod
    def send_message_attempt(self, message):
        pass

    @abstractmethod
    def receive_message_attempt(self):
        pass
