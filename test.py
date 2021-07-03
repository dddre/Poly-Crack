import berl
import random

# p = 3
# f = berl.Poly([berl.FField(x,p) for x in [1, -1, 0, 1]], p)
# g = berl.Poly([berl.FField(x,p) for x in [1, -1, 0, 2]], p)
# h = berl.Poly([berl.FField(x,p) for x in [1, 2]], p)
# print('f={};  g={}; h={}'.format(f,g,h))
# ff = f*g*g*h*h
# print(ff)
# print(berl.berlekamp(ff))
# ff = f*g*g*h*h*h
# print(ff)
# print(berl.berlekamp(ff))

# print('fgh', f * g * h)

errs = 0
for test in range(100):
    p = 5
    coefs = [berl.FField(random.randrange(0, p), p) for i in range(11)]
    poly = berl.Poly(coefs, p)
    b = berl.berlekamp(poly)
    mul = poly / poly
    irred = True
    for pol, pw in b:
        mul *= pol ** pw
        irred = berl.berlekamp(pol, True)
        if not irred:
            print (pol, " is reducible")
            errs += 1
    print(poly, mul)
    print(b)
    assert len(poly / mul) == 1
    
    print("TEST {} OK".format(test))
print("# errors ", errs)
p = 2
f = berl.Poly([berl.FField(x,p) for x in [0]+[-1]+[0]*(p**3-2)+[1]], p)
print(f)
b = berl.berlekamp(f)
for (g,n) in b:
    print(g, " deg ", len(g)-1, " power ", n)

print(b)
mul = berl.Poly([berl.FField(1,p)], p)
for pol, pw in b:
        mul *= pol ** pw
        irred = berl.berlekamp(pol, True)
        if not irred:
            print (pol, " is reducible")
print(mul)
assert len(f / mul) == 1