from django.urls import path
from . import views

urlpatterns = [
    path("", views.quiz_view, name="quiz"),
   # path("result/", views.result_view, name="result"),  # maybe
   # path("contact/", views.contact, name="contact"),
]


