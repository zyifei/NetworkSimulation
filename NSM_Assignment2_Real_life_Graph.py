# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:01:21 2017

@author: zhangyifei
"""

import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt

"""read the real world graph"""
with open('facebook_combined.txt') as f:
    lines = f.readlines()

myList = [line.strip().split() for line in lines]
# [['a', 'b'], ['a', 'c'], ['b', 'd'], ['c', 'e']]

g = nx.Graph()
g.add_edges_from(myList)



n = len(g) # number of nodes
nsteps = 30 # how many time-steps to run

def ego_hub(G):
    """return the node with the most degree in the network"""
    max = 0    
    for u in G.nodes():
        if max <= G.degree(u):
            max = G.degree(u)
            n = u
    return n

def attitude_init_ego(G):
    """inisial the attitude of every node in the network."""
    ego = ego_hub(G)    
    for u in G.nodes():
        G.node[u]["i_state"] = np.random.uniform(0.0,1.0)
        G.node[u]["a_state"] = G.node[u]["i_state"]
        G.node[u]["alpha"] = 0.8
        
        
        if ego == u: 
            G.node[u]["i_state"] = np.random.uniform(0.0,1.0)
            G.node[u]["a_state"] = 1
            G.node[u]["alpha"] = 0.8

def attitude_init_noego(G):
    """inisial the attitude of every node in the network."""
    for u in G.nodes():
        G.node[u]["i_state"] = np.random.uniform(0.0,1.0)
        G.node[u]["a_state"] = G.node[u]["i_state"]
        G.node[u]["alpha"] = 0.8
        
    ego = ego_hub(G)    
    init = ego
    while(init == ego):
        init = random.sample(G.nodes(), 1)
        
    for u in init:
       G.node[u]["i_state"] = np.random.uniform(0.0,1.0)
       G.node[u]["a_state"] = 1
       G.node[u]["alpha"] = 0.8
 
def step(G):
    """Given a graph G, run one time-step."""
    new_state = {}
    for u, d in G.nodes(data=True):# u is the node index and d is the node state
        if d["a_state"] == 1:
            new_state[u] = d["a_state"]
        else:
            w = 1/float(len(G.neighbors(u)))
            s = w*d["a_state"]
            for u2 in G.neighbors(u):
                s += w*G.node[u2]["a_state"]
            new_state[u]=(1-d["alpha"])*d["i_state"] + d["alpha"]*s
        
    for u in G.nodes():
        G.node[u]["a_state"] = new_state[u]




def run_ego(G):

    attitude_init_ego(G)
    palive = []    
    for i in range(nsteps):
        step(G)
        palive.append(sum(G.node[i]["a_state"] >= 0.5 for i in G.nodes()) / n )# check the state of each node to calculate the proportion    
        
    plt.title('Facebook Ego Network - friends circle')
    plt.plot(palive, label = "Ego as influencer")
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("The Propotion of attitude greater than 0.5")

def run_noego(G):

    attitude_init_noego(G)
    palive = []    
    for i in range(nsteps):
        step(G)
        palive.append(sum(G.node[i]["a_state"] >= 0.5 for i in G.nodes()) / n )# check the state of each node to calculate the proportion    
        
    plt.title('Facebook Ego Network - friends circle')
    plt.plot(palive, label = "No Ego as influencer")
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("The Propotion of attitude greater than 0.5")  


if __name__ == "__main__":
    run_ego(g)
    run_noego(g)