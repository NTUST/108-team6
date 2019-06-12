import json
import os

import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from keras import losses
from keras import optimizers
from keras import regularizers
from keras.layers import BatchNormalization, Dense, LeakyReLU, Input
from keras.models import Sequential
import keras

def SeperateModel(neuron_num, input_layer1):
    
    dense = Dense(neuron_num,kernel_initializer='random_uniform')(input_layer1)
    BN = BatchNormalization()(dense)
    leakyReLU = LeakyReLU(alpha=.001)(BN)
    return leakyReLU

def Model(attribute_num):
    input_layer = Input(shape=(attribute_num,))
    BN = BatchNormalization()(input_layer)
    dnn = SeperateModel(128,BN)
    dnn = SeperateModel(128,dnn)
    # dnn = SeperateModel(256,dnn)
    # dnn = SeperateModel(256,dnn)
    outs = Dense(1,kernel_initializer='random_uniform')(dnn)
    
    model = keras.models.Model(inputs=input_layer, outputs=outs)
    model.compile(optimizer=optimizers.Adam(lr=1e-2),
                  loss=losses.mean_absolute_error)
    return model

def predict(request):
    return render(request, "analysis.html",{'title':'Analysis'})

@csrf_exempt
def predict_result(request):
    arr_list = ['Age','Special', 'Acceleration', 'Aggression', 'Agility', 'Balance', 'Ball Control', 'Composure', 'Crossing', 'Curve', 'Dribbling', 'Finishing', 'Free Kick Accuracy', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy', 'Interceptions', 'Jumping', 'Long Passing', 'Long Shots', 'Marking', 'Penalties', 'Positioning', 'Reactions', 'Short Passing', 'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Stamina', 'Standing Tackle', 'Strength', 'Vision', 'Volleys']
    prefer_list = ['CAM', 'CB',  'CDM',  'CF',  'CM',  'GK',  'LB',  'LM',  'LW',  'RB',  'RM',  'RW',  'RWB',  'ST','LWB']

    inputs = []
    for arr in arr_list:
        inputs.append(int(request.POST.get(arr)))

    prefers = [] if request.POST.getlist('prefer[]') is None else request.POST.getlist('prefer[]')
    for prefer in prefer_list:
        if prefer in prefers:
            inputs.append(1)
        else:
            inputs.append(0)
    # import os
    save_model_path =os.path.dirname(os.path.abspath(__file__)) + '/model.h5'
    inputs = np.array(inputs)

    model =  Model(inputs.shape[0])
    model.load_weights(save_model_path)
    wage = int(model.predict(np.expand_dims(inputs, 0))[0][0])

#     import psutil
#     process = psutil.Process(os.getpid())
#     print(process.memory_info().rss/786/1000000,' Mb')  # in bytes 
    return HttpResponse(json.dumps({'wage':wage}), content_type='application/json')


