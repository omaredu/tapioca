import unittest
from src.dictionary import Dictionary


class TestDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Cargar datos de dictionary.csv y posting.csv en la Hash Table"""
        print(
            "\n📂 Cargando dictionary.csv y posting.csv para pruebas de integración..."
        )
        cls.dictionary = Dictionary("out/dictionary.csv", "out/posting.csv")
        cls.dictionary.load_into_hash_table()

    def test_get_token_info(self):
        """Prueba que la Hash Table devuelve posiciones correctas en posting.csv"""
        print("🔎 Probando búsqueda de un token en dictionary.csv...")
        token_info = self.dictionary.get_token_info("example")
        print(f"🔹 Token info obtenido: {token_info}")
        self.assertIsNotNone(token_info)

    def test_invalid_token(self):
        """Verifica que un token inexistente devuelva None"""
        print("🔴 Buscando token inexistente: 'randomwordnotfound'...")
        token_info = self.dictionary.get_token_info("randomwordnotfound")
        print(f"❌ Resultado esperado: None, obtenido: {token_info}")
        self.assertIsNone(token_info)


if __name__ == "__main__":
    unittest.main(verbosity=2)
