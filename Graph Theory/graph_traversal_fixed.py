"""
Resolve the merges that occur while goal nodes are in conflict. One method might be to re-route around to another goal node. In addition, it may be useful to give agents the option to stay in place if their next move would force a collision. Optionally, try to find a way to keep the agents on grid for a single step as they reach the goal node, and display that node as a different colour to signify when an agent reaches its goal.
"""

import numpy as np
import networkx as nx
import random
import copy
import matplotlib.pyplot as pl
from matplotlib import animation

#Moves an agent forward one node along its path and returns node as current_node.
def move(ID, path, goal_nodes, current_node=None):  
    if current_node == None:
        return
    if path != []:
        current_node = path.pop(0)
        print("Agent {} is at position: {}".format(ID, current_node))
        print("Remaining moves: {}".format(path))
        print()
    else:
        current_node = None   
    return current_node

"""
move_all_agents should move agents in sequence.
create occupancy list
For each agent:
    check new position
    if in occupancy list:
        recalibrate path
    perform move
    append new location to occupancy list
    remove previous location from occupancy list   
    

"""

def shortest_path(G, initial_vertex, goal_vertices, conflict_nodes):
    all_paths = []
    #Remove conflicting goal nodes from potential destinations.
    #for node in conflict_nodes:
    #    if node in goal_vertices:
    #        goal_vertices.remove(node)

    for i in range(len(goal_vertices)):
        
        goal_vertex = goal_vertices[i]  

        path = nx.astar_path(G, initial_vertex, goal_vertex)
        
        all_paths.append(path)
    all_paths.sort(key=len)
    shortest_path = all_paths[0]
    return shortest_path 



#Auxiliary function for recalibrate_paths. 
def recalibrate_path(graph, ID, conflict_node, occupancy, paths, goal_nodes):
    mod_graph = copy.deepcopy(graph)
    
    #mod_graph.remove_node(conflict_node)
    
    
    path = shortest_path(mod_graph, occupancy[ID], goal_nodes, conflict_node)

    return path

#Perform move for all agents.
def move_all_agents(G, paths, occupancy, goal_nodes, agents_complete, all_agents_complete):
    #for each agent
    for i in paths.keys():
        #if new position is in occupancy dict:
        if paths[i][0] in occupancy.values():
            #recalibrate path
            paths[i] = recalibrate_path(G, i, paths[i][0], occupancy, paths, goal_nodes)
            
        #perform move        
        occupancy[i] = move(i, paths[i], goal_nodes, current_node=occupancy[i])  
        
        if paths[i] == []:
            agents_complete.append(i)
            all_agents_complete.append(i)
            
            

#Return a list of potential paths from a list of initial and goal vertices.
def return_all_paths(G, initial_vertices, goal_vertices):    
    paths = []
    for i in range(len(initial_vertices)):
        for j in range(len(goal_vertices)):        
            initial_vertex = initial_vertices[i]     
            goal_vertex = goal_vertices[j]           
            path = nx.astar_path(G, initial_vertex, goal_vertex)           
            paths.append(path) 
    return paths


#Uses recalibrate_path and path_duplicate_check to decide which to re-direct based on path length.
def recalibrate_paths(G, conflict_nodes, occupancy, paths, goal_nodes):
    
    #Create a subgraph from the primary graph to navigate.
    subGraph = copy.deepcopy(G)
        
    #Create a dictionary of first path elements.
    next_nodes = dict()          
    for i in paths:          
        next_nodes[i] = paths[i][0]

    #Create map of first path elements.
    nextnode_agent_map = {node:[] for _, node in next_nodes.items()}
    #Assign agent keys to dictionary.
    for agent_key, node in next_nodes.items():
        nextnode_agent_map[node].append(agent_key)
    
    #Create a conflict dictionary.
    conflicted_nodes = {node:conflicts for node, conflicts in nextnode_agent_map.items() if (len(conflicts)>1) and not (node in goal_nodes)}

    #Resolve the conflict by updating paths and occupancy.
    for conflict_node, agents in conflicted_nodes.items():

        #reroute_agents = (ID, path_length). Includes current_node.
        reroute_agents = [(agent_key, len(paths[agent_key])) for agent_key in agents]
        
        #Sort by ascending (lambda +x) or descending (lambda -x) order of path length. List of tuples (agent ID, path length).
        reroute_agents = sorted(reroute_agents, key = lambda x: x[1])
        
        #Pop shortest path from reroute_agents.
        reroute_agents.pop(0)
        
        #Recalibrate all paths marked for rerouting through local subgraphs.
        for rrt_agent_tup in reroute_agents:
            rrt_agent = rrt_agent_tup[0]
        
            subGraph, new_path = recalibrate_path(subGraph, rrt_agent, conflict_node, occupancy, paths, goal_nodes)
            
            paths[rrt_agent]  = new_path
            occupancy[rrt_agent] = paths[rrt_agent].pop(0)
    
