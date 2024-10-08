# Generated by Django 4.1.13 on 2024-08-18 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0003_alter_transactions_transaction_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balance",
            name="user_id",
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name="transactions",
            name="transaction_time",
            field=models.TimeField(default="23:44:21"),
        ),
    ]
