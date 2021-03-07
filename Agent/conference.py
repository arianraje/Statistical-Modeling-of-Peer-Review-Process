import numpy as np
import math

init_prestige = 5.
alpha = 10.
beta = 0.
gamma = 1.
N = 1


class Conference:
    """A instance of a conference"""
    def __init__(self, acc_rate, reward=1., cost=2.):
        self.ar = acc_rate
        self.num_of_papers = 0
        self.prestige = init_prestige
        self.acc_papers = []
        self.rej_papers = []
        self.receive_papers = {}
        self.reviewers = []
        self.reward = self.prestige * reward
        self.cost = cost
        self.agg_review_map = None
        self.ferror = 0.
        self.herror = 0.

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
        cutoff = np.percentile(list(agg_review_map.values()), (1-self.ar) * 100)
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
        acc_num = math.floor(self.ar * self.num_of_papers)
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

    def update(self):
        """ Update results of this conference"""
        self.update_prestige()
        self.update_ferror()
        self.update_herror()

    def update_prestige(self):
        """return the conference prestige"""
        self.prestige = -alpha * self.ar + gamma * np.mean([p.author.resources for p in self.acc_papers])

    def calc_pq(self):
        """return the acc papers true quality"""
        return np.mean([p.pq for p in self.acc_papers])

    def update_ferror(self):
        """ fraction of paper that get accepted while it shouldn't have """
        acc, _ = self.decide(self.receive_papers)
        acc = set(acc)
        correct = 0
        for p in self.acc_papers:
            if p in acc:
                correct += 1
        self.ferror = 100 * (1 - correct / len(acc))

    def update_herror(self):
        """ avg hamming distance error"""
        def get_quality(d):
            return d[1]
        true_order = {p: r + 1 for r, (p, q) in enumerate(sorted(self.receive_papers.items(), key=get_quality,
                                                                 reverse=True))}
        actual_order = {p: r + 1 for r, (p, q) in enumerate(sorted(self.agg_review_map.items(), key=get_quality,
                                                                   reverse=True))}
        self.herror = np.mean([abs(true_order[p] - actual_order[p]) for p in true_order])
