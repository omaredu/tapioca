from typing import Counter, Dict
from utils import measure, logger
from pathlib import Path
import argparse


class Tokenizer:
    def __init__(self, input_path: str, output_path: str):
        self.__words = Counter()
        self.__input_path = input_path
        self.__output_path = output_path

    def tokenize(self):
        self.__create_file_if_not_exists(self.__output_path)
        self.__create_file_if_not_exists(self.__input_path)

        tokens = self.__tokenize_input()

        with open(self.__output_path, "w") as file:
            for token, count in tokens.items():
                file.write(f"{token} {count}\n")

    def __tokenize_input(self) -> Dict[str, int]:
        input_text = self.__read_file(self.__input_path)
        tokens = input_text.split()
        normalized_tokens = map(lambda token: token.lower(), tokens)
        self.__words.update(normalized_tokens)
        return dict(sorted(self.__words.items()))

    def __read_file(self, path: str):
        with open(path, "r") as file:
            return file.read()

    def __create_file_if_not_exists(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)


parser = argparse.ArgumentParser(description="Tokenize words from a file")
parser.add_argument("input", help="Input file path", type=str)
parser.add_argument("output", help="Output file path", type=str)
parser.add_argument("--log", action="store_true", help="Enable logger")
args = parser.parse_args()

measure = measure.Measure()
logger = logger.Logger("logs/tokenizer.log") if args.log else None
measure.start()

tokenizer = Tokenizer(args.input, args.output)
tokenizer.tokenize()

execution_time = measure.stop()
print(f"Execution time (milliseconds): {execution_time} ms")

if logger:
    logger.log(
        f"{args.input} tokenization process completed in {execution_time} ms. Output file: {args.output}"
    )
