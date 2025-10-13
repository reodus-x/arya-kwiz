from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_view, name="quiz"),
    path("contact/", views.contact, name="contact"),
]

