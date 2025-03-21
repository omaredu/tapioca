class HashTable:
    def __init__(self, size=10000):
        self.size = size
        self.table = [""] * size
        self.frequencies = [0] * size
        self.positions = [-1] * size
        self.collisions = 0
    def insert(self, key, frequency, position):
        index = hash(key) % self.size
        original_index = index
        while self.table[index] != "":
            self.collisions += 1
            index = (index + 1) % self.size
            if index == original_index:
                raise Exception("Tabla Hash llena, no se pueden insertar más elementos.")
        self.table[index] = key
        self.frequencies[index] = frequency
        self.positions[index] = position
    def get(self, key):
        index = hash(key) % self.size
        original_index = index
        while self.table[index] != "":
            if self.table[index] == key:
                return self.positions[index]
            index = (index + 1) % self.size
            if index == original_index:
                break
        return None
    def get_collisions(self):
        return self.collisions
    def export_to_ascii(self, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Diccionario Hash Table\n")
            f.write("=" * 40 + "\n")
            f.write("{:<4} {:<20} {:<5} {:<5}\n".format("#", "Token", "Freq", "Pos"))
            f.write("=" * 40 + "\n")
            for i in range(self.size):
                f.write("{:<4} {:<20} {:<5} {:<5}\n".format(i + 1, self.table[i], self.frequencies[i], self.positions[i]))