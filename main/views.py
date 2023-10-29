from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("pub_date")
    context = { "latest_question_list": latest_question_list }
    return render(request, "main/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "main/detail.html", {"question": question})

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)