from django.shortcuts import render
from .models import Question

def home(request):
    if request.method == "POST":
        answers = {}
        score = 0
        for question in Question.objects.all():
            user_answer = request.POST.get(str(question.id))
            answers[question.id] = user_answer
            if user_answer and user_answer.lower().strip() == question.correct_answer.lower().strip():
                score += 1
        return render(request, "quiz/result.html", {"score": score, "total": Question.objects.count()})
    return render(request, "quiz/home.html", {"questions": Question.objects.all()})
