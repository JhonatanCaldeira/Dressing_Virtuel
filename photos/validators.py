from django.core.exceptions import ValidationError
import re

def validate_password_special_chars(password):
    if not re.search(r"[!@#$%^&*()_+]", password):
        raise ValidationError("Password must contain at least one special character from !@#$%^&*()_+")

class CustomPasswordValidator:
    def validate(self, password, user=None):
        validate_password_special_chars(password)

    def get_help_text(self):
        return "Your password must contain at least one special character from !@#$%^&*()_+"