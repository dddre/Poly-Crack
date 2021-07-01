from berl import *

p = 3
f = Poly([FField(x,p) for x in [-1,-1,0,-1,1]], p)
print(f)
n = len(f)
for i in range(n):
    a = [0]*(i*p)+[1]
    g = Poly([FField(x,p) for x in a], p)
    print(str(g)+" = "+str(g%f))

berlekamp(f)