from django.urls import path
from . import views

urlpatterns = [
    path("", views.ScheduleListView.as_view(), name="schedule-list"),
    path("add/", views.LessonCreateView.as_view(), name="lesson-create"),
    path("<int:pk>/edit/", views.LessonUpdateView.as_view(), name="lesson-update"),
    path("<int:pk>/delete/", views.LessonDeleteView.as_view(), name="lesson-delete"),
]
