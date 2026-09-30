"""Формы журнала ограничивают доступные классы и предметы на сервере."""
from django import forms
from school.models import Student
from .models import Attendance, Grade


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ("student", "subject", "teacher", "value", "date", "grade_type", "comment")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher = teacher
        if teacher:
            self.fields.pop("teacher")
            self.fields["student"].queryset = Student.objects.filter(school_class__in=teacher.school_classes.all()).select_related("user", "school_class")
            self.fields["subject"].queryset = teacher.subjects.all()
        self.fields["student"].label_from_instance = lambda student: f"{student} — {student.school_class}"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"

    def clean(self):
        data = super().clean()
        if self.teacher and data.get("student") and data.get("subject"):
            if not self.teacher.school_classes.filter(pk=data["student"].school_class_id).exists():
                raise forms.ValidationError("У вас нет доступа к этому классу.")
            if not self.teacher.subjects.filter(pk=data["subject"].pk).exists():
                raise forms.ValidationError("У вас нет доступа к этому предмету.")
        return data


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ("student", "subject", "lesson_date", "status")
        widgets = {"lesson_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, teacher=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher = teacher
        if teacher:
            self.fields["student"].queryset = Student.objects.filter(school_class__in=teacher.school_classes.all()).select_related("user", "school_class")
            self.fields["subject"].queryset = teacher.subjects.all()
        self.fields["student"].label_from_instance = lambda student: f"{student} — {student.school_class}"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"

    def clean(self):
        data = super().clean()
        if self.teacher and data.get("student") and data.get("subject"):
            if not self.teacher.school_classes.filter(pk=data["student"].school_class_id).exists() or not self.teacher.subjects.filter(pk=data["subject"].pk).exists():
                raise forms.ValidationError("Вы можете отмечать посещаемость только своих классов и предметов.")
        return data
