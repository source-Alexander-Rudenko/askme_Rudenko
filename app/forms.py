from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import hashers
from . import models
from .models import Profile



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

## forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    check_password = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')
    avatar = forms.ImageField(required=False, label='Avatar')

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get('password')
        password_2 = cleaned_data.get('check_password')

        if password_1 and password_1 != password_2:
            raise ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile = Profile(user=user)
            profile.save()
        return user




class ProfileEditForm(forms.ModelForm):
    upload_avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_username = user.username
        self.initial["username"] = user.username
        self.initial["email"] = user.email
        self.initial["first_name"] = user.first_name
        self.initial["last_name"] = user.last_name

    def clean(self):
        username = self.cleaned_data.get('username')

        if models.Profile.objects.get_user_by_username(username) and self.user_username != username:
            self.add_error('username', IntegrityError("User already exists"))

        return self.cleaned_data

    def save(self):
        user = User.objects.get(username=self.user_username)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save()
        profile = user.profile
        avatar = self.cleaned_data["upload_avatar"]
        print(avatar)
        if avatar is not None:
            if not avatar:
                avatar = models.Profile.avatar.field.default
            profile.avatar = avatar
            profile.save()
        return user


# forms.py
class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=150)

    class Meta:
        model = models.Question
        fields = ["title", "text"]  # Изменено на "text" вместо "content"

    def clean_tags(self):
        tags_list = self.cleaned_data["tags"].split(",")
        for tag in tags_list:
            if len(tag.strip()) > 20:
                raise forms.ValidationError("Exceeded the maximum tag length (20 characters)")
        return self.cleaned_data["tags"]

    def save(self, user: User) -> int:
        tags_list = self.cleaned_data["tags"].split(",")
        exists_tags = []
        new_tags = []
        for tag in tags_list:
            tag_title = tag.strip()
            try:
                exists_tags.append(models.Tag.objects.get(name=tag_title))
            except ObjectDoesNotExist:
                new_tags.append(models.Tag(name=tag_title))
        models.Tag.objects.bulk_create(new_tags)
        question = models.Question(title=self.cleaned_data["title"], text=self.cleaned_data["text"], author=user.profile)
        question.save()
        question.tags.set(new_tags + exists_tags)
        return question.id



class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Answer'

    def save(self, user: User, question: models.Question) -> int:
        answer = models.Answer(content=self.cleaned_data['content'], question=question, author=user.profile)
        answer.save()
        return answer.id