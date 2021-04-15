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
        self.topic = {topic}

    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        my_cap = self.resources if p.topic in self.topic else 0.
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
        if conf.prev_conf_pq == 0:
            self.belief = my_score - (-10*conf.ar + 10)
            return self.belief
        else: 
            self.belief = my_score - (conf.prev_conf_pq)
            return self.belief 

    def submit(self, conferences, must_submit: bool):
        """
        decide whether to submit a paper to conference conf, return bool
        """
        # write a paper, calc belief, and evaluate the cost here
        self.write_paper()
        succ_probs = []
        rewards = []
        costs = []
        norm = []
        overall = 0
        for i in range(len(conferences)): 
            succ_probs.append(self.calculate_belief(conferences[i])); 
            rewards.append(-10*conferences[i].ar + 10)
            costs.append(5); 
        for i in range(len(conferences)): 
            norm.append(succ_probs[i] + rewards[i] - costs[i])
        max_val = max(norm)
        max_conf = norm.index(max_val)
        if (must_submit):
            if max_val < 0: 
                return -1
            else: 
                return max_conf
        else: 
            return max_conf

    def resubmit(self):
        """
        ignore this for now
        """
        pass

    def update_resources(self, r):
        """update the resources when the paper result come out"""
        pass
