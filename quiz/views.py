from django.shortcuts import render
from .models import Question
import random

def build_quiz_data_from_db():
    quiz_data = []
    questions = list(Question.objects.all())
    random.shuffle(questions)  # randomize question order

    for q in questions:
        # collect non-empty options
        options = [q.option_a, q.option_b, q.option_c, q.option_d]
        options = [opt.strip() for opt in options if opt and opt.strip()]

        # identify correct answer text
        correct_val = q.correct_value()

        # ensure correct answer exists in options
        if correct_val and correct_val not in options:
            options.append(correct_val)

        # shuffle options while keeping correct_val reference
        random.shuffle(options)

        quiz_data.append({
            "id": q.id,
            "question": q.question_text.strip(),
            "options": options,
            "correct": correct_val.strip() if correct_val else "",
        })
    return quiz_data


def quiz_view(request):
    # rebuild quiz on first load or reshuffle request
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

            # compare as strings (avoid type mismatch)
            is_correct = (str(selected).strip() == str(correct).strip())
            if is_correct:
                score += 1

            results.append({
                "question": q.get("question"),
                "options": q.get("options"),
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct,
            })

        # clear quiz for next reshuffle
        if "quiz_data" in request.session:
            del request.session["quiz_data"]

        return render(request, "quiz/result.html", {
            "score": score,
            "total": len(quiz_data),
            "results": results,
        })

    return render(request, "quiz/quiz.html", {"questions": quiz_data})

