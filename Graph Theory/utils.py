MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
from operator import itemgetter
def get_position_above(original_position):
    """
    Given a position (x,y) returns the position above the original position, defined as (x,y+1)
    """
    (x,y) = original_position
    return (x,y+1)


def get_position_below(original_position):
    """
    Given a position (x,y) returns the position below the original position, defined as (x,y-1)
    """
    (x,y) = original_position
    return (x,y-1)

def get_position_right(original_position):
    """
    Given a position (x,y) returns the position to the right of the original position, defined as (x+1,y)
    """
    (x,y) = original_position
    return (x+1,y)

def get_position_left(original_position):
    """
    Given a position (x,y) returns the position to the left of the original position, defined as (x-1,y)
    """
    (x,y) = original_position
    return (x-1,y)

def reset_game(pyrat,game,starting_point,end_point):
    pyrat.pieces = 1
    game.pieces_of_cheese = [end_point]
    game.player1_location = starting_point
    game.history["pieces_of_cheese"] = [game.convert_cheeses()]
    game.history["player1_location"] = [list(starting_point)]
    game.play_match()
    return game

def create_walk_from_parents(parent_dict,source_node,end_node):
    
    route = list()
    next_node = end_node
    while next_node != source_node:
        route.append(next_node)
        next_node = parent_dict[next_node]
    return list(reversed(route))
   
def get_direction(source_node,end_node):
    if get_position_above(source_node) == end_node:
        return MOVE_UP
    elif get_position_below(source_node) == end_node:
        return MOVE_DOWN
    elif get_position_left(source_node) == end_node:
        return MOVE_LEFT
    elif get_position_right(source_node) == end_node:
        return MOVE_RIGHT
    else:
        raise Exception("Nodes are not connected")

def walk_to_route(walk,source_node):
    
    route = list()
    for node in walk:
        direction = get_direction(source_node,node)
        route.append(direction)
        source_node = node
    return route

def is_labeled(labeled_vertices,vertex):
    return vertex in labeled_vertices

def add_to_labeled_vertices(labeled_vertices,vertex):
    labeled_vertices.append(vertex)

def heap_pop(heap):

    node,weight,parent = heap.pop(0)
    
    return (node, weight, parent)


def heap_add_or_replace(heap, triplet):
    
    add=False
    if(len(heap)==0):
        heap.append(triplet)
    
    else:
        index=len(heap)
        for i in range(len(heap)):
            if(heap[i][0]==triplet[0]):
                
                if(heap[i][1]<=triplet[1]):
                    return 0
                else:
                    heap.pop(i)
                    if(add==False):
                        index=i
                    break
                        
            if(add==False):
                if(heap[i][1]>triplet[1]):
                    index=i
                    add=True
             
        heap.insert(index,triplet)

def Dijkstra(maze_graph,sourceNode):
    # Variable storing the labeled vertices nodes not to go there again
    labeled_vertices = list()
    
    # Stack of nodes
    heap = list()
    
    #Parent Dictionary
    parent_dict = dict()
    # Distances 
    distances = dict()
    
    # First call
    initial_tuple = (sourceNode, 0, sourceNode)#Node to visit, distance from origin, parent
    heap_add_or_replace(heap,initial_tuple)
    while len(heap) > 0:
        # get the tuple  with the smallest weight from heap list using heap_pop function.
        # if tuple is not labeled:
        #     map the obtained parent in tuple as parent of the node.
        #     add node to labeled vertices.
        #     compute distance from initial point to the node.
        #     get all node's neighbor and their corresponding weights.
        #     add all these neighbor to heap.
        #     repeat this process until we visit all graph's nodes.
        #
        # YOUR CODE HERE
        #
        (node, cost, parent) = heap_pop(heap)
        if not (is_labeled(labeled_vertices, node)):
            parent_dict[node] = parent
            add_to_labeled_vertices(labeled_vertices, node)
            distances[node] = cost
            for neighbor in maze_graph[node]:
                if not (is_labeled(labeled_vertices, neighbor)):
                    heap_add_or_replace(heap, (neighbor, cost + maze_graph[node][neighbor], node))
    
    return labeled_vertices, parent_dict, distances

