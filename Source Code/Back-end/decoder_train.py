import numpy as np
from numpy import random
from keras.layers import Input, Dense, Lambda, Flatten, Reshape
from keras.layers import Conv2D, Conv2DTranspose
from keras.models import Model
from keras import backend
from keras import optimizers
from keras import metrics
from sklearn import preprocessing

class DecoderTrain():
    def __init__(self,inference_model,shared_latent_space):
        
        self.decoder_hiddenlayer = Dense(inference_model.CenterDimension, activation='relu')
        self.decoder_up = Dense(inference_model.filters * 14 * 14, activation='relu')

        if backend.image_data_format() == 'channels_first':
            output_size = (inference_model.batch_size, inference_model.filters, 14, 14)
        else:
            output_size = (inference_model.batch_size, 14, 14, inference_model.filters)

        self.decoder_reshape = Reshape(output_size[1:])
        self.decoder_Firstlayer = Conv2DTranspose(inference_model.filters, kernel_size=inference_model.convsize, padding='same', strides=1, activation='relu')
        self.decoder_Secondlayer = Conv2DTranspose(inference_model.filters, kernel_size=inference_model.convsize, padding='same', strides=1, activation='relu')

        if backend.image_data_format() == 'channels_first':
            output_size = (inference_model.batch_size, 29, 29, inference_model.filters)
        else:
            output_size = (inference_model.batch_size, inference_model.filters, 29, 29)
            
        self.decoder_Thirdlayer = Conv2DTranspose(inference_model.filters, kernel_size=(3, 3), strides=(2, 2), padding='valid', activation='relu')
        self.decoder_1 = Conv2D(inference_model.channel, kernel_size=2, padding='valid', activation='sigmoid')

        x_hiddenlayer = self.decoder_hiddenlayer(shared_latent_space.Z)
        x_up = self.decoder_up(x_hiddenlayer)
        x_reshape = self.decoder_reshape(x_up)
        x_Firstlayer = self.decoder_Firstlayer(x_reshape)
        x_Secondlayer = self.decoder_Secondlayer(x_Firstlayer)
        x_Thirdlayer = self.decoder_Thirdlayer(x_Secondlayer)
        X_1 = self.decoder_1 (x_Thirdlayer)

        logc = np.log(2 * np.pi)
        def GMM(Y, Y_1, Y_2): 
            return backend.mean(-(0.5 * logc + 0.5 * Y_2) - 0.5 * ((Y - Y_1)**2 / backend.exp(Y_2)), axis=-1)
        
        def LossFunction(X, X_1):
            X = backend.flatten(X)
            X_1 = backend.flatten(X_1)   
            Lp = 0.5 * backend.mean( 1 + inference_model.Z_2 - backend.square(inference_model.Z_1) - backend.exp(inference_model.Z_2), axis=-1)      
            Lx =  - metrics.binary_crossentropy(X, X_1) # Pixels have a Bernoulli distribution              
            Ly =  GMM(inference_model.Y, inference_model.Y_1, inference_model.Y_2) # Voxels have a Gaussian distribution      
            loss = backend.mean(Lp + 10000 * Lx + Ly)  
            totalloss = - loss
            return  totalloss 

        self.TDNN= Model(inputs=[inference_model.X, inference_model.Y, inference_model.Y_1, inference_model.Y_2], outputs=X_1,name = 'TDNN')
        opt_method = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        self.TDNN.compile(optimizer = opt_method, loss = LossFunction)
        self.TDNN.summary()