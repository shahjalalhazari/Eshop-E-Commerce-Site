# Generated by Django 3.0 on 2020-10-03 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_auto_20201002_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='division',
        ),
    ]
