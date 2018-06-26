import scipy
from matplotlib import pyplot
import random
import time
import numpy


x = [value*random.random() for value in range(200)]
train_fraction = 0.8
x_train = x[:int(len(x)*train_fraction)]
x_test = x[int(len(x)*train_fraction + 1):]
train_end = x[int(len(x)*train_fraction)]

pyplot.plot(x_train, color='b')
pyplot.plot(x_test, color='r')
pyplot.show()

X = scipy.fft(x_train)

print numpy.absolute(X[0])

time.sleep(55)

X_noiseless = []
for item in X:
    if item < max(X)/100:
        pass
    else:
        X_noiseless.append(item)

print(X_noiseless)
#pyplot.plot(X, 'o')
#pyplot.show()