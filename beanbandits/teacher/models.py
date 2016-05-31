from django.db import models

import datetime
import ast


class User(models.Model):

    # Member variables for User
    user_id = models.IntegerField(default=-1)
    score = models.IntegerField(default=-1)
    is_finished = models.BooleanField(default=False)

    # Function to construct a User
    @classmethod
    def create(cls, user_id_):
        user = cls(user_id=user_id_)
        return user


class UserResponse(models.Model):

    # Member variables for UserResponse
    user_id = models.IntegerField(default=-1)
    is_correct = models.BooleanField(default=False)

    # Function to construct a UserResponse
    @classmethod
    def create(cls, user_id_, is_correct_):
        user_response = cls(user_id=user_id_, is_correct=is_correct_)
        return user_response


class WordSet(models.Model):
    """
    Description: List of model sets.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()


class Word(models.Model):
    """
    Description: One quiz set.
    """
    word = models.CharField(max_length=10)
    definition = models.CharField(max_length=255)
    pinyin = models.CharField(max_length=40)
    rank = models.PositiveIntegerField()
    wordset = models.ForeignKey(WordSet, on_delete=models.CASCADE)


class Modes(models.Model):
    RANDOM = 0
    LEASTUSED = 1
    BEANBANDIT = 2
    MODE_CHOICES = (
        (RANDOM, "Random"),
        (LEASTUSED, "Least used"),
        (BEANBANDIT, "Bean Bandit"),
    )
    mode = models.PositiveIntegerField(primary_key=True, choices=MODE_CHOICES)


class Exercise(models.Model):
    """
    Description: Model Description
    """
    wordset = models.ForeignKey(WordSet)
    mode = models.ForeignKey(Modes)
