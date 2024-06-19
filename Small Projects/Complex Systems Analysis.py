#Ordered by exercise number from Sayama Textbook

#%%
# 4.5 Simulate a simple system

from pylab import *

a = 1.1

# define every function

def initialise():
    global x, result
    x = 1.
    result = [x]

def observe():
    global x, result
    result.append(x)

def update():
    global x, result
    x = a * x

# run functions over a suitable range
    
initialise()

for i in range(30):
    update()
    observe()

plot(result)
plot(show)

#%%

