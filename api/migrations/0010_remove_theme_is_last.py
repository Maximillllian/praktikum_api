# Generated by Django 4.0.1 on 2022-01-12 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_theme_is_last'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='is_last',
        ),
    ]