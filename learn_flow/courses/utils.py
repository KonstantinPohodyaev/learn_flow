from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from quizzes.models import Quiz, UserQuizResult
from weasyprint import HTML
import io


def check_passed_all_quizzes(user, course):
    all_courses_quizzes = Quiz.objects.filter(
        lesson__module__course=course
    )
    passed_quizzes = UserQuizResult.objects.filter(
        user=user,
        quiz__in=all_courses_quizzes,
        success_status=True
    ).count()
    return (
        all_courses_quizzes.exists()
        and passed_quizzes == all_courses_quizzes.count()
    )


def generate_certificate_file(user, course):
    html_string = render_to_string(
        'courses/certificate_template.html',
        dict(
            user=user,
            course=course
        )
    )
    pdf = io.BytesIO()
    HTML(string=html_string, base_url='').write_pdf(pdf)
    return ContentFile(pdf.getvalue(), f'certificate_{course.id}_{user.id}.pdf')
