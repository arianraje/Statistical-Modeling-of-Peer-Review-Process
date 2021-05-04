import numpy as np
import math
from all_params import *

class Conference:
    """A instance of a conference"""
    def __init__(self, acc_rate, c_reward, c_cost):
        self.ar = acc_rate
        self.num_of_papers = 0
        self.prestige = (1-self.ar) * 10 / 1.2
        self.acc_papers = []
        self.rej_papers = []
        self.receive_papers = {}
        self.reviewers = []
        self.reward = c_reward
        self.cost = c_cost
        self.agg_review_map = None
        self.precision = 0.
        self.herror = 0.
        self.traj = {"quality": [], "num_of_paper": [], "prestige": [], "precision": [], "hamming_error": [], "var":[], "author_res":[]}
        self.year = 1
        self.receive_paper_stats = {">9":[], ">8":[], ">7":[], ">6":[], ">5":[], "<=5":[]}
        self.receive_author_stats = {">9":[], ">8":[], ">7":[], ">6":[], ">5":[], "<=5":[]}
        self.acc_paper_stats = {">9":[], ">8":[], ">7":[], ">6":[], ">5":[], "<=5":[]}
        self.acc_author_stats = {">9":[], ">8":[], ">7":[], ">6":[], ">5":[], "<=5":[]}

    def changeAr(self, ar):
        self.ar = ar

    def reset(self):
        """ Reset conference """
        self.receive_papers = {}
        self.reviewers = []

    def call_for_papers(self, sci_lst):
        """
        announce acceptance rate, and collect papers from a list of Scientists sci_lst
        """
        for sci in sci_lst:
            if sci.submit(self):
                self.receive_papers[sci.paper] = sci.paper.pq
                # each paper provides some reviewers
                self.reviewers.append(sci)
                sci.experience += 1
        self.num_of_papers = len(self.receive_papers)
        return self.num_of_papers

    def recuite_reviewers(self):
        """ Recruite reviewers, make sure that each paper provide N reviewers
        where N is the number of reviewers for each paper"""
        pass

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
        cutoff = np.percentile(peer_review_results, (1 - self.ar) * 100)
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
        # can ignore this, very unlikely
        acc_num = math.ceil(self.ar * self.num_of_papers)
        if len(acc_papers) < acc_num and middle_set:
            lucky_p = np.random.permutation(len(middle_set))[:acc_num - len(acc_papers)]
            unlucky_p = np.random.permutation(len(middle_set))[acc_num - len(acc_papers):]
            acc_papers += [middle_set[i] for i in lucky_p]
            rej_papers += [middle_set[i] for i in unlucky_p]
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

    def update(self, t):
        """ Update results of this conference"""
        self.update_prestige(t)
        #self.update_precision()
        #self.update_recall()
        #self.update_herror()
        self.year += 1

    def update_prestige(self, t):
        """return the conference prestige"""
        acc_pq = np.mean([p.pq for p in self.acc_papers])
        acc_author_resources = np.mean([p.author.resources for p in self.acc_papers])
        self.prestige = -alpha * self.ar + gamma * acc_author_resources + eta * acc_pq

        self.traj["quality"].append(acc_pq)
        self.traj["author_res"].append(acc_author_resources)

    def update_precision(self):
        """ true good ones / accepted ones
         """
        true_acc, _ = self.decide(self.receive_papers)
        if true_acc:
            acc_set = set(self.acc_papers)
            correct = 0
            for p in true_acc:
                if p in acc_set:
                    correct += 1
            self.precision = correct / len(acc_set)
        else:
            self.precision = 0.

    def update_herror(self):
        """ avg hamming distance error"""
        true_order = {p: r + 1 for r, (p, q) in enumerate(sorted(self.receive_papers.items(), key=lambda item: item[1],
                                                                 reverse=True))}
        actual_order = {p: r + 1 for r, (p, q) in enumerate(sorted(self.agg_review_map.items(), key=lambda item: item[1],
                                                                   reverse=True))}
        self.herror = np.mean([abs(true_order[p] - actual_order[p]) for p in true_order]) / len(true_order)
