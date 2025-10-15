from django.shortcuts import render
from .models import Question
import random

def build_quiz_data_from_db():
    quiz_data = []
    for q in Question.objects.all():
        opts = [q.option_a, q.option_b, q.option_c, q.option_d]
        opts = [o.strip() for o in opts if o and o.strip()]
        correct_val = q.correct_value().strip() if q.correct_value() else ""

        if correct_val and correct_val not in opts:
            opts.append(correct_val)

        random.shuffle(opts)

        quiz_data.append({
            "id": q.id,
            "question": q.question_text,
            "options": opts,
            "correct": correct_val,
        })

    random.shuffle(quiz_data)
    return quiz_data

def quiz_view(request):
    # Reset quiz only if user explicitly clicks "Try Again"
    if request.GET.get("new") == "1":
        request.session.pop("quiz_data", None)

    # Build quiz only once per session
    if "quiz_data" not in request.session:
        request.session["quiz_data"] = build_quiz_data_from_db()
        request.session.modified = True

    quiz_data = request.session["quiz_data"]

    # Handle submission
    if request.method == "POST":
        score = 0
        results = []

        for q in quiz_data:
            selected = request.POST.get(f"question_{q['id']}")
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

        # Delete quiz data AFTER rendering results
        response = render(request, "quiz/result.html", {
            "score": score,
            "total": len(quiz_data),
            "results": results,
        })
        del request.session["quiz_data"]
        return response

    return render(request, "quiz/quiz.html", {"questions": quiz_data})

