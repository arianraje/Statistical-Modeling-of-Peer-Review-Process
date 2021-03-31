from .paper import Paper
from .conference import Conference
import numpy as np
import math
from all_params import *


class Scientist:
    """
    A Scientist instance
    """
    def __init__(self, topic: int):
        """
        belief: estimated probability of being accepted
        """
        self.belief = None
        self.paper = None

        self.resources = np.random.normal(r_mean, r_sigma)
        if self.resources > 10:
            self.resources = 10
        elif self.resources < 0:
            self.resources = 0

        self.experience = 0
        self.topic = {topic}
        #self.bias = np.random.normal(b_mean, b_sigma)

    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        #mu = p.pq + self.bias
        my_cap = self.resources if p.topic in self.topic else 0.
        #sigma = min(max_abtry, abtry_c / abs(p.pq - 5)) + min(max_cap, 1. / (theta_0 * self.experience + theta_1 * my_cap))
        r = np.random.normal(p.pq, 1)
        if r > 10:
            r = 10
        elif r < 0:
            r = 0
        return r

    def write_paper(self):
        """
        write a paper
        """
        t = np.random.randint(len(self.topic))
        self.paper = Paper(self, t)

    def calculate_belief(self, conf: Conference):
        """
        update the belief according to my paper mp, and last year's published papers cp
        """
        my_score = self.review(self.paper)
        """if conf.acc_papers:
            conf_avg_score = np.mean([ for p in conf.acc_papers])
            belief = min(0.45, conf.prestige / 10.)
            self.belief = 1. / (1 + belief * math.exp(-my_score + conf_avg_score))
        else:
            self.belief = 1. if np.random.uniform() >= init_belief_pecent else 0.""" 
        self.belief = my_score - (-10*conf.ar + 10)
        return self.belief

    def submit(self, conferences):
        """
        decide whether to submit a paper to conference conf, return bool
        """
        # write a paper, calc belief, and evaluate the cost here
        self.write_paper()
        succ_probs = []
        rewards = []
        costs = []
        norm = []
        for i in range(len(conferences)): 
            succ_probs.append(self.calculate_belief(conferences[i])); 
            rewards.append(-10*conferences[i].ar + 10)
            costs.append(5); 
        for i in range(len(conferences)): 
            norm.append(succ_probs[i] + rewards[i] - costs[i])
        max_val = max(norm)
        max_conf = norm.index(max_val)
        """submissions = []
        for i in range(len(conferences)): 
            if i == max_conf: 
                submissions.append(True)
            else: 
                submissions.append(False)
        return submissions""" 
        return max_conf

    def resubmit(self):
        """
        ignore this for now
        """
        pass

    def update_resources(self, r):
        """update the resources when the paper result come out"""
        pass
