from quizzes.models import Quiz, UserQuizResult


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
