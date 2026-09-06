from django.contrib import admin

from .models import DailyPuzzle


@admin.register(DailyPuzzle)
class DailyPuzzleAdmin(admin.ModelAdmin):
    list_display = ("date", "sport", "category", "difficulty", "answer")
    list_filter = ("sport", "category", "difficulty")
    search_fields = ("answer", "accepted_answers")
    ordering = ("-date",)