#Return the shortest path from a single vertex to a set of goal vertices
def return_shortest_path(G, current_vertex, goal_vertices):
    all_paths = []
    for i in range(len(goal_vertices)):
        goal_vertex = goal_vertices[i]        
        path = nx.astar_path(G, current_vertex, goal_vertex)
        all_paths.append(path)
    all_paths.sort(key=len)
    shortest_path = all_paths[0]
    return shortest_path 
    
#Produce a list of initial and goal nodes from the base graph. Modify this for different selection criteria.
def initial_goal_nodes(G):    
    initial_nodes = list(G.nodes)[:3]
    goal_nodes = list(G.nodes)[-3:]
    return initial_nodes, goal_nodes

#Draws the graph. For use in animate function.
def drawgraph(G, occupancy, initial_nodes, goal_nodes):
    nx.draw_networkx(G, pos = dict((n,n) for n in G.nodes()), node_color = ["yellow" if n in occupancy.values() and (n in initial_nodes or n in goal_nodes) else "red" if n in occupancy.values() else "green" if n in initial_nodes else "orange" if n in goal_nodes else "pink" for n in G.nodes()])

#Animates the graph.    
def animate(G, occupancy, initial_nodes, goal_nodes):
    fig,ax = pl.subplots()
    animation.FuncAnimation(fig, drawgraph(G, occupancy, initial_nodes, goal_nodes), frames = 1, fargs = (G, ax))    
    pl.show()
    
#Check occupancy dictionary for duplicate values by swapping key/value. Raise an exception if a conflict is found.
def duplicate_check(occupancy):
    occupancy_swap = {}
    for i, j in occupancy.items():
        if j not in occupancy_swap:
            occupancy_swap[j] = [i]
        else:
            occupancy_swap[j].append(i)
        for k in occupancy_swap.values():
            if len(k) > 1:               
                raise Exception("Duplicate occupancy detected: Agents {} at node {}".format(occupancy_swap[j], occupancy[i]))

#Check duplicate values in first path elements and return conflict_agents, which need to be re-calibrated again. Used in recalibrate_paths.
def path_duplicate_check(paths):
    next_swap = {}
    for i, j in paths.items():    
        if j[0] not in next_swap:  
            next_swap[j[0]] = [i]
        else:
            next_swap[j[0]].append(i)        
    for conflict_agents in next_swap.values():
        if len(conflict_agents) > 1:              
            raise Exception("Unresolved conflict detected: Agents {} at node {}".format(conflict_agents, j[0]))


