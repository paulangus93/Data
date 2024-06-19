
LIFO_list = list()

def LIFO_push(LIFO_list,element):
    LIFO_list.append(element)

def LIFO_pop(LIFO_list):
    return LIFO_list.pop(-1)

#%%
#DFS LIFO

#add current vertex to list of explored vertices
def add_to_explored_vertices(explored_vertices, vertex):
    explored_vertices.append(vertex)

#return True if vertex is in the list, or False otherwise
def is_explored(explored_vertices, vertex):
    return vertex in list(explored_vertices)

def DFS(maze_graph, initial_vertex):

    #initialise list of explored vertices
    explored_vertices = list()
    
    #initialise the LIFO stack
    queuing_structure = list()
    
    #initialise parent dictionary
    parent_dict = dict()
    
    #push the initial vertex to the queue
    LIFO_push(queuing_structure, (initial_vertex, None))
    
    #while structure is not empty
    while len(queuing_structure) > 0:
        
        #pop the latest entry in the queuing structure
        vertex, parent = LIFO_pop(queuing_structure)
        
        #if the current vertex is not in explored_vertices list
        if is_explored(explored_vertices, vertex) == False:
            
            #add vertex to explored_vertices list
            add_to_explored_vertices(explored_vertices, vertex)
            
            #add vertex parent to parent_dict
            parent_dict[vertex] = parent
            
            #define neighbours of the current vertex
            def above(vertex):
               (x, y) = vertex
               return (x, y + 1)
           
            def below(vertex):
               (x, y) = vertex
               return (x, y -1) 
           
            def left(vertex):    
               (x, y) = vertex
               return (x - 1, y)
           
            def right(vertex):
               (x, y) = vertex
               return (x + 1, y)
           
           #append all neighbours of the current vertex to a list
            neighbours = list()
            neighbours.append(right(vertex))
            neighbours.append(left(vertex))
            neighbours.append(above(vertex))
            neighbours.append(below(vertex))
            
            #if neighbour corresponds to the current vertex key in maze_graph
            for i in range(len(neighbours)):
                if neighbours[i] in maze_graph[vertex].keys():                
                
                    #if the neighbour is not in the list of explored_vertices
                    if is_explored(explored_vertices,neighbours[i]) == False:
                    
                        #push the tuple (neighbour, vertex) to the LIFO stack
                        LIFO_push(queuing_structure, (neighbours[i], vertex))
                                  
        
    #return the list explored_vertices and the completed dictionary parent_dict                              
    return explored_vertices, parent_dict        

#%%

from operator import itemgetter

maze_graph = {
    (0,0): {(0,1):1,(1,0):1}, 
    (0,1): {(0,2):1,(0,0):1},
    (1,0): {(1,1):1,(0,0):1},
    (1,1): {(1,2):1,(1,0):1},
    (0,2): {(0,1):1,(1,2):1},
    (1,2): {(0,2):1,(1,1):1}
}

initial_vertex = (0,0)

explored_vertices,parent_dict = DFS(maze_graph, initial_vertex)

print("Explored vertices order: {}".format(explored_vertices))

for vertex,parent in sorted(parent_dict.items(),key=itemgetter(0,0)):
    
    print("Vertex {} is the parent of vertex {}".format(parent,vertex))
    

#%%
#BFS FIFO

#define push and pop functions
FIFO_list = list()
def FIFO_push(FIFO_list, element):
    FIFO_list.append(element)
def FIFO_pop(FIFO_list):
    return FIFO_list.pop(0)

def BFS(maze_graph, initial_vertex):

    #initialise list of explored vertices
    explored_vertices = list()
    
    #initialise the LIFO stack
    queuing_structure = list()
    
    #initialise parent dictionary
    parent_dict = dict()
    
    #push the initial vertex to the queue
    FIFO_push(queuing_structure, (initial_vertex, None))
    
    #while structure is not empty
    while len(queuing_structure) > 0:
        
        #pop the latest entry in the queuing structure
        vertex, parent = FIFO_pop(queuing_structure)
        
        #if the current vertex is not in explored_vertices list
        if is_explored(explored_vertices, vertex) == False:
            
            #add vertex to explored_vertices list
            add_to_explored_vertices(explored_vertices, vertex)
            
            #add vertex parent to parent_dict
            parent_dict[vertex] = parent
            
            #define neighbours of the current vertex
            def above(vertex):
               (x, y) = vertex
               return (x, y + 1)
           
            def below(vertex):
               (x, y) = vertex
               return (x, y -1) 
           
            def left(vertex):    
               (x, y) = vertex
               return (x - 1, y)
           
            def right(vertex):
               (x, y) = vertex
               return (x + 1, y)
           
           #append all neighbours of the current vertex to a list
            neighbours = list()
            neighbours.append(right(vertex))
            neighbours.append(left(vertex))
            neighbours.append(above(vertex))
            neighbours.append(below(vertex))
            
            #if neighbour corresponds to the current vertex key in maze_graph
            for i in range(len(neighbours)):
                
                if neighbours[i] in maze_graph[vertex].keys():                
                
                    #if the neighbour is not in the list of explored_vertices
                    if is_explored(explored_vertices,neighbours[i]) == False:
                    
                        #push the tuple (neighbour, vertex) to the LIFO stack
                        FIFO_push(queuing_structure, (neighbours[i], vertex))
                                  
        
    #return the list explored_vertices and the completed dictionary parent_dict                              
    return explored_vertices, parent_dict         

