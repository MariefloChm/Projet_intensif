# Generated by Django 4.2.6 on 2023-10-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Matching",
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
                ("Domains", models.CharField(max_length=100)),
                ("Diplomas", models.CharField(max_length=100)),
                ("Skills", models.CharField(max_length=100)),
                ("Career_objectives", models.TextField()),
                ("Professions", models.CharField(max_length=100)),
                ("Personality", models.CharField(max_length=100)),
            ],
        ),
    ]
