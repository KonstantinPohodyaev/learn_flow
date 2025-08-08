from django.urls import path

from .views import (
    CoursesListView, CourseCreateView, CourseDetailView, CourseDeleteView,
    ModuleCreateView, ModuleDetailView, ModuleDeleteView, 
    LessonCreateView, LessonDetailView, LessonDeleteView
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
        'lesson-detail/course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/',
        LessonDetailView.as_view(),
        name='lesson_detail'
    ),
    path(
        'lesson-delete/course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/',
        LessonDeleteView.as_view(),
        name='lesson_delete'
    ),
    path(
        'course-delete/<int:course_id>/',
        CourseDeleteView.as_view(),
        name='course_delete'
    ),
    path(
        'module-delete/<int:module_id>/',
        ModuleDeleteView.as_view(),
        name='module_delete'
    ),
    path(
        '',
        CoursesListView.as_view(),
        name='course_list'
    )
]
