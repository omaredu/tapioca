# -*- coding: utf-8 -*-

import pandas as pd
import math
import os
import chardet

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result.get("encoding")
    return encoding if encoding is not None else "utf-8"

def load_csv_files(dictionary_csv, posting_csv):
    if not os.path.exists(dictionary_csv) or not os.path.exists(posting_csv):
        print("Error: No se encontraron los archivos CSV.")
        return None, None

    dict_enc = detect_encoding(dictionary_csv)
    post_enc = detect_encoding(posting_csv)

    try:
        dictionary_df = pd.read_csv(dictionary_csv, encoding=dict_enc)
        posting_df = pd.read_csv(posting_csv, encoding=post_enc)
        print("Archivos CSV cargados:")
        print(f"  {dictionary_csv} (encoding={dict_enc})")
        print(f"  {posting_csv} (encoding={post_enc})")
        return dictionary_df, posting_df
    except Exception as e:
        print(f"Error al leer CSV: {e}")
        return None, None

def calculate_tfidf(posting_df, dictionary_df):
    total_documents = len(posting_df)
    tfidf_results = []

    total_tokens = len(dictionary_df)
    print(f"Se procesaran {total_tokens} tokens...")

    current_index = 0

    for i, dict_row in dictionary_df.iterrows():
        token = dict_row["Token"]
        doc_count = dict_row["Cantidad de documentos que lo contienen"]
        if doc_count == 0:
            doc_count = 1
        idf = math.log(total_documents / doc_count)

        if i % 100 == 0:
            print(f"[Debug] Procesado token {i}/{total_tokens}: {token}")

        for _ in range(doc_count):
            if current_index >= len(posting_df):
                break
            post_row = posting_df.iloc[current_index]
            doc_name = post_row["Archivo"]
            freq = post_row["Repeticiones en el archivo"]
            tf = freq  
            tfidf = tf * idf
            tfidf_results.append((token, doc_name, tfidf))
            current_index += 1

    print("Calculo TF-IDF finalizado.")
    return tfidf_results
