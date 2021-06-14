from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from accounts.models import VerificationCode

class GetPhoneForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput)
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone_number')
        if phone < 900_000_0000 or phone > 999_999_9999:
            raise ValidationError(_('شماره تماس وارد شده اشتباه است'))


class CodeVerificationForm(forms.ModelForm):
    class Meta:
        model = VerificationCode
        fields = ['verification_code', ]

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class SetPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError(_('رمزهای ورود با هم تطابق ندارد'))

