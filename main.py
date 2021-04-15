from Agent.conference import Conference
from Agent.scientist import Scientist
from all_params import *
import matplotlib.pyplot as plt
import time

def create_conferences(): 
    conf_list = []
    conf_list.append(Conference(acceptance_rate_1))
    conf_list.append(Conference(acceptance_rate_1))
    return conf_list

def create_community(): 
    community = []
    for i in range(NUM_SCI): 
        community.append(Scientist(topic=0))
    return community

def main():
    conf_list = create_conferences()
    community = create_community()
    for t in range(T): 
        for scientist in community: 
            which_conf = scientist.submit(conf_list, True)
            if (which_conf != -1):
                conf_list[which_conf].receive_papers[scientist.paper] = scientist.paper.pq
                conf_list[which_conf].reviewers.append(scientist)
                conf_list[which_conf].num_of_papers += 1
        print("Conference Year: " + str(t))
        for c in conf_list: 
            reviewer_map = c.assign()
            review_map = {}
            for p in reviewer_map:
                res = p.ask_for_review(reviewer_map[p])
                review_map[p] = res
            c.set_aggregated_review_map(review_map)
            acc, rej = c.decide(c.agg_review_map)
            c.notify_accept(acc)
            c.notify_reject(rej)
            c.reset()
            print("Conference paper quality: " + str(c.prev_conf_pq))

if __name__ == '__main__':
    main()
