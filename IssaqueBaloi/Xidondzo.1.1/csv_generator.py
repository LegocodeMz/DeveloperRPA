import csv
import os
from datetime import datetime
import locale

def gerar_csv(dados_transformados, download_dir):
    """Cria ficheiro CSV com codificação UTF-8 BOM e delimitador ponto e vírgula."""
    # Configurar locale para português
    try:
        locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')
    except locale.Error:
        print("⚠️ Locale 'pt_PT.UTF-8' não disponível. Usando formato padrão.")

    # Gerar nome do arquivo com base no mês e ano
    data_atual = datetime.now()
    mes_ano = data_atual.strftime("%B_%Y").lower()  # Exemplo: outubro_2025
    nome_ficheiro = f"Genericreport_{mes_ano}.csv"
    caminho_saida = os.path.join(download_dir, nome_ficheiro)

    # Remover arquivo existente com o mesmo nome, se houver
    if os.path.exists(caminho_saida):
        try:
            os.remove(caminho_saida)
            print(f"✅ Arquivo existente '{nome_ficheiro}' removido para substituição.")
        except Exception as e:
            print(f"⚠️ Erro ao remover arquivo existente: {str(e)}")

    cabecalhos = ["Nome", "Email", "Contacto", "Estado Civil", "Salário Líquido (MZN)"]

    try:
        with open(caminho_saida, mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=cabecalhos, delimiter=";")
            writer.writeheader()
            for row in dados_transformados:
                writer.writerow(row)
        print(f"✅ Ficheiro CSV criado com sucesso em:\n   {caminho_saida}")
        return caminho_saida
    except Exception as e:
        print(f"Erro ao gerar CSV: {str(e)}")
        return None