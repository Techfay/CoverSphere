# Generated by Django 4.2.16 on 2024-11-20 18:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
