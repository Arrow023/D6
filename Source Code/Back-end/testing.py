import pandas as pd
import numpy as np
from keras.layers import Input, Dense, Lambda, Flatten, Reshape
from keras.models import Model

class Testing():
    def __init__(self,inference_model,decoder_train):
        Z_predict = Input(shape=(inference_model.K,))
        reconstructed_x_hiddenlayer = decoder_train.decoder_hiddenlayer(Z_predict)
        reconstructed_x_up = decoder_train.decoder_up(reconstructed_x_hiddenlayer)
        reconstructed_x_reshape = decoder_train.decoder_reshape(reconstructed_x_up)
        reconstructed_x_Firstlayer = decoder_train.decoder_Firstlayer(reconstructed_x_reshape)
        reconstructed_x_Secondlayer = decoder_train.decoder_Secondlayer(reconstructed_x_Firstlayer)
        reconstructed_x_Thirdlayer = decoder_train.decoder_Thirdlayer(reconstructed_x_Secondlayer)
        reconstructed_X_1 = decoder_train.decoder_1(reconstructed_x_Thirdlayer)
        self.Decoder = Model(inputs=Z_predict, outputs=reconstructed_X_1)
        