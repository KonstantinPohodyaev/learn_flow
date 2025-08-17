from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join, format_html
from .models import Certificate, Course, CourseProgress, Lesson, Module


APP_LINK = 'admin:courses_{model}_{action}'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'description',
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
        description='Модули'
    )
    def modules_field(self, course):
        return format_html_join(
            '\n',
            '<a href="{}">{}</a>',
            (
                (reverse(
                    APP_LINK.format(
                        model=Module._meta.model_name,
                        action='change'
                    ),
                    args=[module.id]
                ), module.title)
                for module in course.modules.all()
            )
        )


@admin.register(Module)
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
        description='Уроки'
    )
    def lessons_field(self, module):
        return format_html_join(
            '\n',
            '<a href="{}">{}</a>',
            (
                (
                    reverse(
                        APP_LINK.format(
                            model=Lesson._meta.model_name,
                            action='change'
                        ),
                        args=[lesson.pk]
                    )
                )
                for lesson in module.lessons.all()
            )
        )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'content',
        'module__title',
        'video_url',
        'file_link',
        'test_exists'
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

    @admin.display(description='Файл урока')
    def file_link(self, lesson):
        if lesson.file:
            return format_html(
                '<a href="{}" download>{}</a>',
                lesson.file.url,
                lesson.file.name
            )
        return '—'

    @admin.display(description='Наличие теста')
    def test_exists(self, lesson):
        try:
            quiz = lesson.quiz
            return format_html(
                '<a href="{}">{}</a>',
                reverse(
                    APP_LINK.format(
                        model=Lesson._meta.model_name,
                        action='change'
                    ),
                    args=[quiz.pk]
                ),
                quiz.title
            )
        except Lesson.quiz.RelatedObjectDoesNotExist:
            return False


admin.site.register(CourseProgress)
admin.site.register(Certificate)
