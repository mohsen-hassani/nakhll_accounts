# Generated by Django 3.2.4 on 2021-06-19 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_auto_20210619_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='جزئیات'),
        ),
    ]
