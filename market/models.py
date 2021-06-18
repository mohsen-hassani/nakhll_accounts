from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class MarketManager(models.Manager):
    def active(self):
        return Market.objects.filter(status=Market.MarketStatus.ACTIVE)

    def deactive(self):
        return Market.objects.filter(status=Market.MarketStatus.DEACTIVE)


class Market(models.Model):
    class MarketStatus(models.TextChoices):
        ACTIVE = 'active', _('فعال')
        DEACTIVE = 'deactive', _('غیرفعال')

    class Meta:
        verbose_name = _('حجره')
        verbose_name_plural = _('حجره‌ها')

    def __str__(self):
        return self.name
    name = models.SlugField(max_length=100, verbose_name=_('نام'), unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, verbose_name=_('کاربر'), related_name='markets')
    status = models.CharField(max_length=8, choices=MarketStatus.choices,
                              default=MarketStatus.ACTIVE, verbose_name=_('وضعیت'))
    redirect_to = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_(
        'انتقال به'), related_name='redirect_from', null=True)
    redirect_permanently = models.BooleanField(verbose_name=_('انتقال دائم'), null=True)
    objects = models.Manager()
    markets = MarketManager()
