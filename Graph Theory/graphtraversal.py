"""
Initial objective: To test efficacy of routing algorithms on the same test grid.

First, create a 2D grid with dimensions N x M, on a lattice so each node has an edge in 4 cardinal
directions, with the intuitive exceptions in the edges and corners.

Use leftmost nodes for inlet, and rightmost nodes for outlet, initially, but ensure they are
reconfigurable as topology is a significant limiting factor.

Keep initial and goal node rows different to make sure lane crossings occur, as this is necessary
to test efficacy.

Only one agent per node is allowed.

Goals:
    1. For a given routing algorithm, find the flow capacity of the grid.
    2. For a set of routing algorithms, find which delivers max flow.
    
Sorting happens on grid, not off grid. So the agents arrive at the entry points randomly.

Topology is not fixed, so feel free to make assumptions and change it up when you deem appropriate.

Try one source of agents with multiple destinations first.

When two agents want to occupy a node, a conflict resolution algorithm is needed.

After this is resolved, add more agents.

Maybe also try configurations where agents must move in opposite directions on the grid.

Problem Summary

Objects arrive at a fixed inflow rate at the entry grid points. They arrive
unsorted and bound for a certain destination - no a priori one-to-one mapping
is assumed.

The grid should transport objects to their destination as quickly as possible
where it is moved off the grid immediately.

Only one object can occupy a grid element at a given time instant.

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
Create a graph of an unweighted N x M grid from
size parameters. The graph is described by an adjacency matrix wherein each
node contains information pertaining to its neighbours.
"""

import networkx as nx


#dimensions of the graph
M = 10
N = 5

#nx generate graph
G = nx.grid_2d_graph(M,N)

nx.draw(G)

#convert to dict of lists
graph = nx.to_dict_of_lists(G)

#%%

"""
Assign an initial and goal vertex, and implement a shortest path algorithm.
"""

#assign vertices
initial_vertex = (0,0) 
goal_vertex = (9,4)

#navigate using A*
path = nx.astar_path(G, initial_vertex, goal_vertex)

print(path)

#%%

"""
Assign a set of initial and goal vertices, and implement a shortest path algorithm to navigate
from every initial to every goal.
"""

#assign vertices
initial_vertices = [(0,0), (0,1), (0,2), (0,3), (0,4)]
goal_vertices = [(9,0), (9,1), (9,2), (9,3), (9,4)]

#Find paths between all initial and all goal vertices
paths = return_all_paths(G, initial_vertices, goal_vertices)

print(paths)

#%%

"""
Go back to single initial/goal vertices and implement a step tracker function to time the traversal.
"""
import networkx as nx

M = 10
N = 5

#nx generate graph
G = nx.grid_2d_graph(M,N)

#set time to zero
current_time = 0

#create variable for time
times = list()

#assign initial and goal vertices
initial_vertex = (0,0)

goal_vertex = (9,4)

#generate path
path = nx.astar_path(G, initial_vertex, goal_vertex)

#assign ID of entity
ID = 1

#set current vertex to initial vertex
current_vertex = initial_vertex

traversals = 0

#move until current_vertex = goal_vertex
while current_vertex != goal_vertex:
    
    current_vertex = path.pop(0)
    
    current_time = current_time + 1

print(current_time)
print(current_vertex)

#%%

"""
Same as above, but implement periodic entity generation every 4 time steps, and run for 100 steps. Use state dictionary (ID: path) to track progress. Remove entry when leaving grid.
"""

import networkx as nx
import numpy as np

M = 30
N = 15

G = nx.grid_2d_graph(M,N)

initial_vertex = (0,0)

goal_vertex = (M-1,N-1)

#generate ID for first entity
ID = 1

#generate dictionary of paths, with key = ID, value = path. This will be edited dynamically.
state = dict()

#customize times
current_time, time_limit, interval = 0, 100, 2

#while current time between 0 and time limit
while current_time in np.arange(0, time_limit):
    
    #if current time also a generation time (in this case multiple of 4)
    if current_time in np.arange(0, time_limit, interval):
           
        #generate its path
        state[ID] = nx.astar_path(G, initial_vertex, goal_vertex)
        
        ID = ID + 1
    
    print("Time: {}".format(current_time))
    
    print()
    
    #move all entities (don't use ID for variable name in loop)
    for idx in state.keys():

        move(idx, state[idx])
    
    
    current_time = current_time + 1


