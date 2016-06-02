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

# Import our eer module (Expected Error Reduction)
import eer

# Import the User and UserResponse models (which are stored in the SQL database)
from teacher.models import Word, WordSet


# Define the teaching and testing lengths
num_teaching_images = 3
num_testing_images = 1
num_shown = 0


num_classes = 10

START = 0
TEACH = 1
RESPONSE = 2
ENDTEACH = 3
TESTING = 4
ENDTEST = 5


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
        # TODO: randomly choose one algorithm to test user.
        return context


@login_required()
def quiz(request, pk):
    #TODO: (jleong) add in logic for when it's time to test instead
    global num_shown
    request.session['wordset_id'] = pk
    if num_shown < num_teaching_images:
        if request.method == 'POST':
            return feedback(request, pk)
        else:  # get request
            num_shown += 1
            return teaching(request, pk)
    elif num_shown - num_teaching_images < num_testing_images:
        num_shown += 1
        return testing(request, pk)
    else:
        return testResults(request)
        


def getNext(n):
    return random.randint(0, n - 1)


def teaching(request, pk):
    """
    Shows a teaching example with options
    """
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)
    next_sample = getNext(len(wordlist))
    next_word = wordlist[next_sample]

    context = {'next_word': next_word,
               'wordlist': wordlist,
               }
    request.session['next_sample'] = next_sample
    request.session['word_id'] = next_word.id
    n = request.session['n']
    request.session['n'] = n + 1

    return render(request, 'teacher/teaching.html', context)


def feedback(request, pk):
    answer_ = int(request.POST['answer'])
    next_sample = int(request.session['next_sample'])
    word_id = int(request.session['word_id'])
    word = Word.objects.filter(pk=word_id).get()

    is_correct = answer_ == next_sample

    context = {'word': word,
               'is_correct': is_correct,
               'wordset': pk}

    return render(request, 'teacher/feedback.html', context)


def testing(request, pk):
    """
    Shows a teaching example with options
    """
    wordsetid = request.session['wordset_id']
    wordset = WordSet.objects.filter(pk=wordsetid).get()
    wordlist = Word.objects.filter(wordset=wordset)
    next_sample = getNext(len(wordlist))
    next_word = wordlist[next_sample]

    context = {'next_word': next_word,
               'wordlist': wordlist,
               }
    request.session['next_sample'] = next_sample
    request.session['word_id'] = next_word.id
    n = request.session['n']
    request.session['n'] = n + 1

    return render(request, 'teacher/teaching.html', context)

def testResults(request):
    # TODO: Implement this view.
    # Should show statistics of the quiz
    # Should have a link to try other quizes

    # Get the average score
    score_sum = 0
    finished_users = User.objects.filter(is_finished=True)
    for u in finished_users:
        finished_correct_responses = UserResponse.objects.filter(
            user_id=u.user_id).filter(is_correct=True)
        score_sum += len(finished_correct_responses)

    user_id_ = request.session['user_id']

    correct_responses = UserResponse.objects.filter(
        user_id=user_id_).filter(is_correct=True)
    score = len(correct_responses)

    user = User.objects.get(user_id=user_id_)
    user.score = score
    user.is_finished = True
    user.save()

    if len(finished_users) > 0:
        ave_score = float(score_sum) / len(finished_users)
    else:
        ave_score = score

    context = {'score': score,
               'num_testing_images': num_testing_images,
               'ave_score': ave_score}

    return render(request, 'teacher/testresults.html', context)



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


def processTestingAnswer(request):

    user_id_ = int(request.session['user_id'])
    testing_class_id_ = int(request.session['testing_class_id'])
    answer_ = int(request.POST['answer'])

    is_correct = True if testing_class_id_ == answer_ else False

    user_response = UserResponse.create(user_id_, is_correct)
    user_response.save()


