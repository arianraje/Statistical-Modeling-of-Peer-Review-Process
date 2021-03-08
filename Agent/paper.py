import numpy as np
from all_params import *


class Paper:
    """ A paper instance """
    def __init__(self, author, topic):
        self.author = author
        self.topic = topic
        self.pq = np.random.normal(self.author.resources, pq_sigma)
        if self.pq > 10:
            self.pq -= np.random.uniform(1, 2) * (self.pq - 10)
        elif self.pq < 0:
            self.pq -= np.random.uniform(1, 2) * self.pq
        self.review_results = []
        self.citation = 0

    def ask_for_review(self, reviewers):
        """ ask for rebiew of each reviewers"""
        for r in reviewers:
            self.review_results.append(r.review(self))
        return self.review_results
