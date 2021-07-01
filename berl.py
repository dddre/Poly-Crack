# -*- coding: utf8 -*-

class FField:
    def __init__(self, n, q):
        # Консруктор, при инициализации берет число по модулю
        self.n = (n % q + q) % q  # element
        self.q = q  # modulus
    
    def __add__(self, other):
        # Сложение, результат по модулю
        assert self.q == other.q
        return FField(self.n + other.n, self.q)

    def __sub__(self, other):
        # Вычитание, результат по модулю
        assert self.q == other.q
        return FField(self.n - other.n, self.q)      
    
    def __neg__(self):
        # Обратный по сложению, результат по модулю
        return FField(-self.n, self.q) 
    
    def __mul__(self, other):
        # Умножение, результат по модулю
        assert self.q == other.q
        return FField(self.n * other.n, self.q)
    
    def __eq__(self, other):
        # Сравнение по модулю
        return self.q == other.q and self.n == other.n
    
    def gcdex(self, a, b, x, y):
        # Расширенный алгоритм Евклида
        if a == 0:
            return 0, 1
        x1, y1 = self.gcdex(b % a, a, 0, 0)
        return y1 - (b // a) * x1, x1
    
    def __truediv__(self, other):
        # Взятие обратного по модулю
        assert other.n != 0 and self.q == other.q
        x, y = self.gcdex(other.n, self.q, 0, 0)
        return FField(x * self.n, self.q)
    
    def __pow__(self, p):
        # Возведение в степень(не быстрое)
        return FField(self.n ** p, self.q)
    
    def __str__(self):
        # Строковое представление
        return '{} (mod {})'.format(self.n, self.q)


class Poly:
    def __init__(self, coeffs, q):
        # Конструктор, коэффициенты не по модулю, а какие дали!
        self.coeffs = coeffs
        self.q = q
        for coef in self.coeffs:
            assert coef.q == self.q
        self.reduce()
    
    def __len__(self):
        # Длинна полинома(aka Степень)
        if len(self.coeffs) == 1 and self.coeffs[0] == FField(0, self.q):
            return 0
        return len(self.coeffs)
    
    def reduce(self):
        # Удаление лишних нулей
        while len(self.coeffs) > 0 and self.coeffs[-1] == FField(0, self.q):
            self.coeffs.pop()
    
    def __add__(self, other):
        # Сложение 
        assert self.q == other.q
        new_coeffs = [FField(0, self.q) for i in range(max(len(self), len(other)))]
        for i, x in enumerate(self.coeffs):
            new_coeffs[i] = new_coeffs[i] + x
        for i, x in enumerate(other.coeffs):
            new_coeffs[i] = new_coeffs[i] + x
        return Poly(new_coeffs, self.q)

    def __sub__(self, other):
        # Вычитание
        return self + -other    

    def __neg__(self):
        # Унарный минус
        return Poly([-coef for coef in self.coeffs], self.q)
    
    def __mul__(self, other):
        # Умножение
        assert self.q == other.q and type(other) == Poly
        new_coeffs = [FField(0, self.q) for i in range(len(self) + len(other))]
        for i, x in enumerate(self.coeffs):
            for j, y in enumerate(other.coeffs):
                new_coeffs[i + j] = new_coeffs[i + j] + x * y
        return Poly(new_coeffs, self.q)

    def gcdex(self, a, b, x, y):
        # Расширенный алгоритм Евклида
        if len(a) == 0:
            return Poly([FField(0, self.q)], self.q), Poly([FField(1, self.q)], self.q)
        x1, y1 = self.gcdex(b % a, a, 0, 0)
        return y1 - (b / a) * x1, x1

    def gcd(self, a, b):
        # Не расширенный алгоритм евклида
        if len(b) == 0:
            return a
        return self.gcd(b, a % b)
    
    def deriv(self):
        # Производная
        res_coefs = [FField(i + 1, self.q) * c for i, c in enumerate(self.coeffs[1:])]
        return Poly(res_coefs, self.q)

    def __floordiv__(self, other):
        # Деление которое возвращает частное и остаток
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
        # Частное
        return (self // other)[0]
    
    
    def __pow__(self, p):
        if p == 0:
            return Poly([FField(1, self.q)], self.q)
        elif p % 2 == 1:
            return self ** (p - 1) * self
        else:
            sqrt = self ** (p // 2)
            return sqrt * sqrt
    
    def __mod__(self, other):
        # Остаток
        return (self // other)[1]

    def __str__(self):
        # Строковое представление
        if len(self) == 0:
            return '0'
        str_coefs = [f'{x}x^{p}'.replace(f' (mod {self.q})', '')
                           for p, x in enumerate(self.coeffs)][::-1]
        str_coefs = list(filter(lambda k: k[0] != '0', str_coefs))
        return (' ' + ' + '.join(str_coefs) + ' ').replace('x^0', '').replace('x^1 ', 'x ').replace(' 1x', ' x')[1:-1] + f' (mod {self.q})'
    

def find_ord(f, g):
    # Степерь вхождения g в f
    power = 0
    q, r = f // g
    while len(r) == 0:
        power += 1
        q, r = q // g
    return power

def berlekamp(f):
    dergcd = f.gcd(f, f.deriv())
    oldf = f
    f = f / dergcd
    # Polynomials x^q^l
    pols = []
    for l in range(len(f) - 1):
        pols.append(monomial(f.q, f.q) ** l % f)
        # print('mnogochlen ', pols[-1])
        # TODO this is char of field not amount of elements
    matrix = [pol.coeffs for pol in pols]
    for i in range(len(matrix)):
        matrix[i] += [FField(0, f.q)] * (len(matrix) - len(matrix[i]))
        matrix[i][i] -= FField(1, f.q)
        
    # transpose matrix
    mt = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    # print matrix
    print('Matrix: ')
    for i in mt:
        print(' '.join(str(j) for j in i).replace('(mod 2)', ''))
    return

def monomial(power, q):
    return Poly([FField(0, q) for i in range(power)] + [FField(1, q)], q)


##x = FField(10, 17)
##y = FField(25, 17)
### print(x + y, x * y, x / y, y / x, x / x)

##p = Poly([x, y, x, x, y], 17)
###print(p) 
###print(p * p)
##rem, div = p / p
###print(rem)
###print(div)

#a = Poly([FField(4, 5), FField(2, 5), FField(3, 5), FField(0, 5), FField(4, 5)], 5)
#b = Poly([FField(3, 5), FField(1, 5), FField(0, 5), FField(1, 5)], 5)
##r, d = a / b
##print(a / b, a % b)

#print(a, 'der', a.deriv())

#print(a, find_ord(a, a), find_ord(a * a * a * a, a))

x8 = Poly([FField(0, 2), FField(0, 2), FField(0, 2), FField(0, 2), 
           FField(0, 2), FField(0, 2), FField(0, 2), FField(0, 2), FField(1, 2)], 2)
mods = Poly([FField(1, 2), FField(0, 2), FField(0, 2), FField(0, 2), FField(1, 2), FField(1, 2)], 2)
#print(x8, mods)
#print(x8 % mods)

berlekamp(mods)