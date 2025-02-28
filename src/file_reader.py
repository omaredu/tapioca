# -*- coding: utf-8 -*-
import chardet  # Detecta la codificación

def open_file(file_path):
    try:
        # Se lee el archivo en modo binario para detectar la codificación
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'  # Usar UTF-8 si no detecta
            
        # Se abre el archivo con la codificación detectada
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: Archivo {file_path} no encontrado.")
        return None
    except Exception as e:
        print(f"Error al abrir el archivo {file_path}: {e}")
        return None

def log_results(log_file, results, total_open_time, total_execution_time):
    with open(log_file, 'w', encoding='utf-8-sig') as log:
        log.write("Archivo, Tiempo de Apertura (segundos)\n")
        for result in results:
            log.write(f"{result['file']}, {result['time']:.6f}\n")
        
        log.write("\n")
        log.write(f"Tiempo total en abrir los archivos: {total_open_time:.6f} segundos\n")
        log.write(f"Tiempo total de ejecucion: {total_execution_time:.6f} segundos\n")



