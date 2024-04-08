from django.db import models

# Create your models here.
USER = [
    {
        'id': id,
        'avatar': f'img/avatar{id}.png',
        'name': f'User{id}',
        'rating': 100 * id
    } for id in range(33)
]

ANSWERS = [
    {
        'id': id,
        'user': USER[id],
        'rating': 100 - id,
        'text': f'Ответ на вопрос с номером -{id}',
        'right_flag': False,
        'time_ago': f"{id} minutes ago"
    } for id in range(30)
]

TAGS = [
    {
        'id': id,
        'name': f'Tag {id}',
    } for id in range(12)
]

QUESTIONS = [
    {
        'id': id,
        'user': USER[id],
        'title': f'Question {id}',
        'text': f'This is question number {id}',
        'rating': 10 * id, 
        "answers_amount": id + 1,
        'answers': ANSWERS[id:(id+7):1],
        'tags': TAGS[id % 8:id % 8 + 3],
        'time_ago': f'{id} minutes ago'
    } for id in range(30)
]






