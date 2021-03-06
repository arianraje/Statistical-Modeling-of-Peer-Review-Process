from .paper import Paper
from .conference import Conference
import numpy as np
import math

r_mean = 5.
r_sigma = 1
b_sigma = 1
b_mean = 0.
theta_0 = 0.
theta_1 = 1.
r_c = 1.


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
        self.experience = 0
        self.topic = {topic}
        self.bias = np.random.normal(b_mean, b_sigma)

    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        mu = p.pq + self.bias
        my_cap = self.paper.pq if p.topic in self.topic else 0.
        sigma = min(2, 1. / abs(p.pq - 5)) + 1. / (theta_0 * self.experience + theta_1 * my_cap + r_c)
        return np.random.normal(mu, sigma)

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
        else:
            return 1. if np.random.uniform() >= 0.8 else 0.
        return 1. / (1 + math.exp(-my_score + conf_avg_score))

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

    def update_resources(self, reward):
        """update the resources when the paper result come out"""
        pass
