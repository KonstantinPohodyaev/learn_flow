from datetime import datetime
import os

from django.core.files.base import ContentFile
from quizzes.models import Quiz, UserQuizResult
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
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
    buffer = io.BytesIO()
    width, height = A4
    font_path = os.path.join('static', 'fonts', 'DejaVuSans.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
    p = canvas.Canvas(buffer, pagesize=A4)
    steps = int(height)
    for i in range(steps):
        ratio = i / steps
        r = (15 + (0 - 15) * ratio) / 255
        g = (30 + (0 - 30) * ratio) / 255
        b = (48 + (0 - 48) * ratio) / 255
        p.setFillColorRGB(r, g, b)
        p.rect(0, i, width, 1, stroke=0, fill=1)
    logo_path = os.path.join('static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        logo_width = 300
        logo_height = 300
        p.drawImage(logo, (width - logo_width) / 2, (height - logo_height) / 2,
                    width=logo_width, height=logo_height, mask='auto')
    p.setStrokeColorRGB(1, 1, 1)
    p.setLineWidth(5)
    p.rect(30, 30, width - 60, height - 60)
    p.setFillColorRGB(1, 1, 1)
    p.setFont("DejaVuSans", 36)
    p.drawCentredString(width / 2, height - 150, "СЕРТИФИКАТ")
    p.setFont("DejaVuSans", 18)
    p.drawCentredString(width / 2, height - 200, "Настоящим подтверждается, что")
    p.setFont("DejaVuSans", 24)
    p.drawCentredString(width / 2, height - 250, user.email)
    p.setFont("DejaVuSans", 18)
    p.drawCentredString(width / 2, height - 300, "успешно прошёл курс")
    p.setFont("DejaVuSans", 22)
    p.drawCentredString(width / 2, height - 340, f"«{course.title}»")
    p.setFont("DejaVuSans", 14)
    p.drawString(50, 50, f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
    p.drawRightString(width - 50, 50, "Подпись: ______________")
    p.showPage()
    p.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), f"certificate_{course.id}_{user.id}.pdf")

