from django.urls import path
from . import views

urlpatterns = [
    path("classes/", views.SchoolClassList.as_view(), name="class-list"),
    path("classes/add/", views.ClassCreate.as_view(), name="class-create"),
    path("classes/<int:pk>/edit/", views.ClassUpdate.as_view(), name="class-update"),
    path("classes/<int:pk>/delete/", views.ClassDelete.as_view(), name="class-delete"),
    path("subjects/", views.SubjectList.as_view(), name="subject-list"),
    path("subjects/add/", views.SubjectCreate.as_view(), name="subject-create"),
    path("subjects/<int:pk>/edit/", views.SubjectUpdate.as_view(), name="subject-update"),
    path("subjects/<int:pk>/delete/", views.SubjectDelete.as_view(), name="subject-delete"),
    path("teachers/", views.TeacherList.as_view(), name="teacher-list"),
    path("teachers/add/", views.TeacherCreate.as_view(), name="teacher-create"),
    path("teachers/<int:pk>/edit/", views.TeacherUpdate.as_view(), name="teacher-update"),
    path("teachers/<int:pk>/delete/", views.TeacherDelete.as_view(), name="teacher-delete"),
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/add/", views.StudentCreate.as_view(), name="student-create"),
    path("students/<int:pk>/edit/", views.StudentUpdate.as_view(), name="student-update"),
    path("students/<int:pk>/delete/", views.StudentDelete.as_view(), name="student-delete"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/add/", views.UserCreate.as_view(), name="user-create"),
    path("users/<int:pk>/edit/", views.UserUpdate.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDelete.as_view(), name="user-delete"),
]
