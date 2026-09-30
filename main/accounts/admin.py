from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class EduPageUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("EduPage", {"fields": ("role", "avatar")}),)
    list_display = ("username", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff")
