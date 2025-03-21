import unittest
from src.hashtable import HashTable


class TestHashTable(unittest.TestCase):

    def setUp(self):
        """ Configuración inicial antes de cada prueba """
        self.hash_table = HashTable(100)
        print("\n🔹 Creando nueva instancia de HashTable con tamaño 100...")

    def test_insert_and_retrieve(self):
        """ Prueba la inserción y recuperación de valores en la Hash Table """
        print("🟢 Insertando 'example' con valor 42 en posición 0...")
        self.hash_table.insert("example", 42, 0)  # Se agregó la posición 0
        retrieved_value = self.hash_table.get("example")
        print(f"🔍 Recuperado: {retrieved_value}")
        self.assertEqual(retrieved_value, 0)  # La posición esperada es 0

    def test_insert_multiple(self):
        """ Inserta varios valores y verifica su correcta recuperación """
        data = {
            "word1": (10, 1),
            "word2": (20, 2),
            "word3": (30, 3)
        }
        print(f"🟢 Insertando múltiples valores: {data}")
        for key, (frequency, position) in data.items():
            self.hash_table.insert(key, frequency, position)

        for key, (_, expected_position) in data.items():
            retrieved_value = self.hash_table.get(key)
            print(f"🔍 Recuperado {key}: {retrieved_value}")
            self.assertEqual(retrieved_value, expected_position)

    def test_nonexistent_key(self):
        """ Verifica que una clave inexistente devuelva None """
        print("🔴 Buscando clave inexistente: 'nonexistent'...")
        retrieved_value = self.hash_table.get("nonexistent")
        print(f"❌ Resultado esperado: None, obtenido: {retrieved_value}")
        self.assertIsNone(retrieved_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
