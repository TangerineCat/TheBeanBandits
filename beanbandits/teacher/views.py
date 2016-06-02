###############################################################################
# Date: June 2015
# Author: Edward Johns (e.johns@imperial.ac.uk)
# This code may be freely distributed, but citations should be made to:
# E. Johns et al, "Becoming the Expert - Interactive Multi-Class Machine
# Teaching", in Proceedings of CVPR 2015
###############################################################################


# Import some Django modules
from django.shortcuts import render, redirect, get_object_or_404
from django.core.management.base import BaseCommand
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic.list import ListView

# Import some standard Python modules
import os
import numpy
import random
from datetime import datetime, time

# Import our eer module (Expected Error Reduction)
import eer
import teach

# Import the User and UserResponse models (which are stored in the SQL database)
from teacher.models import Word, WordSet, Trial, Modes, Question
from django.contrib.auth.models import User
from django.db.models import Max, Min


# Define the teaching and testing lengths
num_teaching_images = 3
num_testing_images = 3
#num_shown = 0
#not_shown = range(10)
teacher = None
#algo = 0


num_classes = 10
teacher = teach.Teach(num_classes, num_teaching_images)

START = 0
TEACH = 1
RESPONSE = 2
ENDTEACH = 3
TESTING = 4
ENDTEST = 5
RANDOM = 0
WSCS = 1
IWSCS = 2
MAB = 3



class WordSetListView(ListView):
    model = WordSet
    template_name = "selection.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WordSetListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return WordSet.objects.all()

    def get_context_data(self, **kwargs):
        context = super(WordSetListView, self).get_context_data(**kwargs)
        self.request.session['n'] = 0
        # randomly choose one algorithm to test user.
        return context


@login_required()
def quiz(request, pk):
    global teacher
    #global algo
    #global num_shown
    #global not_shown
    try:
        num_shown = request.session['num_shown']
    except KeyError:
        num_shown = 0
        request.session['num_shown'] = num_shown
    request.session['wordset_id'] = pk
    if num_shown == 0:
        algo = random.randint(0,3)
        request.session['algo'] = algo
        if algo == RANDOM:
            teacher = teach.Random_Teach(num_classes, num_teaching_images)
        elif algo == WSCS:
            teacher = teach.WSCS_Teach(num_classes, num_teaching_images)
        elif algo == IWSCS:
            teacher = teach.IWSCS_Teach(num_classes, num_teaching_images, 5)
        elif algo == MAB:
            teacher = teach.MAB_Teach(num_classes, num_teaching_images)
        not_shown = range(10)
        request.session['not_shown'] = not_shown
        wordsetid = request.session['wordset_id']
        wordset = WordSet.objects.filter(pk=wordsetid).get()
        mode = Modes(mode = algo)
        mode.save()
        new_trial = Trial(wordset=wordset, mode=mode, user=request.user, score=0)
        new_trial.save()
    if num_shown < num_teaching_images:
        if request.method == 'POST':
            num_shown += 1
            request.session['num_shown'] = num_shown
            return feedback(request, pk)
        else:  # get request
            return teaching(request, pk)
    elif num_shown - num_teaching_images < num_testing_images:
        if request.method == 'POST':
            num_shown += 1
            request.session['num_shown'] = num_shown
            processTestingAnswer(request, pk)
        if num_shown - num_teaching_images < num_testing_images:
            return testing(request, pk)
        else:
            num_shown = 0
            request.session['num_shown'] = num_shown
            return testResults(request)
        


def getNext(n):
    global teacher
    return teacher.get_next_teach_sample()


def teaching(request, pk):
    """
    Shows a teaching example with options
    """
    num_shown = request.session['num_shown']
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)
    next_sample = getNext(len(wordlist))
    try:
        next_word = wordlist[next_sample]
    except TypeError:
        print "TypeError, tried to get" + next_sample
        next_word = wordlist[random.randint(0,9)]

    context = {'next_word': next_word,
               'wordlist': wordlist,
               'teaching_image_num': (num_shown+1),
               'num_teaching_images': num_teaching_images,
    }
    request.session['next_sample'] = next_sample
    request.session['word_id'] = next_word.id
    n = request.session['n']
    request.session['n'] = n + 1

    return render(request, 'teacher/teaching.html', context)


def feedback(request, pk):
    global teacher
    num_shown = request.session['num_shown']
    answer_ = int(request.POST['answer'])
    next_sample = int(request.session['next_sample'])
    word_id = int(request.session['word_id'])
    word = Word.objects.filter(pk=word_id).get()
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)
    teacher.teach_judge(answer_, next_sample)
    is_correct = answer_ == next_sample
    curr_trial = Trial.objects.filter(user = request.user).filter(wordset=wordset).latest('time_started')
    new_question = Question(trial=curr_trial, question_num = num_shown, correct_word=word, correct = is_correct)
    new_question.save()


    context = {'word': word,
               'is_correct': is_correct,
               'wordset': pk}

    return render(request, 'teacher/feedback.html', context)


