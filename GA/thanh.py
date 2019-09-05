import numpy as np

x = np.ones([10])
y = np.zeros([10])

tmp = np.copy(x[2:5])
x[2:5] = np.copy(y[2:5])
y[2:5] = tmp

print x
print y
