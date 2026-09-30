from django.urls import path
from . import views

urlpatterns = [
    path("grades/", views.GradeListView.as_view(), name="grade-list"),
    path("grades/add/", views.GradeCreateView.as_view(), name="grade-create"),
    path("grades/<int:pk>/edit/", views.GradeUpdateView.as_view(), name="grade-update"),
    path("grades/<int:pk>/delete/", views.GradeDeleteView.as_view(), name="grade-delete"),
    path("attendance/", views.AttendanceListView.as_view(), name="attendance-list"),
    path("attendance/add/", views.AttendanceCreateView.as_view(), name="attendance-create"),
    path("attendance/<int:pk>/edit/", views.AttendanceUpdateView.as_view(), name="attendance-update"),
    path("attendance/<int:pk>/delete/", views.AttendanceDeleteView.as_view(), name="attendance-delete"),
]
