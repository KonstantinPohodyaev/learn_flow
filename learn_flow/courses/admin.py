from django.contrib import admin

from .models import Certificate, Course, CourseProgress, Lesson, Module

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(CourseProgress)
admin.site.register(Certificate)