#%%
"""
Create a spawn situation where entities have to cross each other. For example (i1 and i2 spawning at the same time):
    
i2  .   .   g1
.   .   .   .
i1  .   .   g2

(2,0) (2,1) (2,2) (2,3)
(1,0) (1,1) (1,2) (1,3)
(0,0) (0,1) (0,2) (0,3)

Then create a conflict resolution algorithm.
"""

import networkx as nx
import numpy as np

M = 3
N = 4

G = nx.grid_2d_graph(M,N)

initial_vertex = (0,0)

goal_vertex = (M-1,N-1)

current_time = 0

state = dict()

#generate entity 1 and 2
generate_entity(1, (0, 0), (2, 3))

generate_entity(2, (2, 0), (0, 3))

time_limit = 5

while current_time in np.arange(0, time_limit):

    
    print("Time: {}".format(current_time))
    
    print()
    
    #move all entities (don't use ID for variable name in loop)
    for idx in state.keys():

        move(idx, state[idx])
    
    current_time = current_time + 1

#with the above, a clash occurs at time: 1 , as both entities want to move to (1,0)

#%%
"""
Implement an occlusion algorithm that checks the next move for each entity before moving. Keep an occupancy dictionary (id: next_vertex) and avoid movements of all other entities into that vertex. 
"""

import networkx as nx
import numpy as np

M = 3
N = 4

G = nx.grid_2d_graph(M,N)

initial_vertex = (0,0)

goal_vertex = (M-1,N-1)

current_time = 0

#create state and occupancy dictionaries
state, occupancy = dict(), dict()

#generate both entities, producing an initial path and an occupancy entry (vertex: path[1])
generate_entity(1, (0, 0), (2, 3))

generate_entity(2, (2, 0), (0, 3))

time_limit = 7

conflict_nodes = dict()

while current_time in np.arange(0, time_limit):
    
    print("Time: {}".format(current_time))
    
    print()
    
    
    #loop over all entities
    for i in state.keys():

        current_vertex = move(i, state[i])
        
        #update occupancy list with relevant values if the path remains     
        if state[i] != []:
            
            occupancy[i] = state[i][0]
            
        else:
            
            #remove entry from occupancy dict if off grid
            occupancy[i] = None
    
    current_time = current_time + 1        

    
    #check for occupancy matches
    if len(set(occupancy.values())) != len(occupancy.values()):

        #for all entities in conflict          
        for i in occupancy.keys():
            
            #add to dictionary of conflict nodes
            conflict_nodes[i] = list(i for i in set(occupancy.values()))[0]
        
        print("Conflicting nodes: {}".format(conflict_nodes))
        
        print()
    
        #re-compute all paths except one (how to decide which one?) Maybe use shortest path length as priority?
               
    
    print("Occupancy: {}".format(occupancy))
    
    print("---------------------------------------------")
#%% 
"""
Code snippet from meeting. Document for clarity.
"""

import numpy as np
import networkx as nx

#initialise graph
M = 2
N = 5
G = nx.grid_2d_graph(M,N)
   
#move entity ID along its path and modify its current_vertex
def move(ID, path, current_vertex=None):    
    if current_vertex == None:
        return
    #update current_vertex as pop path if not empty
    if path != []:
        current_vertex = path.pop(0)
        print("Entity {} is at position: {}".format(ID, current_vertex))
        print("Remaining moves: {}".format(path))
        print()
    #if path empty, set current_vertex to None
    else:
        current_vertex = None

#modifies state, occupancy dicts, so include in args        
def generate_entity(ID, initial_vertex, goal_vertex, state, occupancy): 
    #generate path of entity
    state[ID] = nx.astar_path(G, initial_vertex, goal_vertex)
    #keep track of current node occupancy of every entity
    occupancy[ID] = state[ID].pop(0)
    
def graph_init():
    state, occupancy = dict(), dict()
    #generate entities, coords (M,N) such that a conflict occurs at time:2
    generate_entity(1, (0, 0), (0, N-1), state, occupancy)
    generate_entity(2, (0, N-1), (0, 0), state, occupancy)
    return state, occupancy
    
