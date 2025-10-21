def extract_info(content_txt):
    info = {}
    for line in content_txt.splitlines():
        if "Nome:" in line:
            info["nome"] = line.split(":")[1].strip()
        elif "Contacto / Tel:" in line:
            info["contacto"] = line.split(":")[1].strip()
        elif "E-mail" in line:
            info["email"] = line.split(":")[1].strip()
        elif "Estado Civil:" in line:
            info["estado_civil"] = line.split(":")[1].strip()
        elif "Salário Líquido:" in line:
            info["salario"] = line.split(":")[1].strip()
    return info
