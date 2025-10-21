import re

from util import ValidationResult


class Validator:
    @staticmethod
    def email(email: str) -> bool:
        """
        Valida se o email está no formato correto.
        """
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(padrao, email))

    @staticmethod
    def contacto(contacto: str) -> bool:
        """
        Valida se o contacto está no formato XX-XXX-XXX (como 84-123-456)
        """
        padrao = r'^\d{2}-\d{3}-\d{3}$'
        return bool(re.match(padrao, contacto))

    @staticmethod
    def salario(salario: str) -> bool:
        """
        Valida se o salário está no formato MZN XX.XXX,YY
        """
        padrao = r'^MZN\s\d{1,3}(?:\.\d{3})*,\d{2}$'
        return bool(re.match(padrao, salario))

def validate_info(extracted_info: dict) -> ValidationResult:
    errors = []

    if not extracted_info.get("nome"):
        errors.append("Nome")

    if not Validator.email(extracted_info.get("email", "")):
        errors.append("Email")

    if not Validator.contacto(extracted_info.get("contacto", "")):
        errors.append("Contacto")

    if not Validator.salario(extracted_info.get("salario", "")):
        errors.append("Saldo")

    if errors:
        return ValidationResult(False, errors=f"Campos inválidos: {", ".join(errors)}")

    return ValidationResult(True)