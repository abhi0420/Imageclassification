import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy
from matplotlib import image
from matplotlib import pyplot
from PIL import Image
import cv2
f = r''
for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((128,128))
    img.save(f_img)
f = r''
for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((128,128))
    img.save(f_img)
train_images = []
for filename in os.listdir(dir2):
    img = cv2.imread(os.path.join(dir2,filename))

    if img is not None:


    train_images.append(img)
test_images = []
for filename in os.listdir(dir1):
    img = cv2.imread(os.path.join(dir1,filename))
    if img is not None:
        test_images.append(img)

train_images = np.array(train_images)
test_images = np.array(test_images)
train_labels = []
test_labels = []
arr2 = os.listdir(dir2)
arr1 = os.listdir(dir1)
train_labels = []
for a in arr2:
    if a[:3] == 'cat':
        train_labels.append(0)
    else:
        train_labels.append(1)
test_labels = []
for a in arr1:
    if a[:3] == 'cat':
        test_labels.append(0)
    else:
        test_labels.append(1)
train_labels = np.array(train_labels)
test_labels = np.array(test_labels)
train_image_flatten = train_images.reshape(train_images.shape[0],-1).T
test_image_flatten = test_images.reshape(test_images.shape[0],-1).T
train_labels = train_labels.reshape(1,train_labels.shape[0])
test_labels = test_labels.reshape(1,test_labels.shape[0])
train_set_imgs = train_image_flatten/255.
test_set_imgs = test_image_flatten/255
def sigmoid(x):
    return 1/(1+np.exp(-x))
def init_param(dim):
    w = np.zeros((dim,1))
    b = 0
    assert(w.shape == (dim, 1))
    assert(isinstance(b, float) or isinstance(b, int))

    return w, b
def propagation(w,b,X,Y):
    m = X.shape[1]    # No. of training examples

    #Forward propagation
    A = sigmoid(np.dot(w.T,X) + b) 
    cost = -np.sum((((Y*np.log(A)) + ((1-Y)*np.log(1-A)))),axis = 1,keepdims=True)/m

    #Backward propagation

    dw = (np.dot(X,(A-Y).T))/m
    db = np.sum(A-Y)/m

    assert(dw.shape == w.shape)
    assert(db.dtype == float)
    cost = np.squeeze(cost)
    assert(cost.shape == ())

    grads = {"dw": dw,
             "db": db}

    return grads, cost
def optimize(w,b,X,Y,N,learning_rate,print_cost = True):
    # N: No. of iterations
    # Learning rate: learning rate of gradient decent
    #print_cost: Will print the cost after certain no. of iterations

    costs = []
    for i in range(N):
        grads,cost =propagation(w,b,X,Y)
        dw = grads["dw"]
        db = grads["db"]
        w = w-(learning_rate*dw)
        b = b-(learning_rate*db)
        if i % 100 == 0:
            costs.append(cost)


        if print_cost and i % 5 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))

    params = {"w": w,
              "b": b}

    grads = {"dw": dw,
             "db": db}

    return params, grads, costs    
#predict function
def predict(w,b,X):
    m = X.shape[1]
    Y_prediction = np.zeros((1,m))
    w = w.reshape(X.shape[0],1)
    A = sigmoid(np.dot(w.T,X)+b)
    for i in range(A.shape[1]):
        if A[0][i] <= 0.5:
            Y_prediction[0][i] = 0
        elif A[0][i] > 0.5:
            Y_prediction[0][i] = 1
        ### END CODE HERE ###

    assert(Y_prediction.shape == (1, m))

    return Y_prediction
  def model(X_train, Y_train, X_test, Y_test, num_iterations = 2000, learning_rate = 0.5, print_cost = False):




    # initialize parameters with zeros (≈ 1 line of code)
    w, b = init_param(X_train.shape[0])

    # Gradient descent (≈ 1 line of code)
    parameters, grads, costs = optimize(w, b, X_train, Y_train, num_iterations, learning_rate, print_cost = False)

    # Retrieve parameters w and b from dictionary "parameters"
    w = parameters["w"]
    b = parameters["b"]

    # Predict test/train set examples (≈ 2 lines of code)
    Y_prediction_test = predict(w,b,X_test)
    Y_prediction_train = predict(w,b,X_train)

    ### END CODE HERE ###

    # Print train/test Errors
    print("train accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_train - Y_train)) * 100))
    print("test accuracy: {} %".format(100 - np.mean(np.abs(Y_prediction_test - Y_test)) * 100))


    d = {"costs": costs,
         "Y_prediction_test": Y_prediction_test, 
         "Y_prediction_train" : Y_prediction_train, 
         "w" : w, 
         "b" : b,
         "learning_rate" : learning_rate,
         "num_iterations": num_iterations}

    return d
d = model(train_set_imgs, train_labels, test_set_imgs, test_labels, num_iterations = 4000, learning_rate = 0.005, print_cost = True)
