from .paper import Paper
from .conference import Conference
import numpy as np
import math

r_sigma = 1
b_sigma = 1


class Scientist:
    def __init__(self, topic: int):
        """
        belief: estimated probability of being accepted
        """
        self.belief = 1.
        self.paper = None
        self.resources = np.random.normal(5, r_sigma)
        self.experience = 0
        self.topic = {topic}
        self.bias = np.random.normal(0, b_sigma)

    def review(self, p: Paper):
        """
        review a paper p, return the review result
        """
        pass

    def write_paper(self):
        """
        write a paper
        """
        pass

    def calculate_belief(self, mp, conf: Conference):
        """
        update the belief according to my paper mp, and last year's published papers cp
        """
        pass

    def submit(self, conf: Conference):
        """
        decide whether to submit a paper to conference conf, return bool
        """
        # write a paper, calc belief, and evaluate the cost here
        pass

    def resubmit(self):
        """
        ignore this for now
        """
        pass

    def update_resources(self, reward):
        """update the resources when the paper result come out"""
        pass
