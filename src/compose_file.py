import os
import re
import time
import chardet
import html

def detect_encoding(file_path):
    # detecta la codificación de un archivo leyendo los primeros bytes.
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Leer hasta 10,000 bytes
    return chardet.detect(raw_data).get('encoding', 'utf-8')  # UTF-8 por defecto

def compose_add_words(file_name, log_file, output_file):
    # agrega las palabras de cad archivo a un archivo compuesto
    encoding = detect_encoding(file_name) or 'utf-8'
    # manejo de excepciones
    try:

        start_time = time.time()

        # se extraen todas las palabras del archivo
        with open(file_name, 'r', encoding=encoding, errors='replace') as file:
            content = file.read().splitlines()
        
        end_time = time.time()
        extract_time = end_time - start_time

        with open(output_file, 'a', encoding='utf-8') as file:
            file.write('\n'.join(content))

        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Archivo: {file_name}, Tiempo de extracción: {extract_time:.6f} segundos\n")

        print(f"Proceso completado. Las palabras del archivo {file_name} se han agregado al resultado")
        print(f"Tiempo de extracción: {extract_time:.6f} segundos")

        return extract_time

    except Exception as e:
        print(f"Error al extraer palabras del archivo {file_name}: {e}")
        return 0.0  # devuelve un número válido en caso de error

def compose_order_file(file_name):
    # ordena el archivo compuesto
    encoding = detect_encoding(file_name) or 'utf-8'
    # manejo de excepciones
    try:

        start_time = time.time()

        # se extraen todas las palabras del archivo
        with open(file_name, 'r+', encoding=encoding, errors='replace') as file:
            content = file.read().splitlines()
            lowercase_content = [word.lower() for word in content]
            ordered_content = sorted(lowercase_content, key=str.lower)
            file.seek(0)
            file.truncate(0)
            file.write('\n'.join(ordered_content))
        
        end_time = time.time()
        order_time = end_time - start_time

        print(f"Proceso completado. El archivo {file_name} se ha ordenado correctamente")
        print(f"Tiempo de ordenación: {order_time:.6f} segundos")

        return order_time

    except Exception as e:
        print(f"Error al ordenar el archivo {file_name}: {e}")
        return 0.0  # devuelve un número válido en caso de error

def log_composing_results(log_file_extraction, results, total_extraction_time, total_order_time, total_execution_time):
    # registra los tiempos de extracción y ejecución en un archivo .txt
    with open(log_file_extraction, 'w', encoding='utf-8-sig') as log:
        log.write("Archivo, Tiempo de Extracción (segundos)\n")
        for result in results:
            log.write(f"{result['file']}, {result.get('extract_time', 0):.6f}\n")
        
        log.write(f"\nTiempo total de Extracción: {total_extraction_time:.6f} segundos\n")
        log.write(f"\nTiempo total de Ordenamiento: {total_order_time:.6f} segundos\n")
        log.write(f"Tiempo total de ejecución: {total_execution_time:.6f} segundos\n")  # Nueva línea
