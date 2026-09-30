"""Просмотр расписания по классу или учителю и администраторский CRUD."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from school.models import SchoolClass, Student, Teacher
from .forms import LessonForm
from .models import Lesson


def is_admin(user):
    return user.is_superuser or user.role == "admin"


class ScheduleListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "schedule/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        user = self.request.user
        queryset = Lesson.objects.select_related("school_class", "subject", "teacher__user")
        if is_admin(user):
            pass
        elif user.role == "teacher":
            try:
                queryset = queryset.filter(teacher=user.teacher_profile)
            except Teacher.DoesNotExist:
                return queryset.none()
        elif user.role == "student":
            try:
                queryset = queryset.filter(school_class=user.student_profile.school_class)
            except Student.DoesNotExist:
                return queryset.none()
        else:
            return queryset.none()
        class_id = self.request.GET.get("class")
        teacher_id = self.request.GET.get("teacher")
        if class_id and is_admin(user):
            queryset = queryset.filter(school_class_id=class_id)
        if teacher_id and is_admin(user):
            queryset = queryset.filter(teacher_id=teacher_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = SchoolClass.objects.all() if is_admin(self.request.user) else []
        context["teachers"] = Teacher.objects.select_related("user").all() if is_admin(self.request.user) else []
        context["can_manage"] = is_admin(self.request.user)
        weekdays = []
        for day, label in Lesson.WEEKDAYS:
            weekdays.append({"number": day, "label": label, "lessons": [lesson for lesson in context["lessons"] if lesson.weekday == day]})
        context["weekdays"] = weekdays
        return context


class AdminScheduleMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)


class LessonCreateView(AdminScheduleMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "schedule/lesson_form.html"
    success_url = reverse_lazy("schedule-list")
    extra_context = {"title": "Добавить урок"}


class LessonUpdateView(AdminScheduleMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "schedule/lesson_form.html"
    success_url = reverse_lazy("schedule-list")
    extra_context = {"title": "Редактировать урок"}


class LessonDeleteView(AdminScheduleMixin, DeleteView):
    model = Lesson
    template_name = "schedule/lesson_confirm_delete.html"
    success_url = reverse_lazy("schedule-list")
