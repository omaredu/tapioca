import time


class Measure:
    def start(self):
        self.__start_timestamp = self.__get_current_timestamp()

    def stop(self) -> int:
        self.__stop_timestamp = self.__get_current_timestamp()
        return self.__stop_timestamp - self.__start_timestamp

    def __get_current_timestamp(self) -> int:
        return int(round(time.time_ns() / 1_000_000))
