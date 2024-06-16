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
    questions = models.Question
    page_obj = paginate(questions, request, 7)
    context = {'page_obj': page_obj,
               'questions': models.Question,
               'tags': models.Tag,
               'users': models.Profile,
               }
    return render(request, 'index.html', context)



def question(request, question_id: int):
    try:
        questions = models.Question
        answers = models.Answer
        page_obj = paginate(answers, request, 3)
        question = questions[question_id]

        context = {
                    'page_obj': page_obj,
                    'question': question,
                    'tags': models.Tag,
                    'users': models.Profile,
                    'answers': answers,
                    }
    except:
        raise Http404("Question does not exist")
    
    return render(request, 'question_detail.html', context)
        

def hot(request):
    try:   
        questions = models.Question[5:]
        page_obj = paginate(questions, request, 6)
        context = {'page_obj': page_obj,
                'questions': models.Question,
                'tags': models.Tag,
                'users': models.Profile,
                }
        return render(request, 'hot.html', context)
    except:
        raise Http404("Page does not exist")

def loging(request):
    return render(request, 'loging.html')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')

def ask(request):
    return render(request, 'ask.html')