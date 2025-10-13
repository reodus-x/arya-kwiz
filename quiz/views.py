from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import random

# --- 1️⃣ Quiz Questions Stored as a List of Dictionaries ---
QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "What is 5 × 6?",
        "options": ["30", "11", "56", "26"],
        "answer": "30"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Picasso", "Da Vinci", "Van Gogh", "Rembrandt"],
        "answer": "Da Vinci"
    },
]

# --- 2️⃣ Home Page: Show Randomized MCQ Questions ---
def home(request):
    if request.method == "POST":
        score = 0
        results = []
        for i, q in enumerate(QUESTIONS):
            selected = request.POST.get(f"q{i}")
            correct = (selected == q["answer"])
            if correct:
                score += 1
            results.append({
                "question": q["question"],
                "selected": selected,
                "correct_answer": q["answer"],
                "is_correct": correct
            })
        return render(request, "quiz/result.html", {
            "score": score,
            "total": len(QUESTIONS),
            "results": results
        })
    else:
        shuffled_questions = random.sample(QUESTIONS, len(QUESTIONS))
        for q in shuffled_questions:
            q["options"] = random.sample(q["options"], len(q["options"]))
        return render(request, "quiz/home.html", {"questions": shuffled_questions})


# --- 3️⃣ Contact Us Page ---
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"Contact from {name}",
            message=f"Email: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["argon@reodus.dev"],
        )
        return render(request, "quiz/contact.html", {"sent": True})
    return render(request, "quiz/contact.html")

