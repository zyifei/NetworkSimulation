# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:01:21 2017

@author: zhangyifei
"""

import networkx as nx
import random as r
import numpy as np
import matplotlib.pyplot as plt

"""creat the graph with differnt density"""
def graph_density(density):
    density
    g=nx.Graph()
    
    for i in range(50):
        g.add_node(i)
        
    ##this will be a simple random graph, every pair of nodes has an
    ##equal probability of connection
    for x in g.nodes():
        for y in g.nodes():
            if r.random()<=density: g.add_edge(x,y)
                
    
    return g
    

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
    """return the node with the most degree in the network"""
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




def run(G,d):
    attitude_init_ego(G)
    
    palive = []    
    for i in range(nsteps):
        step(G)
        palive.append(sum(G.node[i]["a_state"] >= 0.5 for i in G.nodes()) / n )# check the state of each node to calculate the proportion    

    plt.title('Influencial with different density')
    plt.plot(palive, label = "Density: %f" %d)
    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel("The Propotion of attitude greater than 0.5")  

if __name__ == "__main__":
    g = graph_density(0.9)
    n = len(g)
    run(g, 0.9)
    f = graph_density(0.5)
    n = len(f)
    run(f, 0.5)
    