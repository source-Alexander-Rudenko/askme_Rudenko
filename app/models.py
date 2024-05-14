from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
    def get_top_5(self):
        return self.order_by('-rating')[:5]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='static/img/avatar', blank=True, null=True)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)

    objects = ProfileManager()

class Answer(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    rating = models.IntegerField(default=0)
    right = models.BooleanField(null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Like(models.Model):
    from_user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='likes')
    to_question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')

class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=50) 
    text = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')
