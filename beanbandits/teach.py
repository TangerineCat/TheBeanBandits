
# coding: utf-8

# In[ ]:

import random
import Queue

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
    
    def __init__(self, n_samples, teach_times):
        self.n_samples = n_samples
        self.teach_times = teach_times
        self.teach_process = 0
            
    def get_next_teach_sample(self):
        pass
        
    def teach_judge(self, choice, groundtruth):
        pass
    
    def terminated(self):
        return self.teach_process >= self.teach_times
    
    def print_end(self):
        pass
        
    def print_begin(self):
        print "Character Learning begins!"
    
# random choose teaching sample
class Random_Teach(Teach):
    
    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            # print "process: ", self.teach_process, self.teach_times-1, self.state
            character_id = random.randrange(self.n_samples)
            return character_id
        else:
            return (-1)
    
# Wrong-Stay-Correct-Shift: keep teach student until he learns the character
class WSCS_Teach(Teach):
    
    def __init__(self, n_samples, teach_times):
        Teach.__init__(self, n_samples, teach_times)
        self.prev_sample_index = 0
        self.unlearned_character = range(self.n_samples)
        random.shuffle(self.unlearned_character)
        
    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            character_id = self.unlearned_character[self.prev_sample_index]
            return character_id
        else:
            return (-1)
        
    def teach_judge(self, choice, groundtruth):
        if not self.terminated():
            if choice == groundtruth:
                self.prev_sample_index = (self.prev_sample_index+1) % self.n_samples
                
'''
Improved-Wrong-Stay-Correct-Shift: 
keep teach the student every "revisit_period" rounds until he learns the character
'''
class IWSCS_Teach(Teach):
    
    def __init__(self, n_samples, teach_times, revisit_period):
        Teach.__init__(self, n_samples, teach_times)
        self.prev_sample_index = 0
        self.character_id = -1
        self.revisit_period = max(1, revisit_period)
        self.unlearned_character = range(self.n_samples)
        random.shuffle(self.unlearned_character)
        
        self.revisit_queue = Queue.Queue()
        for _ in range(self.revisit_period):
            self.revisit_queue.put(-1)
        
    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            self.character_id = self.revisit_queue.get()
            if self.character_id == -1:
                return self.unlearned_character[self.prev_sample_index]
            else:
                return self.character_id
        else:
            return (-1)
        
    def teach_judge(self, choice, groundtruth):
        if not self.terminated():
            if choice == groundtruth:
                if self.character_id == -1:
                    self.prev_sample_index = (self.prev_sample_index+1) % self.n_samples
                self.revisit_queue.put(-1)
                
            else:
                if self.character_id == -1:
                    self.revisit_queue.put(self.unlearned_character[self.prev_sample_index])
                    self.prev_sample_index = (self.prev_sample_index+1) % self.n_samples
                else:
                    self.revisit_queue.put(self.character_id)
