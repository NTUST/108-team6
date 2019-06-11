import json
import os

import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from keras import losses
from keras import optimizers
from keras import regularizers
from keras.layers import BatchNormalization, Dense, LeakyReLU
from keras.models import Sequential


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
    return render(request, "analysis.html",{'title':'Analysis'})

@csrf_exempt
def predict_result(request):
    arr_list = ['Age', 'Overall', 'Potential', 'Special', 'Acceleration', 'Aggression', 'Agility', 'Balance', 'Ball Control', 'Composure', 'Crossing', 'Curve', 'Dribbling', 'Finishing', 'Free Kick Accuracy', 'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Heading Accuracy', 'Interceptions', 'Jumping', 'Long Passing', 'Long Shots', 'Marking', 'Penalties', 'Positioning', 'Reactions', 'Short Passing', 'Shot Power', 'Sliding Tackle', 'Sprint Speed', 'Stamina', 'Standing Tackle', 'Strength', 'Vision', 'Volleys']
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

    wage = predict_wage(np.array(inputs))
#     import psutil
#     process = psutil.Process(os.getpid())
#     print(process.memory_info().rss/786/1000000,' Mb')  # in bytes 
    return HttpResponse(json.dumps({'wage':wage,'title':'Analysis'}), content_type='application/json')


def predict_wage(inputs):
    save_model_path = os.path.dirname(os.path.abspath(__file__)) + '/model.h5'
    model = Model(inputs.shape[0])
    model.load_weights(save_model_path)
    return int(model.predict(np.expand_dims(inputs, 0))[0][0])