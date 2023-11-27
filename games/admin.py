from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):

    list_display = ('guid', 'title', 'is_active',)

    list_editable = ('is_active',)
