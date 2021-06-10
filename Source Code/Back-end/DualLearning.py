import pandas as pd
import numpy as np
from numpy import random

class OptimalDistribution():
    def __init__(self,XY_TrainLength,Dimension2,K,C):
        self.tau_alpha = 1
        self.tau_beta = 1

        self.eta_alpha = 1
        self.eta_beta = 1

        self.gamma_alpha = 1
        self.gamma_beta = 1

        self.XY_TrainLength = XY_TrainLength
        self.Dimension2 = Dimension2
        self.K = K
        self.C = C
        self.rho = 0.1

        self.Z_1 = np.mat(random.random(size=(self.XY_TrainLength,self.K)))  # K shape
        self.B_mu = np.mat(random.random(size=(self.K,self.Dimension2)))      # use K shape with dimension of Y and it uses tau

        self.R_mu = np.mat(random.random(size=(self.XY_TrainLength,self.C)))  # auxiliary latent variable with C shape
        self.sigma_r = np.mat(np.eye((self.C)))

        self.H_mu = np.mat(random.random(size=(self.C,self.Dimension2)))     # use C shape with dimension of Y and it uses eta
        self.sigma_h = np.mat(np.eye((self.C)))

        self.tau_mu = self.tau_alpha / self.tau_beta  # equation 4
        self.eta_mu = self.eta_alpha / self.eta_beta  # equation 7
        self.gamma_mu = self.gamma_alpha / self.gamma_beta  # equation 7

        self.Y_1 = np.array(self.Z_1 * self.B_mu + self.R_mu * self.H_mu)  # equation 6
        self.Y_2 = np.log(1 / self.gamma_mu * np.ones((self.XY_TrainLength, self.Dimension2)))  # equation 6

    def updateParameters(self,Z_2,Y_train,Z_1):
        self.Z_1 = Z_1
        # update B
        temp1 = np.exp(Z_2)
        temp2 = self.Z_1.T * Z_1 + np.mat(np.diag(temp1.sum(axis=0)))
        temp3 = self.tau_mu * np.mat(np.eye(self.K))
        sigma_b = (self.gamma_mu * temp2 + temp3).I
        self.B_mu = sigma_b * self.gamma_mu * self.Z_1.T * (np.mat(Y_train) - self.R_mu * self.H_mu)
        # update H
        RTR_mu = self.R_mu.T * self.R_mu + self.XY_TrainLength * self.sigma_r
        self.sigma_h = (self.eta_mu * np.mat(np.eye(self.C)) + self.gamma_mu * RTR_mu).I
        self.H_mu = self.sigma_h * self.gamma_mu * self.R_mu.T * (np.mat(Y_train) - self.Z_1 * self.B_mu)
        # update R
        HHT_mu = self.H_mu * self.H_mu.T + self.Dimension2 * self.sigma_h
        sigma_r = (np.mat(np.eye(self.C)) + self.gamma_mu * HHT_mu).I
        R_mu = (sigma_r * self.gamma_mu * self.H_mu * (np.mat(Y_train) - self.Z_1 * self.B_mu).T).T  
        # update tau
        tau_alpha_new = self.tau_alpha + 0.5 * self.K * self.Dimension2
        tau_beta_new = self.tau_beta + 0.5 * ((np.diag(self.B_mu.T * self.B_mu)).sum() + self.Dimension2 * sigma_b.trace())
        tau_mu = tau_alpha_new / tau_beta_new
        tau_mu = tau_mu[0,0] 
        # update eta
        eta_alpha_new = self.eta_alpha + 0.5 * self.C * self.Dimension2
        eta_beta_new = self.eta_beta + 0.5 * ((np.diag(self.H_mu.T * self.H_mu)).sum() + self.Dimension2 * self.sigma_h.trace())
        eta_mu = eta_alpha_new / eta_beta_new
        eta_mu = eta_mu[0,0] 
        # update gamma
        gamma_alpha_new = self.gamma_alpha + 0.5 * self.XY_TrainLength * self.Dimension2
        gamma_temp = np.mat(Y_train) - self.Z_1 * self.B_mu - R_mu * self.H_mu
        gamma_temp = np.multiply(gamma_temp, gamma_temp)
        gamma_temp = gamma_temp.sum(axis=0)
        gamma_temp = gamma_temp.sum(axis=1)
        gamma_beta_new = self.gamma_beta + 0.5 * gamma_temp
        self.gamma_mu = gamma_alpha_new / gamma_beta_new
        self.gamma_mu = self.gamma_mu[0,0] 
        # calculate Y_1   
        self.Y_1 = np.array(self.Z_1 * self.B_mu + R_mu * self.H_mu) 
        self.Y_2 = np.log(1 / self.gamma_mu * np.ones((self.XY_TrainLength, self.Dimension2)))

        return self.Y_1, self.Y_2
    

    def Bayesian(self,s,Z_1,Y_test,i):
        HHT = self.H_mu * self.H_mu.T + self.Dimension2 * self.sigma_h
        Temp = self.gamma_mu * np.mat(np.eye(self.Dimension2)) - (self.gamma_mu**2) * (self.H_mu.T * (np.mat(np.eye(self.C)) + self.gamma_mu * HHT).I * self.H_mu)
        z_sigma_test = (self.B_mu * Temp * self.B_mu.T + (1 + 0.1 * s.sum(axis=0)[0,0]) * np.mat(np.eye(self.K)) ).I
        z_mu_test = (z_sigma_test * (self.B_mu * Temp * (np.mat(Y_test)[i,:]).T + self.rho * np.mat(Z_1).T * s )).T
        return z_sigma_test, z_mu_test