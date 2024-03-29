# Generated by Django 4.2.6 on 2023-12-29 17:59

import django.contrib.postgres.fields
from django.db import migrations, models
import games.checkers.models


class Migration(migrations.Migration):
    dependencies = [
        ("checkers", "0006_multiplayergame"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="grid",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=django.contrib.postgres.fields.ArrayField(
                    base_field=models.IntegerField(), size=None
                ),
                default=games.checkers.models.init_board,
                help_text="The grid of the board.",
                size=None,
                verbose_name="Grid",
            ),
        ),
    ]
