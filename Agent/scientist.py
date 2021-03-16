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
            self.resources -= np.random.uniform(1, 2) * (self.resources - 10)
        elif self.resources < 0:
            self.resources -= np.random.uniform(1, 2) * self.resources

        self.experience = 0
        self.topic = {topic}
        self.bias = np.random.normal(b_mean, b_sigma)

    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        mu = p.pq + self.bias
        my_cap = self.paper.pq if p.topic in self.topic else 0.
        sigma = min(max_abtry, abtry_c / abs(p.pq - 5)) + min(0.5, 1. / (theta_0 * self.experience + theta_1 * my_cap))
        r = np.random.normal(mu, sigma)
        if r > 10:
            r -= np.random.uniform(1, 1.5) * (r - 10)
        elif r < 0:
            r -= np.random.uniform(1, 1.5) * r
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
        if conf.acc_papers:
            conf_avg_score = np.mean([self.review(p) for p in conf.acc_papers])
            self.belief = 1. / (1 + belif_c * math.exp(-my_score + conf_avg_score))
        else:
            self.belief = 1. if np.random.uniform() >= init_belief_pecent else 0.
        return self.belief

    def submit(self, conf: Conference):
        """
        decide whether to submit a paper to conference conf, return bool
        """
        # write a paper, calc belief, and evaluate the cost here
        self.write_paper()
        succ_prob = self.calculate_belief(conf)
        return succ_prob * conf.reward >= conf.cost

    def resubmit(self):
        """
        ignore this for now
        """
        pass

    def update_resources(self, r):
        """update the resources when the paper result come out"""
        pass
