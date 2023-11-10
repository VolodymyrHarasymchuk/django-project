from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.forms import modelformset_factory
from .models import Question, Choice
from .forms import QuestionForm, ChoiceForm

def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).exclude(choice__isnull=True).order_by("pub_date")
    context = { "latest_question_list": latest_question_list }
    return render(request, "main/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "main/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "main/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "main/detail.html",
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
        return HttpResponseRedirect(reverse("main:results", args=(question.id,)))
    
def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form = UserCreationForm()
    
    return render(request, "registration/sign_up.html", {"form": form})

def create_question(request):
    if request.method == "POST":
        form_q = QuestionForm(request.POST)
        ChoiceFormSet = modelformset_factory(Choice, fields=['choice_text'], form=ChoiceForm, extra=3)
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if form_q.is_valid() and choice_formset.is_valid():
            question = form_q.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            
            for choice_form in choice_formset:
                choice = choice_form.save(commit=False)
                if choice.choice_text == "":
                    continue
                choice.question = question
                choice.votes = 0
                choice.save()
            
            return HttpResponseRedirect(reverse("main:index"))
    else:
        form_q = QuestionForm()
        ChoiceFormSet = modelformset_factory(Choice, fields=['choice_text'], form=ChoiceForm, extra=3)
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none())
    return render(request, "main/create_question.html", {"form_q": form_q, "choice_formset": choice_formset})