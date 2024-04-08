from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from app import models

# Create your views here.





def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(models.QUESTIONS, 7)
    page_obj = paginator.page(page_num)
    
    return render(request, "index.html", {"questions": page_obj, "num_pages": paginator.num_pages})

def hot(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(models.QUESTIONS[5:], 7)
    page_obj = paginator.page(page_num)
    return render(request, "hot.html", {"questions": page_obj, "num_pages": paginator.num_pages})

def question(request, question_id):
    item = models.QUESTIONS[question_id]
    return render(request, "question_detail.html", {"question": item})