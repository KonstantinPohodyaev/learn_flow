from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join
from .models import Certificate, Course, CourseProgress, Lesson, Module


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
                    'admin:courses_module_change',
                    args=[module.id]
                ), module.title)
                for module in course.modules.all()
            )
        )


admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(CourseProgress)
admin.site.register(Certificate)
