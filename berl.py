class FField:
    def __init__(self, n, q):
        self.n = (n % q + q) % q  # element
        self.q = q  # modulus
    
    def __add__(self, other):
        assert self.q == other.q
        return FField(self.n + other.n, self.q)

    def __sub__(self, other):
        assert self.q == other.q
        return FField(self.n - other.n, self.q)      
    
    def __neg__(self):
        return FField(-self.n, self.q) 
    
    def __mul__(self, other):
        assert self.q == other.q
        return FField(self.n * other.n, self.q)
    
    def __eq__(self, other):
        return self.q == other.q and self.n == other.n
    
    def gcdex(self, a, b, x, y):
        if a == 0:
            return 0, 1
        x1, y1 = self.gcdex(b % a, a, 0, 0)
        return y1 - (b // a) * x1, x1
    
    def __truediv__(self, other):
        assert other.n != 0 and self.q == other.q
        x, y = self.gcdex(other.n, self.q, 0, 0)
        return FField(x * self.n, self.q)
    
    def __pow__(self, p):
        return FField(self.n ** p, self.q)
    
    def __str__(self):
        return '{} (mod {})'.format(self.n, self.q)


class Poly:
    def __init__(self, coeffs, q):
        self.coeffs = coeffs
        self.q = q
        for coef in self.coeffs:
            assert coef.q == self.q
        self.reduce()
    
    def __len__(self):
        if len(self.coeffs) == 1 and self.coeffs[0] == FField(0, self.q):
            return 0
        return len(self.coeffs)
    
    def reduce(self):
        while len(self.coeffs) > 0 and self.coeffs[-1] == FField(0, self.q):
            self.coeffs.pop()
    
    def __add__(self, other):
        assert self.q == other.q
        new_coeffs = [FField(0, self.q) for i in range(max(len(self), len(other)))]
        for i, x in enumerate(self.coeffs):
            new_coeffs[i] = new_coeffs[i] + x
        for i, x in enumerate(other.coeffs):
            new_coeffs[i] = new_coeffs[i] + x
        return Poly(new_coeffs, self.q)

    def __sub__(self, other):
        return self + -other    

    def __neg__(self):
        return Poly([-coef for coef in self.coeffs], self.q)
    
    def __mul__(self, other):
        assert self.q == other.q and type(other) == Poly
        new_coeffs = [FField(0, self.q) for i in range(len(self) + len(other))]
        for i, x in enumerate(self.coeffs):
            for j, y in enumerate(other.coeffs):
                new_coeffs[i + j] = new_coeffs[i + j] + x * y
        return Poly(new_coeffs, self.q)

    def gcdex(self, a, b, x, y):
        if a == 0:
            return Poly([FField(0, self.q)], self.q), Poly([FField(1, self.q)], self.q)
        x1, y1 = self.gcdex(b % a, a, 0, 0)
        return y1 - (b / a) * x1, x1

    def __floordiv__(self, other):
        assert self.q == other.q and len(other) != 0
        res_coefs = [FField(0, self.q) for i in range(len(self.coeffs))]
        rem = Poly([coef for coef in self.coeffs], self.q)
        print(rem)
        while len(rem) >= len(other):
            diff = len(rem) - len(other)
            other_moved = Poly([FField(0, self.q)] * diff + other.coeffs, self.q)
            other_coef = rem.coeffs[-1] / other.coeffs[-1]
            rem = rem - Poly([other_coef], self.q) * other_moved
            #rem.reduce()
            res_coefs[diff] = other_coef
        rem.reduce()
        return Poly(res_coefs, self.q), rem
    
    
    def __truediv__(self, other):
        return (self // other)[0]
    
    
    def __mod__(self, other):
        return (self // other)[1]

    def __str__(self):
        if len(self) == 0:
            return '0'
        return ' + '.join([f'{x}x^{p}'.replace(f' (mod {self.q})', '')
                           for p, x in enumerate(self.coeffs)][::-1]).replace('x^0', '') + f' (mod {self.q})'
    
    

#x = FField(10, 17)
#y = FField(25, 17)
## print(x + y, x * y, x / y, y / x, x / x)

#p = Poly([x, y, x, x, y], 17)
##print(p) 
##print(p * p)
#rem, div = p / p
##print(rem)
##print(div)

a = Poly([FField(4, 5), FField(2, 5), FField(3, 5), FField(0, 5), FField(4, 5)], 5)
b = Poly([FField(3, 5), FField(1, 5), FField(0, 5), FField(1, 5)], 5)
#r, d = a / b
print(a / b, a % b)