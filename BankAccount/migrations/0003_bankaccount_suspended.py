# Generated by Django 5.1.2 on 2024-10-21 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0002_bankaccount_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='suspended',
            field=models.BooleanField(default=False),
        ),
    ]
