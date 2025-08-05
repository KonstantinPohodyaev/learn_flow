from django.views.generic import ListView, CreateView

from .models import Course


class CoursesListView(ListView):
    model = Course
    template_name = 'courses_list.html'
    context_object_name = 'courses'


class CourseCreateView(CreateView):
    pass
