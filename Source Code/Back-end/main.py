import os
from flask import Flask,jsonify,request,send_file, send_from_directory
import requests
import json
import random
import re
from flask_cors import CORS
import threading
import classification as cl


app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
working_directory = os.getcwd()
data_dir = working_directory+'/data/'
plot_dir = working_directory+'/plots/'

def algorithm(iteration,epochs):
    os.system('python3 -W ignore driver.py'+' '+str(iteration)+' '+str(epochs))

@app.route('/run')
def runner():
    try:
        iterations = request.args.get('iteration')
        epochs = request.args.get('epoch')
        t = threading.Thread(target=algorithm(iterations,epochs))
        t.start()
        return jsonify({'Status':'Success'})
    except:
        return jsonify({'Status':'Failed'})

@app.route('/data/<filename>')
def dataFetcher(filename):
    try:
        return send_from_directory(data_dir,filename,as_attachment=True)
    except:
        return jsonify({'Status':'File Retrieve failed'})

@app.route('/plot/<filename>')
def plotFetcher(filename):
    try:
        return send_from_directory(plot_dir,filename,as_attachment=True)
    except:
        return jsonify({'Status':'File Retrieve failed'})

@app.route('/charts')
def chartter():
    try:
        file_list = os.listdir(plot_dir)
        output = {}
        output["List"] = []
        for i in file_list:
            if i.startswith("2"):
                output["List"].append(i)
        return jsonify(output)
    except:
        return jsonify({"Error":"Could not read files"})

@app.route('/charts/<filename>')
def chartter_file(filename):
    try:
        output = open(plot_dir+filename)
        content = json.loads(output.read())
        return jsonify(content)
    except:
        return jsonify({'Error':'File Retrieve failed'})

@app.route('/classification/random')
def randomRunner():
    output = cl.randomForest() 
    return jsonify(output)

@app.route('/classification/svm')
def svmRunner():
    output = cl.supportVM()
    return jsonify(output)

@app.route('/classification/xgboost')
def xgboostRunner():
    output = cl.XGBoost()
    return jsonify(output)


if __name__ =='__main__':
    app.run(port=2302)
    app.debug=True
