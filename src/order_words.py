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

def order_words_file(file_name, log_file, output_file):
     # separa cada palabra de un archivo y genera una lista ordenada de palabras
    encoding = detect_encoding(file_name) or 'utf-8'
    # manejo de excepciones
    try:
        with open(file_name, 'r', encoding=encoding, errors='replace') as file:
            content = file.read()

        start_time = time.time()
        # extraer palabras del archivo que estén separadas por espacios y ordenarlas, omitiendo numeros y palabras repetidas
        raw_content = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+\b', content, flags=re.DOTALL)
        ordered_content = sorted(set(raw_content), key=str.lower)
        
        end_time = time.time()
        order_time = end_time - start_time

        with open(output_file, 'x', encoding='utf-8') as file:
            file.write('\n'.join(ordered_content))

        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Archivo: {file_name}, Tiempo de ordenamiento: {order_time:.6f} segundos\n")

        print(f"Proceso completado. Archivo {file_name} ordenado y resultado generado.")
        print(f"Tiempo de ordenamiento: {order_time:.6f} segundos")

        return order_time

    except Exception as e:
        print(f"Error al ordenar el archivo {file_name}: {e}")
        return 0.0  # devuelve un número válido en caso de error


def log_ordering_results(log_file_order, results, total_order_time, total_execution_time):
    # registra los tiempos de ordenamiento y ejecución en un archivo .txt
    with open(log_file_order, 'w', encoding='utf-8-sig') as log:
        log.write("Archivo, Tiempo de Ordenamiento (segundos)\n")
        for result in results:
            log.write(f"{result['file']}, {result.get('order_time', 0):.6f}\n")
        
        log.write(f"\nTiempo total de Ordenamiento: {total_order_time:.6f} segundos\n")
        log.write(f"Tiempo total de ejecución: {total_execution_time:.6f} segundos\n")  # Nueva línea
