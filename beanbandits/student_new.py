import random

import numpy as np
from __builtin__ import True

from teach_new import WSCS_Teach

class STUDENT_CONSTANT:
    def __init__(self, _target_amount, _prob, _learning_rate_true, _learning_rate_false):
        self.target_amount = _target_amount
        self.prob = _prob
        self.learning_rate_true = _learning_rate_true
        self.learning_rate_false = _learning_rate_false
        self.data = np.loadtxt("problem_set.txt", delimiter=',', dtype='str')
        
    def get_answer(self, index, right_answer):
        answer = random.random()
        
        if answer < self.prob[index] or np.abs(self.prob[index] - 1) < 0.01 :
            answer = right_answer
        else:
            answer = "W"
        
        return answer
    
    def learn(self, teaching_strategy):
        if teaching_strategy == "WSCS_Teach":
            teacher = WSCS_Teach(self.target_amount, 20, 5)
        else:
            teacher = WSCS_Teach(self.target_amount, 20, 5)

        while (True):
            cur_index = teacher.get_next_teach_sample(5)
            if cur_index == -1:
                break
            
            right_answer = self.data[cur_index, 1]
               
            answer = self.get_answer(cur_index, right_answer)
            
            judge = teacher.teach_judge(answer, right_answer, 5)
            
            if np.abs(self.prob[cur_index] - 1) < 0.01:
                pass
            else:
                if judge == True:
                    self.prob[cur_index] += self.learning_rate_true
                else:
                    self.prob[cur_index] += self.learning_rate_false
        
        return self.prob
    
            
if __name__ == "__main__":
    
    target_amount = 5;
    prob = 0.1 * np.ones(5);
    learning_rate_false = 0.05
    learning_rate_true = 0.1
    student = STUDENT_CONSTANT(target_amount, prob, learning_rate_true, learning_rate_false)
    
    final_prob = student.learn("WSCS_Teach")
    
    for i in range(target_amount):
        print final_prob[i]