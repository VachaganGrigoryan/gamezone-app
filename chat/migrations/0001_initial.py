# Generated by Django 4.2.6 on 2023-12-29 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("games", "0003_alter_game_guid"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique identifier.",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="GUID",
                    ),
                ),
                ("game_guid", models.UUIDField(db_index=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="games.game"
                    ),
                ),
            ],
            options={
                "verbose_name": "Chat",
                "verbose_name_plural": "Chats",
                "db_table": "chat",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="The unique identifier.",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="GUID",
                    ),
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
            name="ChatMembers",
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
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chat"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("chat", "user")},
            },
        ),
        migrations.AddField(
            model_name="chat",
            name="members",
            field=models.ManyToManyField(
                through="chat.ChatMembers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Members",
            ),
        ),
    ]
