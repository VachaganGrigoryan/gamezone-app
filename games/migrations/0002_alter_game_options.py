# Generated by Django 4.2.2 on 2023-06-23 22:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="game",
            options={
                "ordering": ["-pk"],
                "verbose_name": "Game",
                "verbose_name_plural": "Games",
            },
        ),
    ]
