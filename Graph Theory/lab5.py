"""
Exercise A: Define the heuristic to be used for a greedy algorithm. Use Dijkstra algorithm to
obtain a list of distances, and return the location of the nearest metavertex. There may be
multiple nearest metavertices, in which case the first in the list is chosen.
"""

def choose_target(distances,pieces_of_cheese):
    
    #next target is the first in the list of pieces of cheese
    next_target = pieces_of_cheese[0]
    
    #loop over all remaining pieces 
    for vertex in pieces_of_cheese[1:]:
        
        #if the vertex distance is less than the next target
        if distances[vertex] < distances[next_target]:
            
            #set next target to vertex
            next_target = vertex
            
    return next_target

#%%

"""
Exercise B: Define movements_greedy_algorithm, which receives the graph, the metagraph and the
current vertex, and returns the location of the closest metavertex as well as the list of moves
required to travel to it. This requires use of the Dijkstra algorithm and A_to_B from utils, and
the previously defined choose_target function to return the optimal path to the nearest metavertex.
The other function is turn, which uses the algorithm just defined to receive all movements and
return the next movement.
"""

import utils

movements = list()

def movements_greedy_algorithm(maze_graph,pieces_of_cheese,player_location):
    
    # get distances using Dijkstra algorithm
    explored_vertices, parent_dict, distances = utils.Dijkstra(maze_graph, player_location)
    
    # get next_target using choose_target function
    next_target = choose_target(distances, pieces_of_cheese)
    
    # use A_to_B function to get a list of movements that should be done to reach the nearest piece of cheese
    movements = utils.A_to_B(maze_graph, player_location, next_target, parent_dict)

    return movements,next_target

def turn(maze_graph, maze_width, maze_height, player_location, opponent_location, player_score, opponent_score, pieces_of_cheese, time_allowed):
    
    global movements
    
    # if movements is empty
    if len(movements) == 0:
        
        #get list of movements for shortest path to next target
        movements, next_target = movements_greedy_algorithm(maze_graph, pieces_of_cheese, player_location)

    # return the next movement we should perform to reach next target, and remove it from list of movements  
    movement = movements.pop(0)
    
    return movement

#%%

"""
Exercise C: Define greedy_complete_graph, which receives an initial vertex (as an index) and a
graph (as an adjacency matrix) and outputs the path obtained by the closest-vertex heuristic.
Then define bruteforce_complete_graph, which uses lab 4's bruteforce algorithm to find the
shortest walk exploring every vertex. 
"""

#set infinity to an arbitrary value
infinity = 100000000

def greedy_complete_graph(graph, initial_vertex):
    
    #initialise total distance
    total_distance = 0
    
    #initialise explored list
    explored = list()
    current_vertex = initial_vertex
    explored.append(current_vertex)
    
    #create copy of graph to modify
    unexplored_graph = graph
    
    #remove explored vertex from graph
    unexplored_graph.remove(graph[current_vertex])
    
    #while there are unexplored vertices
    while unexplored_graph != []:
        
        #define distances
        distances = unexplored_graph[current_vertex]
        
        #define targets, which is the list of all vertices in the unexplored graph except the current
        vertex = 
        targets = graph.index(vertex)
        
        #obtain nearest vertex
        nearest_vertex = choose_target(distances, targets)
    
    
