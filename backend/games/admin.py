from django.contrib import admin

from .models import DailyPuzzle


@admin.register(DailyPuzzle)
class DailyPuzzleAdmin(admin.ModelAdmin):
    list_display = ("date", "is_active", "sport", "category", "difficulty", "answer")
    list_editable = ("is_active",)
    list_filter = ("sport", "category", "difficulty", "is_active")
    search_fields = ("answer", "accepted_answers_extra")
    ordering = ("-date",)
    fieldsets = (
        (None, {"fields": ("date", "is_active", "sport", "category", "difficulty")}),
        ("Answer", {"fields": ("answer", "accepted_answers_extra")}),
        (
            "Clues (obscure → obvious)",
            {"fields": ("clue_1", "clue_2", "clue_3", "clue_4", "clue_5", "clue_6", "clue_7", "clue_8")},
        ),
    )
