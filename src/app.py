import os
import heapq
from collections import defaultdict
from flask import Flask, request, render_template, url_for

# Rutas importantes
HERE = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(HERE, ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
DICTIONARY_PATH = os.path.join(BASE_DIR, "out", "dictionary.csv")
POSTING_PATH = os.path.join(BASE_DIR, "out", "posting.csv")
STOPLIST_PATH = os.path.join(BASE_DIR, "src", "stoplist", "stoplist.txt")

MAX_TOKEN_SIZE = 30  # tamaño máximo del token

def load_stoplist(path):
    stopwords = set()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    stopwords.add(w)
    return stopwords

STOPWORDS = load_stoplist(STOPLIST_PATH)

def filter_tokens(tokens_raw):
    filtered = [
        t.lower()
        for t in tokens_raw
        if t.lower() not in STOPWORDS and 0 < len(t) <= MAX_TOKEN_SIZE
    ]
    return filtered

def find_token_in_dictionary(token):
    token = token.lower()
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as f:
        next(f)  # saltar encabezado
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue
            dict_token, df, pos = parts
            if dict_token.lower() == token:
                try:
                    return int(df), int(pos)
                except ValueError:
                    return None
    return None

def read_postings(pos, df):
    results = []
    with open(POSTING_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < pos:
                continue
            if i >= pos + df:
                break
            parts = line.strip().split(",")
            if len(parts) != 2:
                continue
            fname, freq = parts
            try:
                freq = int(freq)
            except ValueError:
                freq = 0
            results.append((fname, freq))
    return results

def search(query):
    tokens_raw = query.split()
    tokens = filter_tokens(tokens_raw)

    documentos = defaultdict(int)
    for token in tokens:
        result = find_token_in_dictionary(token)
        if not result:
            continue
        df, pos = result
        postings = read_postings(pos, df)
        for fname, freq in postings:
            documentos[fname] += freq

    return documentos

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

    docs = search(q)
    top10 = heapq.nlargest(10, docs.items(), key=lambda x: x[1])

    results = []
    for idx, (fname, score) in enumerate(top10, start=1):
        html_name = fname if fname.endswith(".html") else f"{fname}.html"
        link = url_for("static", filename=html_name)
        results.append((idx, link, score))

    return render_template("results.html", query=q, results=results)

if __name__ == "__main__":
    app.run(debug=True)
