
#%%

"""
Implement reservation dictionary to replace exclusion dictionary.
Reservation is a dictionary of {agent: [(time,node), (time2,node2)...]}
Priority based purely on spawn order - agent 1 spawns with guaranteed shortest path, and all agents generate their entire fixed path upon spawning, avoiding (time, node) pairs. 

Note: Currently only functional for spawn rate 1.
"""

import numpy as np
import networkx as nx
import random
import copy
import matplotlib.pyplot as pl
from matplotlib import animation
import time


"""
Auxiliary Functions
"""

#spawn a number of agents equal to spawn_rate.

def spawn(ID, spawn_rate, initial_nodes, goal_nodes, occupancy, paths, travelled_paths, exclusion, reservation, current_time):

    new_agent = []
    
    
    init = initial_nodes.copy()
    
    #track number of spawns this step
    counter = 0
    
    while counter < spawn_rate:

        #remove occupied initial nodes from init copy to check for free spawn spaces
        for node in occupancy.values():
            
            if node in init:
                
                init.remove(node)
                
        #assign a goal node at random
        goal_node = random.choice(goal_nodes)        
        
        #choose a random free initial node
        if init != []:
            
            initial_vertex = random.choice(init)
        
            #create a path
            """
            The following path must avoid all current time: node pairs already in the reservation dictionary.
            How to do that?
            One idea: Generate a base path, then determine whether there is a conflict. If none, validate path. If conflict, re-calculate from that step onward. Repeat this until full path to goal is generated.
            """
            path = nx.astar_path(G, initial_vertex, goal_node)
            
            #
            #
            #
            
            paths[ID] = path
            

            
            #create exclusion dictionary entry           
            exclusion[ID] = [path[0] for agent, path in paths.items() if ID != agent]
                                    
            new_agent.append(ID)
            
            """
            reserved_path = {time1: node_at_time1, time2: node_at_time2...}
            """            
            
            reserved_path = {}
            goal_time = current_time + len(paths[ID])
       
            
            for t in range(current_time,goal_time):
                reserved_path[t] = paths[ID][t-current_time]
                
            reservation[ID] = reserved_path

            occupancy[ID] = paths[ID].pop(0)   
            
            # print("Agent {} has spawned at {}".format(ID,occupancy[ID]))
            
            # print("Remaining moves: {}".format(paths[ID]))
            
            # print()
     
            ID = ID + 1
    
     
        counter = counter + 1
        
    # print(reservation)
    # print()
    
    return new_agent, ID, reservation


#Move agent ID along its path, returning its new node as current_node and removing the first element from its path. Used in move_all_agents.
def move(ID, path, current_node, new_agent, exclusion, travelled_paths):  
    
    if current_node == None:
        return

        
    #if the path isn't empty
    if path != []:
        
        #perform move and print outcome
        oldnode = current_node
                    
        current_node = path.pop(0)
                    
        # if current_node != oldnode:
        #    print("Agent {} has moved from {} to {}".format(ID, oldnode, current_node))
        
        # else:
        #    print("Agent {} is currently at {}".format(ID, current_node))
            
        # print("Exclusion: {}".format(exclusion[ID]))
            
        # print("Remaining moves: {}".format(path))
        
        # print()

    
    #if the path is empty
    else:
        
        #unassign the node, as it has reached its destination
        current_node = None   

    #travelled_paths[ID].append(current_node)
    
    #print("Path travelled so far: {}".format(travelled_paths[ID]))
    #print()
    
    return path, current_node

#re-calculate an agent's path based on the predicted paths of all other agents.
def recalibrate_path(G, ID, occupancy, paths, initial_nodes, exclusion):
    
    #create a copy of the graph and remove spawn nodes from routing.
    mod_graph = copy.deepcopy(G)
    
    mod_graph.remove_nodes_from(initial_nodes)
        
    #create copy of paths and remove empty paths
    modpaths = copy.deepcopy(paths)
    
    for i in paths.keys():
        
        if modpaths[i] == []:
            
            modpaths.pop(i)
    

    adjacent_nodes = list(G.neighbors(occupancy[ID]))

    mod_graph.remove_nodes_from([node for node in adjacent_nodes if node in exclusion[ID]])
    
    if (occupancy[ID] in mod_graph.nodes()) :
        valid_nodes = list(mod_graph.adj[occupancy[ID]].keys())
    else :
        valid_nodes = []
        
    #if all adjacent nodes are occupied, perform wait by generating a path through the primary graph and do not remove the first element. This ensures the path goal is maintained and a null move can be performed by moving to the same node.    
    if valid_nodes == []:
        
        path = nx.astar_path(G, occupancy[ID], paths[ID][-1])
        
        #WAIT
        

        
    #if a move is possible, generate a path and remove first element
    else:  
        
        #try a path, and if one cannot be generated, setup a null move.
        try:
            
            
            path = nx.astar_path(mod_graph, occupancy[ID], paths[ID][-1])
            path.pop(0)
            
        except:
            
            path = nx.astar_path(G, occupancy[ID], paths[ID][-1])
            
            #WAIT
            
    exclusion_update(exclusion, paths, occupancy)
      
    return path

