# -*- coding: utf-8 -*-
"""
Edited Version - Haijia

"""

# importing libs# import
import numpy as np
import tensorflow as tf
from keras.layers import Input, Dense, GaussianNoise
from keras.models import Model
from keras import regularizers
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD
import random as rn

# defining parameters
M = 4
k = np.log2(M)
k = int(k)
print ('M:', M, 'k:', k)

# generating data of size N
N = 10000
label = np.random.randint(M, size=N)

# creating one hot encoded vectors# creati
data = []
for i in label:
    temp = np.zeros(M)
    temp[i] = 1
    data.append(temp)

data = np.array(data)

R = 2.0 / 4.0
n_channel = 2
input_signal = Input(shape=(M,))
encoded = Dense(M, activation='relu')(input_signal)
encoded1 = Dense(n_channel, activation='linear')(encoded)
encoded2 = BatchNormalization()(encoded1)

EbNo_train = np.power(10, 0.7)  # coverted 7 db of EbNo
#EbNo_train = EbNo_train.astype('float')
alpha1 = pow((2 * R * EbNo_train), -0.5)
encoded3 = GaussianNoise(alpha1)(encoded2)

decoded = Dense(M, activation='relu')(encoded3)
decoded1 = Dense(M, activation='softmax')(decoded)

autoencoder = Model(input_signal, decoded1)
# sgd = SGD(lr=0.001)
autoencoder.compile(optimizer='adam', loss='categorical_crossentropy')

autoencoder.summary()

N_val = 1500
val_label = np.random.randint(M, size=N_val)
val_data = []
for i in val_label:
    temp = np.zeros(M)
    temp[i] = 1
    val_data.append(temp)
val_data = np.array(val_data)

autoencoder.fit(data, data,
                epochs=20,
                batch_size=300,
                verbose=2,
                validation_data=(val_data, val_data))

from keras.models import load_model

encoder = Model(input_signal, encoded2)

encoded_input = Input(shape=(n_channel,))

deco = autoencoder.layers[-2](encoded_input)
deco = autoencoder.layers[-1](deco)
# create the decoder model
decoder = Model(encoded_input, deco)

N = 400000
test_label = np.random.randint(M, size=N)
test_data = []

for i in test_label:
    temp = np.zeros(M)
    temp[i] = 1
    test_data.append(temp)

test_data = np.array(test_data)

temp_test = 6
print (test_data[temp_test][test_label[temp_test]], test_label[temp_test])
print(encoder.predict(val_data).shape)
print(encoder.predict(val_data)[0])
scatter_plot = []
for i in range(0, M):
    temp = np.zeros(M)
    temp[i] = 1
    scatter_plot.append(encoder.predict(np.expand_dims(temp, axis=0)))

scatter_plot = np.array(scatter_plot)

print(scatter_plot)

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

scatter_plot = scatter_plot.reshape(M, 2, 1)
print(scatter_plot)
plt.scatter(scatter_plot[:,0], scatter_plot[:,1])
plt.axis((-2.5, 2.5, -2.5, 2.5))
plt.grid()
plt.savefig('Constellation_2_2')
plt.show()
