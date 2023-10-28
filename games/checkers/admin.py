from django.contrib import admin
from .models import Histories, Board, BoardPlayers

# Register your models here.

admin.site.register(Histories)
admin.site.register(Board)
admin.site.register(BoardPlayers)
