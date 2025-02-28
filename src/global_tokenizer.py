import csv
from typing import Dict
from utils import measure, logger
from pathlib import Path
from typing import TypedDict


class ItemData(TypedDict):
    count: int
    file_count: int


class GlobalTokenizer:
    def __init__(self, input_dir: str, output_path: str):
        self.__words = {}
        self.__input_dir = input_dir
        self.__output_path = output_path

    def tokenize(self):
        self.__create_file_if_not_exists(self.__output_path)
        log = logger.Logger("logs/global_tokenizer.log")
        log.log("Starting tokenizer")

        global_timer = measure.Measure()
        global_timer.start()

        for file in Path(self.__input_dir).rglob("*.txt"):
            timer = measure.Measure()
            timer.start()
            self.__tokenize_file(file)
            execution_time = timer.stop()
            log.log(f"Tokenized file {file} in {execution_time} ms")

        # Use CSV writer to avoid formatting issues
        with open(self.__output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["token", "count", "file_count"])  # Header

            for token, data in self.__words.items():
                writer.writerow([token, data["count"], data["file_count"]])

        global_execution_time = global_timer.stop()
        log.log(f"Finished tokenizing in {global_execution_time} ms")

    def __tokenize_file(self, file_path) -> Dict[str, ItemData]:
        input_text = self.__read_file(file_path)
        tokens = input_text.split()

        # Normalize: lowercase, strip whitespace, remove empty tokens
        normalized_tokens = [token.strip().lower() for token in tokens if token.strip()]

        for token in normalized_tokens:
            if token in self.__words:
                self.__words[token]["count"] += 1
            else:
                self.__words[token] = {"count": 1, "file_count": 0}

        for token in set(normalized_tokens):
            self.__words[token]["file_count"] += 1

        return self.__words

    def __read_file(self, path: str):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    def __create_file_if_not_exists(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)


tokenizer = GlobalTokenizer("out/tokenized", "out/tokenized.csv")
tokenizer.tokenize()
