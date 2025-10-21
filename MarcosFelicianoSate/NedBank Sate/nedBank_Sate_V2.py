import os
import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException


service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)

try:
    navegador.get("https://rpa.xidondzo.com/")
    time.sleep(5)
except TimeoutException:
    print("Erro: O tempo de carregamento da página excedeu o limite.")

except WebDriverException as e:
    print(f"Erro ao acessar a página: {e}")

except Exception as e:
    print(f"Erro inesperado: {e}")


#Armazena todos os links de botões de download de arquivos txt
botao_download = navegador.find_elements("xpath",
                                         '//a[@class="btn btn-success" and @download]')

#Baixa todos os arquivos txt encontrados
for botao in botao_download:
    try:
        botao.click()
        time.sleep(2)  # Aguarda 2 segundos entre os cliques
    except Exception as e:
        print(f"Erro ao clicar no botão: {e}")

diretorio = os.path.join(os.environ['USERPROFILE'], 'Downloads')

#Obter o diretório atual do script
diretorio_atual = os.getcwd()
print(diretorio_atual)

#Criar o arquivo CSV para armazenar os dados extraídos na pasta atual do script
csv_path = os.path.join(diretorio_atual, 'dados_extraidos.csv')

#Criar o arquivo CSV para armazenar os dados extraídos na pasta atual do script contendo informacao em falta
csv_path_erro = os.path.join(diretorio_atual, 'dados_extraidos_informacao_falta.csv')

waiter = navegador.implicitly_wait(10)

arquivos = [f for f in os.listdir(
    diretorio) if f.startswith('R') and f.endswith('.txt')]

dados_cadastrados = set()

with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile, \
     open(csv_path_erro, mode='a', newline='', encoding='utf-8') as csvfile_erro:
    
    writer = csv.writer(csvfile)
    writer_erro = csv.writer(csvfile_erro)
    
    # Escrever o cabeçalho no CSV apenas se o arquivo estiver vazio (modo 'a' não sobrescreve)
    if csvfile.tell() == 0:  # Verifica se o arquivo está vazio
        writer.writerow(['Nome', 'E-mail', 'Contacto / Tel', 'Estado Civil', 'Salário Líquido'])

    # Escrever o cabeçalho no CSV de erros apenas se o arquivo estiver vazio
    if csvfile_erro.tell() == 0:
        writer_erro.writerow(['Nome', 'E-mail', 'Contacto / Tel', 'Estado Civil', 'Salário Líquido'])

    # Processar os arquivos
    for arquivo in arquivos:
        arquivo_path = os.path.join(diretorio, arquivo)

        with open(arquivo_path, 'r', encoding='utf-8') as file:
            nome, mail, contacto, estadoCivil, salario = None, None, None, None, None

            # Processar o conteúdo do arquivo
            for linha in file:
                if "Nome:" in linha:
                    nome = linha.split(":")[1].strip()
                if "E-mail:" in linha:
                    mail = linha.split(":")[1].strip()
                if "Contacto / Tel:" in linha:
                    contacto = linha.split(":")[1].strip()
                if "Estado Civil:" in linha:
                    estadoCivil = linha.split(":")[1].strip()
                if "Sal" in linha:
                    salario = linha.split(":")[1].strip()
                identificador = (nome, mail)  # Usar tupla como identificador único

                # Quando todos os dados forem encontrados, verificar e adicionar ao CSV
                if identificador not in dados_cadastrados:
                    
                    # Verificar se os dados já foram cadastrados
                    if nome and mail and contacto and estadoCivil and salario:
                        print(f"Cadastrando dados para {nome} ({mail})...")
                        dados_cadastrados.add(identificador)
                        # Escrever no arquivo CSV
                        writer.writerow([nome, mail, contacto, estadoCivil, salario])
                    else:
                        print(f"Dados incompletos para {nome} ({mail}), armazenando no arquivo de erro...")
                        writer_erro.writerow([nome or "Faltando", mail or "Faltando", contacto or "Faltando", estadoCivil or "Faltando", salario or "Faltando"])
                   

                else:
                    print(f"Dados já cadastrados para {nome} ({mail}), ignorando...")     

                    # Resetar as variáveis para o próximo conjunto de dados
                    nome, mail, contacto, estadoCivil, salario = None, None, None, None, None


input('')
