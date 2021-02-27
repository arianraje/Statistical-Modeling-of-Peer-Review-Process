from Agent.conference import Conference
from Agent.scientist import Scientist

NUM_SCI = 1000
NUM_CONF = 1
T = 100
AR = 0.2
topic_map = {1: "DL"}
reward = 2
cost = 2


def main():
    conf_lst = []
    community = []
    traj = {"quality": [], "prestige": [5]}

    for i in range(NUM_CONF):
        conf_lst.append(Conference(AR))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=1))

    for t in range(T):
        for c in conf_lst:
            c.call_for_papers(community)
            reviewer_map = c.assign()
            review_map = {}
            for p in reviewer_map:
                res = p.ask_for_review(review_map[p])
                review_map[p] = res
            c.decide(review_map)
            c.notify_accept(reward * c.prestige)
            c.notify_reject(cost)
            # store results of interest here: prestige, number of papers, ...
            traj["size of community"].append(c.calc_pq())


if __name__ == '__main__':
    main()
