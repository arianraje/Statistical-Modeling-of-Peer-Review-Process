from Agent.conference import Conference
from Agent.scientist import Scientist
import time

NUM_SCI = 1000
NUM_CONF = 1
T = 5
acceptance_rate = 0.2
topic_map = {1: "DL"}


def main():
    conf_lst = []
    community = []
    traj = {"quality": [], "prestige": [], "num_of_paper": [], "frac_error": [], "hamming_error": []}

    for i in range(NUM_CONF):
        conf_lst.append(Conference(acceptance_rate))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=1))

    for t in range(T):
        for c in conf_lst:
            c.call_for_papers(community)
            reviewer_map = c.assign()
            review_map = {}
            for p in reviewer_map:
                res = p.ask_for_review(reviewer_map[p])
                review_map[p] = res
            c.set_aggregated_review_map(review_map)
            acc, rej = c.decide(c.agg_review_map)
            c.notify_accept(acc)
            c.notify_reject(rej)
            c.update()
            # store results of interest here
            traj["quality"].append(c.calc_pq())
            traj["prestige"].append(c.prestige)
            traj["num_of_paper"].append(c.num_of_papers)
            traj["frac_error"].append(c.ferror)
            traj["hamming_error"].append(c.herror)

    # plot the simulation results
    print(traj)


if __name__ == '__main__':
    main()
