# Generated by Django 4.2.6 on 2023-11-29 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("games", "0003_alter_game_guid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
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
                (
                    "guid",
                    models.UUIDField(auto_created=True, db_index=True, unique=True),
                ),
                ("message", models.TextField(max_length=255)),
                ("is_read", models.BooleanField(default=False)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Sender",
                    ),
                ),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
                "db_table": "message",
            },
        ),
        migrations.CreateModel(
            name="Chat",
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
                (
                    "guid",
                    models.UUIDField(auto_created=True, db_index=True, unique=True),
                ),
                ("game_guid", models.UUIDField(db_index=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="games.game"
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        to=settings.AUTH_USER_MODEL, verbose_name="Members"
                    ),
                ),
            ],
            options={
                "verbose_name": "Chat",
                "verbose_name_plural": "Chats",
                "db_table": "chat",
            },
        ),
    ]