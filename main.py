# -*- coding: utf-8 -*-
import os
import time
from file_reader import open_file, log_results
from remove_tags import remove_html_tags, log_cleaning_results
from order_words import order_words_file, log_ordering_results

def main():
    # Ruta principal y subcarpeta donde estan los archivos HTML
    base_directory = os.getcwd() # cambiar ruta !!!!
    subfolder = "resources"
    directory = os.path.join(base_directory, subfolder)
    resources_order_output = "act3_ordered"
    output_directory = os.path.join(base_directory, resources_order_output)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # creacion de dos logs separados
    log_file = "a1_matricula.txt"
    log_file_clean = "a2_clean.txt"
    log_file_order = "a3_matricula.txt"

    if not os.path.exists(directory):
        print(f"Error: El directorio '{directory}' no existe.")
        return

    print(f"Procesando archivos en el directorio: {directory}")
    results = []
    total_start_time = time.time()  # Tiempo total de ejecucion
    total_open_time = 0.0  # Tiempo total en abrir los archivos
    total_clean_time = 0.0  # tiempo total de limpieza
    total_order_time = 0.0 # Tiempo total en ordenar palabras

    # Verifica el contenido del directorio
    files_in_directory = os.listdir(directory)
    print(f"Archivos encontrados: {files_in_directory}")

    for file_name in sorted(files_in_directory):
        if file_name.endswith(".html"):
            file_path = os.path.join(directory, file_name)
            output_file = os.path.join(output_directory, file_name)
            print(f"Procesando archivo: {file_path}")
            
            # Medir tiempo de limpieza
            clean_time = remove_html_tags(file_path, log_file_clean)
            if clean_time is not None:  # Evita errores de suma con NoneType
                total_clean_time += clean_time

            # Se mide el tiempo de apertura de cada archivo
            start_time = time.time()
            content = open_file(file_path)
            end_time = time.time() 

            # Medir tiempo de ordenado de palabras
            order_time = order_words_file(file_path, log_file_order, output_file)
            if order_time is not None:
                total_order_time += order_time
            
            if content is not None:
                open_time = end_time - start_time
                total_open_time += open_time
                results.append({
                    "file": file_name,
                    "time": open_time,
                    "clean_time": clean_time,
                    "order_time": order_time
                })
            else:
                print(f"No se pudo abrir el archivo: {file_path}")

    total_end_time = time.time()  # Tiempo total final
    total_execution_time = total_end_time - total_start_time

    log_results(log_file, results, total_open_time, total_execution_time)
    print(f"Resultados de apertura escritos en {log_file}")

    log_cleaning_results(log_file_clean, results, total_clean_time, total_execution_time)
    print(f"Resultados de limpieza escritos en {log_file_clean}")

    log_ordering_results(log_file_order, results, total_order_time, total_execution_time)
    print(f"Resultados de orden escritos en {log_file_order}")

if __name__ == "__main__":
    main()