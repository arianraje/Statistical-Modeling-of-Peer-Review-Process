import numpy as np
import math


class Scientist:
    """
        A Scientist instance
        """
    def __init__(self, r, topic=0, mu=r_mean, sigma=r_sigma):
        """
        belief: estimated probability of being accepted
        """
        # self.belief = None
        self.paper = None
        self.my_score = None
        
        self.resources = r
        self.experience = 0
        self.topic = {topic}
        self.bias = np.random.normal(b_mean, b_sigma)
        self.conf_quality_map = {}
        """
        if np.random.uniform() > 0.9:
        if np.random.uniform() > 0.5:
        self.fx = 1
        else:
        self.fx = 0
        else:
        self.fx = -1
        """
    
    
    def review(self, p: Paper):
        """
        review a papers p, return the review result
        """
        mu = p.pq #+ self.bias
        #my_cap = self.resources if p.topic in self.topic else 1e-7
        #sigma = min(max_abtry, abtry_c / abs(p.pq - 5)) + min(max_cap, 1. / (theta_0 * self.experience + theta_1 * my_cap))
        #r = np.clip(np.random.normal(mu, sigma), 0, 10)
        r = mu
        return r
    
    def write_paper(self):
        """
        write a paper
        """
        t = np.random.randint(len(self.topic))
        self.paper = Paper(self, t)
        self.my_score = self.review(self.paper)
    
    def calculate_belief(self, conf: Conference):
        """
        update the belief according to my paper mp, and last year's published papers cp
        """
        if conf.year > 1:
            # the scientist read a subsample of the acc papers
            acc_subsample = np.random.permutation(conf.acc_papers)[:50]
            conf_avg_score = np.mean([self.review(p) for p in acc_subsample])
        else:
            conf_avg_score = (1-conf.ar) * 10 / 1.03
        #belief_c = min(0.35, conf.prestige / 5.)
        belief = 1. / (1 + belief_c * math.exp(-self.my_score + conf_avg_score))
        
        return belief
    
    def submit(self, conf: Conference):
        """
            decide whether to submit a paper to conference conf, return bool
            """
        # write a paper, calc belief, and evaluate the cost here
        self.write_paper()
        succ_prob = self.calculate_belief(conf)
        return succ_prob * conf.reward * conf.prestige >= conf.cost
    
    def resubmit(self):
        """
            ignore this for now
            """
        pass
    
    def update_resources(self, r):
        """update the resources when the paper result come out"""
        self.resources = r
    
    def decide(self, conf_lst, debug=False):
        """ Decide which conference to submit by maximzing the gain """
        self.write_paper()
        """
            if self.fx == 0:
            return conf_lst[0]
            elif self.fx == 1:
            return conf_lst[1]
            """
        max_gain = -1e-7
        decision = None
        for ci in range(len(conf_lst)):
            c = conf_lst[ci]
            succ_prob = self.calculate_belief(c)
            #gain0 = c.prestige * c.reward * succ_prob - c.cost
            gain = (np.random.normal(0, 2) + c.prestige) * c.reward * succ_prob - c.cost #* self.paper.pq * 0.5
            #if debug:
            #    print(c.prestige, succ_prob, self.paper.pq, gain0, gain)
            if gain > max_gain:
                max_gain = gain
                decision = c
            elif gain == max_gain:
                if np.random.uniform() >= 0.5:
                    decision = c
        return decision
