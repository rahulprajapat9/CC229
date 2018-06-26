# -*- coding: utf-8 -*-


import numpy as np
import time

from keras.models import Sequential
from keras.layers import Dense
# Simple RNN or simpleRNN or GRU or LSTM
from keras.layers import LSTM, RNN, SimpleRNN, GRU

from keras.utils import plot_model

# Train is 0-99
list = [i for i in range(100)]
data = [list]
data = np.array(data, dtype=float)

# Test is 1-100
target = [[i for i in range(1,101)]]
target = np.array(target, dtype=float)

# reshape(x,y,z); y and z are height and width of input data matrix.
# In following code, (x) 1 is the number of dataset we are giving (here we have
# given only one 1-d vector. So we will make a rnn which has 100 recurrent
# units. so we will input all these 100 parallely. In future, you can input
# many such sequences and get output for each of those.
data = data.reshape((1, 1, 100))
target = target.reshape((1, 1, 100)) 

# ---- Model creation ----
model = Sequential()

# LSTM(future_len) layer
# Be careful which input_shape, if you make a single mistake, and you will
# end up with lots of errors. If you put return_sequences = True, then you
# get many to many rnn.
model.add(LSTM(100, input_shape=(1, 100), return_sequences=True))

# Dense implements the operation:
# output = activation(dot(input, kernel) + bias)
# where activation is the element-wise activation function passed as the
# activation argument, kernel is a weights matrix created by the layer, and
# bias is a bias vector created by the layer (only applicable if use_bias is
# True).
model.add(Dense(100))

# Before training a model, you need to configure the learning process, which
# is done via the compile method.
model.compile(
    loss='mean_absolute_error',
    optimizer='adam',
    metrics=['accuracy']
)

x_test=[i for i in range(100,200)]
x_test=np.array(x_test).reshape((1,1,100))
y_test=[i for i in range(101,201)]
y_test=np.array(y_test).reshape(1,1,100)

# loss as well as val_loss is continuously decreasing.
# acc: 0 because it has not predicted even a single item correctly.
# acc: 1 is not actually one. It comes that way because we are using
# mean_absolute_error as our loss function.
# Pretty fast, because small set of input data. Also number of epochs only
# 10000.
model.fit(
    data,
    target,
    nb_epoch=10000,
    batch_size=1,
    verbose=2,
    validation_data=(x_test, y_test)
)

plot_model(model, to_file='model.png')
print('model plot done')

predict = model.predict(x_test)
print predict