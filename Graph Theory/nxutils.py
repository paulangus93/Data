"""
The return_all_paths function takes a graph and a list of initial and goal vertices, and returns an A* path from every initial vertex to every goal vertex.
"""
def return_all_paths(G, initial_vertices, goal_vertices):
    
    paths = list()
    
    for i in range(len(initial_vertices)):
        
        for j in range(len(goal_vertices)):
        
            initial_vertex = initial_vertices[i]
            
            goal_vertex = goal_vertices[j]
            
            path = nx.astar_path(G, initial_vertex, goal_vertex)
            
            paths.append(path)
    
    return paths

"""
The move function takes an entity ID and its path, pops the first element of path to update the current vertex, and adds 1 to the time counter. If the path is empty, move the entity off the grid.
"""

def move(ID, path):
    
    global current_vertex
    
    if path != []:

        current_vertex = path.pop(0)
        
        print("Entity {} is at position: {}".format(ID, current_vertex))
        
        print("Remaining moves: {}".format(path))
    
        print()
        
    
    else:
        
        current_vertex = None
                   

"""
The generate_entity function causes an entity to spawn at the designated initial_vertex, bound for its goal_vertex by generating an A* path between those two points. The entity has an ID equal to the order in which it was spawned (beginning with 1).
"""

def generate_entity(ID, initial_vertex, goal_vertex):
    
    state[ID] = nx.astar_path(G, initial_vertex, goal_vertex)
    
    occupancy[ID] = state[ID][1] 
    
    
    

    

        
        
    