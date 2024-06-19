"""
Create a simple 3-body simulation to calculate the motions of 3 particles given their initial masses, coordinates and velocities in two dimensions.

Each particle is represented by an array which is updated at each time step.
[mass, [x_coord, y_coord], [x_velocity, y_velocity], [x_a], [y_a]]

Begin with the pythagorean arrangement.

Question: Is it important to keep each particle distinct? Does it affect simulation complexity?
"""
import numpy as np
#initiate all values here
particle_state_1 = [3., [0., 4.], [0., 0.], [0., 0.]]
particle_state_2 = [4., [3., 0.], [0., 0.], [0., 0.]]
particle_state_3 = [5., [0., 0.], [0., 0.], [0., 0.]]

state = {1: particle_state_1, 2: particle_state_2, 3: particle_state_3}

"""
Calculate the instantaneous gravitational acceleration of each particle at t=0
a = g*m/r**2
"""

#gravitational constant
g =  6.6743e-11

def update_acceleration(state):
    for i in state.keys():
        for j in state.keys():
            if i == j:
                accel_component = [0.,0.]
            else:
                accel_component = 
        state[i][3] = ["x_accel, y_accel"]        

update_acceleration(state)    
print(state)