def navigate_graph():
    state, occupancy = graph_init()
    print("Time: 0")
    print()
    for i in state.keys():
        print("Entity {} is at position: {}".format(i,occupancy[i]))
        print("Remaining moves: {}".format(state[i]))
        print()
    time_limit = M+N
    #initialise conflict dictionary for future use
    conflict_nodes = dict()    
    for current_time in np.arange(1, time_limit):
        print("Time: {}".format(current_time))
        print()   
        #agents_complete is a list of agents that have completed their navigation
        agents_complete=[]
        #loop over all entities
        for i in state.keys():    
            #move entity
            current_vertex = move(i, state[i], current_vertex=occupancy[i])
            #if path remains, shift occupancy to first element in the path
            if state[i] != []:
                occupancy[i] = state[i][0]
            #if entity is off grid, append ID to agents_complete list
            else:
                agents_complete.append(i)
        #for all completed agents, remove its state/occupancy entries and advance time
        for i in agents_complete:        
            occupancy.pop(i)
            state.pop(i)

navigate_graph()

#%%
"""
Implement a conflict resolution algorithm. Instead of navigating the base graph, navigate a copy with all currently occupied nodes removed and recompute all paths where a conflict occurs.
"""

import numpy as np
import networkx as nx

#initialise the base graph
M = 2
N = 5
G = nx.grid_2d_graph(M,N)
   
#move entity ID along its path and modify its current_vertex
def move(ID, path, current_vertex=None):    
    if current_vertex == None:
        return
    #update current_vertex as pop path if not empty
    if path != []:
        current_vertex = path.pop(0)
        print("Entity {} is at position: {}".format(ID, current_vertex))
        print("Remaining moves: {}".format(path))
        print()
    #if path empty, set current_vertex to None
    else:
        current_vertex = None


#modifies state, occupancy dicts, so include in args        
def generate_entity(ID, initial_vertex, goal_vertex, state, occupancy): 
    #generate path of entity
    state[ID] = nx.astar_path(G, initial_vertex, goal_vertex)
    #keep track of current node occupancy of every entity
    occupancy[ID] = state[ID].pop(0)
    
def graph_init():
    state, occupancy = dict(), dict()
    #generate entities, coords (M,N) such that a conflict occurs at time:2
    generate_entity(1, (0, 0), (0, N-1), state, occupancy)
    generate_entity(2, (0, N-1), (0, 0), state, occupancy)
    return state, occupancy

#recalibrate paths
def recalibrate_path():
    mod_graph = G.copy()
    mod_graph.remove_node((0,2))
    initial_vertex, goal_vertex = (0,3), (0,0)
    path = nx.astar_path(mod_graph, initial_vertex, goal_vertex)
    return path
    
    
def navigate_graph():
    
    #generate entities
    state, occupancy = graph_init()
    
    #print starting conditions
    print("Time: 0")
    print()
    for i in state.keys():
        print("Entity {} is at position: {}".format(i,occupancy[i]))
        print("Remaining moves: {}".format(state[i]))
        print()
        
    #assign arbitrary time limit
    time_limit = M+N
    
    #initialise conflict dictionary for future use
    conflict_nodes = dict()    
    
    #time loop
    for current_time in np.arange(1, time_limit):
        print("Time: {}".format(current_time))
        print() 
        
        #agents_complete is a list of agents that have completed their navigation
        agents_complete=[]

        #loop over all entities
        for i in state.keys():
            
            #move entity
            move(i, state[i], current_vertex=occupancy[i])
            
            #if path remains, shift occupancy to first element in the path
            if state[i] != []:
                occupancy[i] = state[i][0]
                
            #if entity is off grid, append ID to agents_complete list
            else:
                agents_complete.append(i)
                
        #for all completed agents, remove its state/occupancy entries and advance time
        for i in agents_complete:        
            occupancy.pop(i)
            state.pop(i)       
            
        #check for conflicts
        if len(set(occupancy.values())) != len(occupancy.values()):
            
            #for all entities in conflict          
            for i in occupancy.values():   
                
                #add to dictionary of conflict nodes {node: [list of IDs aiming for node]}
                conflict_nodes[i] = list(i for i in set(occupancy.keys()))
            
            #conflicting nodes structure: {node_coordinates: [list of entities vying for said node]}
            print("Conflicting nodes: {}".format(conflict_nodes))        
            print()
            
            #recalibrate paths here. Consider making a function.
            #recalibrate_path(conflict_nodes)
            

navigate_graph()
#%%

M = 2
N = 5
G = nx.grid_2d_graph(M,N)

def recalibrate_path():
    mod_graph = G.copy()
    mod_graph.remove_node((0,2))
    initial_vertex, goal_vertex = (0,3), (0,0)
    path = nx.astar_path(mod_graph, initial_vertex, goal_vertex)
    return path

a = recalibrate_path()

print(a)

"""
keep track of numbers of agents in and out
"""
