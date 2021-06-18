from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from market.models import Market

class AddMarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('name', )

class CloseMarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('redirect_to', 'redirect_permanently', )
    def clean_redirect_to(self):
        redirect_to = self.cleaned_data.get('redirect_to')
        if redirect_to == self.instance:
            raise ValidationError(_('آدرس جدید نمی‌تواند با آدرس قبل یکسان باشد'))
        return redirect_to
    def save(self, commit=True):
        market = super(CloseMarketForm, self).save(commit=False)
        market.status = Market.MarketStatus.DEACTIVE
        if commit:
            market.save()
        return market
