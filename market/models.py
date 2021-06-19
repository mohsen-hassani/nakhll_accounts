from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Status(models.TextChoices):
    ACTIVE = 'active', _('فعال')
    DEACTIVE = 'deactive', _('غیرفعال')


class MarketManager(models.Manager):
    def active(self):
        return Market.objects.filter(status=Status.ACTIVE)

    def deactive(self):
        return Market.objects.filter(status=Status.DEACTIVE)


class ProductManager(models.Manager):
    def active(self):
        return Product.objects.filter(status=Status.ACTIVE)

    def deactive(self):
        return Product.objects.filter(status=Status.DEACTIVE)




class Redirect(models.Model):
    def __str__(self):
        return f'{self.src_content_type}({self.src_object_id}) --> {self.dst_content_type}({self.dst_object_id})'
    limit = models.Q(app_label='market', model='market') | \
        models.Q(app_label='market', model='product')

    src_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, limit_choices_to=limit, related_name='redirected_from')
    src_object_id = models.PositiveIntegerField(null=True)
    src_content_object = GenericForeignKey(
        'src_content_type', 'src_object_id')

    dst_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, verbose_name=_('مدل مقصد'), limit_choices_to=limit, related_name='redirected_to')
    dst_object_id = models.PositiveIntegerField(null=True, verbose_name=_('آیتم مقصد'))
    dst_content_object = GenericForeignKey('dst_content_type', 'dst_object_id')

    redirect_permanently = models.BooleanField(verbose_name=_('انتقال دائم'), null=True, default=False)

class Market(models.Model):
    class Meta:
        verbose_name = _('حجره')
        verbose_name_plural = _('حجره‌ها')

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('view_market', kwargs={'market_name': self.name})
    name = models.SlugField(max_length=100, verbose_name=_('نام'), unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, verbose_name=_('کاربر'), related_name='markets')
    status = models.CharField(max_length=8, choices=Status.choices,
                              default=Status.ACTIVE, verbose_name=_('وضعیت'))
    # redirect_to = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_(
    # 'انتقال به'), related_name='redirect_from', null=True)
    # redirect_permanently = models.BooleanField(verbose_name=_('انتقال دائم'), null=True)
    objects = models.Manager()
    markets = MarketManager()


class Product(models.Model):
    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')
        unique_together = ('market', 'name', )

    def __str__(self):
        return f'{self.name}'
    def get_absolute_url(self):
        return reverse('view_product', kwargs={'market_name': self.market.name, 'product_name': self.name})
    name = models.CharField(max_length=100, verbose_name=_('نام'))
    desc = models.CharField(max_length=500, verbose_name=_('جزئیات'), null=True, blank=True)
    status = models.CharField(max_length=8, choices=Status.choices,
                              default=Status.ACTIVE, verbose_name=_('وضعیت'))
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name='products', verbose_name=_('حجره'))
    objects = models.Manager()
    products = ProductManager()

