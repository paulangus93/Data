initial_vertex = 0

graph = [[0, 20, 24, 28, 30],[20, 0, 21, 22, 27],[24, 21, 0, 23, 16],[28, 22, 23, 0, 30],[30, 27, 16, 30, 0]]

total_distance = 0

explored = list()

current_vertex = initial_vertex

explored.append(current_vertex)

unexplored_graph = graph

print(unexplored_graph)

print(graph[initial_vertex])

unexplored_graph.remove(graph[current_vertex])
print(unexplored_graph)

