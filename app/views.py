from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from app import models
from django.http import *
from django.http import Http404

# Create your views here.
def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    try:
        limit = int(request.GET.get('page', 10))
    except ValueError:
        limit = 10
    if limit > 10:
        limit = 10
    try:
        page_number  = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    return paginator.get_page(page_number)

def index(request):
    questions = models.QUESTIONS
    page_obj = paginate(questions, request, 7)
    context = {'page_obj': page_obj,
               'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER,
               }
    return render(request, 'index.html', context)

def question(request, question_id: int):
    try:
        questions = models.QUESTIONS
        answers = models.ANSWERS
        page_obj = paginate(answers, request, 5)
        question = questions[question_id]

        context = {
                    'page_obj': page_obj,
                    'question': question,
                    'tags': models.TAGS,
                    'users': models.USER,
                    'answers': answers,
                    }
    except:
        raise Http404("Question does not exist")
    
    return render(request, 'question_detail.html', context)
        

def hot(request):
    questions = models.QUESTIONS[5:]
    page_obj = paginate(questions, request, 6)
    context = {'page_obj': page_obj,
               'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER,
               }
    return render(request, 'hot.html', context)

