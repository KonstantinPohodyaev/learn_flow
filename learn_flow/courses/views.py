from django.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView
)
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from courses.models import Course, Module, Lesson
from quizzes.models import UserQuizResult
from courses.forms import CourseForm, ModuleForm, LessonForm
from courses.mixins import (
    CourseModelMixin, CourseFormTemplateObjectNameMixin,
    CourseSuccessUrlMixin, ModuleModelMixin,
    ModuleFormTemplateObjectNameMixin, LessonModelMixin,
    LessonFormTemplateObjectNameMixin
)


class CoursesListView(CourseModelMixin, ListView):
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    queryset = CourseModelMixin.model.objects.filter(is_published=True)


class CourseCreateView(
    CourseFormTemplateObjectNameMixin,
    CourseSuccessUrlMixin, CreateView
):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseDetailView(CourseModelMixin, DetailView):
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.get_object().modules.all()
        return context


class CourseDeleteView(CourseModelMixin, CourseSuccessUrlMixin, DeleteView):
    template_name = 'courses/course_delete.html'


class CourseUpdateView(
    CourseFormTemplateObjectNameMixin, UpdateView
):
    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail', args=[self.kwargs[self.pk_url_kwarg]]
        )


class ModuleCreateView(ModuleFormTemplateObjectNameMixin, CreateView):
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


class ModuleDetailView(ModuleModelMixin, DetailView):
    template_name = 'courses/module_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessons = self.get_object().lessons.all()
        lessons_and_user_quiz_results = []
        for lesson in lessons:
            try:
                quiz = lesson.quiz
                user_quiz_result = UserQuizResult.objects.filter(
                    quiz=quiz,
                    user=self.request.user
                ).first()
            except Lesson.quiz.RelatedObjectDoesNotExist:
                user_quiz_result = None
            lessons_and_user_quiz_results.append(
                (lesson, user_quiz_result)
            )
        context['lessons_and_user_quiz_results'] = lessons_and_user_quiz_results
        return context

    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related('course').prefetch_related('lessons').all(),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class ModuleDeleteView(ModuleModelMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail',
            args=[self.get_object().course.pk]
        )


class ModuleUpdateView(ModuleFormTemplateObjectNameMixin, UpdateView):
    def get_object(self):
        return self.model.objects.select_related('course').get(
            pk=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.get_object().course.pk, self.kwargs[self.pk_url_kwarg]]
        )


class LessonCreateView(LessonFormTemplateObjectNameMixin, CreateView):
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


class LessonDetailView(LessonModelMixin, DetailView):
    template_name = 'courses/lesson_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = getattr(self.get_object(), 'quiz', None)
        return context

    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related('module__course'),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class LessonDeleteView(LessonModelMixin, DeleteView):
    template_name = 'courses/lesson_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.kwargs['course_id'], self.kwargs['module_id']]
        )


class LessonUpdateView(LessonFormTemplateObjectNameMixin, UpdateView):
    def get_success_url(self):
        lesson = self.get_object()
        return reverse_lazy(
            'courses:lesson_detail',
            args=[
                lesson.module.course.pk,
                lesson.module.pk,
                lesson.pk
            ]
        )

    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related('module__course'),
            pk=self.kwargs[self.pk_url_kwarg]
        )
