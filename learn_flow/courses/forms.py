from django import forms

from .models import Course, Module, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'is_published']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'file']
