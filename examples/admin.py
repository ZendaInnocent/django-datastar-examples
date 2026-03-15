from django.contrib import admin

from .models import Answer, Question


class AnswerInline(admin.TabularInline):
    """Tabular Inline View for Answer"""

    model = Answer
    min_num = 3
    max_num = 4
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
