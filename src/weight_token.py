# -*- coding: utf-8 -*-

import time
import os
from tfidf_calculator import load_csv_files, calculate_tfidf
from ascii_writer import write_dictionary_ascii, write_posting_ascii, verify_fixed_chunks

def run_weightToken():
    dictionary_csv = os.path.join("out", "dictionary.csv")
    posting_csv = os.path.join("out", "posting.csv")
    out_dict_txt = os.path.join("out", "diccionario.dat") 
    out_post_txt = os.path.join("out", "posting.dat")

    if not os.path.exists(dictionary_csv):
        print(f"Error: No existe {dictionary_csv}")
        return
    if not os.path.exists(posting_csv):
        print(f"Error: No existe {posting_csv}")
        return

    start_time_total = time.time()

    # Se cargan los archivos dictionary y posting
    start_time_load = time.time()
    dictionary_df, posting_df = load_csv_files(dictionary_csv, posting_csv)
    if dictionary_df is None or posting_df is None:
        print("Error al cargar los CSV.")
        return
    load_duration = time.time() - start_time_load

    # Se realiza el calculo TF-IDF
    start_time_tfidf = time.time()
    tfidf_results = calculate_tfidf(posting_df, dictionary_df)
    tfidf_duration = time.time() - start_time_tfidf

    # Archivos output
    start_time_write = time.time()
    write_dictionary_ascii(dictionary_df, out_dict_txt)
    write_posting_ascii(tfidf_results, out_post_txt)
    write_duration = time.time() - start_time_write

    total_duration = time.time() - start_time_total

    log_filename = "a10_matricula.txt"
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"Tiempo total: {total_duration:.4f} s\n")
        log_file.write(f"Tiempo carga CSV: {load_duration:.4f} s\n")
        log_file.write(f"Tiempo calculo TF-IDF: {tfidf_duration:.4f} s\n")
        log_file.write(f"Tiempo escritura ASCII: {write_duration:.4f} s\n")

    print("Proceso completado.")
    print(f"Diccionario => {out_dict_txt}")
    print(f"Posting => {out_post_txt}")
    print(f"Log => {log_filename}")

if __name__ == "__main__":
    run_weightToken()
    verify_fixed_chunks("out/diccionario.dat", 80)
    verify_fixed_chunks("out/posting.dat", 80)
