from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/choice/", views.choice, name="choice"),
    path("<int:question_id>/vote_reset/", views.vote_reset, name="vote_reset"),
    path("new/", views.add_question, name="new"),
    path("<int:question_id>/Delete_record/", views.Delete_record, name="Delete_record"),
    path("home/", views.home, name="home"),
]
