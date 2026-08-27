import re

from django.core.exceptions import ValidationError


class ComplexityPasswordValidator:
    """
    Impose au moins une majuscule et un caractère spécial, comme demandé
    par le PID (use case S'inscrire : "min. 6 caractères, au moins une
    majuscule et un caractère spécial").
    """

    SPECIAL_CHARACTERS = r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?\\|`~]"

    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                "Le mot de passe doit contenir au moins une majuscule.",
                code='password_no_upper',
            )

        if not re.search(self.SPECIAL_CHARACTERS, password):
            raise ValidationError(
                "Le mot de passe doit contenir au moins un caractère spécial.",
                code='password_no_special',
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins une majuscule et un caractère spécial."