def A_to_B(maze_graph,node_source,node_end,parent_dict):
    
    walk = create_walk_from_parents(end_node=node_end,source_node=node_source,parent_dict=parent_dict)
    return walk_to_route(walk,node_source)

def auxbf(current_walk,best_walk,adjacency_matrix,vertices,current_distance,best_distance):
    # First we test if the current walk have gone through all vertices
    # if that is the case, we compare the current distance to the best distance
    # and in the case it is better we update the best distance and the best walk
    # if the current_walk is not finished, for each possible vertex not explored,
    # we add it and call ourself recursively    
    ### BEGIN SOLUTION
    if(len(current_walk)>len(vertices)):
        if(current_distance<best_distance):
            best_distance=current_distance
            best_walk=current_walk            
    else:
        for next_vertex in vertices:
            if not(next_vertex in current_walk):                            
                best_walk_temp, best_distance_temp = auxbf(current_walk+[next_vertex],best_walk,adjacency_matrix,vertices,current_distance + adjacency_matrix[current_walk[-1]][next_vertex],best_distance)
                
                if best_distance_temp < best_distance:
                    best_distance = best_distance_temp
                    best_walk = best_walk_temp
    ### END SOLUTION
    return best_walk,best_distance
                    
def bruteforceTSP(maze_graph,pieces_of_cheese,player_location):
    # first we compute the vertices of the meta_graph:
    vertices=create_vertices_meta_graph(pieces_of_cheese, player_location)

    # then we create the adjacency matrix of the meta graph
    adjacency_matrix = create_edge_weight_maze_graph(maze_graph,vertices)
    
    # now we can start defining our variables
    # current_distance is the length of the walk for the current exploration branch
    current_distance = 0
    # current_walk is a container for the current exploration branch
    current_walk = [player_location]
    # best_distance is an indicator of the shortest walk found so far
    best_distance = float('inf')
    # best_walk is a container for the corresponding walk
    best_walk = []
    
    # we start the exploration:
    best_walk, best_distance = auxbf(current_walk,best_walk,adjacency_matrix,pieces_of_cheese,current_distance,best_distance)
    return best_walk, best_distance

def create_vertices_meta_graph(piece_of_cheese, player_location):
    vertices_meta_graph=piece_of_cheese+[player_location]
    return vertices_meta_graph

def create_edge_weight_maze_graph(maze_graph,vertices):
    adjacency_matrix={}
    # for each vertex in vertices:
    #     considere this vertex as source vertex
    #     use this source vertex and maze_graph to browse the graph with dijkstra algorithm
    #     use adjacency_matrix to store distances between source vertex and each vertex in the graph.
    
   
    for initial_vertex in vertices:
        explored_vertices,_,distances=Dijkstra(maze_graph,initial_vertex)
        adjacency_matrix[initial_vertex] = {}
        for vertex in explored_vertices:
            adjacency_matrix[initial_vertex][vertex] = distances[vertex]
    return adjacency_matrix  



def A_to_all(maze_graph,initial_vertex,vertices):
    list_of_movement=list()
    
    best_walk,_=bruteforceTSP(maze_graph,vertices,initial_vertex)
    
    for i in range(1,len(best_walk)):
        list_of_movement.append(A_to_B(maze_graph,best_walk[i-1],best_walk[i]))
    return sum(list_of_movement,[])
    


def FIFO_pop(FIFO_queue):
    return FIFO_queue.pop(0)

movements = list()

def preprocessing(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global movements
    # this function computes the list of movements from the previous exercise
    # and store them in the variable movements
    
    movements = A_to_all(maze_graph,playerLocation,piecesOfCheese)
    
def turn_bf(maze_graph, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):    
    # this function returns the first movement in the variable movements
    # and removes it
    
    return FIFO_pop(movements)    