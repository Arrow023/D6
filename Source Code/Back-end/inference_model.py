import numpy as np
from numpy import random
import pandas as pd
from keras.layers import Input, Dense, Lambda, Flatten, Reshape
from keras.layers import Conv2D, Conv2DTranspose
from keras.models import Model
from keras import backend
from keras import optimizers
from sklearn import preprocessing
import os 

working_dir = os.getcwd()
data_dir = working_dir+"/data/"

class GlobalConfiguration():
    X_train = pd.read_csv(data_dir+"X_train.csv")
    X_train = X_train.iloc[:,1:]
    X_train = X_train.to_numpy()
    X_train = X_train.astype('float32') / 255.
    X_test = pd.read_csv(data_dir+"X_test.csv")
    X_test = X_test.iloc[:,1:]
    X_test = X_test.to_numpy()
    X_test = X_test.astype('float32') / 255.
    Y_train = pd.read_csv(data_dir+"Y_train.csv")
    Y_train = Y_train.to_numpy()
    Y_test = pd.read_csv(data_dir+"Y_test.csv")
    Y_test = Y_test.to_numpy()

    resolution = 28
    Iteration = 50
    Epoch = 1
    batch_size = 10
    CenterDimension = 128

    X_train = X_train.reshape([X_train.shape[0], 1, resolution, resolution])
    X_test = X_test.reshape([X_test.shape[0], 1, resolution, resolution])
    normalize = preprocessing.MinMaxScaler(feature_range=(0, 1))   
    Y_train = normalize.fit_transform(Y_train)     
    Y_test = normalize.transform(Y_test)

    XY_TrainLength=X_train.shape[0]
    XY_TestLength=X_test.shape[0]
    Dimension1 = X_train.shape[1]*X_train.shape[2]*X_train.shape[3] 
    Dimension2 = Y_train.shape[1]

    K = 6
    C = 5

    Beta = 1 # Beta-VAE for Learning Disentangled Representations
    rho = 0.1  # posterior regularization parameter
    k = 10     # k-nearest neighbors
    t = 10.0 # kernel parameter in similarity measure
    L = 100   # Monte-Carlo sampling

    np.random.seed(1000)

    rows, cols, channel = 28, 28, 1
    filters = 64
    convsize = 3
    img_size = (rows, cols, channel)

    if backend.image_data_format() == 'channels_first':
        img_size = (rows, cols, channel)
    else:
        img_size = (channel, rows, cols) 

class InferenceModel(GlobalConfiguration):  
    X = Input(shape=GlobalConfiguration.img_size)
    Y = Input(shape=(GlobalConfiguration.Dimension2,))
    Y_1 = Input(shape=(GlobalConfiguration.Dimension2,))
    Y_2 = Input(shape=(GlobalConfiguration.Dimension2,))

    Firstlayer = Conv2D(GlobalConfiguration.channel, kernel_size=(2, 2), padding='same', activation='relu', name='Firstlayer')(X)
    Secondlayer = Conv2D(GlobalConfiguration.filters, kernel_size=(2, 2), padding='same', activation='relu', strides=(2, 2), name='Secondlayer')(Firstlayer)
    Thirdlayer = Conv2D(GlobalConfiguration.filters, kernel_size=GlobalConfiguration.convsize, padding='same', activation='relu', strides=1, name='Thirdlayer')(Secondlayer)
    Fourthlayer = Conv2D(GlobalConfiguration.filters, kernel_size=GlobalConfiguration.convsize, padding='same', activation='relu', strides=1, name='Fourthlayer')(Thirdlayer)
    flatlayer = Flatten()(Fourthlayer)
    hiddenlayer = Dense(GlobalConfiguration.CenterDimension, activation='relu', name='hiddenlayer')(flatlayer)
    Z_1 = Dense(GlobalConfiguration.K, name='Z_1')(hiddenlayer)
    Z_2 = Dense(GlobalConfiguration.K, name='Z_2')(hiddenlayer)
    
    Encoder = Model(inputs=X, outputs=[Z_1,Z_2])