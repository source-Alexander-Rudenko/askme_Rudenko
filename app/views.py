from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from app import models
from django.http import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

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
        # Handle empty page, return last page
        page_obj = paginator.page(paginator.num_pages)
    if int(page_number) > paginator.num_pages:
        raise Http404("Page does not exist")

    return page_obj

def index(request):
    questions = models.Question.objects.order_by('-created_at')  # Получение всех объектов Question
    page_obj = paginate(questions, request, 7)
    context = {
        'page_obj': page_obj,
        'tags': models.Tag.objects.all(),  # Получение всех объектов Tag
        'users': models.Profile.objects.all(),  # Получение всех объектов Profile
    }
    sidebar_content(context)
    return render(request, 'index.html', context)

def sidebar_content(context):
    context['top_tags'] = models.Tag.objects.get_top5()
    context['top_users'] = models.Profile.objects.get_top_5()

def tag(request, tag_name):
    try:
        tag = models.Tag.objects.get(name=tag_name)
        questions = models.Question.objects.filter(tags=tag)
        page_obj = paginate(questions, request, 7)
        
        context = {
            'page_obj': page_obj,
            'tag': tag,
            'tags': models.Tag.objects.all(),  # Получение всех объектов Tag
            'users': models.Profile.objects.all(),  # Получение всех объектов Profile
        }
        sidebar_content(context)
        return render(request, 'tag.html', context)
    except models.Tag.DoesNotExist:
        raise Http404("Tag does not exist")


def tag_view(request, tag_name):
    tag = models.Tag.objects.get(name=tag_name)
    questions = models.Question.objects.filter(tags=tag)
    page_obj = paginate(questions, request, 7)
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    sidebar_content(context)  # Обновление контекста с топ 5 тегов и пользователей
    return render(request, 'tag_detail.html', context)



def question(request, question_id: int):
    try:
        question = models.Question.objects.get(pk=question_id)  # Получение конкретного вопроса
        answers = models.Answer.objects.filter(question=question)  # Получение всех ответов на вопрос
        page_obj = paginate(answers, request, 3)

        context = {
            'page_obj': page_obj,
            'question': question,
            'tags': models.Tag.objects.all(),  # Получение всех объектов Tag
            'users': models.Profile.objects.all(),  # Получение всех объектов Profile
            'answers': answers,
        }
        sidebar_content(context)
    except models.Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'question_detail.html', context)

        

def hot(request):
    questions = models.Question.objects.order_by('-rating') # Получение всех объектов Question
    page_obj = paginate(questions, request, 7)
    context = {
        'page_obj': page_obj,
        'tags': models.Tag.objects.all(),  # Получение всех объектов Tag
        'users': models.Profile.objects.all(),  # Получение всех объектов Profile
    }
    sidebar_content(context)
    return render(request, 'hot.html', context)

def loging(request):
    return render(request, 'loging.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')

def ask(request):
    return render(request, 'ask.html')