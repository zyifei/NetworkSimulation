# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:01:21 2017

@author: zhangyifei
"""

import networkx as nx
import random as r
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import seaborn


def ego_hub(G):
    """return the node with the most degree in the network"""
    max = 0    
    for u in G.nodes():
        if max <= G.degree(u):
            max = G.degree(u)
            n = u
    return n

def infection_init(G):
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




def run(m):
    n= 5*m
    G=nx.generators.barabasi_albert_graph(n,m)
    node_and_degree=G.degree()
    (largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
    hub_ego=nx.ego_graph(G, largest_hub)
    G = hub_ego
    infection_init(G)
    palive = []
    for i in range(20):
        step(G)
        palive.append(sum(G.node[i]["a_state"] >= 0.5 for i in G.nodes()) / n )# check the state of each node to calculate the proportion    
    
      
    plt.title('Ego Influence in network over time')    
    plt.plot(palive, label = "n = %d" %n)
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("The Propotion of attitude greater than 0.5")
    
if __name__ == "__main__":   
    m = 10 
    
    while(m <= 190):
        #nsteps = 10 # how many time-steps to run
        
        run(m)
        m += 20
        
    