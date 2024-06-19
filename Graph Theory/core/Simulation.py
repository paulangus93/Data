"""
First version of base simulation.
Remnants of visualisation commented out.
"""

import numpy as np
import networkx as nx
import random
import copy
#import matplotlib.pyplot as pl
#from matplotlib import animation
import time

"""
Auxiliary Functions
"""

def spawn(ID, spawn_rate, initial_nodes, goal_nodes, occupancy, paths, travelled_paths, exclusion ):

    new_agent = []
    
    init = initial_nodes.copy()
    
    counter = 0
    
    while counter < spawn_rate:

        for node in occupancy.values():
            
            if node in init:
                
                init.remove(node)
                
        goal_node = random.choice(goal_nodes)        
        
        if init != []:
            
            initial_vertex = random.choice(init)
        
            paths[ID] = nx.astar_path(G, initial_vertex, goal_node)
            
            occupancy[ID] = paths[ID].pop(0)
     
            exclusion[ID] = [path[0] for agent, path in paths.items() if ID != agent]
                                    
            new_agent.append(ID)
            
            #print("Agent {} has spawned at {}".format(ID,occupancy[ID]))
            
            #print("Remaining moves: {}".format(paths[ID]))
            
            #print()
     
            ID = ID + 1
    
     
        counter = counter + 1
    
    return new_agent, ID

def move(ID, path, current_node, new_agent, exclusion, travelled_paths):  
    
    if current_node == None:
        return

    if path != []:
        
        # oldnode = current_node
                    
        current_node = path.pop(0)
                    
        # if current_node != oldnode:
        #    print("Agent {} has moved from {} to {}".format(ID, oldnode, current_node))
        
        # else:
        #    print("Agent {} is currently at {}".format(ID, current_node))
            
        # print("Exclusion: {}".format(exclusion[ID]))
            
        # print("Remaining moves: {}".format(path))
        
        # print()

    else:

        current_node = None   
    
    return path, current_node


def recalibrate_path(G, ID, occupancy, paths, initial_nodes, exclusion):
    
    mod_graph = copy.deepcopy(G)
    
    mod_graph.remove_nodes_from(initial_nodes)
        
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
          
    if valid_nodes == []:
        
        path = nx.astar_path(G, occupancy[ID], paths[ID][-1])
             
    else:  
        
        try:
        
            path = nx.astar_path(mod_graph, occupancy[ID], paths[ID][-1])
            
            path.pop(0)
            
        except:
            
            path = nx.astar_path(G, occupancy[ID], paths[ID][-1])
            
    exclusion_update(exclusion, paths, occupancy)
      
    return path

def exclusion_update(exclusion, paths, occupancy):
    
    for agent in paths.keys():
        
        if paths[agent] != []:
            
            exclusion[agent] = list(dict.fromkeys([occ_node for occ_ag, occ_node in occupancy.items() if occ_ag != agent]))

        else:
            
            exclusion[agent] = []

def move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete, initial_nodes, goal_nodes, new_agent, exclusion, travelled_paths):
    
    agents_to_move = [x for x in paths.keys()]
        
    while agents_to_move != []:
            
        i = agents_to_move[0]
        
        exclusion[i] = [occ_node for occ_ag, occ_node in occupancy.items() if occ_ag != i]
        
        if paths[i] != [] and paths[i][0] in exclusion[i]:
            
            # oldpath = paths[i]
              
            paths[i] = recalibrate_path(G, i, occupancy, paths, initial_nodes, exclusion)

            # if paths[i][0] != oldpath[0]:
            
            #     print("Agent {} recalibrated.".format(i))
            
            # else:
                
            #     print("Agent {} failed recalibration.".format(i))
            
        paths[i], occupancy[i] = move(i, paths[i], occupancy[i], new_agent, exclusion, travelled_paths)
        
        exclusion_update(exclusion, paths, occupancy)
        
        agents_to_move.pop(0)
  
    for agent in paths.keys():
        
        if paths[agent] == []:
            
            agents_complete.append(agent)
            
            all_agents_complete.append(agent)
    
           
# #Draw the graph. Used in animate.
# def drawgraph(G, occupancy, initial_nodes, goal_nodes):
    
#     nx.draw_networkx(G, pos = dict((n,n) for n in G.nodes()), node_color = ["yellow" if n in occupancy.values() and (n in initial_nodes or n in goal_nodes) else "red" if n in occupancy.values() else "green" if n in initial_nodes else "orange" if n in goal_nodes else "grey" for n in G.nodes()],node_size = 100,with_labels=False)

# #Animates the graph.  
# def animate(G, occupancy, initial_nodes, goal_nodes):
    
#     fig,ax = pl.subplots()
    
#     animation.FuncAnimation(fig, drawgraph(G, occupancy, initial_nodes, goal_nodes), frames = 1, fargs = (G, ax))    
#     pl.show()

"""
Troubleshooting Functions.
"""

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

def navigate_graph(seed=0, spawn_rate = 1):    

    on_grid, number_of_spawns_total, spawns_current_step, off_grid, off_grid_current_step, spawntime, movetime = [], [],[],[],[],[],[]
        
    # start = time.time()
    
    occupancy, paths, exclusion, travelled_paths = dict(), dict(), dict(), dict()
    
    ID = 1
    
    offgrid = 0
        
    if spawn_rate > len(initial_nodes):
        
        raise Exception("Spawn rate exceeds capacity. Maximum value: {}".format(len(initial_nodes)))
    
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
        
        # print("Time: {}".format(current_time))
        
        # print() 

        spawntime0=time.time()
        
        new_agent, ID = spawn(ID, spawn_rate, initial_nodes, goal_nodes, occupancy, paths, travelled_paths, exclusion)
        
        spawntime1=time.time()
        
        spawntime.append(spawntime1-spawntime0)       

        movetime0 = time.time()
        
        move_all_agents(G, paths, occupancy, agents_complete, all_agents_complete, initial_nodes, goal_nodes, new_agent, exclusion, travelled_paths)
        
        movetime1=time.time()
        
        movetime.append(movetime1-movetime0)

        duplicate_check(occupancy)
        
        oldoffgrid = offgrid
        
        for i in agents_complete:  
            
            occupancy.pop(i)
            
            paths.pop(i)
            
            offgrid = offgrid + 1   
            
        current_offgrid = offgrid - oldoffgrid
            
        ongrid = len(paths.keys())
        
        # print("Agents Currently On Grid: {}".format(ongrid))
        
        # print("Successful Traversals: {}".format(offgrid))
        
        # print("Completed Agent list: {}".format(all_agents_complete))
        
        # print()
        
        on_grid.append(ongrid)
        
        number_of_spawns_total.append(ID-1)
        
        spawns_current_step.append(len(new_agent))
        
        off_grid.append(offgrid)        
        
        off_grid_current_step.append(current_offgrid)
       
    # end = time.time()
    
    # time_elapsed = end - start
    
    # print("Total simulation time: {}".format(time_elapsed))

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

initial_nodes, goal_nodes = [(0,1),(0,2),(0,3),(0,4),(0,0)], [(M-1,N-1),(M-2,N-1),(M-3,N-1),(M-4,N-1),(M-5,N-1)]

time_limit = 50

seed = 8

spawn_rate = 1

start = time.time()

while spawn_rate <= 5:
    
    navigate_graph(seed, spawn_rate)
    
    spawn_rate = spawn_rate + 1

end = time.time()

print("Simulation time: {}".format(end-start))