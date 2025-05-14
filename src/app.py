import os
import heapq
from collections import defaultdict
from functools import lru_cache
from flask import Flask, request, render_template, url_for

# Rutas
HERE             = os.path.dirname(__file__)                          
BASE_DIR         = os.path.abspath(os.path.join(HERE, ".."))           
TEMPLATES_DIR    = os.path.join(BASE_DIR, "templates")                
RESOURCES_DIR    = os.path.join(BASE_DIR, "resources")                
DICTIONARY_PATH  = os.path.join(BASE_DIR, "out", "dictionary.csv")
POSTING_PATH     = os.path.join(BASE_DIR, "out", "posting.csv")

# Carga en memoria
def load_dictionary(path):
    d = {}
    with open(path, "r", encoding="utf-8") as f:
        next(f)  # saltar encabezado
        for line in f:
            try:
                token, df, pos = line.strip().split(",")
                d[token.lower()] = (int(df), int(pos))
            except ValueError:
                continue
    return d

def load_postings(path):
    lst = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                fname, freq = line.strip().split(",")
                lst.append((fname, int(freq)))
            except ValueError:
                continue
    return lst

# Índices en RAM
DICTIONARY = load_dictionary(DICTIONARY_PATH)
POSTINGS   = load_postings(POSTING_PATH)

# Función de búsqueda cacheada 
@lru_cache(maxsize=128)
def search(query: str) -> dict:
    tokens     = tuple(query.lower().split())
    documentos = defaultdict(int)
    for token in tokens:
        if token not in DICTIONARY:
            continue
        df, pos = DICTIONARY[token]
        for fname, freq in POSTINGS[pos:pos+df]:
            documentos[fname] += freq
    return documentos

# Flask App
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=RESOURCES_DIR,
    static_url_path="/resources"
)

@app.route("/", methods=["GET"])
def index():
    q = request.args.get("q")
    if not q:
        return render_template("index.html")

    # Se ejecuta la búsqueda y nos quedamos con los primeros 10 resultados
    docs  = search(q)
    top10 = heapq.nlargest(10, docs.items(), key=lambda x: x[1])

    # Se construye la lista de vínculos
    results = []
    for fname, score in top10:
        html_name = fname if fname.endswith(".html") else f"{fname}.html"
        link      = url_for("static", filename=html_name)
        results.append((link, score))

    return render_template("results.html", query=q, results=results)

if __name__ == "__main__":
    app.run(debug=True)
