import berl
import random

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


for test in range(1000):
    p = 11
    coefs = [berl.FField(random.randrange(0, p), p) for i in range(11)]
    poly = berl.Poly(coefs, p)
    b = berl.berlekamp(poly)
    mul = poly / poly
    for pol, pw in b:
        mul *= pol ** pw
    # print(poly, mul)
    assert len(poly / mul) == 1
    print("TEST {} OK".format(test))
    