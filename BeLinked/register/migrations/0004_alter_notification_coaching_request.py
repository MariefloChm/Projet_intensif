# Generated by Django 4.2.6 on 2023-11-12 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0003_coachingrequest_available_dates_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="coaching_request",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="register.coachingrequest",
            ),
        ),
    ]
