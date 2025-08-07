from django.urls import path

from .views import (
    CoursesListView, CourseCreateView, CourseDetailView, ModuleCreateView,
    ModuleDetailView, LessonCreateView, LessonDetailView
)

app_name = 'courses'


urlpatterns = [
    path(
        'course-create/',
        CourseCreateView.as_view(),
        name='course_create'
    ),
    path(
        '<int:course_id>/',
        CourseDetailView.as_view(),
        name='course_detail'
    ),
    path(
        'module-create/<int:course_id>/',
        ModuleCreateView.as_view(),
        name='module_create'
    ),
    path(
        'course/<int:course_id>/module/<int:module_id>/',
        ModuleDetailView.as_view(),
        name='module_detail'
    ),
    path(
        'lesson-create/course/<int:course_id>/module/<int:module_id>/',
        LessonCreateView.as_view(),
        name='lesson_create'
    ),
    path(
        'course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/',
        LessonDetailView.as_view(),
        name='lesson_detail'
    ),
    path(
        '',
        CoursesListView.as_view(),
        name='course_list'
    )
]