#%%


maze_graph = {
    (0,0): {(0,1):1,(1,0):1}, 
    (0,1): {(0,2):1,(0,0):1},
    (1,0): {(1,1):1,(0,0):1},
    (1,1): {(1,2):1,(1,0):1},
    (0,2): {(0,1):1,(1,2):1},
    (1,2): {(0,2):1,(1,1):1}
}

initial_vertex = (0,0)

explored_vertices,parent_dict = BFS(maze_graph, initial_vertex)

print("Explored vertices order: {}".format(explored_vertices))

for vertex,parent in sorted(parent_dict.items(),key=itemgetter(0,0)):

    print("vertex {} is the parent of vertex {}".format(parent,vertex))
    
#%%

#use the parent dictionary as input to generate a walk between two points

def create_walk_from_parents(parent_dict, initial_vertex, target_vertex):
    
    #find target_vertex in maze_graph
    current_vertex = target_vertex
    
    #create the array of vertices that will create the walk from initial_vertex to target_vertex
    walk = []    
        
    while current_vertex != initial_vertex:
        
        #find current vertex' parent in the parent_dict
        parent = parent_dict[current_vertex]
        
        #insert current vertex to start of path array: form is [(x,y), (x2,y2), (x3,y3)]    
        walk.insert(0,current_vertex)        
    
        #reassign parent to current_vertex
        current_vertex = parent
        
    #return the walk array that we defined earlier
    return walk
    
    
    
#%%

initial_vertex = (0,0)
target_vertex = (0,0)
explored_vertices,parent_dict = DFS(maze_graph,initial_vertex)
route = create_walk_from_parents(parent_dict,initial_vertex,target_vertex)
print("The route to go from vertex {} to {} is: {}".format(initial_vertex,target_vertex,route))


initial_vertex = (0,0)
target_vertex = (0,2)
explored_vertices,parent_dict = DFS(maze_graph,initial_vertex)
route = create_walk_from_parents(parent_dict,initial_vertex,target_vertex)
print("The route to go from vertex {} to {} is: {}".format(initial_vertex,target_vertex,route))

#%%

#use walk and the get_direction function to return a list of movements to get
#from initial_vertex to target_vertex

#define movement directions

MOVE_UP = "U"
MOVE_DOWN = "D"
MOVE_LEFT = "L"
MOVE_RIGHT = "R"

#define relative positions for movements to work
def above(vertex):
    (x, y) = vertex
    return (x, y + 1)
           
def below(vertex):
    (x, y) = vertex
    return (x, y -1) 
           
def left(vertex):    
    (x, y) = vertex
    return (x - 1, y)
           
def right(vertex):
    (x, y) = vertex
    return (x + 1, y)

#define a get_direction function to return a movement direction
def get_direction(initial_vertex, target_vertex):
    if above(initial_vertex) == target_vertex:
        return MOVE_UP
    
    elif below(initial_vertex) == target_vertex:
        return MOVE_DOWN
    
    elif left(initial_vertex) == target_vertex:
        return MOVE_LEFT
    
    elif right(initial_vertex) == target_vertex:
        return MOVE_RIGHT
    
    else:
        raise Exception("Vertices are not connected.")

#define the walk_to_route function
#walk is a list that is always len(directions)+1
#walk[0] = initial_vertex
#walk[-1] = target_vertex
   
def walk_to_route(walk, initial_vertex):
    global directions
    #start empty list to append directions to
    directions = list()
    
    #initialise current vertex
    current_vertex = initial_vertex
    
    #initialise next vertex
    next_vertex = walk[0]
    
    #append first direction to list
    direction = get_direction(current_vertex, next_vertex)
    directions.append(direction)
    
    #for loop for elements in walk
    for coord in range(len(walk)-1):
            
        #set current_vertex
        current_vertex = walk[coord]
            
        #set target vertex to the next in the walk
        next_vertex = walk[coord+1]
            
        #append subsequent directions to list
        direction = get_direction(current_vertex,next_vertex)
        directions.append(direction)
    
    #return directions
    return directions