#The primary function uses all of the above auxiliary functions to traverse a graph, avoiding collisions. Use a seed for reproducibility.
def navigate_graph(seed=0, spawn_interval = 2):    
    
    #Initialise parameters and data structures.
    occupancy, paths = dict(), dict()
    ID = 1
    offgrid = 0
    initial_nodes, goal_nodes = initial_goal_nodes(G)

    #Generate the seed.
    random.seed(seed)

    all_agents_complete = []
        
    #Loop until the time limit.
    for current_time in np.arange(0, time_limit): 
        
        #Check for duplicates and raise an exception if one is found.
        duplicate_check(occupancy)        
        
        #Track agents with completed paths.
        agents_complete=[]
    
        #Periodically generate an agent at a random initial node and initialise its path towards its closest of a set of goal nodes.          
        if current_time in np.arange(0, time_limit, spawn_interval):                      
            init = initial_nodes.copy()
            for node in occupancy.values():
                if node in init:
                    init.remove(node)
            if init != []:
                initial_vertex = random.choice(init)
            
            """
            instead of shortest path, make path go to random goal node. Could also cycle through goal nodes in order, instead of random.
            """
            goal_node = random.choice(goal_nodes)
            paths[ID] = nx.astar_path(G, initial_vertex, goal_node)

            occupancy[ID] = paths[ID][0]    
            ID = ID + 1
            
        print("Time: {}".format(current_time))
        print() 
        
        #recalibrate_paths(G, conflict_nodes, occupancy, paths, goal_nodes) 
        
        #Move all agents, and document completed paths upon successfully reaching a goal node.
        move_all_agents(G, paths, occupancy, goal_nodes, agents_complete, all_agents_complete)

        animate(G, occupancy, initial_nodes, goal_nodes)
        
        #Remove completed paths from the dictionary and add them to the offgrid count.
        for i in agents_complete:        
            occupancy.pop(i)
            paths.pop(i) 
            offgrid = offgrid + 1            
        
        #Count on-grid agents at the end of each time step.
        ongrid = len(paths.keys())
        
        print("Agents Currently On Grid: {}".format(ongrid))
        print("Successful Traversals: {}".format(offgrid))
        print("Completed Agent list: {}".format(all_agents_complete))
        print()
        
    
#Initialise the base graph.
M = 5
N = 5
G = nx.grid_2d_graph(M,N)

#Set the time limit.
time_limit = 40

#Navigate the graph using the customizeable seed.
seed = 8
spawn_interval = 1

navigate_graph(seed, spawn_interval)

"""
Essentially rather than running an a conflict check you need to run it parallel with the occupancy update. Move that bit into the for . i would suggest create a list of agents with current_occ, and keep updating current occupancy. 
"""

#%%

import numpy as np
import networkx as nx
import random
import copy
import matplotlib.pyplot as pl
from matplotlib import animation

#Moves an agent forward one node along its path and returns node as current_node.
def move(ID, path, current_node=None):  
    if current_node == None:
        return
    if path != []:
        current_node = path.pop(0)
        
        print("Agent {} is at position: {}".format(ID, current_node))
        print("Remaining moves: {}".format(path))
        print()
    else:
        current_node = None   
    return current_node

#Auxiliary function for recalibrate_paths. 
def recalibrate_path(graph, ID, occupancy, paths):
    
    #create graph copy
    mod_graph = copy.deepcopy(graph)

    #if next node is in occupancy, create conflict node
    if paths[ID][0] in list(occupancy.values()):
        conflict_node = paths[ID][0]
        
        mod_graph.remove_node(conflict_node)
      
            
    #calculate path
    path = nx.astar_path(mod_graph, occupancy[ID], paths[ID][-1])
    

    
    
    
    return path

#Perform move for all agents.
# def move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete, goal_nodes):
    
#     #continuously update occupancy list
#     occupancylist = list(occupancy.values())

#     #for each agent
#     for i in paths.keys():
        
#         #muststop boolean indicates whether the next move would result in a conflict.
#         muststop = False

#         #if next position is occupied, recalibrate
#         if paths[i][0] in occupancy.values():

#             paths[i] = recalibrate_path(G, i, occupancy, paths, goal_nodes)
            
#             if paths[i][0] in occupancy.values():
#                 muststop = True
                
#             print("Agent {} recalibrated. New path: {}".format(i,paths[i]))
                 
#         #if stop flagged, add same position to beginning of path so that the move does nothing
#         if muststop == True:
#             paths[i].insert(0, occupancy[i])
             
#         occupancy[i] = move(i, paths[i], current_node=occupancy[i])  

#         if paths[i] == []:
#             agents_complete.append(i)
#             all_agents_complete.append(i)

