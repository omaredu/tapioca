import os
import pandas as pd
import time
import chardet
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
RESOURCES_DIR = os.path.join(BASE_DIR, "..", "resources") 
OUT_DIR = os.path.join(BASE_DIR, "..", "out")  

POSTING_ORIGINAL = os.path.join(OUT_DIR, "posting.csv")  
DOCUMENTS = os.path.join(OUT_DIR, "documents.csv")  
POSTING_MODIFICADO = os.path.join(OUT_DIR, "posting.csv")
LOG = os.path.join(OUT_DIR, "a11_matricula.txt")

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    return result.get("encoding", "utf-8")
def calculate_tf(file_name, total_documents, document_map):
    file_path = os.path.join(RESOURCES_DIR, file_name)  
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().split()
            total_tokens = len(tokens)
            if total_tokens == 0:
                return 0.0
            freq = {}
            for token in tokens:
                freq[token] = freq.get(token, 0) + 1
            tf_total = 0.0
            for token, count in freq.items():
                tf = (count * 100) / total_tokens  
                tf_total += tf  
            return tf_total  
    except Exception as e:
        print(f"Error al calcular TF para el archivo {file_name}: {e}")
        return 0.0

# Crear índice de documentos
def create_document_index(input_dir, output_doc_path):
    document_map = []
    for idx, i in enumerate(range(2, 504), start=1):
        filename = f"{i:03}.html"
        if filename not in {"hard.html", "medium.html", "simple.html"}:
            document_map.append({"DocumentID": idx, "FileName": filename})
    df = pd.DataFrame(document_map)
    df.to_csv(output_doc_path, index=False)  
    return df

def load_document_mapping(doc_csv_path):
    df = pd.read_csv(doc_csv_path)
    return dict(zip(df["FileName"], df["DocumentID"]))  

# Reescribir Posting 
def rewrite_posting_with_ids_and_weights(posting_path, doc_map, output_path):
    print("Calculando el peso de los tokens...")
    
    posting_data = []
    total_documents = len(doc_map)
    
    for file_name, document_id in doc_map.items():
        weight = calculate_tf(file_name, total_documents, doc_map)
        posting_data.append({"DocumentID": document_id, "Weight": weight})  

    posting_df = pd.DataFrame(posting_data)
    posting_df = posting_df[['DocumentID', 'Weight']]  
    posting_df.to_csv(output_path, index=False, header=True)

# Consultas al diccionario
def run_query_phase():
    start_total = time.time()
    log_lines = []
    
    # Crear Documents.csv
    log_lines.append("Creando Documents.csv...\n")
    start_docs = time.time()
    create_document_index(RESOURCES_DIR, DOCUMENTS)
    time_docs = time.time() - start_docs
    log_lines.append(f"Creación Documents.csv: {time_docs:.4f} segundos\n")
    
    # Modificar Posting.csv 
    start_mod = time.time()
    doc_map = load_document_mapping(DOCUMENTS)
    rewrite_posting_with_ids_and_weights(POSTING_ORIGINAL, doc_map, POSTING_MODIFICADO)
    time_mod = time.time() - start_mod
    log_lines.append(f"Modificación Posting.csv: {time_mod:.4f} segundos\n")
    
    # Calcular el peso de los tokens 
    start_weight = time.time()
    time_weight = time.time() - start_weight
    log_lines.append(f"Cálculo de peso de los tokens: {time_weight:.4f} segundos\n")
    
    # Tiempo total
    total_time = time.time() - start_total
    log_lines.append(f"Tiempo total : {total_time:.4f} segundos\n")

    # Crear Log
    print("Creando Log...")
    with open(LOG, "w", encoding="utf-8") as log:
        log.writelines(log_lines)

if __name__ == "__main__":
    run_query_phase()
