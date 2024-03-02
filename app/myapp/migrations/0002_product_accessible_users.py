# Generated by Django 3.2.4 on 2024-03-01 14:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='accessible_users',
            field=models.ManyToManyField(related_name='accessible_products', to=settings.AUTH_USER_MODEL),
        ),
    ]