# Generated by Django 2.2 on 2021-10-01 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
