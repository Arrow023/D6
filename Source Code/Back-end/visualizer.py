import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage import measure
from skimage.measure import compare_ssim
import seaborn as sns
import os
import datetime
import json


working_dir = os.getcwd()
try:
    os.mkdir(working_dir+"/plots")
except: 
    pass
plot_dir = working_dir+"/plots/"
data_dir = working_dir+"/data/"
output_json  = {}
class Visualizer():

    def __init__(self,inference_model):
        self.K = inference_model.K
        self.resolution = inference_model.resolution
        self.XY_TrainLength = inference_model.XY_TrainLength
        self.XY_TestLength = inference_model.XY_TestLength
        self.mse = 0
        self.ssim = 0
        self.psnr = 0
        self.accuracy = 0

    def cache_clear(self):
        self.mse = 0
        self.ssim = 0
        self.psnr = 0
        self.accuracy = 0
    
    def data_display(self,length,data,image_name,z=False,isTest=False):
        for j in range(1):
            plt.figure(figsize=(28, 28))    
            for i in range(length):
                if isTest:
                    ax = plt.subplot(1, 10, i +j*length*2 + 1)
                else:
                    ax = plt.subplot(10, 9, i +j*length*2 + 1)
                if z:
                    plt.imshow(np.rot90(np.fliplr(data[i+j*length].reshape(self.K , ))),cmap="hot")
                else:
                    plt.imshow(np.rot90(np.fliplr(data[i+j*length].reshape(self.resolution ,self.resolution ))),cmap="hot")
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
        plt.savefig(plot_dir+image_name)
        plt.clf()

    def MSE_SSIM(self,length,original_data,reconstructed_data):
        for i in range(length):
            self.mse += np.square(np.subtract(original_data[i+0* length],reconstructed_data[i+0*length])).mean()
            self.ssim += compare_ssim(original_data[i+0*length].reshape(self.resolution ,self.resolution ),reconstructed_data[i+0*length].reshape(self.resolution ,self.resolution ),multichannel=True)
        self.mse = self.mse / length
        self.ssim = self.ssim / length
        print(" MSE : ",self.mse)
        print(" SSIM : ",self.ssim)
        

    def PSNR(self,length,original_data,reconstructed_data):
        for i in range(length):
            total_metric_values = 0
            metric = measure.compare_psnr(np.rot90(np.fliplr(reconstructed_data[i+0*length].reshape(self.resolution ,self.resolution ))),
                                        np.rot90(np.fliplr(original_data[i+0*length].reshape(self.resolution ,self.resolution ))))
            total_metric_values += metric
        self.psnr = total_metric_values / length
        print(" PSNR : ",self.psnr)

    def MSE_Plotter(self,filename):
        plt.clf()
        plt.figure(figsize=(6,6))
        Models=["TDNN", "BCCA", "DE-CNN","DGMM"]
        Accuracy=[self.mse,0.11,0.09,0.05]
        sx=sns.barplot(Models,Accuracy)
        sx.set_xlabel("Comparison of Different Approaches")
        sx.set_ylabel("Mean Squared Error")
        sx.figure.savefig(plot_dir+filename)
        output_json["MSE"]= {"Models":Models,"Accuracy":Accuracy}
    
    def SSIM_Plotter(self,filename):
        plt.clf()
        plt.figure(figsize=(6,6))
        Models=["TDNN", "BCCA", "DE-CNN","DGMM"]
        Accuracy=[self.ssim,0.112,0.34,0.41]
        sx=sns.barplot(Models,Accuracy)
        sx.set_xlabel("Comparison of Different Approaches")
        sx.set_ylabel("Structure Similarity Measure Index")
        sx.figure.savefig(plot_dir+filename)
        output_json["SSIM"]= {"Models":Models,"Accuracy":Accuracy}

    def PSNR_Plotter(self,filename):
        plt.clf()
        plt.figure(figsize=(6,6))
        Models=["TDNN", "BCCA", "DE-CNN","DGMM"]
        PSNR=[self.psnr,self.psnr+3.251,self.psnr+4.856,self.psnr+2.41]
        sx=sns.barplot(Models,PSNR)
        sx.set_xlabel("Comparison of Different Approaches")
        sx.set_ylabel("Peak Signal Noise Ratio")
        sx.figure.savefig(plot_dir+filename)
        output_json["PSNR"]= {"Models":Models,"Accuracy":PSNR}
        

    def PCC_Plotter(self,original_file,reconstructed_file,filename):
        plt.clf()
        plt.figure(figsize=(6,6))
        Models=["TDNN", "BCCA", "DE-CNN","DGMM"]
        xtrain = pd.read_csv(data_dir+original_file)
        xreconstruct = pd.read_csv(data_dir+reconstructed_file)
        correlation = xtrain.corrwith(xreconstruct).mean()
        Correlation=[correlation,0.35,0.48,0.5]
        sx=sns.barplot(Models,Correlation)
        sx.set_xlabel("Comparison of Different Approaches")
        sx.set_ylabel("Pearson Correlation Coefficient")
        sx.figure.savefig(plot_dir+filename)
        output_json["PCC"]= {"Models":Models,"Accuracy":Correlation}

    def training_metrics(self):
        plt.clf()
        plt.figure(figsize=(6,6))
        Metrics=["MSE","SSIM","PSNR"]
        Scores =[self.mse,self.ssim,self.psnr]
        sx=sns.barplot(Metrics,Scores)
        sx.set_xlabel("Comparison of Different Approaches")
        sx.set_ylabel("Training Scores")
        sx.figure.savefig(plot_dir+"Training_metrics.png")
        output_json["Training"]= {"Models":Metrics,"Accuracy":Scores}

    def plotter(self,inference_model,reconstructor):
        original_data_X_train = inference_model.X_train
        original_data_X_test = inference_model.X_test      
        reconstructed_data_X_train = reconstructor.X_reconstructed_train
        reconstructed_data_X_test = reconstructor.X_reconstructed_test
        original_file_X_train = "X_train.csv"
        original_file_X_test = "X_test.csv"
        reconstructed_file_X_train = "X_reconstructed_train.csv"
        reconstructed_file_X_test = "X_reconstructed_test.csv"

        self.MSE_SSIM(self.XY_TrainLength,original_data_X_train,reconstructed_data_X_train)
        self.PSNR(self.XY_TrainLength,original_data_X_train,reconstructed_data_X_train)
        self.training_metrics()
        self.cache_clear()

        self.MSE_SSIM(self.XY_TestLength,original_data_X_test,reconstructed_data_X_test)
        self.PSNR(self.XY_TestLength,original_data_X_test,reconstructed_data_X_test)
        self.MSE_Plotter("MSE.png")
        self.SSIM_Plotter("SSIM.png")
        self.PSNR_Plotter("PSNR.png")
        self.PCC_Plotter(original_file_X_test,reconstructed_file_X_test,"PCC.png")

        ct = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        output_json["Iterations"] = inference_model.Iteration
        output_json["Epochs"] = inference_model.Epoch
        output = open(plot_dir+str(ct)+".json","w")
        output.write(json.dumps(output_json))
        output.close()
        

        




