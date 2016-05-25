
# coding: utf-8

# In[1]:

import random
import Queue

########################################################################
'''
This is the class to test the student's ability in character recognition.

Example: 
quiz = Quiz(len(quiz_set), quiz_times)

quiz.print_begin()
while not quiz.terminated():
    character_id = quiz.get_next_quiz_sample()
    get response from learner
    quiz.quiz_judge(response, groundtruth)
    
quiz.print_end()
'''
class Quiz(object):
    
    ''' 
    INPUT: 
    n_samples: The number of samples (i.e. characters) in the quiz set
    quiz_times: The number of samples (i.e. characters) you expect students to take
    
    OUTPUT: NULL
    '''
    def __init__(self, n_samples, quiz_times):
        self.n_samples = n_samples
        self.quiz_times = max(quiz_times, self.n_samples)
        self.quiz_process = 0
        self.score = 0.0
    
    '''
    This is the function to get the next quiz sample.
    
    INPUT: NULL
    
    OUTPUT: 
    Character_id: the index of character in the quiz set (0-indexed). 
    It will return -1 if the quiz process is terminated. 
    '''
    def get_next_quiz_sample(self):
        if not self.terminated():
            character_id = self.quiz_process % self.n_samples
            self.quiz_process += 1
            return character_id
        else:
            return (-1)
    
    '''
    This is the function to update the student score and other learning parameters. 
    
    INPUT: 
    Choice: the choice that the student choose
    groundtruth: the correct choice
    
    OUTPUT: NULL
    '''
    def quiz_judge(self, choice, groundtruth):
        if choice == groundtruth:
            self.score += (100.0 / self.quiz_times)
    
    '''
    This is the function to get the student score.
    
    INPUT: NULL
    
    OUTPUT: student's score
    '''
    def get_score(self):
        return self.score
    
    '''
    This is the function to know if the quiz process has been terminated
    
    INPUT: NULL
    
    OUTPUT: if the quiz process has been terminated
    '''
    def terminated(self):
        return self.quiz_process >= self.quiz_times
    
    def print_end(self):
        print "Congratulations! This is the end of Character Quiz!"
        print "Your score is: ", self.score
        
    def print_begin(self):
        print "Character Quiz begins! Good luck!"

