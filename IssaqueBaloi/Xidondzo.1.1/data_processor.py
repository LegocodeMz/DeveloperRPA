import re
import os

def identificar_formato(caminho_ficheiro):
    """Verifica se o ficheiro é .txt."""
    _, extensao = os.path.splitext(caminho_ficheiro)
    if extensao.lower() == ".txt":
        print("✅ Ficheiro no formato correto (.txt)")
        return True
    else:
        print(f"⚠️ Formato incorreto: {extensao}. Esperado: .txt")
        return False

def ler_e_extrair_campos(caminho_ficheiro):
    """Lê o ficheiro .txt e extrai os campos Nome, Email, Contacto, Estado Civil e Salário Líquido."""
    campos_extraidos = []
    try:
        with open(caminho_ficheiro, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        print(f"Erro ao ler ficheiro: {str(e)}")
        return campos_extraidos

    registos = re.split(r"--- END Registro: .*? ---", conteudo)
    for reg in registos:
        if not reg.strip():
            continue

        nome = re.search(r"Nome:\s*(.*)", reg)
        email = re.search(r"E-mail:\s*(.*)", reg)
        contacto = re.search(r"Contacto\s*/\s*Tel:\s*(.*)", reg)
        estado_civil = re.search(r"Estado Civil:\s*(.*)", reg)
        salario = re.search(r"Salário Líquido:\s*([\d.,]+)", reg)

        if nome and email and contacto and estado_civil and salario:
            campos_extraidos.append({
                "Nome": nome.group(1).strip(),
                "Email": email.group(1).strip(),
                "Contacto": contacto.group(1).strip(),
                "Estado Civil": estado_civil.group(1).strip(),
                "Salário Líquido": salario.group(1).strip()
            })
    return campos_extraidos

def validar_dados(lista_dados):
    """Valida campos de email, contacto e salário."""
    dados_validos = []
    for d in lista_dados:
        email_valido = re.match(r"[^@]+@[^@]+\.[^@]+", d["Email"])
        contacto_valido = re.match(r"8[23456789]-\d{3}-\d{3}", d["Contacto"])
        salario_valido = re.match(r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?", d["Salário Líquido"])

        if email_valido and contacto_valido and salario_valido:
            d["Validação"] = "✅ Válido"
        else:
            d["Validação"] = "⚠️ Inválido"
        dados_validos.append(d)
    return dados_validos

def transformar_dados(lista_dados):
    """Normaliza e transforma dados para CSV."""
    dados_transformados = []
    for d in lista_dados:
        nome = d["Nome"].title()
        email = d["Email"].lower()
        contacto = re.sub(r"[^0-9]", "", d["Contacto"])
        estado_civil = d["Estado Civil"].capitalize()

        try:
            # Remove separadores de milhar e converte decimal para ponto
            salario = d["Salário Líquido"]
            salario = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", salario)  # remove pontos/vírgulas de milhar
            salario = salario.replace(",", ".")  # decimal sempre com ponto
            salario = "{:.2f}".format(float(salario))
        except ValueError:
            salario = "0.00"

        dados_transformados.append({
            "Nome": nome,
            "Email": email,
            "Contacto": contacto,
            "Estado Civil": estado_civil,
            "Salário Líquido (MZN)": salario
        })
    return dados_transformados