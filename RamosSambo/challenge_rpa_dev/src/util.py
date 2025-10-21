class RequestResult:
    def __init__(self, success: bool, text: str = None, error: str = None):
        self.success = success
        self.text = text
        self.error = error

    def __repr__(self):
        return f"RequestResult(success={self.success}, text={self.text} error={self.error})"

class ValidationResult:
    def __init__(self, is_valid: bool, errors: str = None):
        self.is_valid = is_valid
        self.errors = errors

    def __repr__(self):
        return f"ValidatorResult(is_valid={self.is_valid}, errors={self.errors})"
