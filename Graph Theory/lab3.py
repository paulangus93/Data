"""
Implement a Dijkstra algorithm to find a minimum spanning tree of a weighted
graph. The primary data structure used is a min-heap of the form
(vertex, distance_estimation, this_parent). Ensure the list of triplets is
in ascending order of estimated distances, and that each vertex exists only
once. This is done so that popping the first element always pops the smallest
value.
"""

#return the first element of the list if it is not empty, using heap_pop(heap)
#this also functions to remove the first element from the list.
def heap_pop(heap):
    if heap != []:
        vertex, weight, parent = heap.pop(0)
        return (vertex, weight, parent)
    else:
        raise Exception('List is empty.')

example_triplet_heap=[
    ((1,1),2,(1,0)),
    ((1,2),4,(0,2)),
    ((2,1),18,(2,0))
]

(vertex, distance, parent) = heap_pop(example_triplet_heap)
print("The element of the heap of minimum distance contains as vertex: {}, as distance: {}, and as parent: {}".format(vertex,distance,parent))
#%%

"""
add_or_replace is similar to push but considers estimated distances. Also,
duplicate vertices must be avoided - if a smaller value is obtained, it
replaces the original, but if a larger or equal value is obtained, it is
discarded.
"""
#add triplet to heap so that the triplets remain in ascending distance order.
#triplet is (vertex, weight, parent).

def heap_add_or_replace(heap, triplet):
    
    #tag state with "added" when appropriate - initialise to False
    added = False
    
    #loop over all heap elements
    for i in range(0,len(heap)):

        if not added:
                
                #if vertex is in the heap and distance is less than one in the heap, update the ith element to the triplet
                if triplet[0] == heap[i][0]:

                    if triplet[1] < heap[i][1]:

                        heap[i] = triplet
                    
                    return
                
                #if distance is less than one in the heap and vertex is not in the heap, insert the triplet at index i and update added to True
                elif triplet[1] < heap[i][1]:
                    
                    heap.insert(i, triplet)
                    
                    added = True
        
        #if added and the vertex exists in the heap, pop the ith value.
        elif triplet[0] == heap[i][0]:
            
            heap.pop(i)
            
            return
    
    #if not added yet, simply append triplet to heap
    if not added:
        
        heap.append(triplet)

#%%

"""
Define the Dijkstra function to find the optimal distance and an optimal parent for each vertex.
It receives a graph and a starting vertex, and either retrieves the smallest weight or adds a
triplet to the heap. It returns explored vertices in order of visits, the parent of each vertex,
and the distance from the starting point to each vertex. is_explored and add_to_explored_vertices
are necessary definitions.
"""

def is_explored(explored_vertices, vertex):
    return vertex in explored_vertices

def add_to_explored_vertices(explored_vertices, vertex):
    explored_vertices.append(vertex)
    
def Dijkstra(maze_graph, initial_vertex):
    
    #store explored vertices and initialise the heap
    explored_vertices, heap = list(), list()
    
    #dictionaries for parents and distances
    parent_dict, distances = dict(), dict()
    
    #initialise vertex
    initial_vertex = (initial_vertex, 0, initial_vertex)
    
    #use add/replace function to add the initial vertex to the heap.
    heap_add_or_replace(heap, initial_vertex)
    
    #the following occurs only when the heap is not empty
    while len(heap) > 0:
        
        #pop the heap to obtain vertex, distance and parent triplet
        vertex, distance, parent = heap_pop(heap)
        
        #check if vertex is explored. Following loop acts if False.
        if is_explored(explored_vertices, vertex) == False:
            
            #mark vertex as explored
            add_to_explored_vertices(explored_vertices, vertex)
            
            #map the vertex to its parent and distance
            parent_dict[vertex], distances[vertex] = parent, distance
            
            #loop over maze graph neighbours
            for adjacent in maze_graph[vertex]:
                
                #define weight
                weight = maze_graph[vertex][adjacent]
                
                #if not explored
                if is_explored(explored_vertices, adjacent) == False:
                    
                    #use add/replace function for values of distance + weight
                    triplet = (adjacent, distance + weight, vertex)
                    heap_add_or_replace(heap, triplet)     
    
    #return values
    return explored_vertices, parent_dict, distances
    
#%%
"""
Dijkstra has obtained all of the shortest distances from initial vertex, so we can now obtain
the corresponding walks by defining the A_to_B function. This uses walk_to_route and
create_walk_from_parents, receives an initial and target vertex, and returns a list of movements
that correspond to the shortest path.
"""
import utils

def A_to_B(maze_graph, initial_vertex, target_vertex):
    
    #use the Dijkstra algorithm to generate the parent_dict
    explored_vertices, parent_dict, distances = Dijkstra(maze_graph, initial_vertex)
    
    #use utils.create_walk_from_parents to generate a walk from initial to target vertex
    utils.create_walk_from_parents(parent_dict, initial_vertex, target_vertex)
    
    #use utils.walk_to_route to return a list of movements
    utils.walk_to_route(walk, initial_vertex)
