# Generated by Django 4.2.9 on 2024-02-06 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("limit", models.IntegerField()),
                ("initial_balance", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                (
                    "type",
                    models.CharField(
                        choices=[("c", "Credito"), ("d", "Debito")], max_length=1
                    ),
                ),
                ("description", models.CharField(max_length=10)),
                ("created_at", models.DateTimeField()),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="bank.client"
                    ),
                ),
            ],
        ),
    ]
