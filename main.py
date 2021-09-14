from Agent.conference import Conference
from Agent.scientist import Scientist
from all_params import *
import matplotlib.pyplot as plt
import numpy as np
import time


def one_conf():
    """ independent conferences scenerio"""
    conf_lst = []
    community = []
    ar = [0.2, 0.4, 0.6, 0.7, 0.8]
    for i in range(5):
        conf_lst.append(Conference(ar[i], reward, cost))
    
    for i in range(NUM_SCI):
        r = (i+1) **(-0.12) *10 # zipf
        #r = np.random.normal(5, 1.5)
        community.append(Scientist(r, topic=0))
    
    for t in range(T):
        print(t)
        for c in conf_lst:
            c.reset()
            c.call_for_papers(community)
            reviewer_map = c.assign()
            review_map = {}
            for p in reviewer_map:
                res = p.ask_for_review(reviewer_map[p])
                review_map[p] = res
            c.set_aggregated_review_map(review_map)
            #print(review_map)
            acc, rej = c.decide(c.agg_review_map)
            c.notify_accept(acc)
            c.notify_reject(rej)
            c.update()

    # plot the simulation results
    return conf_lst


def max_gain():
    """ submit to the conf that max the gain"""
    conf_lst = []
    community = []
    ar = [0.2, 0.7]
    for i in range(NUM_CONF):
        conf_lst.append(Conference(ar[i], reward, cost))

    for i in range(NUM_SCI):
        community.append(Scientist(topic=0))

    for t in range(T):
        print("time: %d ==================================================" % t)

        for sci in community:
            c = sci.decide(conf_lst)
            if c:
                sci.experience += 1
                c.receive_papers[sci.paper] = sci.paper.pq
                c.reviewers.append(sci)

        for c in conf_lst:
            c.receive_paper_stats[">9"].append(np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 9, 1, 0)))
            c.receive_paper_stats[">8"].append(np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 8, 1, 0)))
            c.receive_paper_stats[">7"].append(np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 7, 1, 0)))
            c.receive_paper_stats[">6"].append(np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 6, 1, 0)))
            c.receive_paper_stats[">5"].append(np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 5, 1, 0)))
            c.receive_paper_stats["<=5"].append(
                np.sum(np.where(np.asarray([p.pq for p in c.receive_papers]) > 0, 1, 0)))

            c.receive_author_stats[">9"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 9, 1, 0)))
            c.receive_author_stats[">8"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 8, 1, 0)))
            c.receive_author_stats[">7"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 7, 1, 0)))
            c.receive_author_stats[">6"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 6, 1, 0)))
            c.receive_author_stats[">5"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 5, 1, 0)))
            c.receive_author_stats["<=5"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.receive_papers]) > 0, 1, 0)))

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

            c.acc_paper_stats[">9"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 9, 1, 0)))
            c.acc_paper_stats[">8"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 8, 1, 0)))
            c.acc_paper_stats[">7"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 7, 1, 0)))
            c.acc_paper_stats[">6"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 6, 1, 0)))
            c.acc_paper_stats[">5"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 5, 1, 0)))
            c.acc_paper_stats["<=5"].append(np.sum(np.where(np.asarray([p.pq for p in c.acc_papers]) > 0, 1, 0)))

            c.acc_author_stats[">9"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 9, 1, 0)))
            c.acc_author_stats[">8"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 8, 1, 0)))
            c.acc_author_stats[">7"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 7, 1, 0)))
            c.acc_author_stats[">6"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 6, 1, 0)))
            c.acc_author_stats[">5"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 5, 1, 0)))
            c.acc_author_stats["<=5"].append(
                np.sum(np.where(np.asarray([p.author.resources for p in c.acc_papers]) > 0, 1, 0)))

            if t == 25:
                conf_lst[1].changeAr(0.5)

            if t == 50:
                conf_lst[1].changeAr(0.3)

            if t == 80:
                conf_lst[1].changeAr(0.1)

            c.update(t)

            # store results of interest here
            c.traj["prestige"].append(c.prestige)
            c.traj["num_of_paper"].append(c.num_of_papers)
            print("quality: %f" % c.traj["quality"][-1])
            print("num: %d" % c.traj["num_of_paper"][-1])
            print("pres: %f" % c.traj["prestige"][-1])
            # c.traj["precision"].append(c.precision)
            # c.traj["hamming_error"].append(c.herror)
            c.reset()

    return conf_lst[0], conf_lst[1]


if __name__ == '__main__':
    one_conf()
