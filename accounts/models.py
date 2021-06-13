from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.utils import generate_code, send_verification_code

# Create your models here.

class VerificaitonCodeManager(models.Manager):    

    def generate_verification_code(self, phone):
        verification_object, created = VerificationCode.objects.get_or_create(phone_number=phone)
        if created or verification_object.code_expire_datetime < datetime.now():
            # if previous code has been expired, assign new code and send it
            code, code_expire_datetime = generate_code()
            verification_object.code_expire_datetime = code_expire_datetime
            verification_object.verification_code = code
            verification_object.save()
            send_verification_code(phone, code)
        return verification_object.verification_code, verification_object.code_expire_datetime

    def verify_code(self, phone, code):
        verification_object, created = VerificationCode.objects.get_or_create(phone_number=phone)
        if created or verification_object.code_expire_datetime < datetime.now():
            return False
        if code != verification_object.verification_code:
            return False
        # now that verification is succeed, verification code should be removed,
        # so nobody can use it before expire-time
        verification_object.delete()
        return True





class Profile(models.Model):
    class Meta:
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل‌ها')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, unique=True, verbose_name=_('شماره همراه'))
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        '''Create a profile for each new created User object '''
        if created:
            Profile.objects.create(user=instance)
        instance.profile.phone_number = instance.username
        instance.profile.save()
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        '''Save user.profile every time a user changed '''
        instance.profile.save()
    def __str__(self):
        return self.user.username


class VerificationCode(models.Model):
    phone_number = models.CharField(
        max_length=11, null=True, blank=True, unique=True, verbose_name=_('شماره همراه'))
    verification_code = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('کد تایید'))
    code_expire_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_('انقضا کد تایید'))
    verificaiton = VerificaitonCodeManager()
    objects = models.Manager()
