import json
import unittest
from io import BytesIO
import sys
import os

# Adiciona o diretório pai ao path para importar api_ibge
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_ibge import buscar_municipios_por_uf


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def read(self):
        return self.payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class IBGEApiIntegrationTest(unittest.TestCase):
    def test_buscar_municipios_por_uf_formata_resposta_da_api(self):
        resposta_ibge = [
            {"id": 3550308, "nome": "Sao Paulo"},
            {"id": 3509502, "nome": "Campinas"},
        ]

        def opener(url, timeout):
            self.assertIn("/estados/SP/municipios", url)
            self.assertEqual(timeout, 10)
            return FakeResponse(json.dumps(resposta_ibge).encode("utf-8"))

        municipios = buscar_municipios_por_uf("sp", opener=opener)

        self.assertEqual(municipios, ["Sao Paulo", "Campinas"])

    def test_buscar_municipios_por_uf_rejeita_uf_invalida(self):
        with self.assertRaises(ValueError):
            buscar_municipios_por_uf("Sao Paulo")


if __name__ == "__main__":
    unittest.main()
