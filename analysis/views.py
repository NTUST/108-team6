from django.shortcuts import render
from keras import optimizers
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.layers import Activation, BatchNormalization, Conv1D, CuDNNGRU, Dense, Dropout, Embedding, Flatten, Input, MaxPooling1D, LeakyReLU
from keras.models import Sequential
from sklearn import preprocessing
import pandas as pd
from keras import losses
import numpy as np
import random
from keras import regularizers
from django.views.decorators.csrf import csrf_exempt 
import os
from django.http import HttpResponse
import json
# Create your views here.

def Model(attribute_num):
    model = Sequential()
    model.add(Dense(512,kernel_initializer='random_uniform', input_shape=(attribute_num,), activity_regularizer=regularizers.l2(0.001)))
    model.add(BatchNormalization())
    # model.add(Activation('relu'))
    model.add(LeakyReLU(alpha=.001))
    model.add(Dense(256, kernel_initializer='random_uniform', activity_regularizer=regularizers.l2(0.001)))
    model.add(BatchNormalization())
    # model.add(Activation('relu'))
    model.add(LeakyReLU(alpha=.001))
    model.add(Dense(128, kernel_initializer='random_uniform', activity_regularizer=regularizers.l2(0.001)))
    model.add(BatchNormalization())
    # model.add(Activation('relu'))
    model.add(LeakyReLU(alpha=.001))
    model.add(Dense(64, kernel_initializer='random_uniform', activity_regularizer=regularizers.l2(0.001)))
    model.add(BatchNormalization())
    model.add(LeakyReLU(alpha=.001))
    # model.add(Activation('relu'))
    model.add(Dense(1))

    model.compile(optimizer=optimizers.Adam(lr=1e-2),
                  loss=losses.mean_absolute_error)
    return model

def predict(request):
    return render(request, "analysis.html")

@csrf_exempt
def predict_result(request):
    arr_list = ['Age', 'Overall', 'Potential', 'Special', 'Acceleration', 'Aggression', 'Agility', 'Balance', 'Ball Control', 'Composure', 'Crossing', 'Curve', 'Dribbling', 'Finishing', 'Free Kick Accuracy', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy', 'Interceptions', 'Jumping', 'Long Passing', 'Long Shots', 'Marking', 'Penalties', 'Positioning', 'Reactions', 'Short Passing', 'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Stamina', 'Standing Tackle', 'Strength', 'Vision', 'Volleys']
    prefer_list = ['CAM', 'CB',  'CDM',  'CF',  'CM',  'GK',  'LB',  'LM',  'LW',  'RB',  'RM',  'RW',  'RWB',  'ST','LWB']

    inputs = []
    for arr in arr_list:
        inputs.append(int(request.POST.get(arr)))
        print(arr, request.POST.get(arr))

    print('prefer : ', request.POST.get('prefer'))
    prefers = [] if request.POST.get('prefer') is None else request.POST.get('prefer')
    for prefer in prefer_list:
        if prefer in prefers:
            inputs.append(1)
            print(prefer,1)
        else:
            inputs.append(0)
            print(prefer,0)
    inputs = np.array(inputs)
    save_model_path = os.getcwd() + '/analysis/model.h5'
    model =  Model(inputs.shape[0])
    model.load_weights(save_model_path)
    wage = int(model.predict(np.expand_dims(inputs, 0))[0][0])

    return HttpResponse(json.dumps({'wage':wage}), content_type='application/json')

