"""Администраторский CRUD школьных справочников и профилей."""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from accounts.mixins import AdminRequiredMixin
from accounts.forms import UserCreateForm, UserUpdateForm
from .models import SchoolClass, Student, Subject, Teacher
from .forms import SchoolClassForm, SubjectForm, TeacherForm, StudentForm

User = get_user_model()


class AdminListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    paginate_by = 20
    template_name = "school/object_list.html"
    context_object_name = "objects"
    title = "Записи"
    create_url = "#"

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title=self.title, create_url=self.create_url)
        return context


class SchoolClassList(AdminListView):
    model = SchoolClass
    title = "Классы"
    create_url = "class-create"
    def get_queryset(self): return SchoolClass.objects.select_related("homeroom_teacher__user")

class SubjectList(AdminListView):
    model = Subject
    title = "Предметы"
    create_url = "subject-create"

class TeacherList(AdminListView):
    model = Teacher
    title = "Учителя"
    create_url = "teacher-create"
    def get_queryset(self): return Teacher.objects.select_related("user").prefetch_related("subjects")

class StudentList(AdminListView):
    model = Student
    title = "Ученики"
    create_url = "student-create"
    def get_queryset(self): return Student.objects.select_related("user", "school_class")

class UserList(AdminListView):
    model = User
    title = "Пользователи"
    create_url = "user-create"


class ObjectCreate(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = "school/object_form.html"
    success_url = reverse_lazy("class-list")
    page_title = "Добавление записи"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.page_title
        return context

class ObjectUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = "school/object_form.html"
    success_url = reverse_lazy("class-list")
    page_title = "Редактирование записи"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.page_title
        return context

class ObjectDelete(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    template_name = "school/object_confirm_delete.html"
    success_url = reverse_lazy("class-list")

class ClassCreate(ObjectCreate): model = SchoolClass; form_class = SchoolClassForm; page_title = "Новый класс"; success_url = reverse_lazy("class-list")
class ClassUpdate(ObjectUpdate): model = SchoolClass; form_class = SchoolClassForm; success_url = reverse_lazy("class-list")
class ClassDelete(ObjectDelete): model = SchoolClass; success_url = reverse_lazy("class-list")
class SubjectCreate(ObjectCreate): model = Subject; form_class = SubjectForm; page_title = "Новый предмет"; success_url = reverse_lazy("subject-list")
class SubjectUpdate(ObjectUpdate): model = Subject; form_class = SubjectForm; success_url = reverse_lazy("subject-list")
class SubjectDelete(ObjectDelete): model = Subject; success_url = reverse_lazy("subject-list")

class TeacherCreate(LoginRequiredMixin, AdminRequiredMixin, FormView):
    template_name = "school/object_form.html"; form_class = TeacherForm; success_url = reverse_lazy("teacher-list")
    extra_context = {"title": "Новый учитель"}
    def form_valid(self, form): form.save(); return super().form_valid(form)

class TeacherUpdate(TeacherCreate):
    extra_context = {"title": "Редактирование учителя"}
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs["instance"] = Teacher.objects.get(pk=self.kwargs["pk"]); return kwargs

class TeacherDelete(ObjectDelete): model = Teacher; success_url = reverse_lazy("teacher-list")

class StudentCreate(LoginRequiredMixin, AdminRequiredMixin, FormView):
    template_name = "school/object_form.html"; form_class = StudentForm; success_url = reverse_lazy("student-list")
    extra_context = {"title": "Новый ученик"}
    def form_valid(self, form): form.save(); return super().form_valid(form)

class StudentUpdate(StudentCreate):
    extra_context = {"title": "Редактирование ученика"}
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs(); kwargs["instance"] = Student.objects.select_related("user").get(pk=self.kwargs["pk"]); return kwargs

class StudentDelete(ObjectDelete): model = Student; success_url = reverse_lazy("student-list")

class UserCreate(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User; form_class = UserCreateForm; template_name = "school/object_form.html"; success_url = reverse_lazy("user-list")
    extra_context = {"title": "Новый пользователь"}

class UserUpdate(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User; form_class = UserUpdateForm; template_name = "school/object_form.html"; success_url = reverse_lazy("user-list")
    extra_context = {"title": "Редактирование пользователя"}

class UserDelete(ObjectDelete): model = User; success_url = reverse_lazy("user-list")
