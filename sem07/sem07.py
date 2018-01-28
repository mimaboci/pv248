import numpy as np
import re
from collections import Counter

matrix = np.loadtxt('matrix.txt')
print("matrix:\n", matrix)
determinant = np.linalg.det(matrix)
print("determinant:\n{}".format(determinant))
inverse = np.linalg.inv(matrix)
print("inverse:\n{}".format(inverse))

matrix2 = np.loadtxt('matrix2.txt')
[a, b] = np.hsplit(matrix2, [3])
res = np.linalg.solve(a, b)
print("\n matrix:\n", matrix2)
print("x1={:.2}, x2={:.2}, x3={:.2}"
      .format(res[0][0], res[1][0], res[2][0]))

f = open('equations.txt', 'r')
r = re.compile(r'(.*)[ ]*=[ ]*(.*)')
b = []
vars_values = []
               
for eq in f:
    m = r.match(eq)
    left = m.group(1).split()
    right = int(m.group(2))
    b.append(right)

    vars_ = Counter()
    number = 1
    sign = 1
    for word in left:
        if word.isnumeric():
            number = int(word)
        elif word == '-':
            sign = -1
        elif word == '+':
            sign = 1
        else:
            vars_[word] = sign*number
            number = 1
     
    vars_values.append(list(vars_.values()))

vars_names = list(vars_.keys())
a = np.array(vars_values)
res = np.linalg.solve(a,b)
print("\n equations: ")
print(a)
print(b)
print("solution: ")
for i in range(0, len(res)):
    print("{}={:.2}".format(vars_names[i], res[i]))
    
f.close()
