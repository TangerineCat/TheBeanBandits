###################################################################################################################
# Date: June 2015
# Author: Edward Johns (e.johns@imperial.ac.uk)
# This code may be freely distributed, but citations should be made to:
# E. Johns et al, "Becoming the Expert - Interactive Multi-Class Machine Teaching", in Proceedings of CVPR 2015
###################################################################################################################



# Import some Django modules
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.management.base import BaseCommand

# Import some standard Python modules
import os
import numpy
import random

# Import our eer module (Expected Error Reduction)
import eer

# Import the User and UserResponse models (which are stored in the SQL database)
from teacher.models import User, UserResponse, Word, WordSet


# Set the name of the dataset
dataset_name = 'chinese'
# Define the teaching and testing lengths
num_teaching_images = 3
num_testing_images = 1



num_classes = 10 

START = 0
TEACH = 1
RESPONSE = 2
ENDTEACH = 3
TESTING = 4
ENDTEST = 5

def index(request):
    # Has a mode been assigned?
    if 'mode' in request.POST:
        mode = int(request.POST['mode'])
        if mode == START:
            request.session.flush()
            return selection(request)
        elif mode == TEACH: # last mode was new user
            processSelection(request)
            request.session['teaching_image_num'] = 0
            return teaching(request)
        elif mode == RESPONSE: # last mode was teaching
            processTeachingAnswer(request)
            return feedback(request)
        elif mode == ENDTEACH: # last mode was feedback
            teaching_image_num_ = int(request.session['teaching_image_num'])
            if teaching_image_num_ == num_teaching_images:
                request.session['testing_image_num'] = 1
                context = {'num_testing_images': num_testing_images}
                return render(request, 'teacher/endteaching.html', context)
            else:
                return teaching(request)
        elif mode == TESTING: # last mode was endTeaching
            request.session['testing_image_num'] = 0
            return testing(request)
        elif mode == ENDTEST: # last mode was testing
            processTestingAnswer(request)
            testing_image_num_ = int(request.session['testing_image_num'])
            if testing_image_num_ == num_testing_images:
                return testResults(request)
            else:
                return testing(request)
    else: # No mode, therefore the user has just visited the website
        return render(request, 'teacher/newuser.html')



def selection(request):
    context = {'class_names': WordSet.objects.all()}
    return render(request, 'teacher/selection.html', context)

def processSelection(request):
    answer_ = int(request.POST['answer'])
    # # Load the image paths
    characters = Word.objects.filter(wordset=answer_).all()
    # Make the set of testing samples (different for each user)
    request.session['characters'] = characters


def teaching(request):
    """
    Shows a teaching example with options
    """
    user_id_ = request.user
    teaching_image_num_ = request.session['teaching_image_num']
    testing_samples_ = request.session['testing_samples']

    teaching_image_num = teaching_image_num_ + 1

    #X_path = '../User-Data/X_' + str(user_id_) + '.npy'
    #X = numpy.load(X_path)
    L = request.session['L']
    #next_sample = int(eer.get_next_sample(X, Y, W, L, testing_samples_))
    next_sample = random.randint(0,9)
    teaching_class_id = sample_classes[next_sample]
    character = characters[next_sample]

    context = {'teaching_image_num': teaching_image_num, 'num_teaching_images': num_teaching_images, 'class_names': class_names, 'character': character}

    request.session['teaching_class_id'] = teaching_class_id
    request.session['teaching_image_id'] = next_sample
    request.session['teaching_image_num'] = teaching_image_num
    request.session['character'] = character

    return render(request, 'teacher/teaching.html', context)


def feedback(request):

    answer_ = int(request.POST['answer'])
    teaching_image_num_ = int(request.session['teaching_image_num'])
    teaching_class_id_ = int(request.session['teaching_class_id'])
    character = request.session['character']

    true_class_name = class_names[teaching_class_id_]
    answer_class_name = class_names[answer_]
    if answer_ == teaching_class_id_:
        is_correct = True
    else:
        is_correct = False

    context = {'class_names': class_names, 'teaching_image_num': teaching_image_num_, 'true_class_name': true_class_name, 'answer_class_name': answer_class_name, 'is_correct': is_correct, 'character': character}

    return render(request, 'teacher/feedback.html', context)


def testing(request):

    testing_image_num_ = request.session['testing_image_num']
    testing_samples_ = request.session['testing_samples']

    testing_image_num = testing_image_num_ + 1

    testing_image_id = testing_samples_[testing_image_num - 1]
    testing_class_id = sample_classes[testing_image_id]
    character = characters[testing_image_id]

    request.session['testing_image_num'] = testing_image_num
    request.session['testing_image_id'] = testing_image_id
    request.session['testing_class_id'] = testing_class_id
    request.session['character'] = character

    context = {'testing_image_num': testing_image_num, 'num_testing_images': num_testing_images, 'class_names': class_names, 'character': character}

    return render(request, 'teacher/testing.html', context)


def processTeachingAnswer(request):

    user_id_ = int(request.session['user_id'])
    teaching_image_id_ = int(request.session['teaching_image_id'])
    answer_ = int(request.POST['answer'])

    L_ = request.session['L']
    L_.append(teaching_image_id_)
    X_path = '../User-Data/X_' + str(user_id_) + '.npy'
    X_ = numpy.load(X_path)
    X_[teaching_image_id_][:] = 0
    X_[teaching_image_id_][answer_] = 1 # Always update X with the class answered by the student (rather than necessarily the ground truth)
    numpy.save(X_path, X_)
    request.session['L'] = L_


def processTestingAnswer(request):

    user_id_ = int(request.session['user_id'])
    testing_class_id_ = int(request.session['testing_class_id'])
    answer_ = int(request.POST['answer'])

    is_correct = True if testing_class_id_ == answer_ else False

    user_response = UserResponse.create(user_id_, is_correct)
    user_response.save()


def testResults(request):

    # Get the average score
    score_sum = 0
    finished_users = User.objects.filter(is_finished = True)
    for u in finished_users:
        finished_correct_responses = UserResponse.objects.filter(user_id = u.user_id).filter(is_correct = True)
        score_sum += len(finished_correct_responses)

    user_id_ = request.session['user_id']

    correct_responses = UserResponse.objects.filter(user_id = user_id_).filter(is_correct = True)
    score = len(correct_responses)

    user = User.objects.get(user_id = user_id_)
    user.score = score
    user.is_finished = True
    user.save()

    if len(finished_users) > 0:
        ave_score = float(score_sum) / len(finished_users)
    else:
        ave_score = score

    context = {'score': score, 'num_testing_images': num_testing_images, 'ave_score': ave_score}

    return render(request, 'teacher/testresults.html', context)
