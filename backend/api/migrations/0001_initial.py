# Generated by Django 2.2.16 on 2022-07-31 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('measurement_unit', models.CharField(max_length=20)),
                ('quantity', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('color', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='This value may contain only letters and\n                digits.', regex='^#([A-Fa-f\\d]{6,8})')])),
                ('slug', models.SlugField(max_length=150)),
            ],
        ),
    ]
