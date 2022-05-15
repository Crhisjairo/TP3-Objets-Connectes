import logging
import random
import string

from Models.Logger import TailLogger


class AerationModel:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tail = TailLogger(10)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        self.log_handler = self.tail.log_handler
        self.log_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.log_handler)

        self.levels = [logging.INFO, logging.ERROR, logging.DEBUG]
        self.logger.setLevel(logging.INFO)

    def add_log(self, level: logging, message: string):
        self.logger.log(level, 'Message {}'.format(message))

    def get_logs(self) -> str:
        return self.tail.contents()

