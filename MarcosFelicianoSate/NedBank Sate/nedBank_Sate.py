import os
import csv
import time 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
navegador.get("https://rpa.xidondzo.com/")

navegador.find_element("xpath",
                        '/html/body/section/div[2]/div[2]/div/div/table/tbody/tr[1]/td[6]/a').click()

navegador.find_element("xpath",
                        '/html/body/section/div[2]/div[2]/div/div/table/tbody/tr[2]/td[6]/a').click()

navegador.find_element("xpath",
                        '/html/body/section/div[2]/div[2]/div/div/table/tbody/tr[3]/td[6]/a').click()

navegador.find_element("xpath",
                        '/html/body/section/div[2]/div[2]/div/div/table/tbody/tr[4]/td[6]/a').click()

navegador.find_element("xpath",
                        '/html/body/section/div[2]/div[2]/div/div/table/tbody/tr[5]/td[6]/a').click()

diretorio = 'c:/Users/Sate/Downloads/'


csv_path = 'D:/Python/Projectos/NedBank Sate/dados_extraidos.csv'

waiter = navegador.implicitly_wait(10)

arquivos = [f for f in os.listdir(diretorio) if f.startswith('R') and f.endswith('.txt')]


with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Nome', 'E-mail', 'Contacto / Tel', 'Estado Civil', 'Salário Líquido'])

    for arquivo in arquivos:
        arquivo_path = os.path.join(diretorio, arquivo)    
            
        with open(arquivo_path, 'r') as file:
            dados = []
            nome, mail, contacto, estadoCivil, salario = None, None, None, None, None

            for linha in file:
                if "Nome:" in linha:  
                    nome = linha.split(":")[1].strip()  # Extrai o nome
                if "E-mail:" in linha:  
                    mail = linha.split(":")[1].strip()  # Extrai o e-mail
                if "Contacto / Tel:" in linha:  
                    contacto = linha.split(":")[1].strip()  # Extrai o contacto
                if "Estado Civil:" in linha:  
                    estadoCivil = linha.split(":")[1].strip()     # Extrai o estado civil
                if "Sal" in linha:  
                    salario = linha.split(":")[1].strip()
                
                if nome and mail and contacto and estadoCivil:
                    dados.append([nome, mail, contacto, estadoCivil, salario])
                    nome, mail, contacto, estadoCivil, salario = None, None, None, None, None

#writer.writerow(['Nome', 'E-mail', 'Contacto / Tel', 'Estado Civil']) 

            with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(dados)



input('')
