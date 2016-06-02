
# coding: utf-8

# In[ ]:

import random
import Queue

import numpy as np
from __builtin__ import True

'''
These are classes to teach the student to recognize character.

get_next_teach_sample: This is the function to get the next teach sample.
OUTPUT: Character_id: the index of character in the quiz set (0-indexed). It will return -1 if the quiz process is terminated. 

teach_judge: This is the function to update the student's learning parameters. 
INPUT: Choice: the choice that the student choose; groundtruth: the correct choice

terminated: This is the function to know if the quiz process has been terminated

Example: 
teaching_strategy = IWSCS_Teach(len(teach_set), teach_times, 2)

teaching_strategy.print_begin()
while not teaching_strategy.terminated():
    character_id = teaching_strategy.get_next_teach_sample()
    get response from learner
    teaching_strategy.teach_judge(choice, groundtruth)
    
teaching_strategy.print_end()
'''

# abstract teach class
class Teach(object):
    #         n_samples = data[0, 0]
    #         teach_times = data[0, 1]
    #         teach_process = data[0, 2]
    #         prev_sample_index = data[0, 3]
    #         unlearned_chars
    def __init__(self, n_samples, teach_times, user_id):
        # n_sample, teach_times, teach_process
        file_name = "data" + str(user_id) + ".txt"
        f1 = open(file_name,'w')
        f1.write(str(n_samples) + ", " + str(teach_times) + ", " + str(0))
        f1.close()

    def read_file(self, user_id):
        file_name = "data" + str(user_id) + ".txt"
        data = np.loadtxt(file_name, delimiter=',', dtype='str')
        return data
    
    def write_file(self, data, user_id):
        file_name = "data" + str(user_id) + ".txt"
        f1 = open(file_name,'w')
        f1.write(str(data[0]))
        for i in range(len(data) - 1):
            f1.write(", " + str(data[i + 1]))
        f1.close()
    
    def get_next_teach_sample(self, user_id):
        pass
        
    def teach_judge(self, choice, groundtruth, user_id):
        pass
    
    def terminated(self, user_id):
        data = self.read_file(user_id)
        temp1 = int(data[2])
        temp2 = int(data[1])
        return temp1 >= temp2
    
    def print_end(self):
        pass
        
    def print_begin(self):
        print "Character Learning begins!"
    
# random choose teaching sample
class Random_Teach(Teach):
    
    def get_next_teach_sample(self, user_id):
        file_name = "data" + user_id + ".txt"
        data = np.loadtxt(file_name, delimiter=',', dtype='str')
        teach_process = data[0, 2]
        n_samples = data[0, 0]
        
        if not self.terminated(user_id):
            teach_process += 1
            # print "process: ", self.teach_process, self.teach_times-1, self.state
            character_id = random.randrange(n_samples)
            return character_id
        else:
            return (-1)
    
# Wrong-Stay-Correct-Shift: keep teach student until he learns the character
class WSCS_Teach(Teach):
    
    def __init__(self, n_samples, teach_times, user_id):
        # n_sample, teach_times, teach_process, prev_sample_index
        Teach.__init__(self, n_samples, teach_times, user_id)
        
        data = self.read_file(user_id)
        
        unlearned_character = range(n_samples)
        random.shuffle(unlearned_character)

        file_name = "data" + str(user_id) + ".txt"
        f1 = open(file_name,'w')
        f1.write(str(data[0]) + ", " + str(data[1]) + ", " + str(data[2]) + ", " + str(0))
        for i in range(n_samples):   
            f1.write("," + str(unlearned_character[i]))
        f1.close()
        
    def get_next_teach_sample(self, user_id):
        data = self.read_file(user_id)
        
        if not self.terminated(user_id):
            temp = int(data[2])
            data[2] = temp + 1
            character_id = int(data[4 + int(data[3])])
            
            self.write_file(data, user_id)
            
            return character_id
        else:
            return (-1)

        
    def teach_judge(self, choice, groundtruth, user_id):
        
        data = self.read_file(user_id)

        
        if not self.terminated(user_id):
            if choice == groundtruth:
                temp1 = int(data[3]) + 1
                temp2 = int(data[0])
                
                data[3] = temp1 % temp2
                
                self.write_file(data, user_id)
                return True
            else:
                return False
