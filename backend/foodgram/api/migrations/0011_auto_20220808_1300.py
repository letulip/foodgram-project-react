# Generated by Django 2.2.16 on 2022-08-08 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20220808_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='recipe',
            field=models.ForeignKey(error_messages={'unique_together': 'Recipe already in favorites'}, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='api.Recipe'),
        ),
        migrations.AlterField(
            model_name='favorites',
            name='user',
            field=models.ForeignKey(error_messages={'unique_together': 'Recipe already in favorites'}, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]
