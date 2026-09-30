"""ModelForm для управления школьными справочниками."""
from django import forms
from accounts.models import User
from .models import SchoolClass, Student, Subject, Teacher


class BootstrapModelForm(forms.ModelForm):
    """Добавляет единый Bootstrap-класс полям формы."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (field.widget.attrs.get("class", "") + " form-control").strip()
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] += " form-select"


class SchoolClassForm(BootstrapModelForm):
    class Meta:
        model = SchoolClass
        fields = ("name", "homeroom_teacher")


class SubjectForm(BootstrapModelForm):
    class Meta:
        model = Subject
        fields = ("name",)


class TeacherForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    email = forms.EmailField(label="Электронная почта", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=False)
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=False, label="Предметы")
    school_classes = forms.ModelMultipleChoiceField(queryset=SchoolClass.objects.all(), required=False, label="Назначенные классы")

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs["class"] += " form-select"
        if self.instance:
            self.fields["username"].initial = self.instance.user.username
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["subjects"].initial = self.instance.subjects.all()
            self.fields["school_classes"].initial = self.instance.school_classes.all()
            self.fields["password"].required = False
        else:
            self.fields["password"].required = True

    def clean_username(self):
        username = self.cleaned_data["username"]
        users = User.objects.filter(username=username)
        if self.instance:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise forms.ValidationError("Этот логин уже используется.")
        return username

    def save(self):
        data = self.cleaned_data
        if self.instance:
            teacher = self.instance
            user = teacher.user
        else:
            user = User(role=User.Role.TEACHER)
            teacher = Teacher(user=user)
        user.username = data["username"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.role = User.Role.TEACHER
        if data.get("password"):
            user.set_password(data["password"])
        elif not user.pk:
            user.set_unusable_password()
        user.save()
        teacher.user = user
        teacher.save()
        teacher.subjects.set(data["subjects"])
        teacher.school_classes.set(data["school_classes"])
        return teacher


class StudentForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=150)
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    email = forms.EmailField(label="Электронная почта", required=False)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=False)
    school_class = forms.ModelChoiceField(queryset=SchoolClass.objects.all(), label="Класс")

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
        if self.instance:
            self.fields["username"].initial = self.instance.user.username
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email
            self.fields["school_class"].initial = self.instance.school_class
        else:
            self.fields["password"].required = True

    def clean_username(self):
        username = self.cleaned_data["username"]
        users = User.objects.filter(username=username)
        if self.instance:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise forms.ValidationError("Этот логин уже используется.")
        return username

    def save(self):
        data = self.cleaned_data
        student = self.instance or Student()
        user = student.user if self.instance else User(role=User.Role.STUDENT)
        user.username, user.first_name, user.last_name, user.email = data["username"], data["first_name"], data["last_name"], data["email"]
        user.role = User.Role.STUDENT
        if data.get("password"):
            user.set_password(data["password"])
        elif not user.pk:
            user.set_unusable_password()
        user.save()
        student.user, student.school_class = user, data["school_class"]
        student.save()
        return student
