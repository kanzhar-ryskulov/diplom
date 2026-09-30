"""Журнал с разграничением доступа на уровне queryset и формы."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from school.models import Student
from .forms import AttendanceForm, GradeForm
from .models import Attendance, Grade


def is_admin(user):
    return user.is_superuser or user.role == "admin"


def teacher_profile(user):
    try:
        return user.teacher_profile
    except AttributeError:
        return None


class JournalStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user) or (self.request.user.role == "teacher" and teacher_profile(self.request.user) is not None)


class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = "journal/grade_list.html"
    context_object_name = "grades"
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        queryset = Grade.objects.select_related("student__user", "student__school_class", "subject", "teacher__user")
        if is_admin(user):
            pass
        elif user.role == "teacher" and teacher_profile(user):
            teacher = teacher_profile(user)
            queryset = queryset.filter(teacher=teacher, student__school_class__in=teacher.school_classes.all(), subject__in=teacher.subjects.all())
        elif user.role == "student" and hasattr(user, "student_profile"):
            queryset = queryset.filter(student=user.student_profile)
        else:
            return queryset.none()
        class_id = self.request.GET.get("class")
        subject_id = self.request.GET.get("subject")
        if class_id and (is_admin(user) or (user.role == "teacher" and teacher_profile(user).school_classes.filter(pk=class_id).exists())):
            queryset = queryset.filter(student__school_class_id=class_id)
        if subject_id and (is_admin(user) or (user.role == "teacher" and teacher_profile(user).subjects.filter(pk=subject_id).exists())):
            queryset = queryset.filter(subject_id=subject_id)
        return queryset

    def get_context_data(self, **kwargs):
        from school.models import SchoolClass, Subject
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if is_admin(user):
            context["classes"] = SchoolClass.objects.all()
            context["subjects"] = Subject.objects.all()
        elif user.role == "teacher" and teacher_profile(user):
            teacher = teacher_profile(user)
            context["classes"] = teacher.school_classes.all()
            context["subjects"] = teacher.subjects.all()
        else:
            context["classes"] = context["subjects"] = []
        context["can_edit"] = is_admin(user) or user.role == "teacher"
        return context


class TeacherGradeQuerysetMixin(JournalStaffMixin):
    def get_queryset(self):
        queryset = super().get_queryset().select_related("student__school_class", "student__user", "subject", "teacher__user")
        if is_admin(self.request.user):
            return queryset
        teacher = teacher_profile(self.request.user)
        return queryset.filter(teacher=teacher, student__school_class__in=teacher.school_classes.all(), subject__in=teacher.subjects.all())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not is_admin(self.request.user):
            kwargs["teacher"] = teacher_profile(self.request.user)
        return kwargs


class GradeCreateView(JournalStaffMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "journal/object_form.html"
    success_url = reverse_lazy("grade-list")
    extra_context = {"title": "Выставить оценку"}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not is_admin(self.request.user):
            kwargs["teacher"] = teacher_profile(self.request.user)
        return kwargs

    def form_valid(self, form):
        if not is_admin(self.request.user):
            form.instance.teacher = teacher_profile(self.request.user)
        return super().form_valid(form)


class GradeUpdateView(TeacherGradeQuerysetMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = "journal/object_form.html"
    success_url = reverse_lazy("grade-list")
    extra_context = {"title": "Редактировать оценку"}

    def form_valid(self, form):
        if not is_admin(self.request.user):
            form.instance.teacher = teacher_profile(self.request.user)
        return super().form_valid(form)


class GradeDeleteView(JournalStaffMixin, DeleteView):
    model = Grade
    template_name = "journal/confirm_delete.html"
    success_url = reverse_lazy("grade-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        teacher = teacher_profile(self.request.user)
        return queryset.filter(teacher=teacher, student__school_class__in=teacher.school_classes.all(), subject__in=teacher.subjects.all())


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = "journal/attendance_list.html"
    context_object_name = "records"
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.select_related("student__user", "student__school_class", "subject")
        if is_admin(user):
            return queryset
        if user.role == "teacher" and teacher_profile(user):
            teacher = teacher_profile(user)
            return queryset.filter(student__school_class__in=teacher.school_classes.all(), subject__in=teacher.subjects.all())
        if user.role == "student" and hasattr(user, "student_profile"):
            return queryset.filter(student=user.student_profile)
        return queryset.none()


class AttendanceManageMixin(JournalStaffMixin):
    def get_queryset(self):
        queryset = super().get_queryset().select_related("student__school_class", "student__user", "subject")
        if is_admin(self.request.user):
            return queryset
        teacher = teacher_profile(self.request.user)
        return queryset.filter(student__school_class__in=teacher.school_classes.all(), subject__in=teacher.subjects.all())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not is_admin(self.request.user):
            kwargs["teacher"] = teacher_profile(self.request.user)
        return kwargs


class AttendanceCreateView(AttendanceManageMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "journal/object_form.html"
    success_url = reverse_lazy("attendance-list")
    extra_context = {"title": "Отметить посещаемость"}


class AttendanceUpdateView(AttendanceManageMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "journal/object_form.html"
    success_url = reverse_lazy("attendance-list")
    extra_context = {"title": "Редактировать посещаемость"}


class AttendanceDeleteView(AttendanceManageMixin, DeleteView):
    model = Attendance
    template_name = "journal/confirm_delete.html"
    success_url = reverse_lazy("attendance-list")
