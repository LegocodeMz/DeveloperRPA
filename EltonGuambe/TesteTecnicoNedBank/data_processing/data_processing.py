import pandas as pd
import os
import re
import json

class DataProcessing:
    VALID_ESTADOS = ["Solteira", "Casado", "Divorciada", "Viúvo"]

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.DataFrame(columns=["Nome","E-mail","Contacto","Estado Civil","Salário Líquido"])
        self.file_type = self._detect_file_type()

    def _detect_file_type(self):
        """Identifica o formato do arquivo"""
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext in [".txt"]:
            return "txt"
        elif ext in [".csv"]:
            return "csv"
        elif ext in [".json"]:
            return "json"
        elif ext in [".xls", ".xlsx"]:
            return "excel"
        else:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")

    def read_file(self):
        """Lê o arquivo e extrai os campos necessários"""
        if self.file_type == "txt":
            self._read_txt()
        elif self.file_type == "csv":
            self._read_csv()
        elif self.file_type == "json":
            self._read_json()
        elif self.file_type == "excel":
            self._read_excel()
        else:
            raise ValueError("Tipo de arquivo desconhecido.")

        print(f"📄 {len(self.df)} registros extraídos do arquivo ({self.file_type})")

    def _read_txt(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()

        registros = content.split('--- END Registro')
        data = []

        for reg in registros:
            if not reg.strip():
                continue

            nome = re.search(r'Nome:\s*(.*)', reg)
            email = re.search(r'E-mail:\s*(.*)', reg)
            contacto = re.search(r'Contacto\s*/\s*Tel:\s*(.*)', reg)
            estado = re.search(r'Estado Civil:\s*(.*)', reg)
            salario = re.search(r'Salário Líquido:\s*([\d.,]+)', reg)

            data.append({
                "Nome": nome.group(1).strip() if nome else "",
                "E-mail": email.group(1).strip() if email else "",
                "Contacto": contacto.group(1).strip() if contacto else "",
                "Estado Civil": estado.group(1).strip() if estado else "",
                "Salário Líquido": salario.group(1).strip() if salario else ""
            })

        self.df = pd.DataFrame(data)

    def _read_csv(self):
        self.df = pd.read_csv(self.file_path, usecols=["Nome","E-mail","Contacto","Estado Civil","Salário Líquido"])

    def _read_json(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.df = pd.DataFrame(data)[["Nome","E-mail","Contacto","Estado Civil","Salário Líquido"]]

    def _read_excel(self):
        self.df = pd.read_excel(self.file_path, usecols=["Nome","E-mail","Contacto","Estado Civil","Salário Líquido"])

    def validate_data(self):
        """Valida os campos principais"""
        if self.df.empty:
            print("⚠️ Nenhum dado para validar.")
            return

        # Validar Nome
        self.df["Nome_Valido"] = self.df["Nome"].apply(lambda x: bool(re.match(r'^[A-Za-zÀ-ÿ\s]+$', x)))

        # Validar Email
        self.df["Email_Valido"] = self.df["E-mail"].apply(lambda x: bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', x)))

        # Validar Estado Civil
        self.df["Estado_Valido"] = self.df["Estado Civil"].apply(lambda x: x in self.VALID_ESTADOS)

        # Validar Salário
        def parse_salario(x):
            try:
                val = re.sub(r'[^\d,]', '', x)
                val = val.replace(',', '.')
                return float(val)
            except:
                return None

        self.df["Salario_Num"] = self.df["Salário Líquido"].apply(parse_salario)
        self.df["Salario_Valido"] = self.df["Salario_Num"].apply(lambda x: x is not None and x > 0)

        # Registro válido se todos forem válidos
        self.df["Registro_Valido"] = self.df[["Nome_Valido","Email_Valido","Estado_Valido","Salario_Valido"]].all(axis=1)

        print(f"✅ {self.df['Registro_Valido'].sum()} registros válidos de {len(self.df)}")

    def get_valid_data(self):
        """Retorna apenas registros válidos"""
        if self.df.empty:
            return pd.DataFrame()
        return self.df[self.df["Registro_Valido"]][["Nome","E-mail","Contacto","Estado Civil","Salário Líquido"]]

    def save_to_csv(self, filename):
        """Salva registros válidos em CSV"""
        valid_df = self.get_valid_data()
        if valid_df.empty:
            print("Nenhum registro válido para salvar.")
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        valid_df.to_csv(filename, index=False, encoding="utf-8", quoting=1)  # quoting=1 adiciona aspas
        print(f"✅ CSV final salvo em: {filename}")
