from django.contrib import admin
from games.bazarblot import models


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    ...
