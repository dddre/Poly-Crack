#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from berl import *



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

