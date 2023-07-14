from urllib import request
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.template import loader
from .models import Question
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})


def choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "GET":
        return render(request, "polls/choice.html", {"question": question})
    elif request.method == "POST":
        user_submitted_choice = request.POST["choice"]
        if not user_submitted_choice:
            return render(
                request,
                "polls/choice.html",
                {"question": question, "error_message": "Please enter a valid choice"},
            )

        new_choice = Choice(
            question=question,
            choice_text=user_submitted_choice,
        )
        new_choice.save()
        return HttpResponseRedirect(reverse("polls:detail", args=(question.id,)))


def vote_reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    for choice in question.choice_set.all():
        choice.votes = 0
        choice.save()

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def Reset(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    for choice in question.choice_set.all():
        choice.vote = 0
        choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


def add_question(request):
    if request.method == "GET":
        return render(request, "polls/new_question.html", {})
    elif request.method == "POST":
        user_submitted_question = request.POST["question"]
        if not user_submitted_question:
            return render(
                request,
                "polls/new_question.html",
                {"error_message": "Please enter a valid question"},
            )

        new_question = Question(
            question_text=user_submitted_question,
            pub_date=timezone.now(),
        )
        new_question.save()
    return HttpResponseRedirect(
        reverse(
            "polls:index",
        )
    )
