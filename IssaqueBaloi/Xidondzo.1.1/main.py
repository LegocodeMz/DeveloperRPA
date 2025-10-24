import os
from web_scraper import download_file
from data_processor import identificar_formato, ler_e_extrair_campos, validar_dados, transformar_dados
from csv_generator import gerar_csv
import unittest
import sys
from io import StringIO

def main():
    """Orquestra o processo de download, processamento e geração do CSV."""
    download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    caminho_ficheiro = download_file(download_dir)
    
    if caminho_ficheiro and identificar_formato(caminho_ficheiro):
        dados = ler_e_extrair_campos(caminho_ficheiro)
        if not dados:
            print("⚠️ Nenhum dado extraído do ficheiro.")
            return
        dados_validados = validar_dados(dados)
        dados_transformados = transformar_dados(dados_validados)
        caminho_saida = gerar_csv(dados_transformados, download_dir)
        
        # Validação simples do CSV
        if caminho_saida and os.path.exists(caminho_saida):
            with open(caminho_saida, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")
                rows = list(reader)
                if len(rows) != len(dados_transformados):
                    print("⚠️ Verificação do CSV: Número de linhas incorreto.")
        else:
            print("⚠️ Verificação do CSV: Ficheiro não encontrado.")

if __name__ == "__main__":
    print("\nIniciando automação...")
    main()
    
    print("\nExecutando testes de validação...")
    # Redirecionar saída para capturar resultados dos testes
    old_stdout = sys.stdout
    result_output = StringIO()
    sys.stdout = result_output
    
    # Carregar e executar testes
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__('tests'))
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)
    
    # Restaurar stdout e exibir resultados
    sys.stdout = old_stdout
    print(result_output.getvalue())
    
    # Resumo dos resultados
    print("\nResumo dos Testes:")
    print(f"Testes executados: {result.testsRun}")
    print(f"Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Falhas: {len(result.failures)}")
    print(f"Erros: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ Todos os testes passaram com sucesso.")
    else:
        print("⚠️ Alguns testes falharam ou apresentaram erros.")