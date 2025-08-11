from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import CreateView
from django.urls import include, path, reverse_lazy

from courses.views import vk_callback
from users.forms import CustomUserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quizzes.urls')),
    path(
        'auth/registration',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login')
        ),
        name='registration'
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/vk/callback/', vk_callback, name='vk_callback'),
    path('', include('courses.urls'))
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

handler404 = 'courses.views.custom_404'
handler500 = 'courses.views.custom_500'
handler403 = 'courses.views.custom_403'
handler400 = 'courses.views.custom_400'
