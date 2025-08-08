from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from courses.models import Course, Module, Lesson
from courses.forms import CourseForm, ModuleForm, LessonForm


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    queryset = model.objects.filter(is_published=True)


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_create.html'
    success_url = reverse_lazy('courses:courses_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.get_object().modules.all()
        return context


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'courses/course_delete.html'
    pk_url_kwarg = 'course_id'
    success_url = reverse_lazy('courses:course_list')


class ModuleCreateView(CreateView):
    model = Module
    template_name = 'courses/module_create.html'
    form_class = ModuleForm

    def form_valid(self, form):
        form.instance.course = Course.objects.get(
            pk=self.kwargs[self.pk_url_kwarg]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail',
            args=[self.kwargs[self.pk_url_kwarg]]
        )


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'courses/module_detail.html'
    pk_url_kwarg = 'module_id'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.get_object().lessons.all()
        return context

    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related('course').all(),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class ModuleDeleteView(DeleteView):
    model = Module
    template_name = 'courses/module_delete.html'
    pk_url_kwarg = 'module_id'

    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail',
            args=[self.get_object().course.pk]
        )


class LessonCreateView(CreateView):
    model = Lesson
    template_name = 'courses/lesson_create.html'
    form_class = LessonForm

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['course_id'])
        form.instance.module = Module.objects.get(pk=self.kwargs['module_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module'] = Module.objects.get(pk=self.kwargs['module_id'])
        return context

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.kwargs['course_id'], self.kwargs['module_id']]
        )


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'courses/lesson_detail.html'
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = getattr(self.get_object(), 'quiz', None)
        return context

    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related('module__course'),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'courses/lesson_delete.html'
    pk_url_kwarg = 'lesson_id'

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.kwargs['course_id'], self.kwargs['module_id']]
        )
