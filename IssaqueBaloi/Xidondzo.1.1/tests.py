import unittest
import tempfile
import os
import csv
from data_processor import identificar_formato, ler_e_extrair_campos, validar_dados, transformar_dados
from csv_generator import gerar_csv

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.sample_content = """
Nome: João Silva
E-mail: joao@example.com
Contacto / Tel: 82-123-456
Estado Civil: Solteiro
Salário Líquido: 10,000.00
--- END Registro: 1 ---

Nome: Maria Oliveira
E-mail: maria@example.com
Contacto / Tel: 84-789-012
Estado Civil: Casada
Salário Líquido: 15.500,50
--- END Registro: 2 ---
"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        self.temp_file.write(self.sample_content.encode('utf-8'))
        self.temp_file.close()
        self.temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv').name

    def tearDown(self):
        os.unlink(self.temp_file.name)
        if os.path.exists(self.temp_csv):
            os.unlink(self.temp_csv)

    def test_identificar_formato(self):
        self.assertTrue(identificar_formato(self.temp_file.name))
        temp_wrong = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_wrong.close()
        self.assertFalse(identificar_formato(temp_wrong.name))
        os.unlink(temp_wrong.name)

    def test_ler_e_extrair_campos(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        self.assertEqual(len(dados), 2)
        self.assertEqual(dados[0]['Nome'], 'João Silva')
        self.assertEqual(dados[1]['Salário Líquido'], '15.500,50')

    def test_validar_dados(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        self.assertEqual(dados_validados[0]['Validação'], '✅ Válido')
        self.assertEqual(dados_validados[1]['Validação'], '✅ Válido')

    def test_transformar_dados(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        dados_transformados = transformar_dados(dados_validados)
        self.assertEqual(dados_transformados[0]['Salário Líquido (MZN)'], '10000.00')
        self.assertEqual(dados_transformados[1]['Salário Líquido (MZN)'], '15500.50')

    def test_gerar_csv(self):
        dados = ler_e_extrair_campos(self.temp_file.name)
        dados_validados = validar_dados(dados)
        dados_transformados = transformar_dados(dados_validados)
        caminho_saida = gerar_csv(dados_transformados, os.path.dirname(self.temp_csv))
        self.assertTrue(os.path.exists(caminho_saida))
        with open(caminho_saida, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            rows = list(reader)
            self.assertEqual(rows[0]['Salário Líquido (MZN)'], '10000.00')
            self.assertEqual(rows[1]['Salário Líquido (MZN)'], '15500.50')
        if os.path.exists(caminho_saida):
            os.unlink(caminho_saida)