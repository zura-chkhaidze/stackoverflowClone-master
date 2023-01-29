from django.db import models
from django.shortcuts import reverse

from users.models import User


# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # one to many

    title = models.CharField(max_length=120)
    text = models.TextField()
    views = models.PositiveBigIntegerField(default=0, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('forum:question-detail', kwargs={'pk': self.pk})


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    def get_absolute_url(self):
        return reverse('forum:question-detail', kwargs={'pk': self.pk})



class Tag(models.Model):
    name = models.CharField(max_length=120)
    questions = models.ManyToManyField(Question, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
   

