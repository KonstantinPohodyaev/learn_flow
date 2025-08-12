from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from courses.utils import generate_certificate_file
from courses.models import Course
from users.models import CustomUser
from celery import shared_task


User = get_user_model()

EMAIL_SUBJECT = 'Ваш сертификат'
EMAIL_BODY = '''
{full_name}, поздравляем с прохождением курса {title}!
Сертификат об окончании во вложении!
'''


@shared_task
def send_certificate_by_email(user_id, course_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    course = get_object_or_404(Course, pk=course_id)
    pdf_file = generate_certificate_file(user, course)
    email = EmailMessage(
        subject=EMAIL_SUBJECT,
        body=EMAIL_BODY.format(
            full_name=user.full_name,
            title=course.title
        ),
        to=[user.email]
    )
    email.attach('certificate.pdf', pdf_file.read(), 'application/pdf')
    email.send()
