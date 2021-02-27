class Conference:
    def __init__(self, ar):
        self.ar = ar
        self.num_of_papers = 0
        self.prestige = 5.
        self.acc_papers = []
        self.rej_papers = []
        self.receive_papers = []
        self.reviewers = []

    def call_for_papers(self, sci_lst):
        """
        announce acceptance rate, and collect papers from a list of Scientists sci_lst
        """
        for sci in sci_lst:
            if sci.submit(self):
                self.receive_papers.append(sci.paper)
                # each paper provides some reviewers
                self.reviewers.append(sci)
        self.num_of_papers = len(self.receive_papers)

    def assign(self):
        """Assign the papers to reviewers, return a map from paper to reviewers"""
        pass

    def decide(self, review_map):
        """
        decide the acc_papers and the rej_papers
        """
        pass

    def notify_accept(self, reward):
        """
        notify the accepted paper's author with reward
        """
        for p in self.acc_papers:
            p.author.update_resources(reward)

    def notify_reject(self, cost):
        """
        notify the rejected papers with cost
        """
        pass

    def update_prestige(self):
        """return the conference prestige"""
        pass

    def calc_pq(self):
        """return the acc papers true quality"""
        pass
