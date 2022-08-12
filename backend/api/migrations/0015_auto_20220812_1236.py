# Generated by Django 2.2.16 on 2022-08-12 12:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20220812_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#ffffff', max_length=9, unique=True, validators=[django.core.validators.RegexValidator(message='This value may contain only letters and\n                digits.', regex='^#([A-Fa-f\\d]{6,8})')]),
        ),
    ]