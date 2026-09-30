from django.contrib import admin
from .models import Attendance, Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "teacher", "value", "date", "grade_type")
    list_filter = ("subject", "grade_type", "date")
    search_fields = ("student__user__first_name", "student__user__last_name")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "lesson_date", "status")
    list_filter = ("subject", "status", "lesson_date")
