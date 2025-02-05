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

def remove_html_tags(file_name, log_file):
     # elimina etiquetas HTML y sobrescribe el mismo archivo.
    encoding = detect_encoding(file_name) or 'utf-8'
    
    # mamejo de excepciones
    try:
        with open(file_name, 'r', encoding=encoding, errors='replace') as file:
            content = file.read()

        start_time = time.time()
        # eliminar etiquetas HTML, en multiples lineas, y convierte entidades HTML
        clean_content = re.sub(r'<.*?>', '', content, flags=re.DOTALL)
        clean_content = html.unescape(clean_content)
        
        end_time = time.time()
        clean_time = end_time - start_time

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(clean_content)

        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"Archivo: {file_name}, Tiempo de limpieza: {clean_time:.6f} segundos\n")

        print(f"Proceso completado. Archivo {file_name} sobrescrito con contenido limpio.")
        print(f"Tiempo de limpieza: {clean_time:.6f} segundos")

        return clean_time

    except Exception as e:
        print(f"Error al limpiar el archivo {file_name}: {e}")
        return 0.0  # devuelve un número válido en caso de error


def log_cleaning_results(log_file_clean, results, total_clean_time, total_execution_time):
    # registra los tiempos de limpieza y ejecución en un archivo .txt
    with open(log_file_clean, 'w', encoding='utf-8-sig') as log:
        log.write("Archivo, Tiempo de Limpieza (segundos)\n")
        for result in results:
            log.write(f"{result['file']}, {result.get('clean_time', 0):.6f}\n")
        
        log.write(f"\nTiempo total de limpieza: {total_clean_time:.6f} segundos\n")
        log.write(f"Tiempo total de ejecución: {total_execution_time:.6f} segundos\n")  # Nueva línea
