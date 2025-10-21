def extrair_informacoes(conteudo_txt):
    info = {}
    for linha in conteudo_txt.splitlines():
        if "Nome:" in linha:
            info["nome"] = linha.split(":")[1].strip().encode("latin1").decode("utf-8")
        elif "Contacto / Tel:" in linha:
            info["contacto"] = linha.split(":")[1].strip()
        elif "E-mail" in linha:
            info["email"] = linha.split(":")[1].strip()
        elif "Estado Civil" in linha:
            info["estado_civil"] = linha.split(":")[1].strip().encode("latin1").decode("utf-8")
        elif "Salário Líquido" in linha:
            info["salario"] = linha.split(":")[1].strip()
    return info