from Agent.conference import Conference
from Agent.scientist import Scientist
from all_params import *
import matplotlib.pyplot as plt
import numpy as np
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


def one_conf():
    """ independent conferences scenerio"""
    conf_lst = []
    community = []
    for i in range(NUM_CONF):
        conf_lst.append(Conference(acceptance_rate, reward, cost))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=0))

    for t in range(T):
        print(t)
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
            c.traj["quality"].append(c.calc_pq())
            c.traj["prestige"].append(c.prestige)
            c.traj["num_of_paper"].append(c.num_of_papers)
            c.traj["precision"].append(c.precision)
            c.traj["hamming_error"].append(c.herror)
            c.reset()

            # plot the simulation results
            if t == 20:
                print(c.traj)
                make_plot(c.traj)


def max_gain():
    """ submit to the conf that max the gain"""
    conf_lst = []
    community = []
    ar = [0.2, 0.2]
    for i in range(NUM_CONF):
        conf_lst.append(Conference(ar[i], reward, cost))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=0))
    for t in range(T):
        print(t)
        for sci in community:
            c = sci.decide(conf_lst)
            if c:
                sci.experience += 1
                c.receive_papers[sci.paper] = sci.paper.pq
                c.reviewers.append(sci)
        #a = np.asarray([p.paper.pq for p in community])
        #print(np.sum(np.where(a > 8, 1, 0)))
        #print(np.sum(np.where(a > 9, 1, 0)))
        #print(np.sum(np.where(a > 7, 1, 0)))

        for c in conf_lst:
            c.num_of_papers = len(c.receive_papers)
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
            c.traj["quality"].append(c.calc_pq())
            c.traj["prestige"].append(c.prestige)
            c.traj["num_of_paper"].append(c.num_of_papers)
            c.traj["precision"].append(c.precision)
            c.traj["hamming_error"].append(c.herror)
            #print(c.calc_pq())
            #print("num: %d" % len(c.receive_papers))
            #print([(p.paper.pq, p.calculate_belief(c), c.reward, c.cost) for p in community])
            c.reset()
            if t == 20:
                print(c.traj)


if __name__ == '__main__':
    one_conf()
