# Generated by Django 5.1.2 on 2024-10-21 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BankAccount', '0004_remove_bankaccount_name_remove_bankaccount_suspended'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='name',
            field=models.CharField(default='Your Name', max_length=255),
        ),
    ]