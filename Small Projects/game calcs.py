import random
import numpy as np
#damage calculator


atk = 100.
defense = 50.
strength = 50.
lv = 50.
vit = 50.
spd = 50.
mdef = 50.
magic = 50.

def axe_damage():
    
    rng = random.uniform(0,1.111)
    a = atk * rng - defense
    b = 1 + strength * (lv + vit) / 128    

    if a * b > 0:
        damage = a*b
    else:
        damage = 0
    
    return int(np.floor(damage)) #fix negative

def sword_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - defense
    b = 1 + strength * (lv + strength) / 256    

    damage = a * b
    
    
    return int(np.floor(damage))

def dagger_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - defense
    b = 1 + strength * (lv + spd) / 218    

    damage = a * b
    
    return int(np.floor(damage))

def mace_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - defense
    b = 1 + magic * (lv + magic) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def katana_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - defense
    b = 1 + strength * (lv + magic) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def pole_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - mdef
    b = 1 + strength * (lv + strength) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def staff_damage():
    
    rng = random.uniform(1,1.125)
    a = atk * rng - defense
    b = 1 + strength * (lv + magic) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def gun_damage():

    damage = (atk*random.uniform(1,1.125))**2
    if damage <= 0:
        damage = 0
    return int(np.floor(damage))


def unarmed_damage():
    
    rng = random.uniform(1,1.125)
    a = 12 * rng - defense
    b = strength * (lv + strength) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def brawler_damage():
    
    rng = random.uniform(1,1.125)
    a = ((lv + strength) / 2 ) * rng - defense
    b = strength * (lv + strength) / 256    

    damage = a * b
    if a * b > 0:
        damage = a*b
    else:
        damage = 0    
    return int(np.floor(damage))

def average_damage():
    damages = []
    for i in range(1000):
        damage = sword_damage()
        damages.append(damage)
    return int(np.round(sum(damages)/len(damages)))

print("average damage: ",average_damage())















