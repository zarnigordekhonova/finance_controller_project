# Generated by Django 5.0.7 on 2024-07-23 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wallet', '0006_expenditures_account_type_incomes_account_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenditures',
            name='expenditure_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Wallet.typeexpenditures'),
        ),
        migrations.AlterField(
            model_name='incomes',
            name='income_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Wallet.typeincomes'),
        ),
    ]
