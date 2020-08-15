import tkinter as tk
from tkinter.filedialog import askopenfilename
import shutil
import os
import sys
from PIL import Image, ImageTk


def bact():
    rem = "The remedies for Bacterial Spot are:\n\n "
    rem1 = " Discard or destroy any affected plants. \n  Do not compost them. \n  Rotate yoour tomato plants yearly to prevent re-infection next year. \n Use copper fungicites"
    return(rem+rem1)
    
def vir():
    rem = "The remedies for Yellow leaf curl virus are: "
    rem1 = " Monitor the field, handpick diseased plants and bury them. \n  Use sticky yellow plastic traps. \n  Spray insecticides such as organophosphates, carbametes during the seedliing stage. \n Use copper fungicites"
    return(rem+rem1)

def latebl():
    rem = "The remedies for Late Blight are: "
    rem1 = " Monitor the field, remove and destroy infected leaves. \n  Treat organically with copper spray. \n  Use chemical fungicides,the best of which for tomatoes is chlorothalonil."
    return(rem+rem1)

def analysis():
    dis="HEALTHY !!"
    tret="HEALTHY !!"
    acc=""
    print("reached analysis() $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")
    import cv2  # working with, mainly resizing, images
    import numpy as np  # dealing with arrays
    import os  # dealing with directories
    from random import shuffle  # mixing up or currently ordered data that might lead our network astray in training.
    from tqdm import \
        tqdm  # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
    verify_dir = 'testpicture'
    IMG_SIZE = 50
    LR = 1e-3
    MODEL_NAME = 'farming/healthyvsunhealthy-{}-{}.model'.format(LR, '2conv-basic')

    def process_verify_data():
        verifying_data = []
        for img in tqdm(os.listdir(verify_dir)):
            path = os.path.join(verify_dir, img)
            img_num = img.split('.')[0]
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            verifying_data.append([np.array(img), img_num])
        np.save('verify_data.npy', verifying_data)
        return verifying_data

    verify_data = process_verify_data()
    #verify_data = np.load('verify_data.npy')

    import tflearn
    from tflearn.layers.conv import conv_2d, max_pool_2d
    from tflearn.layers.core import input_data, dropout, fully_connected
    from tflearn.layers.estimator import regression
    import tensorflow as tf
    tf.reset_default_graph()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 4, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded!\n \n')

    import matplotlib.pyplot as plt

    fig = plt.figure()

    for num, data in enumerate(verify_data):

        img_num = data[1]
        img_data = data[0]

        y = fig.add_subplot(3, 4, num + 1)
        orig = img_data
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)
        # model_out = model.predict([data])[0]
        pred=model.predict([data])
        model_out = pred[0]
        ec=np.argmax(pred[0])
        print("The Result is Predicted with : {:0.2f}".format(list(pred[0])[ec]*100) ,"percent success !\n \n")
        #print((pred[ec])*100," this is percentage of prediciton")
        acc="The Result is Predicted with : {:0.2f}".format(list(pred[0])[ec]*100)
        acc=acc+" percent success"
        #print("Prediction: %s" % str(pred))  # only show first 3 probas
        if np.argmax(model_out) == 0:
            str_label = 'healthy'
        elif np.argmax(model_out) == 1:
            str_label = 'bacterial'
        elif np.argmax(model_out) == 2:
            str_label = 'viral'
        elif np.argmax(model_out) == 3:
            str_label = 'lateblight'

        if str_label =='healthy':
            status ="HEALTHY"
        else:
            status = "UNHEALTHY"
        if str_label == 'bacterial':
            dis = "Bacterial Spot "
            tret=bact()
        elif str_label == 'viral':
            dis = "Yellow leaf curl "
            tret=vir()
        elif str_label == 'lateblight':
            dis = "Late Blight "
            tret=latebl()

        else:
            print("FOUND HEALTHY !!!!!!!!!!!!!!!!!!!\n")
      
    folder=verify_dir    
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
                  
        if os.path.isfile(file_path) or os.path.islink(file_path):     
            os.unlink(file_path)
                 
        elif os.path.isdir(file_path):
            
            shutil.rmtree(file_path)
    
    folder = 'detect'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)  
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    
    return (dis,tret,acc)

def openphoto():
    fileName="detect"
    
    for file in os.listdir(fileName):
        print(file)
        fileName = os.path.join(fileName, file)
    print(fileName)
    dst = "testpicture"
    shutil.copy(fileName, dst)
    dis,tret,acc=analysis()
    return (dis,tret,acc)


