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
        # self.belief = None
        self.paper = None

        self.resources = np.random.normal(r_mean, r_sigma)
        if self.resources > 10:
            self.resources -= np.random.uniform(1, 2) * (self.resources - 10)
        elif self.resources < 0:
            self.resources -= np.random.uniform(1, 2) * self.resources

        self.experience = 0
        self.topic = {topic}
        self.bias = np.random.normal(b_mean, b_sigma)
        self.conf_quality_map = {}

    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        mu = p.pq + self.bias
        my_cap = self.resources if p.topic in self.topic else 0.
        sigma = min(max_abtry, abtry_c / abs(p.pq - 5)) + min(max_cap, 1. / (theta_0 * self.experience + theta_1 * my_cap))
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
            if conf not in self.conf_quality_map:
                self.conf_quality_map[conf] = [conf_avg_score]
            discounted_b = discount * conf_avg_score + (1-discount) * self.conf_quality_map[conf][-1]
            self.conf_quality_map[conf].append(discounted_b)

            # belief_c = min(0.45, conf.prestige / 10.)
            belief = 1. / (1 + belief_c * math.exp(-my_score + discounted_b))
        else:
            belief = 1. if np.random.uniform() >= init_belief_pecent else 0.
        return belief

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

    def decide(self, conf_lst):
        """ Decide which conference to submit by maximzing the gain """
        self.write_paper()
        max_gain = -0.0000001
        smax_gain = -0.0000001
        decision, d1, d2 = None, None, None
        if conf_lst[0].acc_papers:
            for ci in range(len(conf_lst)):
                c = conf_lst[ci]
                succ_prob = self.calculate_belief(c)
                gain = c.reward * succ_prob - c.cost * self.paper.pq / 8.
                if gain > max_gain:
                    smax_gain = max_gain
                    max_gain = gain
                    d2 = d1
                    d1 = c
                elif gain > smax_gain:
                    smax_gain = gain
                    d2 = c
            # print(d1, d2, self.paper.pq, conf_lst[0].calc_pq(), conf_lst[1].calc_pq())
            if max_gain * smax_gain <= 0:
                decision = d1
            elif max_gain - smax_gain > 1:
                decision = d1
            elif smax_gain >= 0:
                decision = d1 if np.random.uniform() >= 0.5 else d2
        else:
            if np.random.uniform() >= init_belief_pecent:
                decision = conf_lst[np.random.choice(len(conf_lst))]
        return decision
