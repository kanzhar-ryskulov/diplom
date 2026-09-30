"""Оценки и ежедневные отметки посещаемости."""
from django.db import models
from school.models import Student, Subject, Teacher


class Grade(models.Model):
    class GradeType(models.TextChoices):
        CURRENT = "current", "Текущая"
        EXAM = "exam", "Экзамен"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades", verbose_name="ученик")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="grades", verbose_name="предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="grades", verbose_name="учитель")
    value = models.PositiveSmallIntegerField("оценка", choices=[(v, str(v)) for v in range(2, 6)])
    date = models.DateField("дата")
    grade_type = models.CharField("тип оценки", max_length=10, choices=GradeType.choices, default=GradeType.CURRENT)
    comment = models.CharField("комментарий", max_length=300, blank=True)

    class Meta:
        ordering = ["-date", "student__user__last_name"]
        verbose_name = "оценка"
        verbose_name_plural = "оценки"

    def __str__(self):
        return f"{self.student}: {self.value} ({self.subject}, {self.date})"


class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Присутствовал"
        ABSENT = "absent", "Отсутствовал"
        LATE = "late", "Опоздал"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance_records", verbose_name="ученик")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="attendance_records", verbose_name="предмет")
    lesson_date = models.DateField("дата урока")
    status = models.CharField("статус", max_length=10, choices=Status.choices)

    class Meta:
        ordering = ["-lesson_date", "student__user__last_name"]
        constraints = [models.UniqueConstraint(fields=("student", "subject", "lesson_date"), name="unique_attendance_per_student_subject_day")]
        verbose_name = "посещение"
        verbose_name_plural = "посещаемость"

    def __str__(self):
        return f"{self.student}: {self.get_status_display()} ({self.lesson_date})"
