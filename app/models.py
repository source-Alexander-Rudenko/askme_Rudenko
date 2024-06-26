from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.db.models import F

class ProfileManager(models.Manager):
    def get_top_5(self):
        return self.order_by('-rating')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='static/img/avatar', blank=True, null=True)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)

    objects = ProfileManager()
    def __str__(self):
        return f'({self.id}) {self.user.username}'
    class Meta:
        app_label = 'app'

class AnswerManager(models.Manager):
    def get_by_question(self, current_question):
        return self.filter(question=current_question)

class Answer(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    rating = models.IntegerField(default=0)
    right = models.BooleanField(null=True)
    objects = AnswerManager()

    def __str__(self):
        return f'({self.id}) {self.author.user.username} commented question {self.question.title}'

class TagManager(models.Manager):
    def get_top5(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:5]

    def get_by_question(self, question):
        return self.filter(questions=question)

    def get_by_title(self, current_title):
        return self.filter(title=current_title)[0]

class Tag(models.Model):
    name = models.CharField(max_length=50)
    objects = TagManager()

    def __str__(self):
        return f'({self.id}) {self.title}'


class Like(models.Model):
    from_user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes')
    to_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')
    def __str__(self):
        return f'({self.id}) {self.from_user.user.username} like question {self.to_question.title}'

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-create_date')

    def hot_questions(self):
        return self.order_by('-rating')

    def tag_questions(self, tag):
        return self.filter(tags=tag).order_by('-rating')

    def get_question(self, qid):
        try:
            q = self.get(pk=qid)
        except:
            return None
        return q
    
class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=50) 
    text = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')

    objects = QuestionManager()

    def __str__(self):
        return f'({self.id}) {self.author.user.username}: {self.title}'
