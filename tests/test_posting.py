import unittest
from src.postingfile import PostingFile


class TestPostingFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Cargar archivos dictionary.csv y posting.csv antes de ejecutar pruebas"""
        print("\n📂 Cargando archivos dictionary.csv y posting.csv...")
        cls.posting_file = PostingFile("out/posting.csv")

    def test_get_documents(self):
        """Verifica que se puedan obtener documentos desde posting.csv"""
        print("🔎 Probando acceso a documentos en posting.csv...")
        doc_info = self.posting_file.get_documents(0)
        print(f"📄 Documento obtenido: {doc_info}")
        self.assertIsNotNone(doc_info)

    def test_invalid_position(self):
        """Verifica que una posición inválida en posting.csv devuelva None"""
        print("🔴 Buscando documento en una posición inválida...")
        invalid_doc = self.posting_file.get_documents(999999)
        print(f"❌ Resultado esperado: None, obtenido: {invalid_doc}")
        self.assertIsNone(invalid_doc)


if __name__ == "__main__":
    unittest.main(verbosity=2)
