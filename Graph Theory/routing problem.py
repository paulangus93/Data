"""
Problem Summary

Objects arrive at a fixed inflow rate at the entry grid points. They arrive
unsorted and bound for a certain destination - no a priori one-to-one mapping
is assumed.

The grid should transport objects to their destination as quickly as possible
where it is moved off the grid immediately.

Onl one object can occupy a grid element at a given time instant.

Compare and contrast the flow rates of different routing algorithms with
networkx on a given graph layout, and find the optimal one.

The network in question is, tentatively, a grid of dimensions M x N, with
initial nodes (i) on the left and goal nodes (g) on the right. The layout of a
5 x 10 grid, for example, is as follows:

i . . . . . . . . g
i . . . . . . . . g
i . . . . . . . . g
i . . . . . . . . g
i . . . . . . . . g

The dimensions of the graph and the number of input and goal nodes should be
customizeable.
"""
#%%

"""
Create a graph generator which produces an unweighted N x M grid from
size parameters. The graph is described by an adjacency matrix wherein each
node contains information pertaining to its neighbours.
"""

import networkx as nx

N = 5
M = 10

def generate_grid(N,M):
    
    #create empty grid
    G = nx.graph()
    
    #create list of lists to add with G.add_nodes_from()
    nodes = list()
    
    for i in range(len(N*M)):
        
        node = list()
