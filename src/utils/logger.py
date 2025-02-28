from pathlib import Path


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log(self, message):
        self.__create_file_if_not_exists(self.log_file)
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def __create_file_if_not_exists(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
