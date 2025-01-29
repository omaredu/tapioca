# -*- coding: utf-8 -*-
import os
import time
from file_reader import open_file, log_results  

def main():
    # Ruta principal y subcarpeta donde est?n los archivos HTML
    base_directory = r"C:\Users\Natalia Espinosa\Downloads\CS13309_Archivos_HTML"
    subfolder = "Files"
    directory = os.path.join(base_directory, subfolder)
    log_file = "a1_matricula.txt"

    if not os.path.exists(directory):
        print(f"Error: El directorio '{directory}' no existe.")
        return

    print(f"Procesando archivos en el directorio: {directory}")
    results = []
    total_start_time = time.time()  # Tiempo total de ejecuci?n
    total_open_time = 0.0  # Tiempo total en abrir los archivos

    # Verifica el contenido del directorio
    files_in_directory = os.listdir(directory)
    print(f"Archivos encontrados: {files_in_directory}")

    for file_name in sorted(files_in_directory):
        if file_name.endswith(".html"):
            file_path = os.path.join(directory, file_name)
            print(f"Procesando archivo: {file_path}")
            
            # Se mide el tiempo de apertura de cada archivo
            start_time = time.time()
            content = open_file(file_path)
            end_time = time.time()
            
            if content is not None:
                open_time = end_time - start_time
                total_open_time += open_time
                results.append({"file": file_name, "time": open_time})
            else:
                print(f"No se pudo abrir el archivo: {file_path}")

    total_end_time = time.time()  # Tiempo total final
    total_execution_time = total_end_time - total_start_time

    # Se escriben los resultados en el archivo de log
    log_results(log_file, results, total_open_time, total_execution_time)
    print(f"Resultados escritos en el archivo {log_file}")

if __name__ == "__main__":
    main()



