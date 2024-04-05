from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.


QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(15)
]

def index(request):
    return render(request, "index.html",{"questions": QUESTIONS})


def hot(request):
    return render(request, "hot.html",{"questions": QUESTIONS})