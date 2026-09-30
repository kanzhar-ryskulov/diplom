from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("weekday", "time_start", "time_end", "school_class", "subject", "teacher")
    list_filter = ("weekday", "school_class", "teacher", "subject")
