import pandas as pd
import os
import sympy


class HashTable:
    def __init__(self, size=1000):
        self.size = sympy.nextprime(size)
        self.table = [""] * self.size
        self.frequencies = [0] * self.size
        self.positions = [-1] * self.size
        self.collisions = 0

    def insert(self, key, frequency, position):
        index = hash(key) % self.size

        original_index = index
        while self.table[index] != "":
            self.collisions += 1
            index = (index + 1) % self.size
            if index == original_index:
                raise Exception(
                    "Tabla Hash llena, no se pueden insertar más elementos."
                )

        self.table[index] = key
        self.frequencies[index] = frequency
        self.positions[index] = position

    def get_collisions(self):
        return self.collisions

    def display_table(self):
        output_path = "out/dictionary_ascii.txt"
        print("\n📂 Mostrando y guardando Hash Table en formato ASCII...\n")

        header = "Diccionario Hash Table\n" + "=" * 40 + "\n"
        header += "{:<4} {:<20} {:<5} {:<5}\n".format("#", "Token", "Freq", "Pos")
        header += "=" * 40 + "\n"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
            print(header)
            for i in range(self.size):
                token = str(self.table[i])
                frequency = self.frequencies[i]
                position = self.positions[i]
                line = (
                    f"{i + 1:<4} {''.ljust(20)} {0:<5} {-1:<5}\n"
                    if token == ""
                    else f"{i + 1:<4} {token.ljust(20)} {frequency:<5} {position:<5}\n"
                )

                f.write(line)
                print(line, end="")
            collision_info = f"\nNúmero total de colisiones: {self.get_collisions()}\n"
            f.write(collision_info)
            print(collision_info)
        print("\n✅ Hash Table mostrada y guardada correctamente en", output_path)


class DictionaryHashTable:
    def __init__(
        self, dictionary_path="out/dictionary.csv", posting_path="out/posting.csv"
    ):
        if not os.path.exists(dictionary_path) or not os.path.exists(posting_path):
            raise FileNotFoundError(
                f"❌ Archivos {dictionary_path} o {posting_path} no encontrados."
            )

        self.dictionary_path = dictionary_path
        self.posting_path = posting_path
        self.dictionary_df = pd.read_csv(dictionary_path, dtype={"Token": str})
        self.posting_df = pd.read_csv(posting_path)
        num_tokens = len(self.dictionary_df)
        self.hash_table = HashTable(size=num_tokens * 2)

    def load_into_hash_table(self):
        print("\n🛠️ Cargando dictionary.csv en la Hash Table...\n")

        for _, row in self.dictionary_df.iterrows():
            token = str(row["Token"])
            frequency = row["Cantidad de documentos que lo contienen"]
            position = row["Posicion del primer registro en posting"]
            self.hash_table.insert(token, frequency, position)

        print("✅ Datos cargados en la Hash Table.")

    def display_and_save_ascii(self):
        self.hash_table.display_table()


if __name__ == "__main__":
    print("\n🚀 Ejecutando `hash_table_dictionary.py`...\n")
    dictionary = DictionaryHashTable()
    dictionary.load_into_hash_table()
    dictionary.display_and_save_ascii()
