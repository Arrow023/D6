import pandas as pd
import numpy as np
import os 

working_dir = os.getcwd()
data_dir = working_dir+"/data/"

class Reconstructor():
    def __init__(self):
        df= pd.read_csv(data_dir+'matrix.csv')
        self.S=np.mat(np.mat(df))
        self.X_reconstructed_test = None
        self.X_reconstructed_train = None
        self.XY_TrainLength = None
        self.XY_TestLength = None

    def constructXtrain(self,inference_model,training,testing):
        self.XY_TrainLength = inference_model.XY_TrainLength
        self.X_reconstructed_train = np.zeros((inference_model.XY_TrainLength, inference_model.channel, inference_model.rows, inference_model.cols))
        for i in range(inference_model.XY_TrainLength):
            sample1 = testing.Decoder.predict(training.Z_1[i,:], batch_size=1)
            sample1 = sample1.reshape((-1, 1,28,28))
            self.X_reconstructed_train[i,:,:,:] = sample1
        self.constructCSV(self.X_reconstructed_train,self.XY_TrainLength,'X_train.csv','X_reconstructed_train.csv')
        

    def constructXtest(self,inference_model,training,testing):
        self.XY_TestLength = inference_model.XY_TestLength
        self.X_reconstructed_test = np.zeros((inference_model.XY_TestLength, inference_model.channel, inference_model.rows , inference_model.cols ))
        for i in range(inference_model.XY_TestLength):
            s=self.S[:,i]
            z_sigma_test, z_mu_test = training.variable_changes.Bayesian(s,training.Z_1,inference_model.Y_test,i)
            epsilon_std = 1
            for l in range(inference_model.L):
                epsilon=np.random.normal(0,epsilon_std,1)
                z_test = z_mu_test + np.sqrt(np.diag(z_sigma_test))*epsilon
            sample2 = testing.Decoder.predict(z_test, batch_size=1)
            sample2 = sample2.reshape((-1, 1,28,28))
            self.X_reconstructed_test[i,:,:,:] = sample2
        self.constructCSV(self.X_reconstructed_test,self.XY_TestLength,'X_test.csv','X_reconstructed_test.csv')


    def constructCSV(self,data,length,sourcefile,destfile):
        pixels = data * 255   #for normalizing values to 255
        pixels = pixels.astype('uint8') # to convert to uint8 from float32 normalized

        #column generator 
        columns = ['label']
        for i in range(1,29):
            string = str(i)+"x"
            temp = string
            for j in range(1,29):
                temp +=str(j)
                columns.append(temp)
                temp = string
            
        df = pd.DataFrame(columns=columns)
        dataframe = pd.read_csv(data_dir+sourcefile)
        for k in range(length):
            label = dataframe['label'][k]
            if label == 1:
                label = 6
            elif label == 2 :
                label = 9
            record = [label]
            for i in range(28):
                for j in range(28):
                    record.append(pixels[k][0][i][j])
            df.loc[len(df.index)] = record
        df.to_csv(data_dir+destfile,index=False)
