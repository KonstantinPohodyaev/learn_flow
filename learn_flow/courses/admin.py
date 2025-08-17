from django.contrib import admin
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.urls import reverse, path
from django.utils.html import format_html_join, format_html
from courses.models import Certificate, Course, CourseProgress, Lesson, Module
from quizzes.models import Quiz
from core_admin.admin_site import custom_admin_site


User = get_user_model()


A_TAG_PATTERN = '<a href={}>{}</a>'
APP_LINK = 'admin:{app_label}_{model}_{action}'

COURSE_ADMIN_MODULES_FIELD_DESCRIPTION = 'Модули'
MODULE_ADMIN_LESSONS_FIELD_DESCRIPTION = 'Уроки'
LESSON_ADMIN_FILE_FIELD_DESCRIPTION = 'Файл урока'
LESSON_ADMIN_QUIZ_EXISTS_DESCRIPTION = 'Наличие теста'
CERTIFICATE_ADMIN_FILE_FIELD_DESCRIPTION = 'Файл сертификата'


def get_list_of_object_links(app_label, model_name, queryset, action='change'):
    return format_html_join(
        '\n',
        A_TAG_PATTERN,
        (
            (
                reverse(
                    APP_LINK.format(
                        app_label=app_label,
                        model=model_name,
                        action=action
                    ),
                    args=[object.pk]
                )
            )
            for object in queryset
        )
    )


def get_object_link(app_label, model_name, object, action='change'):
    return format_html(
        A_TAG_PATTERN,
        reverse(
            APP_LINK.format(
                app_label=app_label,
                model=model_name,
                action=action
            ),
            args=[object.pk]
        ),
        object.title
    )


def get_file_link(file):
    if file:
        return format_html(
            A_TAG_PATTERN,
            file.url,
            file.name
        )
    return False


@admin.register(Course, site=custom_admin_site)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
        'is_published',
        'owner',
        'modules_field'
    ]
    search_fields = [
        'title', 'owner__email'
    ]
    list_filter = [
        'title', 'owner__email'
    ]
    list_display_links = [
        'title'
    ]


    @admin.display(
        description=COURSE_ADMIN_MODULES_FIELD_DESCRIPTION
    )
    def modules_field(self, course):
        return get_list_of_object_links(
            Course._meta.app_label,
            Course._meta.model_name,
            course.modules.all()
        )


@admin.register(Module, site=custom_admin_site)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'course__title',
        'lessons_field'
    ]
    search_fields = [
        'title',
        'course__title'
    ]
    list_filter = [
        'title',
        'course__title'
    ]
    list_display_links = [
        'title'
    ]

    @admin.display(
        description=MODULE_ADMIN_LESSONS_FIELD_DESCRIPTION
    )
    def lessons_field(self, module):
        return get_list_of_object_links(
            Module._meta.app_label,
            Module._meta.model_name,
            module.lessons.all()
        )


@admin.register(Lesson, site=custom_admin_site)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'content',
        'module__title',
        'video_url',
        'file_link',
        'quiz_exists'
    ]
    search_fields = [
        'title',
        'module__title'
    ]
    list_filter = [
        'title',
        'module__title'
    ]
    list_display_links = [
        'title'
    ]

    @admin.display(
            description=LESSON_ADMIN_FILE_FIELD_DESCRIPTION
        )
    def file_link(self, lesson):
        return get_file_link(lesson.file)

    @admin.display(description=LESSON_ADMIN_QUIZ_EXISTS_DESCRIPTION)
    def quiz_exists(self, lesson):
        try:
            return get_object_link(
                Quiz._meta.app_label,
                Quiz._meta.model_name,
                lesson.quiz
            )
        except Lesson.quiz.RelatedObjectDoesNotExist:
            return False


@admin.register(CourseProgress, site=custom_admin_site)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = [
        'user__email',
        'course__title',
        'current_lesson__title',
        'completed'
    ]
    search_fields = [
        'user__email',
        'course__title'
    ]
    list_filter = [
        'user__email',
        'course__title'
    ]
    list_display_links = [
        'user__email'
    ]


@admin.register(Certificate, site=custom_admin_site)
class CertificateAdmin(admin.ModelAdmin):
    list_display = [
        'user__email',
        'course__title',
        'file_field'
    ]
    search_fields = [
        'user__email'
    ]
    list_filter = [
        'user__email',
        'course__title'
    ]
    list_display_links = [
        'user__email'
    ]

    @admin.display(
        description=CERTIFICATE_ADMIN_FILE_FIELD_DESCRIPTION
    )
    def file_field(self, certificate):
        return get_file_link(certificate.file)
