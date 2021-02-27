import numpy as np

pq_sigma = 1


class Paper:
    def __init__(self, author, topic):
        self.author = author
        self.topic = topic
        self.pq = np.random.normal(self.author.resources, pq_sigma)
        self.review_results = []
        self.citation = 0

    def ask_for_review(self, reviewers):
        for r in reviewers:
            self.review_results.append(r.review(self))
        return self.review_results
