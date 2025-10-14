# quiz/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question
import random

def build_quiz_data_from_db():
    quiz_data = []
    for q in Question.objects.all():
        # gather only non-empty options
        opts = [q.option_a, q.option_b, q.option_c, q.option_d]
        opts = [o for o in opts if o and o.strip()]
        # correct answer value (string)
        correct_val = q.correct_value()
        # if correct_val not present in opts (possible for old records), insert at start
        if correct_val not in opts:
            opts.insert(0, correct_val or "")
        # shuffle the options but keep track of correct value
        shuffled = opts.copy()
        random.shuffle(shuffled)
        quiz_data.append({
            "id": q.id,
            "question": q.question_text,
            "options": shuffled,
            "correct": correct_val  # we store the correct *value* (not index)
        })
    # shuffle questions order
    random.shuffle(quiz_data)
    return quiz_data

def quiz_view(request):
    # initialize once per session so reshuffle stays stable per attempt
    if "quiz_data" not in request.session or request.GET.get("new") == "1":
        request.session["quiz_data"] = build_quiz_data_from_db()
        # set a small session version to detect corruption
        request.session.modified = True

    quiz_data = request.session.get("quiz_data", [])

    if request.method == "POST":
        score = 0
        results = []
        # iterate using stored quiz_data (guarantees mapping)
        for idx, q in enumerate(quiz_data):
            selected = request.POST.get(f"question_{idx}")
            correct = q.get("correct")
            is_correct = (selected == correct)
            if is_correct:
                score += 1
            results.append({
                "question": q.get("question"),
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct,
                "options": q.get("options"),
            })
        # clear session quiz if you'd like them to re-shuffle next try
        # del request.session["quiz_data"]
        return render(request, "quiz/result.html", {
            "score": score,
            "total": len(quiz_data),
            "results": results,
        })

    return render(request, "quiz/quiz.html", {"questions": quiz_data})

