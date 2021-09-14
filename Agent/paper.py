class Paper:
    """ A paper instance """
    def __init__(self, author, topic, pq=None):
        self.author = author
        self.topic = topic
        if pq:
            self.pq = pq
        else:
            self.pq = np.random.normal(self.author.resources, pq_sigma)
    
        self.review_results = []
                self.citation = 0

    def ask_for_review(self, reviewers):
        """ ask for rebiew of each reviewers"""
            for r in reviewers:
                self.review_results.append(r.review(self))
        return self.review_results
