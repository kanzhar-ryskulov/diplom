"""Учебное расписание по классам и учителям."""
from django.core.exceptions import ValidationError
from django.db import models
from school.models import SchoolClass, Subject, Teacher


class Lesson(models.Model):
    WEEKDAYS = [(0, "Понедельник"), (1, "Вторник"), (2, "Среда"), (3, "Четверг"), (4, "Пятница"), (5, "Суббота"), (6, "Воскресенье")]

    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="lessons", verbose_name="класс")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="lessons", verbose_name="предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="lessons", verbose_name="учитель")
    weekday = models.PositiveSmallIntegerField("день недели", choices=WEEKDAYS)
    time_start = models.TimeField("начало")
    time_end = models.TimeField("окончание")

    class Meta:
        ordering = ["weekday", "time_start", "school_class__name"]
        verbose_name = "урок"
        verbose_name_plural = "расписание"

    def clean(self):
        if self.time_start and self.time_end and self.time_start >= self.time_end:
            raise ValidationError({"time_end": "Время окончания должно быть позже времени начала."})
        if self.weekday is None or not self.time_start or not self.time_end:
            return
        overlaps = Lesson.objects.filter(weekday=self.weekday).exclude(pk=self.pk) if self.pk else Lesson.objects.filter(weekday=self.weekday)
        overlaps = overlaps.filter(
            models.Q(time_start__lt=self.time_end) & models.Q(time_end__gt=self.time_start)
        )
        if overlaps.filter(school_class=self.school_class).exists():
            raise ValidationError("У класса уже есть урок в это время.")
        if overlaps.filter(teacher=self.teacher).exists():
            raise ValidationError("У учителя уже есть урок в это время.")

    def __str__(self):
        return f"{self.get_weekday_display()}, {self.time_start:%H:%M}: {self.school_class} — {self.subject}"
