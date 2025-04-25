import sys
import heapq
import time
from collections import defaultdict

DICTIONARY_PATH = 'out/dictionary.csv'
POSTING_PATH = 'out/posting.csv'
LOG_PATH = 'out/a13_matricula.txt'  # Cambia "matricula" por tu número si es necesario

def buscar_posiciones(tokens):
    posiciones = {}
    with open(DICTIONARY_PATH, 'r', encoding='utf-8') as f:
        next(f)  # Saltar encabezado
        for line in f:
            try:
                token, df, pos = line.strip().split(',')
                token = token.lower()
                if token in tokens:
                    posiciones[token] = {'df': int(df), 'pos': int(pos)}
            except ValueError:
                continue
    return posiciones

def leer_postings(pos, df):
    resultados = []
    with open(POSTING_PATH, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < pos:
                continue
            if i >= pos + df:
                break
            try:
                filename, freq = line.strip().split(',')
                resultados.append((filename, int(freq)))
            except ValueError:
                continue
    return resultados

def calcular_relevancia(tokens):
    posiciones = buscar_posiciones(tokens)
    documentos = defaultdict(int)
    for token in tokens:
        if token not in posiciones:
            continue
        datos = posiciones[token]
        resultados = leer_postings(datos['pos'], datos['df'])
        for filename, freq in resultados:
            documentos[filename] += freq
    return documentos

def imprimir_resultados(tokens, documentos, tiempo_total):
    top10 = heapq.nlargest(10, documentos.items(), key=lambda x: x[1])
    
    with open(LOG_PATH, 'w', encoding='utf-8') as log:
        log.write(f"Consulta: {' '.join(tokens)}\n")
        
        if not documentos:
            print(" No se encontraron documentos relevantes.")
            log.write("No se encontraron documentos relevantes.\n")
        else:
            print(f"\n Resultados para tokens: {' '.join(tokens)}")
            print("Top documentos:")
            log.write("Top 10 documentos:\n")
            for i, (doc, score) in enumerate(top10, 1):
                print(f"{i}. {doc} (puntaje: {score})")
                log.write(f"{i}. {doc} (puntaje: {score})\n")
        
        print(f"\n⏱ Tiempo de búsqueda: {tiempo_total:.6f} segundos")
        log.write(f"\n⏱ Tiempo de búsqueda: {tiempo_total:.6f} segundos\n")

    print(f" Resultados guardados en {LOG_PATH}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python retrieve13.py palabra1 palabra2 ...")
        return

    tokens = [word.lower() for word in sys.argv[1:]]

    inicio = time.time()
    documentos = calcular_relevancia(tokens)
    fin = time.time()
    tiempo_total = fin - inicio

    imprimir_resultados(tokens, documentos, tiempo_total)

if __name__ == '__main__':
    main()
