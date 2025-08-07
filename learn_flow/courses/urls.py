from django.urls import path

from .views import CoursesListView, CourseCreateView, CourseDetailView

app_name = 'courses'


urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='courses_create'),
    path('<int:course_id>/', CourseDetailView.as_view(), name='detail'),
    path('', CoursesListView.as_view(), name='courses_list')
]
