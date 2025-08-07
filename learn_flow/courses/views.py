from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy

from .models import Course
from .forms import CourseForm


class CoursesListView(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/courses_create.html'
    success_url = reverse_lazy('courses:courses_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_object(self, *args, **kwargs):
        return self.model.objects.get(pk=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.get_object().modules.all()
        return context

