from .component import Component
from threading import Thread


class ActionComponent(Component):
    def __init__(self, device_id, **kwargs):
        super().__init__(device_id, **kwargs)
        self.action_name = None
        self.action_config = None

    def init_action(self, action_name, action_config):
        self.action_name = action_name
        self.action_config = action_config

    def start_action(self, **kwargs):
        self.logger.info("Start action for " + self.action_name)
        thread = Thread(target=self.trigger_action, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    def trigger_action(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def configure_action():
        raise NotImplementedError
