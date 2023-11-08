from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("sign-up", views.sign_up, name="sign_up"),
    path("create-question", views.create_question, name="create_question"),
]