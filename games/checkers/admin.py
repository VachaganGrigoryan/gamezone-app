from django.contrib import admin
from .models import Board, BoardPlayers


class BoardPlayersInline(admin.TabularInline):
    model = BoardPlayers
    extra = 1
    min_num = 1
    max_num = 2


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('guid', 'owner', 'length', 'is_ended', 'is_active', 'created_at')
    readonly_fields = ('guid', 'grid', 'winner', 'is_ended', 'created_at', 'updated_at')
    fieldsets = (
        (
            None,
            {
                'fields': ('guid', 'grid', 'length', 'owner')
            },
        ),
        (
            'Configurations',
            {
                'fields': ('queue', 'winner', 'is_ended', 'is_active')
            }
        ),
        (
            'Dates',
            {
                'fields': ('created_at', 'updated_at')
            }
        )
    )

    inlines = [
        BoardPlayersInline,
    ]
