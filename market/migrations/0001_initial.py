# Generated by Django 3.2.4 on 2021-06-18 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=100, unique=True, verbose_name='نام')),
                ('status', models.CharField(choices=[('active', 'فعال'), ('deactive', 'غیرفعال')], default='active', max_length=8, verbose_name='وضعیت')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='markets', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حجره',
                'verbose_name_plural': 'حجره\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_permanently', models.BooleanField(verbose_name='انتقال دائم')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redirect_from', to='market.market', verbose_name='حجره')),
                ('redirect_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redirect_to', to='market.market', verbose_name='انتقال به')),
            ],
        ),
    ]
