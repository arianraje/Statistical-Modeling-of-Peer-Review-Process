from Agent.conference import Conference
from Agent.scientist import Scientist
from all_params import *
import matplotlib.pyplot as plt
import time


def make_plot(trajry):
    """plot the simulation results"""
    t = range(T)
    plt.subplot(2, 2, 1)
    plt.xlabel("year")
    plt.plot(t, trajry['quality'])
    plt.title("accepted paper instrinsic quality")
    plt.subplot(2, 2, 2)
    plt.plot(t, trajry['prestige'])
    plt.title("conference prestige")
    plt.subplots_adjust(hspace=0.5)
    plt.subplot(2, 2, 3)
    plt.plot(t, trajry['num_of_paper'])
    plt.title("number of submitted paper")
    plt.subplot(2, 2, 4)
    linef, = plt.plot(t, trajry['precision'])
    lineh, = plt.plot(t, trajry['hamming_error'])
    plt.title("Eval")
    plt.legend((linef, lineh), ("precision (%)", "avg hamming error"))
    plt.show()


def main():
    conf_lst = []
    community = []
    traj = {"quality": [], "prestige": [], "num_of_paper": [], "precision": [], "hamming_error": []}

    for i in range(NUM_CONF):
        conf_lst.append(Conference(acceptance_rate, reward, cost))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=0))

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
            traj["precision"].append(c.precision)
            traj["hamming_error"].append(c.herror)
            c.reset()

    # plot the simulation results
    print(traj)
    make_plot(traj)


if __name__ == '__main__':
    main()