#%%

#use the BFS search and all auxiliary functions to complete a function A_to_B
#which receives an initial vertex A and a target vertex B and returns the list
#of movements that should be done

#inputs
initial_vertex = (0,0)
target_vertex = (1,2)
maze_graph = {
    (0,0): {(0,1):1,(1,0):1}, 
    (0,1): {(0,2):1,(0,0):1},
    (1,0): {(1,1):1,(0,0):1},
    (1,1): {(1,2):1,(1,0):1},
    (0,2): {(0,1):1,(1,2):1},
    (1,2): {(0,2):1,(1,1):1}
}

#define the function
def A_to_B(maze_graph, initial_vertex, target_vertex):
    
    #use BFS to return explored_vertices and parent_dict
    explored_vertices, parent_dict = BFS(maze_graph, initial_vertex)
    
    #use create_walk_from_parents to return walk from parent_dict, initial_vertex and target_vertex
    walk = create_walk_from_parents(parent_dict, initial_vertex, target_vertex)
    
    #get the list of directions from walk_to_route
    directions = walk_to_route(walk, initial_vertex)
    
    return directions
    
#%%
#
# AUTOGRADER TEST - DO NOT REMOVE
#

a = (0,0)
b = (1,2)
print("The route from {} to {} is {}".format(a,b,A_to_B(maze_graph,a,b)))
print("The route from {} to {} is {}".format(b,a,A_to_B(maze_graph,b,a)))

#%%

#all definitions used as a list
def add_to_explored_vertices(explored_vertices, vertex):
    explored_vertices.append(vertex)
def is_explored(explored_vertices, vertex):
    return vertex in list(explored_vertices)

FIFO_list = list()
def FIFO_push(FIFO_list, element):
    FIFO_list.append(element)
def FIFO_pop(FIFO_list):
    return FIFO_list.pop(0)

def BFS(maze_graph, initial_vertex):
    explored_vertices = list()
    queuing_structure = list()
    parent_dict = dict()
    FIFO_push(queuing_structure, (initial_vertex, None))
    while len(queuing_structure) > 0:
        vertex, parent = FIFO_pop(queuing_structure)
        if is_explored(explored_vertices, vertex) == False:
            add_to_explored_vertices(explored_vertices, vertex)
            parent_dict[vertex] = parent
            def above(vertex):
               (x, y) = vertex
               return (x, y + 1)           
            def below(vertex):
               (x, y) = vertex
               return (x, y -1)            
            def left(vertex):    
               (x, y) = vertex
               return (x - 1, y)           
            def right(vertex):
               (x, y) = vertex
               return (x + 1, y)          
            neighbours = list()
            neighbours.append(right(vertex))
            neighbours.append(left(vertex))
            neighbours.append(above(vertex))
            neighbours.append(below(vertex))
            for i in range(len(neighbours)):                
                if neighbours[i] in maze_graph[vertex].keys():                 
                    if is_explored(explored_vertices,neighbours[i]) == False:
                        FIFO_push(queuing_structure, (neighbours[i], vertex))
    return explored_vertices, parent_dict

def create_walk_from_parents(parent_dict, initial_vertex, target_vertex):
    current_vertex = target_vertex
    walk = []        
    while current_vertex != initial_vertex:
        parent = parent_dict[current_vertex]
        walk.insert(0,current_vertex)        
        current_vertex = parent
    return walk
    
MOVE_UP = "U"
MOVE_DOWN = "D"
MOVE_LEFT = "L"
MOVE_RIGHT = "R"

def above(vertex):
    (x, y) = vertex
    return (x, y + 1)
def below(vertex):
    (x, y) = vertex
    return (x, y -1) 
def left(vertex):    
    (x, y) = vertex
    return (x - 1, y)        
def right(vertex):
    (x, y) = vertex
    return (x + 1, y)

def get_direction(initial_vertex, target_vertex):
    if above(initial_vertex) == target_vertex:
        return MOVE_UP
    elif below(initial_vertex) == target_vertex:
        return MOVE_DOWN
    elif left(initial_vertex) == target_vertex:
        return MOVE_LEFT
    elif right(initial_vertex) == target_vertex:
        return MOVE_RIGHT
    else:
        raise Exception("Vertices are not connected.")
        
def walk_to_route(walk, initial_vertex):
    global directions
    directions = list()
    current_vertex = initial_vertex
    next_vertex = walk[0]
    direction = get_direction(current_vertex, next_vertex)
    directions.append(direction)
    for coord in range(len(walk)-1):
        current_vertex = walk[coord]
        next_vertex = walk[coord+1]
        direction = get_direction(current_vertex,next_vertex)
        directions.append(direction)
    return directions
