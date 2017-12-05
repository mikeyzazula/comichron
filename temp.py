import ast
import numpy as np
from io import BytesIO
file = open('./Data/1996-09.txt', 'r')

datax = np.genfromtxt("./Data/test.txt", delimiter=",")
print("hello")
for line in file:
    print(' '.join(ast.literal_eval(line)))