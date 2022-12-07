import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    last_name = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    photo = models.ImageField(max_length=254, verbose_name='Фотография', blank=False,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.first_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    description = models.TextField(max_length=500, blank=False)
    description_small = models.CharField(max_length=200, blank=False)
    photo = models.ImageField(max_length=254, verbose_name='Фотография', blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])])
    vote = models.IntegerField(default=0, blank=True)
    user_vote = models.ManyToManyField(User, related_name='user_vote', blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percent(self):
        return self.votes*100/self.question.vote

    def __str__(self):
        return self.choice_text
