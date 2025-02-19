# -*- coding: utf-8 -*-
import os
import time
import shutil
from file_reader import open_file, log_results
from remove_tags import remove_html_tags, log_cleaning_results
from order_words import order_words_file, log_ordering_results
from compose_file import compose_add_words, compose_order_file, log_composing_results

def main():
    # Ruta principal y subcarpeta donde estan los archivos HTML
    base_directory = os.getcwd() # cambiar ruta !!!!
    subfolder = "resources"
    directory = os.path.join(base_directory, subfolder)

    # Directorio para archivos output de actividad 3
    resources_order_output = "act3_ordered"
    output_directory = os.path.join(base_directory, resources_order_output)
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
        os.makedirs(output_directory)
    else:
        os.makedirs(output_directory)
    
    # Archivo para output de actividad 4
    compose_file_output = "act4_archivoConsolidado.txt"
    compose_file_directory = os.path.join(base_directory, compose_file_output)
    if os.path.exists(compose_file_directory):
        os.remove(compose_file_directory)
    
    # creacion de los logs separados
    log_file = "a1_matricula.txt"
    log_file_clean = "a2_clean.txt"
    log_file_order = "a3_matricula.txt"
    log_file_compose = "a4_matricula.txt"

    if not os.path.exists(directory):
        print(f"Error: El directorio '{directory}' no existe.")
        return

    print(f"Procesando archivos en el directorio: {directory}")
    results = []
    total_start_time = time.time()  # Tiempo total de ejecucion
    total_open_time = 0.0  # Tiempo total en abrir los archivos
    total_clean_time = 0.0  # tiempo total de limpieza
    total_order_time = 0.0 # Tiempo total en ordenar palabras
    total_compose_time = 0.0 # Tiempo total en llenar el archivo compuesto

    # Verifica el contenido del directorio
    files_in_directory = os.listdir(directory)
    print(f"Archivos encontrados: {files_in_directory}")

    for file_name in sorted(files_in_directory):
        if file_name.endswith(".html"):
            file_path = os.path.join(directory, file_name)
            act3_output_file = os.path.join(output_directory, file_name)
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
            order_time = order_words_file(file_path, log_file_order, act3_output_file)
            if order_time is not None:
                total_order_time += order_time

            # Medir el tiempo al agregar palabras al archivo consolidado
            extract_time = compose_add_words(act3_output_file, log_file_compose, compose_file_output)
            if extract_time is not None:
                total_compose_time += extract_time
            
            if content is not None:
                open_time = end_time - start_time
                total_open_time += open_time
                results.append({
                    "file": file_name,
                    "time": open_time,
                    "clean_time": clean_time,
                    "order_time": order_time,
                    "extract_time": extract_time,
                })
            else:
                print(f"No se pudo abrir el archivo: {file_path}")

    compose_order_time = compose_order_file(compose_file_directory)
    total_end_time = time.time()  # Tiempo total final
    total_execution_time = total_end_time - total_start_time

    log_results(log_file, results, total_open_time, total_execution_time)
    print(f"Resultados de apertura escritos en {log_file}")

    log_cleaning_results(log_file_clean, results, total_clean_time, total_execution_time)
    print(f"Resultados de limpieza escritos en {log_file_clean}")

    log_ordering_results(log_file_order, results, total_order_time, total_execution_time)
    print(f"Resultados de orden escritos en {log_file_order}")

    log_composing_results(log_file_compose, results, total_compose_time, compose_order_time, total_execution_time)
    print(f"Resultados de archivo consolidado escritos en {log_file_order}")

if __name__ == "__main__":
    main()