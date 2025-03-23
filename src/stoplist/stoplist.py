import os

from utils.logger import Logger
from utils.measure import Measure


class StopList:
    def __init__(self, stop_list_path: str):
        self.__stop_list = set()
        self.__input_path = stop_list_path
        self.__logger = Logger("logs/stoplist.log")
        self.load_stop_list()

    def load_stop_list(self):
        if not os.path.exists(self.__input_path):
            self.__logger.log(f"Stop list file not found: {self.__input_path}")
            return

        self.__logger.log(f"Loading stop list from: {self.__input_path}")
        timer = Measure()
        timer.start()
        words = set()
        with open(self.__input_path) as f:
            words = set(line.strip() for line in f if line.strip())
        self.__stop_list = words
        self.__logger.log(f"Stop list loaded in {timer.stop()} ms")

    def is_stop_word(self, word: str) -> bool:
        return word in self.__stop_list
