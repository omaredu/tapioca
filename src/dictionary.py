import pandas as pd
import os
from src.hashtable import HashTable
from stoplist.stoplist import StopList


class Dictionary:
    def __init__(self, dictionary_path, posting_path):
        if not os.path.exists(dictionary_path) or not os.path.exists(posting_path):
            raise FileNotFoundError(
                f"❌ Archivos {dictionary_path} o {posting_path} no encontrados."
            )
        self.stop_list = StopList("src/stoplist/stoplist.txt")
        self.dictionary_path = dictionary_path
        self.posting_path = posting_path
        self.dictionary_df = pd.read_csv(dictionary_path)
        self.posting_df = pd.read_csv(posting_path)
        self.hash_table = HashTable(len(self.dictionary_df))

    def load_into_hash_table(self):
        print("\n🛠️ Cargando dictionary.csv en la Hash Table...")
        for _, row in self.dictionary_df.iterrows():
            token = row["Token"]
            frequency = row["Cantidad de documentos que lo contienen"]
            position = row["Posicion del primer registro en posting"]

            if self.stop_list.is_stop_word(str(token)):
                continue

            self.hash_table.insert(token, frequency, position)
        print("✅ Datos cargados en la Hash Table.")

    def get_token_info(self, token):
        position = self.hash_table.get(token)
        if position is not None:
            return self.posting_df.iloc[position].to_dict()
        return None

    def save_dictionary(self, output_path):
        self.dictionary_df.to_csv(output_path, index=False)
        print(f"✅ Diccionario guardado en: {output_path}")


if __name__ == "__main__":
    dictionary = Dictionary("out/dictionary.csv", "out/posting.csv")
    dictionary.load_into_hash_table()
    print(dictionary.get_token_info("example"))
