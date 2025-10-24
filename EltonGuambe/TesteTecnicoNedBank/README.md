# CHALLENGE NEDBANK - RPA DEVELOLMENT

# Visão Geral do projecto
## Objectivo
**Desenvolver uma solução eficiente, escalável que visa extrair dados do website https://rpa.xidondzo.com, fazendo todas as analises e validações propostas e salva-los num file csv**

## Tecnologias usadas
 - Linguagem de Programação: Python 
 - Frameworks: Selenium, Pandas 
 - IDE: PyCharm(recomendado) ou VSCode


## Fases do desenvolvimento
### 1-Fase
A primeiro fase é de analise e Planemento onde foram realizadas as seguintes tarefas:
 - Aceder ao website para analise uma analise geral e verificao da estrutura dos dados 

 **Foi possivel ver que os dados estão num formato txt, organizados em blocos como as seguintes variáveis:**
 - Nome
 - Contacto / Tel
 - E-mail
 - Estado Civil
 - Documento
 - Dept.
 - Período
 - Vencimentos brutos
 - Bónus
 - Seguros
 - OUTROS
 - Salário Líquido
 - Pagamento via
 - Referência recibo
 - Obs.
 - Assinatura gestor
 - Data

O objectivo do teste é apenas extrair os seguintes campos:
- Nome
- Email
- Contacto
- Estado civil
- Salario liquido
E os outros campos podem ser ignorados

## 2- Fase : Desenvolvimento da solução
### Arquitetura modular
Foi escolhida a arquitetura em modulos, porque ela é simples e facil, mas principalmente, ela permite escalar o projecto e também permite um uso do paradigma orientado a objectos com ificiencia
 - Modulos criados:
   - data_extraction: que é reponsavel pela extracão, download e armazenamento dos daos
   - data_processing: responsável pelo processamento dos dados e validações e também pela criação de um file csv que guarda dos dados finas anteriormente citados
 files:
   - constants: que guarda todas constantes usadas no sistema, como, links e paths dos files descarregados e também dos files sintetizados(csv)
   - run: ficheiro responsável por executar todo sistema/processo

Após a execução temos um file chamado valid_registro que contém os dados em csv após o processamento e validação



### Exemplo do file csv gerado:
"Nome","E-mail","Contacto","Estado Civil","Salário Líquido"

"Carla Nhantumbo","c.nhantumbo@empresa.mz","84-123-456","Solteira","16.050,00"

"Tomás Cossa","t.cossa@empresa.mz","86-987-321","Casado","19.300,00"

"Elsa Mucave","e.mucave@empresa.mz","85-456-789","Divorciada","15.900,00"

"Júlio Matusse","j.matusse@empresa.mz","83-789-123","Viúvo","12.300,00"


## Acesso ao projecto

- Crie uma pasta com um nome para o projecto 
- acesse essa pasta no terminal

Execute as seguintes instruçoes num terminal ou no terminal da IDE:

- git pull https://github.com/LegocodeMz/DeveloperRPA
- crie um ambiente virtual
- pip install -r requirements.txt
- e execute o projecto com o comando: python run.py
