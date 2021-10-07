# Generated by Django 3.2.4 on 2021-10-07 20:22

from django.db import migrations, models
import pcshop.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='code',
            field=models.CharField(default=pcshop.core.utils.product_randcode_gen, max_length=100, verbose_name='CODE'),
        ),
    ]
