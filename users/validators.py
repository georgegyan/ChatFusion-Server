from zxcvbn import zxcvbn
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _ 

class ComplexityValidator:
    def __init__(self, min_score=3):
        self.min_score = min_score

    def validate(self, password, user=None):
        result = zxcvbn(password, user_inputs=[
            user.username if user else '',
            user.email.split('@')[0] if user and user.email else ''
        ])

        if result['score'] < self.min_score:
            feedback = result['feedback']['warning'] or "Password is too weak"
            suggestions = result['feedback']['suggestions']
            raise ValidationError(
                _(f"{feedback}. {' '.join(suggestions)}"),
                code='password_too_weak'
            )
    
    def get_help_text(self):
        return _(
            f"Your password must have at least {self.min_score}/4 "
            "on our strength meter"
        )