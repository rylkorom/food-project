# Generated by Django 4.0.1 on 2022-01-25 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_remove_history_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='comment',
        ),
    ]
