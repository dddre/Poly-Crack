import berl

p = 3
f = berl.Poly([berl.FField(x,p) for x in [1, -1, 0, 1]], p)
g = berl.Poly([berl.FField(x,p) for x in [1, -1, 0, 2]], p)
h = berl.Poly([berl.FField(x,p) for x in [1, 2]], p)
print('f={};  g={}; h={}'.format(f,g,h))
ff = f*g*g*h*h
print(ff)
print(berl.berlekamp(ff))
ff = f*g*g*h*h*h
print(ff)
print(berl.berlekamp(ff))

print('fgh', f * g * h)
