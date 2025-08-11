from http import HTTPStatus
import requests

from courses.mixins import (CourseFormTemplateObjectNameMixin,
                            CourseModelMixin, CourseSuccessUrlMixin,
                            LessonFormTemplateObjectNameMixin,
                            LessonModelMixin,
                            ModuleFormTemplateObjectNameMixin,
                            ModuleModelMixin, CheckSuperUserStatus)
from courses.models import Certificate, Course, Lesson, Module
from courses.utils import check_passed_all_quizzes, generate_certificate_file
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.contrib.auth import login
from django.conf import settings
from quizzes.models import UserQuizResult
from users.models import CustomUser


class CoursesListView(CourseModelMixin, ListView):
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    queryset = CourseModelMixin.model.objects.filter(is_published=True)


class CourseCreateView(
    CheckSuperUserStatus,
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
        user = self.request.user
        course = self.get_object()
        if user.is_authenticated:
            certificate = Certificate.objects.filter(
                user=user, course=course
            ).first()
            if certificate and not check_passed_all_quizzes(user, course):
                certificate.delete()
            if (
                user.is_authenticated
                and not certificate
                and check_passed_all_quizzes(user, course)
            ):
                certificate = Certificate.objects.create(
                    user=user,
                    course=course,
                    file=generate_certificate_file(user, course)
                )
            context['certificate'] = certificate
        else:
            certificate = None
        return context


class CourseDeleteView(
    CheckSuperUserStatus, CourseModelMixin, CourseSuccessUrlMixin, DeleteView
):
    template_name = 'courses/course_delete.html'


class CourseUpdateView(
    CheckSuperUserStatus, CourseFormTemplateObjectNameMixin, UpdateView
):
    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail', args=[self.kwargs[self.pk_url_kwarg]]
        )


class ModuleCreateView(
    CheckSuperUserStatus, ModuleFormTemplateObjectNameMixin, CreateView
):
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
        user = self.request.user
        for lesson in lessons:
            try:
                quiz = lesson.quiz
                if user.is_authenticated:
                    user_quiz_result = UserQuizResult.objects.filter(
                        quiz=quiz,
                        user=user
                    ).first()
                else:
                    user_quiz_result = None
            except Lesson.quiz.RelatedObjectDoesNotExist:
                user_quiz_result = None
            lessons_and_user_quiz_results.append(
                (lesson, user_quiz_result)
            )
        context['lessons_and_user_quiz_results'] = lessons_and_user_quiz_results
        return context


    def get_object(self):
        return get_object_or_404(
            self.model.objects.select_related(
                'course'
            ).prefetch_related(
                'lessons'
            ).all(),
            pk=self.kwargs[self.pk_url_kwarg]
        )


class ModuleDeleteView(
    CheckSuperUserStatus, ModuleModelMixin, DeleteView
):
    def get_success_url(self):
        return reverse_lazy(
            'courses:course_detail',
            args=[self.get_object().course.pk]
        )


class ModuleUpdateView(
    CheckSuperUserStatus, ModuleFormTemplateObjectNameMixin, UpdateView
):
    def get_object(self):
        return self.model.objects.select_related('course').get(
            pk=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.get_object().course.pk, self.kwargs[self.pk_url_kwarg]]
        )


class LessonCreateView(
    CheckSuperUserStatus, LessonFormTemplateObjectNameMixin, CreateView
):
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


class LessonDeleteView(
    CheckSuperUserStatus, LessonModelMixin, DeleteView
):
    template_name = 'courses/lesson_delete.html'

    def get_success_url(self):
        return reverse_lazy(
            'courses:module_detail',
            args=[self.kwargs['course_id'], self.kwargs['module_id']]
        )


class LessonUpdateView(
    CheckSuperUserStatus, LessonFormTemplateObjectNameMixin, UpdateView
):
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


def custom_404(request, exception):
    return render(request, 'errors/404.html', status=HTTPStatus.NOT_FOUND)


def custom_500(request):
    return render(request, 'errors/500.html', status=HTTPStatus.INTERNAL_SERVER_ERROR)


def custom_403(request, exception):
    return render(request, 'errors/403.html', status=HTTPStatus.FORBIDDEN)


def custom_400(request, exception):
    return render(request, 'errors/400.html', status=HTTPStatus.BAD_REQUEST)

def vk_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('login')
    token_url = 'https://oauth.vk.com/access_token'
    params = {
        'client_id': settings.VK_CLIENT_ID,
        'client_secret': settings.VK_CLIENT_SECRET,
        'redirect_uri': 'https://yourdomain.com/accounts/vk/callback/',
        'code': code,
    }
    resp = requests.get(token_url, params=params)
    data = resp.json()
    access_token = data.get('access_token')
    user_id = data.get('user_id')
    email = data.get('email')
    if not access_token or not user_id:
        return redirect('login')
    user_info_url = 'https://api.vk.com/method/users.get'
    user_info_params = {
        'user_ids': user_id,
        'fields': 'photo_100,first_name,last_name',
        'access_token': access_token,
        'v': '5.131',
    }
    user_info_resp = requests.get(user_info_url, params=user_info_params)
    user_info = user_info_resp.json()['response'][0]
    user, created = CustomUser.objects.get_or_create(email=email, defaults={
        'full_name': f"{user_info['first_name']} {user_info['last_name']}",
    })
    login(request, user)
    return redirect('courses:course_list')
