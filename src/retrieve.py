import time

def search(word, dictionary, postings, documents):
    word = word.lower().strip()

    if word not in dictionary:
        print(f"⚠ La palabra '{word}' no fue encontrada en el diccionario.")
        return None

    entry = dictionary[word]
    start = entry['pos']  # Posición del primer registro en 'posting.csv'
    df = entry['df']  # Cantidad de documentos que contienen la palabra

    # Imprimir valores para depuración
    print(f"Palabra encontrada: '{word}'")
    print(f"Posición de inicio: {start}, Número de documentos que contienen la palabra: {df}")
    print(f"Longitud de postings: {len(postings)}")

    # Comprobación de rango antes de acceder
    if start + df > len(postings):
        print(f" Error: El índice de los postings está fuera de rango. La posición 'start' + 'df' excede la longitud de 'postings'.")
        return None

    results = []
    for i in range(start, start + df):
        # Obtener el nombre del archivo en la línea correspondiente de 'posting.csv'
        doc_name = postings[i].split(",")[0]  # Por ejemplo, '269.html'
        
        # Buscar la ruta completa del archivo en 'documents.csv'
        if doc_name in documents:
            results.append(documents[doc_name])
        else:
            print(f" El archivo '{doc_name}' no tiene una ruta en documents.csv.")

    return results

def main():
    # Leer los archivos CSV con codificación UTF-8
    dictionary = {}
    with open('out/dictionary.csv', 'r', encoding='utf-8') as file:
        next(file)  # Omitir la primera línea (encabezado)
        for line in file:
            line = line.strip()
            if not line:  # Ignorar líneas vacías
                continue
            parts = line.split(',')
            if len(parts) == 3:  # Asegurarse de que la línea tenga 3 elementos
                token, df, pos = parts
                dictionary[token.lower()] = {'df': int(df), 'pos': int(pos)}
            else:
                print(f"Advertencia: La línea no tiene el formato esperado: {line}")

    postings = []
    with open('out/posting.csv', 'r', encoding='utf-8') as file:
        for line in file:
            postings.append(line.strip())

    documents = {}
    with open('out/documents.csv', 'r', encoding='utf-8') as file:
        for line in file:
            doc_id, file_name = line.strip().split(',')
            documents[file_name] = file_name  # Almacenar solo el nombre del archivo

    # Pedir la palabra a buscar
    word = input("Ingresa la palabra a buscar: ").lower()

    start_time = time.time()
    results = search(word, dictionary, postings, documents)
    end_time = time.time()

    if results:
        print(f"\n Resultados encontrados para '{word}':")
        for result in results:
            print(result)
    else:
        print(f"\n No se encontraron documentos que contengan la palabra '{word}'.")

    # Guardar el log con el tiempo de búsqueda
    with open('out/a12_matricula.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"Palabra buscada: '{word}'\n")
        log_file.write(f"Tiempo de búsqueda: {end_time - start_time:.4f} segundos\n\n")

if __name__ == "__main__":
    main()