def exclusion_update(exclusion, paths, occupancy):
    
    for agent in paths.keys():
        
        if paths[agent] != []:
            
#             exclusion[agent] = [path[0] for path in paths.values() if path != [] and path[0] != paths[agent][0]]
            exclusion[agent] = [occ_node for occ_ag, occ_node in occupancy.items() if occ_ag != agent]# if path != [] and path[0] != paths[agent][0]]
            
            exclusion[agent] = list(dict.fromkeys(exclusion[agent]))

        else:
            
            exclusion[agent] = []

        

def move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete, initial_nodes, goal_nodes, new_agent, exclusion, travelled_paths):
    
    #create a list of agents to move
  
    
    agents_to_move = [x for x in paths.keys()] #if x not in new agent
    
    #move all agents that have not spawned this time step
    #for paths[i in new_agent][0]: #
        #


        
    while agents_to_move != []:
            
        i = agents_to_move[0]
        
        
        #exclusion entry = first element of all other agents' paths, provided the path is not empty.
#         exclusion[i] = [path[0] for agent, path in paths.items() if i != agent and path != []]
        exclusion[i] = [occ_node for occ_ag, occ_node in occupancy.items() if occ_ag != i]# if path != [] and path[0] != paths[agent][0]]

        
        #if next path element is in exclusion
        if paths[i] != [] and paths[i][0] in exclusion[i]:
            
            oldpath = paths[i]
              
            paths[i] = recalibrate_path(G, i, occupancy, paths, initial_nodes, exclusion)

            # if paths[i][0] != oldpath[0]:
            # #  
            #     print("Agent {} recalibrated.".format(i))
            
            # else:
                
            #     print("Agent {} failed recalibration.".format(i))
            
        #perform proper or null move
        paths[i], occupancy[i] = move(i, paths[i], occupancy[i], new_agent, exclusion, travelled_paths)
        
        exclusion_update(exclusion, paths, occupancy)
        
        agents_to_move.pop(0)
  
    for agent in paths.keys():
        
        if paths[agent] == []:
            
            agents_complete.append(agent)
            
            all_agents_complete.append(agent)
    

 

            
#Draw the graph. Used in animate.
def drawgraph(G, occupancy, initial_nodes, goal_nodes):
    
    nx.draw_networkx(G, pos = dict((n,n) for n in G.nodes()), node_color = ["yellow" if n in occupancy.values() and (n in initial_nodes or n in goal_nodes) else "red" if n in occupancy.values() else "green" if n in initial_nodes else "orange" if n in goal_nodes else "grey" for n in G.nodes()],node_size = 100,with_labels=False)

#Animates the graph.  
def animate(G, occupancy, initial_nodes, goal_nodes):
    
    fig,ax = pl.subplots()
    
    animation.FuncAnimation(fig, drawgraph(G, occupancy, initial_nodes, goal_nodes), frames = 1, fargs = (G, ax))    
    pl.show()

"""
Troubleshooting Functions.
"""
#Check occupancy dictionary for duplicate values. Raise an exception if a conflict is found. To insert for troubleshooting purposes.
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

#Check duplicate values in first path elements and return conflict_agents. To insert for troubleshooting purposes. 
def path_duplicate_check(paths):
    
    next_swap = {}
    
    conflict_agents, conflict_node = None, None
    
    for i, j in paths.items():    
        
        if len(j) > 1 and j[1] not in next_swap:  
            
            next_swap[j[1]] = [i]
            
        elif len(j) > 1 and j[1] in next_swap:
            
            next_swap[j[1]].append(i)     
            
    for k in next_swap.values():
        
        if len(k) > 1:              
            
            conflict_agents = k
            
            conflict_node = j[0]
     
    return conflict_agents, conflict_node
            
"""
Primary Function.
"""

