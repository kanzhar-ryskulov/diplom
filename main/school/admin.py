from django.contrib import admin
from .models import SchoolClass, Student, Subject, Teacher

admin.site.register(SchoolClass)
admin.site.register(Student)
admin.site.register(Subject)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    filter_horizontal = ("subjects", "school_classes")
