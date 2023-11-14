from django.contrib import admin

from games.millionaire.models import Quiz, Question, Option


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'guid',
        'title',
        'total',
        'status',
        'created_at',
    )


class OptionTabularInline(admin.TabularInline):
    model = Option
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'guid',
        'complexity',
        'is_active',
    )

    inlines = (
        OptionTabularInline,
    )

