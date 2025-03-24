# -*- coding: utf-8 -*-

import os
def write_dictionary_ascii(dictionary_df, output_file):
    """
    Se escribe cada registro del diccionario en 80 bytes (79 de datos + 1 de newline).
      - Token: 30 chars
      - #Doc: 10 chars
      - Pointer: 10 chars
      - Relleno: 29 chars
      - '\n': 1 byte
    Total = 79 + 1 = 80 bytes por linea
    """
    with open(output_file, "wb") as f:  
        for _, row in dictionary_df.iterrows():
            token = str(row["Token"])[:30].ljust(30)
            doc_count = str(int(row["Cantidad de documentos que lo contienen"])).rjust(10, '0')[:10]
            pointer = str(int(row.get("Posicion del primer registro en posting", 0))).rjust(10, '0')[:10]
            filler = " " * 29  
            line = token + doc_count + pointer + filler
   
            line_bytes = line.encode("ascii", errors="replace")

            if len(line_bytes) < 79:
                line_bytes += b' ' * (79 - len(line_bytes))
            elif len(line_bytes) > 79:
                line_bytes = line_bytes[:79]

            line_bytes += b'\n'
            f.write(line_bytes)

def write_posting_ascii(tfidf_results, output_file):
    """
    Se escribe cada registro del posting en 80 bytes (79 de datos + 1 de newline).
      - DocID: 15 chars
      - Peso: 15 chars
      - Relleno: 49 chars
      - '\n': 1 byte
    Total = 79 + 1 = 80 bytes por linea
    """
    with open(output_file, "wb") as f:  
        for (token, doc_name, tfidf) in tfidf_results:
            doc_id_str = doc_name.split(".")[0]
            doc_id = doc_id_str[:15].rjust(15)
            weight = f"{tfidf:.5f}"
            if len(weight) > 15:
                weight = weight[:15]
            weight = weight.rjust(15)

            filler = " " * 49
            line = doc_id + weight + filler

            line_bytes = line.encode("ascii", errors="replace")

            if len(line_bytes) < 79:
                line_bytes += b' ' * (79 - len(line_bytes))
            elif len(line_bytes) > 79:
                line_bytes = line_bytes[:79]

            line_bytes += b'\n'
            f.write(line_bytes)

def verify_fixed_chunks(filename, chunk_size=80):
    total_bytes = os.path.getsize(filename)
    print(f"Verificando {filename} (tamano total: {total_bytes} bytes)")

    # Chequeo de tamano total
    if total_bytes % chunk_size != 0:
        print(f"Advertencia: El tamano total ({total_bytes} bytes) NO es multiplo de {chunk_size}.")
    else:
        print(f"OK: El tamano total es multiplo de {chunk_size}.")

    with open(filename, "rb") as f:
        index = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            if len(chunk) < chunk_size:
                print(f"Error: Bloque {index} incompleto ({len(chunk)} bytes en vez de {chunk_size}).")
            index += 1

    print("Verificacion finalizada.\n")