#Navigate the graph.
def navigate_graph(seed=0, spawn_rate = 1):    
    
    #initialise data lists
    on_grid = []
    number_of_spawns_total = []
    spawns_current_step = []
    off_grid = []
    off_grid_current_step = []
    
    start = time.time()
    
    occupancy, paths, exclusion, travelled_paths, reservation = dict(), dict(), dict(), dict(), dict()
    

    ID = 1
    
    offgrid = 0
    
    if spawn_rate > len(initial_nodes):
        raise Exception("Spawn rate exceeds capacity. Maximum value: {}".format(len(initial_nodes)))
        
   
    #remove edges between all initial nodes and all goal nodes
    edgeview = list(G.edges())
    
    for i in range(len(edgeview)):
        
        if edgeview[i][0] in initial_nodes or edgeview[i][0] in goal_nodes:
            
            if edgeview[i][1] in initial_nodes or edgeview[i][1] in goal_nodes:
                
                G.remove_edge(edgeview[i][0],edgeview[i][1])
    
    random.seed(seed)
    
    all_agents_complete = []
    
    new_agent = []
        
    for current_time in np.arange(0, time_limit):     
        
        agents_complete=[]
        
        #print("Time: {}".format(current_time))
        
        #print() 
     


        #animate(G, occupancy, initial_nodes, goal_nodes)
        
        duplicate_check(occupancy)
        
        oldoffgrid = offgrid
        
        for i in agents_complete:  
            
            occupancy.pop(i)
            
            paths.pop(i)
            
            offgrid = offgrid + 1   
            
        current_offgrid = offgrid - oldoffgrid
            
        ongrid = len(paths.keys())
        
        #print("Agents Currently On Grid: {}".format(ongrid))
        
        #print("Successful Traversals: {}".format(offgrid))
        
        #print("Completed Agent list: {}".format(all_agents_complete))
        
        #print()
        
        #end of time loop, collect data here
        on_grid.append(ongrid)
        number_of_spawns_total.append(ID-1)
        spawns_current_step.append(len(new_agent))
        off_grid.append(offgrid)        
        off_grid_current_step.append(current_offgrid)
       
    end = time.time()
    time_elapsed = end - start
    print("Total simulation time: {}".format(time_elapsed))

    #movetime = sum(movetime)/len(movetime)
    #spawntime = sum(spawntime)/len(spawntime)
    #animatetime = sum(animatetime)/len(animatetime)
    #print("Move times: {}".format(movetime))
    #print("Spawn times: {}".format(spawntime))
    #print("Animate times: {}".format(animatetime))

    
    
    # pl.plot(on_grid)
    # pl.title(spawn_rate)
    # pl.ylabel("Agents Currently On Grid")
    # pl.xlabel("Time Steps")
    # pl.savefig("{}a.png".format(spawn_rate))
    # pl.show()
    
    # pl.plot(number_of_spawns_total)
    # pl.title(spawn_rate)
    # pl.ylabel("Total Number of Agents Spawned")
    # pl.xlabel("Time Steps")
    # pl.savefig("{}b.png".format(spawn_rate))
    # pl.show()
    
    # pl.plot(spawns_current_step)
    # pl.title(spawn_rate)
    # pl.ylabel("Number of Actual Spawns Per Time Step")
    # pl.xlabel("Time Steps")
    # pl.savefig("{}c.png".format(spawn_rate))
    # pl.show()
    
    # pl.plot(off_grid)
    # pl.title(spawn_rate)    
    # pl.ylabel("Number of Successful Traversals")
    # pl.xlabel("Time Steps")
    # pl.savefig("{}d.png".format(spawn_rate))
    # pl.show()
   
    # pl.plot(off_grid_current_step)
    # pl.title(spawn_rate)    
    # pl.ylabel("Number of Successful Traversals Per Time Step")
    # pl.xlabel("Time Steps")
    # pl.savefig("{}e.png".format(spawn_rate))
    # pl.show()
    
"""
Parameters.
""" 

M = 10
N = 15
G = nx.grid_2d_graph(M,N)

#initial and goal nodes here
initial_nodes = [(0,1),(0,2),(0,3),(0,4),(0,0)]
goal_nodes = [(M-1,N-1),(M-2,N-1),(M-3,N-1),(M-4,N-1),(M-5,N-1)]

time_limit = 2
seed = 8
#spawn_rate = number of agents spawned per time step (maximum = number of initial nodes)

spawn_rate = 1

    
navigate_graph(seed, spawn_rate)

"""
Next stages:
    Go back to previous version (this version's changes will not be wasted as they can be iterated on later), and separate it into defined core and visualisation sections. Ensure good commenting practice and commit them to Kiran's repository.
In addition, work on familiarising yourself with Github Desktop on both Windows and Linux.
Be more thorough and take better care when visualising data. For example, run for longer and combine metrics for easy visual comparison.
Look up saving to Python binaries (pkl?) which should NOT be stored.
Make sure visualisation includes both graphical display and data analytics.

FROM KIRAN:
    store your data as chunks and save progressively as a binary, use an  iteration number or something to disntiguish each file - think of a sensible chunk of time and use it. Then post processing will involve reading those and collating as needed 

Remind yourself of the reason for this project - For a given grid size and prescribed inflow rate what is the outflow? Any and all metrics that give insight into this question are welcome.
"""

#%%
