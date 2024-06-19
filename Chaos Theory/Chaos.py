#find the chaotic regimes in an iterative system

import matplotlib.pyplot as pl

def chaos(r, initial):
    x = []
    n = []
    x.append(initial)
    points = 150
    for i in range(points):
        xnew = r * x[i] - x[i] ** 3.
        x.append(xnew)
    for j in range(points + 1):
        n.append(j)
    pl.plot(n, x, 'rx-', linewidth = 0.8)

r = 0.01

initial = 0.5

while r <= 3:
    chaos(r, initial)
    pl.title('r = ', round(r,2))
    pl.xlabel('n')
    pl.ylabel('x')
    r = r + 0.01
    pl.show()
    
#%%

#Create a bifurcation map of the above system

import matplotlib.pyplot as pl

def chaos2(r, initial, rend, inc):
    x = []
    rstore = r
    r = []
    r.append(rstore)
    while rstore <= rend:
        n = 1
        xstorage = []
        xstore = initial
        while n <= 10000:
            xstore = r[-1] * xstore - xstore ** 3.
            n = n + 1 
            if n >= 8000:
                xstorage.append(xstore)
            else:
                continue
        rstore = rstore + inc
        r.append(rstore)
        x.append(xstorage)
        print(x)
    if initial >= 0:
        pl.plot(r[1:], x, 'b.', markersize = 0.05, alpha = 0.1)
    else:
        pl.plot(r[1:], x, 'r.', markersize = 0.05, alpha = 0.1)
    pl.xlabel('r')
    pl.ylabel('x')
    
inc = 0.001

r = 1.

rend = 3.

initial = 0.9

chaos2(r, initial, rend, inc)

initial = -0.9

chaos2(r, initial, rend, inc)

pl.figure(figsize = (20,20))

pl.savefig('bifurcation.eps', format = 'eps', dpi = 1200)