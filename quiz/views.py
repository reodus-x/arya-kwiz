# quiz/views.py
from django.shortcuts import render
from .models import Question
import random

def build_quiz_data_from_db():
    quiz_data = []
    questions = list(Question.objects.all())
    random.shuffle(questions)  # shuffle questions first

    for q in questions:
        # Gather only non-empty options
        opts = [q.option_a, q.option_b, q.option_c, q.option_d]
        opts = [o for o in opts if o and o.strip()]

        # Get the correct answer text
        correct_val = q.correct_value()

        # Ensure the correct answer is in the list
        if correct_val not in opts:
            opts.append(correct_val)

        # Shuffle the options
        shuffled_opts = opts.copy()
        random.shuffle(shuffled_opts)

        # Build structured quiz data
        quiz_data.append({
            "id": q.id,
            "question": q.question_text,
            "options": shuffled_opts,
            "correct": correct_val,  # Store the correct *value*
        })

    return quiz_data


def quiz_view(request):
    # New quiz or reshuffle request
    if "quiz_data" not in request.session or request.GET.get("new") == "1":
        request.session["quiz_data"] = build_quiz_data_from_db()
        request.session.modified = True

    quiz_data = request.session.get("quiz_data", [])

    if request.method == "POST":
        score = 0
        results = []

        for idx, q in enumerate(quiz_data):
            selected = request.POST.get(f"question_{idx}")
            correct = q.get("correct")

            is_correct = (selected == correct)
            if is_correct:
                score += 1

            results.append({
                "question": q.get("question"),
                "options": q.get("options"),
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct,
            })

        # clear quiz_data to reshuffle on next try
        if "quiz_data" in request.session:
            del request.session["quiz_data"]

        return render(request, "quiz/result.html", {
            "score": score,
            "total": len(quiz_data),
            "results": results,
        })

    return render(request, "quiz/quiz.html", {"questions": quiz_data})

