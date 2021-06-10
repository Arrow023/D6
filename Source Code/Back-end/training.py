import numpy as np
from DualLearning import OptimalDistribution


class Training():
    def __init__(self,inference_model,decoder_train):
        self.variable_changes = OptimalDistribution(inference_model.XY_TrainLength,inference_model.Dimension2,inference_model.K,inference_model.C)
        Y_1 = self.variable_changes.Y_1
        Y_2 = self.variable_changes.Y_2
        for l in range(inference_model.Iteration):
            print ('**************************************************iter= '+str(l)+" *****************************************",)
            decoder_train.TDNN.fit([inference_model.X_train, inference_model.Y_train, Y_1, Y_2], inference_model.X_train, shuffle=True, verbose=2, epochs=inference_model.Epoch, batch_size=inference_model.batch_size) 
            [Z_1,Z_2] = inference_model.Encoder.predict(inference_model.X_train)
            self.Z_1 = Z_1
            self.Z_2 = Z_2
            self.Z_1 = np.mat(self.Z_1)
            Y_1,Y_2 = self.variable_changes.updateParameters(self.Z_2,inference_model.Y_train,self.Z_1)