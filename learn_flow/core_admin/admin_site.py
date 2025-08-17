from django.contrib import admin
from django.urls import path
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse

from courses.models import Course, Module, Lesson


User = get_user_model()


class CustomAdminSite(admin.AdminSite):
    site_header = 'LearnFlow панель'
    site_title = 'LearnFlow админка'
    index_title = 'Добро пожаловать в систему управления обучением'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'dashboard/',
                self.admin_view(self.dashboard),
                name='dashboard'
            )
        ]
        return custom_urls + urls

    def dashboard(self, request):
        stats = {
            'courses': Course.objects.count(),
            'modules': Module.objects.count(),
            'lessons': Lesson.objects.count(),
            'users': User.objects.count()
        }
        return TemplateResponse(
            request, 'admin/dashboard.html', dict(
                self.each_context(request),
                stats=stats
            )
        )


custom_admin_site = CustomAdminSite(name='custom_admin')
