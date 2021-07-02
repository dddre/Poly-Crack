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
    
    def __eq__(self, other):
        # Сравнение с числом и элементом поля
        if isinstance(other, int):
            return self == FField(other, self.q) 
        return self.n == other.n and self.q == other.q

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
    
    def __repr__(self):
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
        if len(a) == 0:
            return b
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

    def __repr__(self):
        # Строковое представление
        if len(self) == 0:
            return '0'
        str_coefs = [f'{x}x^{p}'.replace(f' (mod {self.q})', '')
                           for p, x in enumerate(self.coeffs)][::-1]
        str_coefs = list(filter(lambda k: k[0] != '0', str_coefs))
        return (' ' + ' + '.join(str_coefs) + ' ').replace('x^0', '').replace('x^1 ', 'x ').replace(' 1x', ' x')[1:-1] + f' (mod {self.q})'
    



def SwapRows(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]

def DivideRow(A, B, row, divider):
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider

def CombineRows(A, B, row, source_row, weight):
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight

def Gauss(A, B):
    ans = []

    zero_columns_ind = [0 for x in A[0]]
    zero_columns = []
    for j in range(0, len(A[0])):
      flag = 0
      for i in range(0, len(A)):
        if(A[i][j].n != 0):
          flag = 1
      if(flag == 0):
        zero_columns_ind[j] = 1
        zero_columns.append(j)
    
    new_A = []
    for i in range(len(A)):
      cur_raw = []
      for j in range(len(A[0])):
        if(zero_columns_ind[j] == 0):
          cur_raw.append(A[i][j])
      new_A.append(cur_raw)
    A = new_A
    column = 0
    
    for i in zero_columns:
      X = [FField(0, A[0][0].q)]*len(A)
      X[i] = FField(1, A[0][0].q)
      ans.append(X)

    while (column < len(A[0])):
        current_row = None
        for r in range(column, len(A)):
            if A[r][column].n != 0:
                 current_row = r
        if current_row is None:
            column += 1
            continue
        if current_row != column:
            SwapRows(A, B, current_row, column)
        #print(column,A[column][column])
        DivideRow(A, B, column, A[column][column])
        for r in range(column + 1, len(A)):
            CombineRows(A, B, r, column, -A[r][column])
        column += 1
    rank = 0
    for i in range(len(A)-1,0,-1):
      flag = 1
      for j in range(0, len(A[i])):
        if(A[i][j].n != 0):
          flag = 0
      if(flag == 0):
        break
      rank += 1
    rank = len(A) - rank

    for ii in range(0, len(A) - rank - len(zero_columns)):
      c = [FField(0,A[0][0].q) for _ in range(len(A) - rank - len(zero_columns))]
      c[-1 - ii] = FField(1,A[0][0].q)
      new_A = [i[:rank] for i in A[:rank]]

      new_B = [FField(0,new_A[0][0].q)]*rank
      for i in range(0, len(new_A)):
        s = FField(0,new_A[0][0].q)
        for j in range(rank, len(A[0])):
          s+=A[i][j]*c[j-rank]
        new_B[i] = - s 
      
      X = [FField(0, new_A[0][0].q) for b in new_B]

      for i in range(len(new_B) - 1, -1, -1):
          s = FField(0,A[0][0].q)
          for j in range(i+1, len(new_A[i])):
              s += X[j]*new_A[i][j]
          X[i] = new_B[i] - s
      
      X += c 

      new_X = []
      j = 0
      for i in zero_columns_ind:
        if i:
          new_X.append(FField(0,new_A[0][0].q))
          
        else:
          new_X.append(X[j])
          j += 1
      
      ans.append(new_X)

    return ans, rank




def find_ord(f, g):
    # Степерь вхождения g в f
    power = 0
    q, r = f // g
    while len(r) == 0:
        power += 1
        q, r = q // g
    return power

def berlekamp(f):
    ans = []
    oldf = f    
    while len(oldf) > 1:
        f = oldf
        # print(f, f.deriv(), f.gcd(f, f.deriv()))
        dergcd = f.gcd(f, f.deriv())
        while len(dergcd) > 1 or len(dergcd) == 0:
            if len(dergcd) == 0 or len(dergcd) == len(f):
                # divide all powers by p, for Zp
                newcoefs = [f.coeffs[i] for i in range(0, len(f.coeffs), f.q)]
                f = Poly(newcoefs, f.q)
            else:
                f = f / dergcd
            dergcd = f.gcd(f, f.deriv())
            
        # print('derived f', f, len(f))
        
        if len(f) == 2:
            for p in m:
                pord = find_ord(oldf, f)
                if pord > 0:
                    oldf /= f ** pord
                    ans.append((f, pord))
            continue
        
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
        # print(matrix)
        mt = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        # print matrix
        #print('Matrix: ')
        #for i in mt:
            #print(' '.join(str(j) for j in i).replace('(mod ' + str(f.q) + ')', ''))
        
        # print('matrix ', mt)
        mtg, rank = Gauss(mt, [FField(0, f.q) for i in range(len(mt))])
        rank = len(mtg)
    
        hs = [Poly(coefs, f.q) for coefs in mtg]
        #print([str(h) for h in hs])
      
        m = [f]
        changed = True
        while changed:
            changed = False
            for ai in range(f.q):
                if changed: break
                a = Poly([FField(ai, f.q)], f.q)
                for h in hs:
                    if changed: break
                    for j in range(len(m)):
                        if changed: break                    
                        g = m[j]
                        gcd = g.gcd(g, h - a)
                        if len(gcd) > 1 and len(gcd) < len(g):
                            changed = True
                            # remove and add
                            m[j] = gcd
                            m.append(g / gcd)
                            # print([str(x) for x in m])
                            break
        
        # return ans
        for p in m:
            pord = find_ord(oldf, p)
            if pord > 0:
                oldf /= p ** pord
                ans.append((p, pord))
            
    return ans
        

def monomial(power, q):
    return Poly([FField(0, q) for i in range(power)] + [FField(1, q)], q)


if __name__ == '__main__':
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
    
    
    p = 3
    f = Poly([FField(x,p) for x in [-1,-1,0,-1,1]], p)    
    #m = berlekamp(mods)
    m = berlekamp(f)
    print(m)