def testing(request, pk):
    """
    Shows a testing example with options
    """
    num_shown = request.session['num_shown']
    not_shown = request.session['not_shown']
    next_sample = request.session['next_sample']
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)
    while next_sample not in not_shown:
        next_sample = random.randint(0,9)
    not_shown.remove(next_sample)
    next_word = wordlist[next_sample]
    
    context = {'next_word': next_word,
               'wordlist': wordlist,
               'testing_image_num': (num_shown - num_teaching_images + 1),
               'num_testing_images': num_testing_images,
               }
    request.session['next_sample'] = next_sample
    request.session['word_id'] = next_word.id
    request.session['not_shown'] = not_shown
    n = request.session['n']
    request.session['n'] = n + 1

    return render(request, 'teacher/testing.html', context)

def testResults(request):
    # Should show statistics of the quiz
    # Should have a link to try other quizes
    # Get the average score
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    score_sum = 0
    curr_trial = Trial.objects.filter(user=request.user).filter(wordset=wordset).filter(time_finished=None).latest('time_started')
    score = len(Question.objects.filter(trial=curr_trial).filter(correct=True).filter(question_num__gt=num_teaching_images))
    time_finished = datetime.now()
    min_time = Trial.objects.all().aggregate(Min('time_started'))
    curr_trial.time_finished = time_finished
    finished_trials = Trial.objects.filter(wordset=wordset)
    curr_trial.score = score
    curr_trial.save()
    print len(finished_trials)
    for trial in finished_trials:
        score_sum += float(trial.score)
    print(score_sum)

    user = request.user
    user.score = score
    user.is_finished = True

    if len(finished_trials) > 0:
        ave_score = float(score_sum) / len(finished_trials)
    else:
        ave_score = score

    context = {'score': score,
               'num_testing_images': num_testing_images,
               'ave_score': ave_score,
               'origin': "",
               }

    return render(request, 'teacher/testresults.html', context)

def processTestingAnswer(request, pk):

    num_shown = request.session['num_shown']
    answer_ = int(request.POST['answer'])
    next_sample = int(request.session['next_sample'])
    word_id = int(request.session['word_id'])
    word = Word.objects.filter(pk=word_id).get()
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)

    is_correct = answer_ == next_sample
    curr_trial = Trial.objects.filter(user = request.user).filter(wordset=wordset).latest('time_started')
    new_question = Question(trial=curr_trial, question_num = num_shown, correct_word=word, correct = is_correct)
    new_question.save()





##### DEPRECATED #########

def index(request):
    # Has a mode been assigned?
    if 'mode' in request.POST:
        mode = int(request.POST['mode'])
        if mode == TEACH:  # last mode was new user
            processSelection(request)
            request.session['teaching_image_num'] = 0
            return teaching(request)
        elif mode == RESPONSE:  # last mode was teaching
            processTeachingAnswer(request)
            return feedback(request)
        elif mode == ENDTEACH:  # last mode was feedback
            teaching_image_num_ = int(request.session['teaching_image_num'])
            if teaching_image_num_ == num_teaching_images:
                request.session['testing_image_num'] = 1
                context = {'num_testing_images': num_testing_images}
                return render(request, 'teacher/endteaching.html', context)
            else:
                return teaching(request)
        elif mode == TESTING:  # last mode was endTeaching
            request.session['testing_image_num'] = 0
            return testing(request)
        elif mode == ENDTEST:  # last mode was testing
            processTestingAnswer(request)
            testing_image_num_ = int(request.session['testing_image_num'])
            if testing_image_num_ == num_testing_images:
                return testResults(request)
            else:
                return testing(request)
    else:  # No mode, therefore the user has just visited the website
        return render(request, 'teacher/newuser.html')
        request.session.flush()
        return selection(request)


def selection(request):
    context = {'class_names': WordSet.objects.all()}
    return render(request, 'teacher/selection.html', context)


def processSelection(request):
    answer_ = int(request.POST['answer'])
    # # Load the image paths
    characters = Word.objects.filter(wordset=answer_).all()
    # Make the set of testing samples (different for each user)
    request.session['characters'] = characters



def processTeachingAnswer(request):

    user_id_ = int(request.session['user_id'])
    teaching_image_id_ = int(request.session['teaching_image_id'])
    answer_ = int(request.POST['answer'])

    L_ = request.session['L']
    L_.append(teaching_image_id_)
    X_path = '../User-Data/X_' + str(user_id_) + '.npy'
    X_ = numpy.load(X_path)
    X_[teaching_image_id_][:] = 0
    # Always update X with the class answered by the student (rather than
    # necessarily the ground truth)
    X_[teaching_image_id_][answer_] = 1
    numpy.save(X_path, X_)
    request.session['L'] = L_


