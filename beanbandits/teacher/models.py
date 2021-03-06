from django.db import models

# import datetime
# import ast
from django.contrib.auth.models import User

class WordSet(models.Model):
    """
    Description: List of model sets.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/wordsets', null=True)

    def __unicode__(self):
        return '%s' % (self.name)


class Word(models.Model):
    """
    Description: One quiz set.
    """
    word = models.CharField(max_length=10)
    definition = models.CharField(max_length=255)
    pinyin = models.CharField(max_length=40)
    rank = models.PositiveIntegerField()
    wordset = models.ForeignKey(WordSet, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % (self.word)


class Modes(models.Model):
    RANDOM = 0
    WSCS = 1
    IWSCS = 2
    MAB = 3
    MODE_CHOICES = (
        (RANDOM, "Random"),
        (WSCS, "Wrong Stay Correct Shift"),
        (IWSCS, "Improved Wrong Stay Correct Shift"),
        (MAB, "Multi-armed Bandit"),
    )
    mode = models.PositiveIntegerField(primary_key=True, choices=MODE_CHOICES)


class Trial(models.Model):
    """
    Description: Model Description
    """
    wordset = models.ForeignKey(WordSet)
    mode = models.ForeignKey(Modes)
    user = models.ForeignKey(User)
    time_started = models.DateTimeField(auto_now_add=True)
    time_finished = models.DateTimeField(null=True)
    score = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.user) + ' on ' + str(self.wordset)

class Question(models.Model):
    trial = models.ForeignKey(Trial)
    question_num = models.PositiveIntegerField()
    correct_word = models.ForeignKey(Word)
    correct = models.NullBooleanField(null=True)
    choice = models.PositiveIntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True)
