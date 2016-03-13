from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import authenticate, login

from .models import Question, Answer
from .utils import paginate
from .forms import AskForm, AnswerForm, UserCreationForm


def test(request, *args, **kwargs):
    return HttpResponse("OK")


@require_GET
def index(request):
    paginator, page = paginate(request, Question.objects.order_by('-added_at'))
    return render(request, 'qa/index.html', {
        'page': page,
        'paginator': paginator,
    })


@require_GET
def question(request, id):
    question = get_object_or_404(Question, id=id)
    answers = question.answer_set.all()
    answer_form = AnswerForm({"question": question.id})
    return render(request, 'qa/question.html', {
        'question': question,
        'answers': answers,
        'form': answer_form
    })

@require_POST
def answer(request):
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.author = request.user
        answer.save()
        return redirect(answer.question)


@require_GET
def popular(request):
    paginator, page = paginate(request, Question.objects.order_by('-rating'))
    return render(request, 'qa/index.html', {
        'page': page,
        'paginator': paginator
    })


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect(question)
    else:
        form = AskForm()
    return render(request, 'qa/ask.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, 'qa/signup.html', {'form': form})


def my_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, 'qa/login.html')
