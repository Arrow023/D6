# Reconstructing Perceived Images from Human Brain Activities using TWIN DEEP NEURAL NETWORK
 What if I tell you that I could show you what you are thinking ? This is a hope for the future. We have developed a nueral network that does it (kindof). 
 
## Demo Clip
[![image](https://user-images.githubusercontent.com/42842987/128367767-e1302896-0ff1-4cc0-b768-87f919595e49.png)](https://drive.google.com/file/d/1IDh_I5RpZyQL1jbdz--gTbKzn0xIyFEF/view?usp=sharing)


 
 ## Abstract [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/D6/LICENSE)
Understanding the Human Visual System necessitates the use of neural decoding. The human visual system is capable of extracting and comparing features from any object. The majority of the articles are concerned with either the classification of brain function patterns or the recognition of visual stimuli. We implement the Twin Deep Neural Network model for accurate image reconstruction in this project. We present the Twin Deep Neural Network model for accurate image reconstruction from human brain activity using functional Magnetic Resonance Imaging in this research (fMRI). For better visual reconstruction and to make full use of each dataset, the TDNN method may be used to compare the relationship between a sample pair of similar features. The TDNN approach reduces the constraints imposed by high dimensionality and a limited amount of FMRI data. Essentially, this method will increase the training data from N samples to 2N sample pairs, allowing the limited number of training samples to be fully utilised. On an open dataset of handwritten digital images and character datasets, we found that the proposed TDNN approach outperformed all current state-of-the-art methods on the Convolutional Neural Network by about 10%. (CNN).

## Parts of the Project
The project execution is divided into two structure.
* Front End - This is the UI that helps the user to easily work with the algorithms and displays the observation of the algorithm that run on specific configuration [![Generic badge](https://img.shields.io/badge/Angular-10-green.svg)](https://shields.io/)
* Back End - The heart where the real algorithm resides, it acts as the intermediate API that serves the request of the front-end [![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)


## Architecture of the overall Project

* Deployment Diagram <br/> <br/> 
![image](https://user-images.githubusercontent.com/42842987/121522174-78cf3680-ca12-11eb-98ce-9d2e12257938.png) 
* Python Configuration Diagram <br/> <br/>
![image](https://user-images.githubusercontent.com/42842987/121522714-03b03100-ca13-11eb-8328-edf43195fa17.png)

## Directory Structure of the FrontEnd
``` 
FrontEnd -------------
              |---- e2e
              |---- node modules
              |---- src
                |---- app
                  |---- Home   ( Intro Component )
                  |---- Trainer ( The real algo runner )
                  |---- Resources ( Repos used for the project )
                  |---- Charts ( Displays the evaluation report )
                  |---- ChartList ( Displays the list of configuration runned before )
                  |---- Footer ( Credits component )
                |---- environment
                |---- assets ( Shared resources )
 ```
 ## Directory Structure of the BackEnd
 ```
 BackEnd -------------
              |---- data
              |---- plots
              |---- classification.py ( The API for classification )
              |---- decoder_train.py ( The Econder algorithm )
              |---- driver.py ( The driver code of the entire algorithm )
              |---- DualLearning.py ( Knowledge analyzer algorithm )
              |---- inference_model.py ( Part of Encoder algorithm )
              |---- main.py ( The API runner )
              |---- reconstructor.py ( The Reconstruction algorithm )
              |---- shared_latent_space.py ( A space to store the knowledge analyzed )
              |---- testing.py ( The testing phase of the algorithm )
              |---- training.py ( The training phase of the algorithm )
              |---- visualizer.py ( The Chart generator algorithm ) 
                
```
## Execution of the Project 

------------------ 
1. First Step is to execute the heart of the project ( The BackEnd) [![npm version](https://badge.fury.io/js/%40angular%2Fcore.svg)](https://badge.fury.io/js/%40angular%2Fcore)
2. Second Step is to execute the Web Client ( The FrontEnd) [![PyPI version](https://badge.fury.io/py/f.svg)](https://badge.fury.io/py/f)

Let's break these two steps into individual execution of each .

### 1. BackEnd Execution sequences

The first process is to install the necessary libraries required to run the BackEnd. So, the below command will guide you through this process. <br/>
1. First Navigate to the main root directory of the project
    ```
    $ cd BackEnd
    ```
2. Now install the requirements using the PIP installer
    ```
    $ pip install -r requirements.txt
    ```
3. It's time to run the algorithm.
    ```
    $ python main.py
    ```
    After all these steps, you will see a terminal with the following message
    ```
     * Serving Flask app "main" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:2302/ (Press CTRL+C to quit)
     ```
 Alas!!! 😃 You have succeeded in successfully executing the difficult part. 
  
### FrontEnd Execution Sequences
The front end is developed using the *Angular 10*. In order to run the application, we have to install Node Environment.
1. First install the Node from the official Node website
    > https://nodejs.org/en/download/ 
   
2. Second step is to install **@angular/cli**
   ```
   $ npm install -g @angular/cli
   ```
3. Navigate to the Root Directory of the front-end
    ```
    $ cd FrontEnd
    ```
4. Install the Library dependencies 
    ```
    $ npm install
    ```
6. Run the project by running Node
    ```
    $ npm start
    ```
After executing all these steps, a new browser window will popup. And, Alas!!! You have completed both the steps. 

# Credits
-------------------
* Developers
  > [Piyush Chouhan](https://www.github.com/Arrow023) 
  >> University RegNo : 211417104183
  
  > [Kedar R](https://github.com/kedar-2206)
  >> University RegNo : 211417104117
  
  > [Mohanavel R](https://github.com/Mohanavel2000)
  >> University RegNo : 211417104149
  
* Supporting Staffs
  > Dr. N. Pughazendi ( Project Incharge )
  
  > Jainulabudeen S.A.K ( Evaluation & Feedback )

* Special Thanks <br/>
<p align="center">
  <img width="600" height="150" src="https://user-images.githubusercontent.com/42842987/121531150-c8fec680-ca1b-11eb-8e14-c46ebc755e83.png">
</p>
  

  
