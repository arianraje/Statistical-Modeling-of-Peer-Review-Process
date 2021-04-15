import numpy as np
import math
from all_params import *


class Conference:
    """A instance of a conference"""
    def __init__(self, acc_rate):
        self.ar = acc_rate
        self.num_of_papers = 0
        self.acc_papers = []
        self.rej_papers = []
        self.receive_papers = {}
        self.reviewers = []
        self.agg_review_map = None
        self.prev_conf_pq = 0 

    def reset(self):
        """ Reset conference """
        self.receive_papers = {}
        self.reviewers = []

    def call_for_papers(self, sci_lst):
        """
        announce acceptance rate, and collect papers from a list of Scientists sci_lst
        """
        for sci in sci_lst:
            if sci.submit(self, True):
                self.receive_papers[sci.paper] = sci.paper.pq
                # each paper provides some reviewers
                self.reviewers.append(sci)
        self.num_of_papers = len(self.receive_papers)
        return self.num_of_papers

    def assign(self):
        """Assign the papers to reviewers, return a map from paper to reviewers"""
        permuted = np.random.permutation(self.num_of_papers)
        return {p: [self.reviewers[k] for k in permuted[N * i: N * (i + 1)]]
                for i, p in enumerate(self.receive_papers)}

    def set_aggregated_review_map(self, review_map):
        """Set the review map {paper: aggregated_review_result}
        Use avg for now
        """
        self.agg_review_map = {p: np.mean(review_map[p]) for p in review_map}

    def decide(self, agg_review_map):
        """
        decide the acc_papers and the rej_papers
        the middle set are randomly accepted
        """
        peer_review_results = list(agg_review_map.values())
        if not peer_review_results:
            return [], []
        cutoff = np.percentile(list(agg_review_map.values()), (1 - self.ar) * 100)
        middle_set = []
        acc_papers = []
        rej_papers = []
        for p in agg_review_map:
            if agg_review_map[p] > cutoff:
                acc_papers.append(p)
            elif agg_review_map[p] < cutoff:
                rej_papers.append(p)
            else:
                middle_set.append(p)
        return acc_papers, rej_papers

    def notify_accept(self, acc):
        """
        notify the accepted paper's author with reward
        """
        self.acc_papers = acc

    def notify_reject(self, rej):
        """
        notify the rejected papers with cost
        """
        self.rej_papers = rej

    def reset(self): 
        self.prev_conf_pq = np.mean([p.pq for p in self.acc_papers])
        self.receive_papers = {}
        self.reviewers = []
        self.num_of_papers = 0

    def calc_pq(self):
        """return the acc papers true quality"""
        return np.mean([p.pq for p in self.acc_papers])


