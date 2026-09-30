"""Основные сущности школьной структуры."""
from django.conf import settings
from django.db import models


class Subject(models.Model):
    name = models.CharField("название", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile", verbose_name="пользователь")
    subjects = models.ManyToManyField(Subject, blank=True, related_name="teachers", verbose_name="предметы")
    # Назначенные классы нужны для ограничения доступа учителя к журналу.
    school_classes = models.ManyToManyField("SchoolClass", blank=True, related_name="teachers", verbose_name="назначенные классы")

    class Meta:
        verbose_name = "учитель"
        verbose_name_plural = "учителя"

    def __str__(self):
        return str(self.user)


class SchoolClass(models.Model):
    name = models.CharField("название класса", max_length=20, unique=True)
    homeroom_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="homeroom_classes", verbose_name="классный руководитель")

    class Meta:
        ordering = ["name"]
        verbose_name = "класс"
        verbose_name_plural = "классы"

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile", verbose_name="пользователь")
    school_class = models.ForeignKey(SchoolClass, on_delete=models.PROTECT, related_name="students", verbose_name="класс")

    class Meta:
        ordering = ["user__last_name", "user__first_name"]
        verbose_name = "ученик"
        verbose_name_plural = "ученики"

    def __str__(self):
        return str(self.user)
