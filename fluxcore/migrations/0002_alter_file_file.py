# Generated by Django 5.0.1 on 2024-07-06 06:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nba", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(upload_to="nba/"),
        ),
    ]
