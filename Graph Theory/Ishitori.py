"""
The goal with this project is to write a simple game of Ishitori using graph theory.

Rules:
    
1. Two players take turns removing stones from a pile of a known, random size.
2. The player must remove between 1 and 3 stones during their turn.
3. When there is one stone left after a move, the other player loses.
    
Technical Information:
    
1. The "graph" is a list of vertices, each of which describes the entire state of the game.
2. Each "edge" in the graph represents a move which changes the game state.

A single vertex contains information pertaining to which person's turn it is and the number of 
stones left in the pile. From each vertex is up to 3 edges corresponding to the removal of 
that many stones from the pile. Player 1's goal is to travel to the nearest vertex for which
there is 1 stone left and it is currently Player 2's turn.

The first vertex is of the form [N, 0/1], where 0/1 depends on the player turn and N is the
current number of stones.
"""

from random import randint
import support

#print the message which informs the player of the initial state of the game.
print("Let's play a game of Ishitori.")
print("The rules are simple.")
print("Two players take turns removing stones from a pile of a known, random size.")
print("The player must remove between 1 and 3 stones during their turn.")
print("When there is one stone left after a move, the other player loses.")
print()
    
#initialise the number of stones
initial_stone_count = 5

#display the initial state of the game
print("There are {} stones in the pile.".format(str(initial_stone_count)))

#decide who goes first
who_goes_first = randint(0,1)    

#display which player goes first    
print("Player {} goes first.".format(str(who_goes_first+1)))
print()

#determine initial state of the game
initial_vertex = [initial_stone_count, who_goes_first]

#create parent dictionary
parent_dict = create_parent_dict(initial_stone_count)

#visualise parent_dict, starting vertex and target vertex.
visualise(parent_dict, who_goes_first, initial_stone_count)

current_vertex = initial_vertex

remova1(parent_dict, current_vertex)





 




