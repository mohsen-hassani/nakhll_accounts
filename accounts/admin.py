from accounts.views import register
from django.contrib import admin
from accounts.models import Profile, VerificationCode
# Register your models here.

admin.site.register(VerificationCode)
admin.site.register(Profile)