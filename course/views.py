from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Course, Question, Choice, Submission, Enrollment, Learner
from datetime import date

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details_bootstrap.html', {'course': course})

def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__course=course)
    return render(request, 'exam.html', {'course': course, 'questions': questions})

def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Mock learner, assume first learner
    learner = Learner.objects.first()
    if not learner:
        return HttpResponse("No learner found")
    enrollment, created = Enrollment.objects.get_or_create(
        learner=learner, course=course,
        defaults={'date_enrolled': date.today(), 'mode': 'H'}
    )
    if request.method == 'POST':
        selected_choices = request.POST.getlist('choice')
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(selected_choices)
        return redirect('show_exam_result', course_id=course_id, submission_id=submission.id)
    return redirect('exam', course_id=course_id)

def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, enrollment__course_id=course_id)
    course = submission.enrollment.course
    selected_ids = list(submission.choices.values_list('id', flat=True))
    total_score = 0
    possible_score = 0
    for question in Question.objects.filter(lesson__course=course):
        possible_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
    grade_percentage = (total_score / possible_score * 100) if possible_score > 0 else 0
    context = {
        'course': course,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'possible_score': possible_score,
        'grade_percentage': grade_percentage,
    }
    return render(request, 'exam_result.html', context)
