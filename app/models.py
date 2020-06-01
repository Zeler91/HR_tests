from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

    question = models.TextField()
    answers = models.TextField(default='{}', help_text='use syntax: {"answer content":"answer weight"}. E.g. : {"answer1":"1", "answer2":"2"}')

    def __str__(self):
        return self.question

class Test(models.Model):

    name = models.CharField(max_length=20)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    tests = models.ManyToManyField(Test, blank=True)
    completed_tests = models.TextField(default='', blank=True)
    super_user = models.BooleanField()

    def __str__(self):
        return self.user.username

class Result(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    data = models.TextField(default='{}')

    def __str__(self):
        return f'{self.test} results'