def move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete):
    #occupancy list for continuous update
    occupancylist = list(occupancy.values())

    #for each agent
    for i in paths.keys():
        
        muststop = False
        
        #reroute if next node is in the occupancy list
        if paths[i][0] in occupancylist:
                        
            paths[i] = recalibrate_path(G, i, occupancy, paths)
            
            if paths[i][0] in occupancylist:
                muststop = True
            
        if muststop == True:
            
            print("Agent {} has stopped for 1 time step.".format(i))
            
        
        else:
            occupancylist.remove(occupancy[i])  
            occupancy[i] = move(i, paths[i], occupancy[i])
            occupancylist.append(occupancy[i])
        

        #troubleshooting segment
        

                
        
        if paths[i] == []:
            agents_complete.append(i)
            all_agents_complete.append(i)
            
            

#Return a list of potential paths from a list of initial and goal vertices.
def return_all_paths(G, initial_vertices, goal_vertices):    
    paths = []
    for i in range(len(initial_vertices)):
        for j in range(len(goal_vertices)):        
            initial_vertex = initial_vertices[i]     
            goal_vertex = goal_vertices[j]           
            path = nx.astar_path(G, initial_vertex, goal_vertex)           
            paths.append(path) 
    return paths


#Uses recalibrate_path and path_duplicate_check to decide which to re-direct based on path length.
def recalibrate_paths(G, conflict_nodes, occupancy, paths, goal_nodes):
    
    #Create a subgraph from the primary graph to navigate.
    subGraph = copy.deepcopy(G)
        
    #Create a dictionary of first path elements.
    next_nodes = dict()          
    for i in paths:          
        next_nodes[i] = paths[i][0]

    #Create map of first path elements.
    nextnode_agent_map = {node:[] for _, node in next_nodes.items()}
    #Assign agent keys to dictionary.
    for agent_key, node in next_nodes.items():
        nextnode_agent_map[node].append(agent_key)
    
    #Create a conflict dictionary.
    conflicted_nodes = {node:conflicts for node, conflicts in nextnode_agent_map.items() if (len(conflicts)>1) and not (node in goal_nodes)}

    #Resolve the conflict by updating paths and occupancy.
    for conflict_node, agents in conflicted_nodes.items():

        #reroute_agents = (ID, path_length). Includes current_node.
        reroute_agents = [(agent_key, len(paths[agent_key])) for agent_key in agents]
        
        #Sort by ascending (lambda +x) or descending (lambda -x) order of path length. List of tuples (agent ID, path length).
        reroute_agents = sorted(reroute_agents, key = lambda x: x[1])
        
        #Pop shortest path from reroute_agents.
        reroute_agents.pop(0)
        
        #Recalibrate all paths marked for rerouting through local subgraphs.
        for rrt_agent_tup in reroute_agents:
            rrt_agent = rrt_agent_tup[0]
        
            subGraph, new_path = recalibrate_path(subGraph, rrt_agent, conflict_node, occupancy, paths, goal_nodes)
            
            paths[rrt_agent]  = new_path
            occupancy[rrt_agent] = paths[rrt_agent].pop(0)
    
#Return the shortest path from a single vertex to a set of goal vertices
def return_shortest_path(G, current_vertex, goal_vertices):
    all_paths = []
    for i in range(len(goal_vertices)):
        goal_vertex = goal_vertices[i]        
        path = nx.astar_path(G, current_vertex, goal_vertex)
        all_paths.append(path)
    all_paths.sort(key=len)
    shortest_path = all_paths[0]
    return shortest_path 
    
#Produce a list of initial and goal nodes from the base graph. Modify this for different selection criteria.
def initial_goal_nodes(G):    
    initial_nodes = list(G.nodes)[:3]
    #goal_nodes = list(G.nodes)[-3:]
    goal_nodes = [(2,4),(3,4),(4,4)]
    return initial_nodes, goal_nodes

#Draws the graph. For use in animate function.
def drawgraph(G, occupancy, initial_nodes, goal_nodes):
    nx.draw_networkx(G, pos = dict((n,n) for n in G.nodes()), node_color = ["yellow" if n in occupancy.values() and (n in initial_nodes or n in goal_nodes) else "red" if n in occupancy.values() else "green" if n in initial_nodes else "orange" if n in goal_nodes else "pink" for n in G.nodes()])

