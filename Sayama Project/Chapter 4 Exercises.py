#Ordered by exercise number from Sayama Textbook

#%%
# 4.5 Simulate a simple system

import matplotlib.pyplot as pl

#vary this parameter and observe its effect
a = -1.1

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
    
initialise()

for i in range(30):
    update()
    observe()

pl.plot(result)
pl.show()

#%%
# 4.6 Simulate a similar system with time steps and an additional constant

import matplotlib.pyplot as pl

#vary these parameters and observe their effects
a = 0.5
b = 0.6

def initialise():
    global x, result, t, step
    x = 1.
    result = [x]
    t = 0.
    step = [t]
    
def observe():
    global x, result, t, step
    result.append(x)
    step.append(t)
    
def update():
    global x, t
    x = a * x + b
    t = t + 1.

initialise()
while t <= 30.:
    update()
    observe()
    
pl.plot(step, result)
print(result)

#%%
# 4.7 Simulate a 2 variable system and observe the different behaviours
# Don't need time step for this one.

import matplotlib.pyplot as pl

a = -0.1
b = -0.9

def initialise():
    global x, y, xresult, yresult
    x = 1.
    y = 1.
    xresult = [x]
    yresult = [y]
    
def observe():
    global x, y, xresult, yresult
    xresult.append(x)
    yresult.append(y)

def update():
    global x, y
    x2 = a * x + y
    y2 = b * x + y
    x, y = x2, y2
    
initialise()

for i in range(300):
    update()
    observe()    

#plot x, y progression    
pl.plot(xresult, 'b-')
pl.plot(yresult, 'r-')
pl.show()

#plot in x-y phase space to see their relationship more clearly
pl.plot(xresult, yresult)
pl.show()

#%%
#4.8 Simulate the behaviour of the Fibonnacci Sequence

import matplotlib.pyplot as pl


def initialise():
    global x, xprev, result
    x = 1.
    xprev = 1.
    result = [xprev, x]
    
def observe():
    global x, result
    result.append(x)

def update():
    global x, xprev
    x = x + xprev
    xprev = x - xprev
    
initialise()

for i in range(12):
    update()
    observe()
    
pl.plot(result)
pl.show()

#%%
#4.9 Simulate population growth

import matplotlib.pyplot as pl

initial = 100
capacity = 100000
a = 1.1

k = capacity

def initialise():
    global x, result
    x = initial
    result = [x]

def observe():
    global x, result
    result.append(x)
    
def update():
    global x
    x = ((1 - a) * x / k + a) * x

initialise()
    
for i in range(200):
    update()
    observe()

pl.plot(result)
pl.show()
    
#%%
#4.10 Simulate population growth with a more complex growth factor.

import matplotlib.pyplot as pl
import math

initial = 10
capacity = 1000
a = 1.1

def initialise():
    global x, result
    x = initial
    result = [x]

def observe():
    global x, result
    result.append(x)
    
def update():
    global x
    k = capacity
    x = ((1 - a) * x / k + a) * x
    
def update1():
    global x
    if x <= k:
        x = a * x / k
    else:
        x = 2 * a - a * x / k
    
def update2():
    global x
    if x <= k:
        growth = (a - 1) * x / k + 1
    else:
        growth = -(a - 1) * x / k + 2 * a - 1
    x = growth * x

def update3():
    global x
    x = a * math.exp(-((x - b)**2) / (2 * c**2))
    
def update4():
    global x    
    b = capacity
    c = 0.4
    x = x * (a - 1) * math.exp(-((x - b)**2) / (2 * c**2))

    
initialise()
    
for i in range(100):
    update4()
    observe()

pl.plot(result)
print(result)

#come back to this one optionally, to figure out gaussian growth

#%%
#4.11 Simulate a predator-prey system
#4.12 Vary parameters and document their effects.

import matplotlib.pyplot as pl

prey = 1
predator = 1
k = 5
r = 1
b = 1
d = 1
c = 1

def initialise():
    global x, y, resultx, resulty
    x = prey
    y = predator
    resultx = [x]
    resulty = [y]

def observe():
    global x, y, resultx, resulty
    resultx.append(x)
    resulty.append(y)

def update():
    global x, y
    x2 = x + r * x * (1 - (x / k)) - (1 - (1 / (b * y + 1))) * x
    y2 = y - d * y + c * x * y
    x, y = x2, y2
    
initialise()

for i in range(20000):
    update()
    observe()
    
pl.plot(resultx)
pl.plot(resulty)
pl.show()

pl.plot(resultx, resulty, 'b-', linewidth = 0.5)
pl.xlabel('Prey Population')
pl.ylabel('Predator Population')

pl.show()
print('x = ', resultx[-1])
print('y = ', resulty[-1])

#%%
#4.13 Revise the above model to fix the invalid behaviours

import matplotlib.pyplot as pl

prey = 1
predator = 1
k = 5
r = 1
b = 1
d = 1
c = 1

def initialise():
    global x, y, resultx, resulty
    x = prey
    y = predator
    resultx = [x]
    resulty = [y]

def observe():
    global x, y, resultx, resulty
    resultx.append(x)
    resulty.append(y)

def update():
    global x, y
    x2 = x + r * x * (1 - (x / k)) - (1 - (1 / (b * y + 1))) * x
    y2 = y - d * y + c * x * y
    x, y = x2, y2
    
initialise()

for i in range(200):
    update()
    observe()
    
pl.plot(resultx, label = 'Prey')
pl.plot(resulty, label = 'Predators')
pl.xlabel('Time Step')
pl.ylabel('Population')
pl.legend()
pl.show()

pl.plot(resultx, resulty, 'b-')
pl.xlabel('Prey Population')
pl.ylabel('Predator Population')

pl.show()
print('x = ', resultx[-1])
print('y = ', resulty[-1])

    
