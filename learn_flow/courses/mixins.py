from courses.forms import CourseForm, LessonForm, ModuleForm
from courses.models import Course, Lesson, Module
from django.urls import reverse_lazy


class CourseModelMixin:
    model = Course
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'


class CourseFormTemplateObjectNameMixin:
    model = Course
    pk_url_kwarg = 'course_id'
    template_name = 'courses/course_create.html'
    form_class = CourseForm
    context_object_name = 'course'


class CourseSuccessUrlMixin:
    success_url = reverse_lazy('courses:course_list')


class ModuleModelMixin:
    model = Module
    pk_url_kwarg = 'module_id'
    context_object_name = 'module'


class ModuleFormTemplateObjectNameMixin:
    model = Module
    template_name = 'courses/module_create.html'
    form_class = ModuleForm
    context_object_name = 'module'
    pk_url_kwarg = 'module_id'


class LessonModelMixin:
    model = Lesson
    pk_url_kwarg = 'lesson_id'
    context_object_name = 'lesson'


class LessonFormTemplateObjectNameMixin:
    model = Lesson
    template_name = 'courses/lesson_create.html'
    form_class = LessonForm
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'
