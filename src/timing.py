import time
import os
import glob
HTML_DIR = "resources/"
LOG_FILE = "resources/a8_matricula.txt"

def log_time(file_path, duration):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{file_path:<40} {duration:.2f}\n")
def process_files():
    print("\n🚀 Iniciando medición de tiempos...\n")

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    total_start = time.time()
    file_count = 0
    html_files = sorted(glob.glob(os.path.join(HTML_DIR, "*.html")))
    for file_path in html_files:
        start_time = time.time()
        time.sleep(0.01)
        duration = time.time() - start_time
        file_count += 1
        print(f"{file_path:<40} {duration:.2f}")
        log_time(file_path, duration)
    total_duration = time.time() - total_start
    print(f"\nTiempo total de ejecución del programa: {total_duration:.2f} segundos")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\nTiempo total de ejecución del programa: {total_duration:.2f} segundos\n")
    print(f"\n✅ Medición de tiempos completada. 📂 Log guardado en '{LOG_FILE}'.")
if __name__ == "__main__":
    process_files()
