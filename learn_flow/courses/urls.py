from django.urls import path

from .views import (CourseCreateView, CourseDeleteView, CourseDetailView,
                    CoursesListView, CourseUpdateView, LessonCreateView,
                    LessonDeleteView, LessonDetailView, LessonUpdateView,
                    ModuleCreateView, ModuleDeleteView, ModuleDetailView,
                    ModuleUpdateView, send_certificate)

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
        'course/<int:course_id>/module/<int:module_id>/',
        ModuleDetailView.as_view(),
        name='module_detail'
    ),
    path(
        'course-update/<int:course_id>/',
        CourseUpdateView.as_view(),
        name='course_update'
    ),
    path(
        'course-delete/<int:course_id>/',
        CourseDeleteView.as_view(),
        name='course_delete'
    ),
    path(
        'module-create/<int:course_id>/',
        ModuleCreateView.as_view(),
        name='module_create'
    ),
    path(
        'course/<int:course_id>/module-update/<int:module_id>/',
        ModuleUpdateView.as_view(),
        name='module_update'
    ),
    path(
        'module-delete/<int:module_id>/',
        ModuleDeleteView.as_view(),
        name='module_delete'
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
        'lesson-delete/course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/',
        LessonDeleteView.as_view(),
        name='lesson_delete'
    ),
    path(
        'lesson-update/course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/',
        LessonUpdateView.as_view(),
        name='lesson_update'
    ),
    path(
        'send-certificate-by-email/user/<int:user_id>/course/<int:course_id>/',
        send_certificate,
        name='send_certificate'
    ),
    path(
        '',
        CoursesListView.as_view(),
        name='course_list'
    )
]
