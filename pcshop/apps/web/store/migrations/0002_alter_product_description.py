# Generated by Django 3.2.4 on 2021-10-06 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=22, null=True, verbose_name='DESCRIPTION'),
        ),
    ]
