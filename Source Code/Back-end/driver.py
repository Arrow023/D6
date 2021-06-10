import sys
from inference_model import InferenceModel
from shared_latent_space import SharedLatentSpace
from decoder_train import DecoderTrain
from training import Training
from testing import Testing
from reconstructor import Reconstructor
from visualizer import Visualizer
import warnings
warnings.filterwarnings("ignore")


arguments = sys.argv

inference_model = InferenceModel()
if len(arguments)>1:
    iteration = arguments[1]
    epochs = arguments[2]
    inference_model.Iteration= int(iteration)
    inference_model.Epoch = int(epochs)

visualizer = Visualizer(inference_model)
shared_latent_space = SharedLatentSpace()
shared_latent_space.calculateZ(inference_model)
decoder = DecoderTrain(inference_model,shared_latent_space)
training = Training(inference_model,decoder)
testing = Testing(inference_model,decoder)
reconstructor = Reconstructor()
reconstructor.constructXtest(inference_model,training,testing)
reconstructor.constructXtrain(inference_model,training,testing)

visualizer.data_display(inference_model.XY_TrainLength,reconstructor.X_reconstructed_train,'X_reconstructed_train.png',False,False)
visualizer.data_display(inference_model.XY_TrainLength,inference_model.X_train,'X_train.png',False,False)
visualizer.data_display(inference_model.XY_TestLength,reconstructor.X_reconstructed_test,'X_reconstructed_test.png',False,True)
visualizer.data_display(inference_model.XY_TestLength,inference_model.X_test,'X_test.png',False,True)
visualizer.plotter(inference_model,reconstructor)


