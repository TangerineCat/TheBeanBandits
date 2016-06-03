
# coding: utf-8

# In[ ]:

import random
import Queue
import math

'''
These are classes to teach the student to recognize character.

get_next_teach_sample: This is the function to get the next teach sample.
OUTPUT: Character_id: the index of character in the quiz set (0-indexed). It
will return -1 if the quiz process is terminated.

teach_judge: This is the function to update the student's learning parameters.
INPUT: Choice: the choice that the student choose; groundtruth: the correct
choice

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
    
    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times))

# random choose teaching sample


class Random_Teach(Teach):

    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            # print "process: ", self.teach_process, self.teach_times-1,
            # self.state
            character_id = random.randrange(self.n_samples)
            return character_id
        else:
            return (-1)
    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times))

# Wrong-Stay-Correct-Shift: keep teach student until he learns the character


class WSCS_Teach(Teach):

    def __init__(self, n_samples, teach_times, prev_sample_index, unlearned_character):
        Teach.__init__(self, n_samples, teach_times)
        self.prev_sample_index = prev_sample_index
        self.unlearned_character = unlearned_character
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
                self.prev_sample_index = (
                    self.prev_sample_index + 1) % self.n_samples

    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times,self.prev_sample_index,self.unlearned_character))

'''
Improved-Wrong-Stay-Correct-Shift:
keep teach the student every "revisit_period" rounds until he learns the
character
'''


class IWSCS_Teach(Teach):

    def __init__(self, n_samples, teach_times, revisit_period, prev_sample_index, character_id, unlearned_character,revisit_queue):
        Teach.__init__(self, n_samples, teach_times)
        self.prev_sample_index = prev_sample_index
        self.character_id = character_id
        self.revisit_period = revisit_period
        self.unlearned_character = unlearned_character
        random.shuffle(self.unlearned_character)
        self.revisit_queue = revisit_queue 
    
    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times,self.revisit_period,self.prev_sample_index,self.character_id,self.unlearned_character,self.revisit_queue))

    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            self.character_id = self.revisit_queue.pop(0)
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
                    self.prev_sample_index = (
                        self.prev_sample_index + 1) % self.n_samples
                self.revisit_queue.append(-1)

            else:
                if self.character_id == -1:
                    self.revisit_queue.append(self.unlearned_character[
                                           self.prev_sample_index])
                    self.prev_sample_index = (
                        self.prev_sample_index + 1) % self.n_samples
                else:
                    self.revisit_queue.append(self.character_id)
                    

# Worst performance teaching strategy           
class WP_Teach(Teach):
    
    def __init__(self, n_samples, teach_times, accuracy, counts, sample_index):
        
        Teach.__init__(self, n_samples, teach_times)
        '''
        self.accuracy = [0.0 for _ in range(self.n_samples)]
        self.counts = [0 for _ in range(self.n_samples)]
        self.sample_index = 0
        '''
        
        self.accuracy = accuracy
        self.counts = counts
        self.sample_index = sample_index
        
    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times,self.accuracy,self.counts,self.sample_index))
        
        
    def get_next_teach_sample(self):
        
        if not self.terminated():
            self.teach_process += 1
            minimum = min(self.accuracy)
            indices = [x for x in range(self.n_samples) if self.accuracy[x] == minimum]
            self.sample_index = random.choice(indices)
            self.counts[self.sample_index] += 1
            return self.sample_index
            
        else:
            return (-1)
            
    def teach_judge(self, choice, groundtruth):
        if not self.terminated():
            n = self.counts[self.sample_index]
            if choice == groundtruth:
                self.accuracy[self.sample_index] = self.accuracy[self.sample_index] * (n-1) / n + 1.0 / n
            else:
                self.accuracy[self.sample_index] = self.accuracy[self.sample_index] * (n-1) / n
                    
                    
# Multi-armed bandit teaching strategy
class MAB_Teach(Teach):
    
    def __init__(self, n_samples, teach_times, sample_index, arm_index, recent_performance, performance, learning_counts, indices, counts, avg):
        Teach.__init__(self, n_samples, teach_times)
        self.sample_index = sample_index
        self.arm_index = arm_index
        
        self.recent_performance = recent_performance
        self.performance = performance
        self.learning_counts = learning_counts
        
        self.indices = indices
        
        self.counts = counts
        self.avg = avg
    
    def __reduce__(self):
        return (self.__class__,(self.n_samples,self.teach_times,self.sample_index,self.arm_index,self.recent_performance,self.performance,self.learning_counts,self.indices,self.counts,self.avg))
        
    def get_next_teach_sample(self):
        if not self.terminated():
            self.teach_process += 1
            
            for arm in range(self.n_samples):
                if self.counts[arm] == 0:
                    self.arm_index = arm
                    self.sample_index = self.indices[arm]
                    return self.sample_index
            # UCB1 algorithm
            ucb_values = [0.0 for _ in range(self.n_samples)]
            total_counts = sum(self.counts)
            for arm in range(self.n_samples):
                bonus = math.sqrt((2 * math.log(total_counts)) / float(self.counts[arm]))
                ucb_values[arm] = self.avg[arm] + bonus
            
            self.arm_index = ucb_values.index(max(ucb_values))
            self.sample_index = self.indices[self.arm_index]
            return self.sample_index

        else:
            return (-1)
        
    def segment(self):
        seg_num = int(math.ceil(max(self.performance)))+1
        seg_list = [[] for _ in range(seg_num)]

        for i in range(self.n_samples):
            seg_list[int(math.ceil(self.performance[i]))].append(i)

        for i in range(len(seg_list)):
            random.shuffle(seg_list[i])

        self.indices = []
        for i in range(len(seg_list)):
            self.indices += seg_list[i]
        
    def teach_judge(self, choice, groundtruth):
        if not self.terminated():
            if choice == groundtruth:
                performance_value = 1.0
            else:
                performance_value = 0
                
            reward = performance_value - self.recent_performance[self.sample_index]
            # reward = performance_value - self.performance[self.sample_index]
            
            self.counts[self.arm_index] += 1
            n = self.counts[self.arm_index]
            avg_value = self.avg[self.arm_index]
            new_avg_value = ((n - 1) / float(n)) * avg_value + (1 / float(n)) * reward
            self.avg[self.arm_index] = new_avg_value
            
            self.performance[self.sample_index] += performance_value
            self.learning_counts[self.sample_index] += 1
            n = self.learning_counts[self.sample_index]
            # self.performance[self.sample_index] = ((n - 1) / float(n)) * self.performance[self.sample_index] + (1 / float(n)) * performance_value
            if (self.teach_process < self.teach_times):
                self.indices = sorted(range(len(self.performance)), key=lambda k: self.performance[k])
            else:
                self.segment()
            
            self.recent_performance[self.sample_index] = performance_value
