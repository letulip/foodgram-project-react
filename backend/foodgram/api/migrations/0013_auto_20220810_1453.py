# Generated by Django 2.2.16 on 2022-08-10 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20220808_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='static/images/recipes/'),
        ),
    ]
