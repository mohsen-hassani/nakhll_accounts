from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if (not any(x.isupper() for x in password) or \
            not any(x.islower() for x in password) or \
            not any(x.isdigit() for x in password)):
            raise ValidationError(
                _('رمز عبور باید ترکیبی از حروف کوچک، حروف بزرگ و اعداد باشد'))

    def get_help_text(self):
        return _('رمز عبور باید ترکیبی از حروف کوچک، حروف بزرگ و اعداد باشد')