from keras import backend
from keras.layers import Input, Dense, Lambda, Flatten, Reshape
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True

def Vae(args):
    Z_1, Z_2 = args
    epsilon = backend.random_normal(shape=(backend.shape(Z_1)[0], 6), mean=0., stddev=1.0)
    return Z_1 + backend.exp(Z_2) * epsilon

class SharedLatentSpace():
    def __init__(self):
        self.Z = ''
    def calculateZ(self,obj):
        self.Z = Lambda(Vae, output_shape =(obj.K,))([obj.Z_1, obj.Z_2])
        a=5
        print("success....")