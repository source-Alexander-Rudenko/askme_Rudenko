from . import models
from django.contrib.auth.decorators import login_required
from django.db.models.fields import json
import json
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.http import *
from django.http import Http404
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST
from . import models
from .forms import *
from .forms import RegistrationForm
from .forms import LoginForm
from django.contrib import auth
from django.shortcuts import render, reverse
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import logout as auth_logout




def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')

    if page_number is None:
        page_number = 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        raise Http404("Page number is not an integer")
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    if int(page_number) > paginator.num_pages:
        raise Http404("Page does not exist")

    return page_obj

def sidebar_content(context):
    context['top_tags'] = models.Tag.objects.get_top5()
    context['top_users'] = models.Profile.objects.get_top_5()

def get_context_and_render(request, queryset, template_name, extra_context=None, per_page=7):
    page_obj = paginate(queryset, request, per_page)
    context = {
        'page_obj': page_obj,
        'tags': models.Tag.objects.all(),
        'users': models.Profile.objects.all(),
    }
    if extra_context:
        context.update(extra_context)
    sidebar_content(context)
    return render(request, template_name, context)

def index(request):
    questions = models.Question.objects.order_by('-created_at')
    return get_context_and_render(request, questions, 'index.html')

def hot(request):
    questions = models.Question.objects.order_by('-rating')
    return get_context_and_render(request, questions, 'hot.html')

def tag(request, tag_name):
    try:
        tag = models.Tag.objects.get(name=tag_name)
        questions = models.Question.objects.filter(tags=tag)
        extra_context = {'tag': tag}
        return get_context_and_render(request, questions, 'tag.html', extra_context)
    except models.Tag.DoesNotExist:
        raise Http404("Tag does not exist")

def question(request, question_id):
    question = models.Question.objects.get_question(question_id)
    if question == None:
        raise Http404("Question does not exist")
    answers = models.Answer.objects.get_by_question(question_id)
    page_obj = paginate(answers, request, 3)
    context = {'question': question, 'page_obj':page_obj}
    sidebar_content(context)
    if request.method == "GET":
        answer_form = AnswerForm()
    elif request.method == "POST":
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse("loging"))
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_id = answer_form.save(request.user, question)
            answers_cnt = question.answers.count()
            num_page = (answers_cnt // 10) + 1
            return HttpResponseRedirect(reverse("question", args=[question_id]) + f"?page=1#answer-{answer_id}")
    context['form'] = answer_form
    return render(request, "question_detail.html", context)



@csrf_protect
def login_view(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                continue_url = request.GET.get("continue")
                if continue_url is None or continue_url[0] != "/":
                    continue_url = "/"
                return HttpResponseRedirect(continue_url)
            else:
                login_form.add_error(field=None, error="Wrong username or/and password")
    context['form'] = login_form
    return render(request, "loging.html", context)

    



@csrf_protect
@login_required(login_url="login")
def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


# views.py
@csrf_protect
def signup(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    elif request.method == 'POST':
        user_form = RegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            user = auth.authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect("/")
        else:
            messages.error(request, "There was an error with your registration. Please check your details and try again.")
    context = {'form': user_form}
    sidebar_content(context)
    return render(request, 'signup.html', context=context)

@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        ask_form = QuestionForm()
    elif request.method == 'POST':
        ask_form = QuestionForm(request.POST)
        if ask_form.is_valid():
            question_id = ask_form.save(request.user)
            return HttpResponseRedirect(reverse("question", args=[question_id]))
    context['form'] = ask_form
    return render(request, 'ask.html', context)

def settings(request):
    return render(request, 'settings.html')