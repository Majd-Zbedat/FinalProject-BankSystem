# Generated by Django 5.1.2 on 2024-10-21 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0003_bankaccount_suspended'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='name',
        ),
        migrations.RemoveField(
            model_name='bankaccount',
            name='suspended',
        ),
    ]
