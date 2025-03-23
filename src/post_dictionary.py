import os
import csv
import argparse
from collections import defaultdict

from utils import measure, logger
from stoplist.stoplist import StopList

measureGlobal = measure.Measure()
logger = logger.Logger("logs/a7_matricula.log")
stop_list = StopList("src/stoplist/stoplist.txt")


def get_words_from_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        words = set()
        for line in file:
            if stop_list.is_stop_word(line):
                continue
            words.update(line.lower().split())
    return words


def process_directory(input_dir, dictionary_file, posting_file):
    word_occurrences = defaultdict(int)
    posting_data = defaultdict(list)
    posting_position = 0

    if not os.path.exists(input_dir):
        print(f"El directorio {input_dir} no existe.")
        return

    files_processed = 0
    for filename in os.listdir(input_dir):
        measureFile = measure.Measure()
        measureFile.start()
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            words = get_words_from_file(filepath)
            word_counts = defaultdict(int)
            for word in words:
                word_counts[word] += 1
                word_occurrences[word] += 1
            for word, count in word_counts.items():
                posting_data[word].append((filename, count))
            files_processed += 1
        logger.log(f"{filepath}   {measureFile.stop()}ms")

    sorted_words = sorted(word_occurrences.keys())

    with open(dictionary_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Token",
                "Cantidad de documentos que lo contienen",
                "Posicion del primer registro en posting",
            ]
        )
        for word in sorted_words:
            if stop_list.is_stop_word(word):
                continue
            writer.writerow([word, word_occurrences[word], posting_position])
            posting_position += len(posting_data[word])

    with open(posting_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Archivo", "Repeticiones en el archivo"])
        for word in sorted_words:
            for filename, count in posting_data[word]:
                writer.writerow([filename, count])

    print(
        f"Procesados {files_processed} archivos. Diccionario generado en {dictionary_file}. Archivo posting generado en {posting_file}."
    )


parser = argparse.ArgumentParser(
    description="Procesa archivos y cuenta palabras únicas por archivo."
)
parser.add_argument("input_dir", help="Directorio de entrada con los archivos")
parser.add_argument("dictionary_file", help="Ruta del archivo de salida")
parser.add_argument("posting_file", help="Ruta del archivo de posting")

args = parser.parse_args()

measureGlobal.start()
process_directory(args.input_dir, args.dictionary_file, args.posting_file)
logger.log(f"Tiempo de ejecución del programa: {measureGlobal.stop()}ms")
