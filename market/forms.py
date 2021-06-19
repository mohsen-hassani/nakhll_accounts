from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms import widgets
from django.utils.translation import ugettext as _
from market.models import Market, Product, Redirect, Status

class AddMarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('name', )

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'desc',)

class CloseObjectForm(forms.ModelForm):
    class Meta:
        model = Redirect
        fields = ('dst_content_type', 'dst_object_id', 'redirect_permanently' )
        widgets = {
            'dst_object_id': forms.Select()
        }
    def clean(self):
        cleaned_data = super().clean()
        dst_object = cleaned_data.get('dst_object_id')
        dst_content = cleaned_data.get('dst_content_type')
        if dst_content == self.instance.src_content_type and \
            dst_object == self.instance.src_object_id:
            raise ValidationError(_('آدرس جدید نمی‌تواند با آدرس قبل یکسان باشد'))
    def save(self, commit=True):
        redirect_object = super(CloseObjectForm, self).save(commit=False)
        redirect_object.src_content_object.status = Status.DEACTIVE
        redirect_object.src_content_object.save()

        if commit:
            redirect_object.save()
