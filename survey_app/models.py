from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

class Option(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)

class Response(models.Model):
    option = models.ForeignKey(Option, related_name='responses', on_delete=models.CASCADE)

