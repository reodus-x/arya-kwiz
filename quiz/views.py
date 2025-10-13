from django.shortcuts import render
import random

QUESTIONS = [
    {
        "question": "What is the capital of Japan?",
        "options": ["Seoul", "Beijing", "Tokyo", "Kyoto"],
        "answer": "Tokyo",
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Oxygen", "Gold", "Osmium", "Oganesson"],
        "answer": "Oxygen",
    },
    {
        "question": "Who created Python programming language?",
        "options": ["Elon Musk", "Guido van Rossum", "Bill Gates", "James Gosling"],
        "answer": "Guido van Rossum",
    },
    {
        "question": "What year did World War II end?",
        "options": ["1945", "1939", "1918", "1963"],
        "answer": "1945",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": "Mars",
    },
]

def quiz_view(request):
    # Always reshuffle questions and options
    shuffled_questions = []
    for q in QUESTIONS:
        opts = q["options"].copy()
        random.shuffle(opts)
        shuffled_questions.append({
            "question": q["question"],
            "options": opts,
            "answer": q["answer"]
        })
    random.shuffle(shuffled_questions)

    if request.method == "POST":
        score = 0
        results = []
        for idx, q in enumerate(shuffled_questions):
            selected = request.POST.get(f"question_{idx+1}")
            correct = q["answer"]
            is_correct = selected == correct
            if is_correct:
                score += 1
            results.append({
                "question": q["question"],
                "selected": selected,
                "correct": correct,
                "is_correct": is_correct,
            })
        return render(request, "quiz/result.html", {
            "score": score,
            "total": len(shuffled_questions),
            "results": results,
        })

    return render(request, "quiz/quiz.html", {"questions": shuffled_questions})

# ----------------------------
# Contact Us Page
# ----------------------------
from django.shortcuts import render

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # (Optional) print in console to verify form submissions
        print(f"📩 Contact form received from {name} ({email}): {message}")

        return render(request, "quiz/contact.html", {"success": True})

    return render(request, "quiz/contact.html")

