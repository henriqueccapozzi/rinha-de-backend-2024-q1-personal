# Generated by Django 4.2.9 on 2024-02-12 03:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("bank", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="current_balance",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