#Animates the graph.    
def animate(G, occupancy, initial_nodes, goal_nodes):
    fig,ax = pl.subplots()
    animation.FuncAnimation(fig, drawgraph(G, occupancy, initial_nodes, goal_nodes), frames = 1, fargs = (G, ax))    
    pl.show()
    
#Check occupancy dictionary for duplicate values by swapping key/value. Raise an exception if a conflict is found.
def duplicate_check(occupancy):
    occupancy_swap = {}
    for i, j in occupancy.items():
        if j not in occupancy_swap:
            occupancy_swap[j] = [i]
        else:
            occupancy_swap[j].append(i)
        for k in occupancy_swap.values():
            if len(k) > 1:               
                raise Exception("Duplicate occupancy detected: Agents {} at node {}".format(occupancy_swap[j], occupancy[i]))

#Check duplicate values in first path elements and return conflict_agents, which need to be re-calibrated again. Used in recalibrate_paths.
def path_duplicate_check(paths):
    next_swap = {}
    for i, j in paths.items():    
        if j[0] not in next_swap:  
            next_swap[j[0]] = [i]
        else:
            next_swap[j[0]].append(i)        
    for conflict_agents in next_swap.values():
        if len(conflict_agents) > 1:              
            raise Exception("Unresolved conflict detected: Agents {} at node {}".format(conflict_agents, j[0]))


#The primary function uses all of the above auxiliary functions to traverse a graph, avoiding collisions. Use a seed for reproducibility.
def navigate_graph(seed=0, spawn_interval = 2):    
    
    #Initialise parameters and data structures.
    occupancy, paths = dict(), dict()
    ID = 1
    offgrid = 0
    initial_nodes, goal_nodes = initial_goal_nodes(G)

    #Generate the seed.
    random.seed(seed)

    all_agents_complete = []
        
    #Loop until the time limit.
    for current_time in np.arange(0, time_limit): 
        

        
        #Check for duplicates and raise an exception if one is found.
        duplicate_check(occupancy)        
        
        #Track agents with completed paths.
        agents_complete=[]
    
        #Periodically generate an agent at a random initial node and initialise its path towards its closest of a set of goal nodes.          
        if current_time in np.arange(0, time_limit, spawn_interval):                      
            init = initial_nodes.copy()
            for node in occupancy.values():
                if node in init:
                    init.remove(node)
            if init != []:
                initial_vertex = random.choice(init)
            
            goal_node = random.choice(goal_nodes)
            paths[ID] = nx.astar_path(G, initial_vertex, goal_node)
        
        

            occupancy[ID] = paths[ID].pop(0)    

            ID = ID + 1

        print("Time: {}".format(current_time))
        print() 
        
        #recalibrate_paths(G, conflict_nodes, occupancy, paths, goal_nodes) 
        

        
        #Move all agents, and document completed paths upon successfully reaching a goal node.
        """
        or if you implement adding animate into move_all _agents, then compute animate and then remove
        """
        animate(G, occupancy, initial_nodes, goal_nodes)
        
        move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete)

        
        
        
        #Remove completed paths from the dictionary and add them to the offgrid count.
        for i in agents_complete:        
            occupancy.pop(i)
            paths.pop(i) 
            offgrid = offgrid + 1            
        
        #Count on-grid agents at the end of each time step.
        ongrid = len(paths.keys())
        
        print("Agents Currently On Grid: {}".format(ongrid))
        print("Successful Traversals: {}".format(offgrid))
        print("Completed Agent list: {}".format(all_agents_complete))
        print()
        
    
#Initialise the base graph.
M = 5
N = 5
G = nx.grid_2d_graph(M,N)

#Set the time limit.
time_limit = 100

#Navigate the graph using the customizeable seed.
seed = 8
spawn_interval = 1

navigate_graph(seed, spawn_interval)

"""
Essentially rather than running an a conflict check you need to run it parallel with the occupancy update. Move that bit into the for . i would suggest create a list of agents with current_occ, and keep updating current occupancy. 
"""

#%%
"""
Problem function:
    move_all_agents > recalibrate_path > nx.astar_path
Problem summary:
    initial node occupancy[ID] in path not in graph
Explanation:
    
"""
