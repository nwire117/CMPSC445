# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 17:30:24 2022

@author: Jason
"""

from pandas_datareader import data
import urllib.request, json
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np 
import pandas as pd
import datetime as dt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import StandardScaler


def train():
    
    return "#RockyMusic"

def prediction():
    
    return "prediction complete"

def setTicker(t): 
    ticker= t
    print(ticker)
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=RCURB8MB4MUMOVQT&datatype=csv'
    #names = ['date', 'open', 'high', 'low', 'close', 'volume']

    df = pd.read_csv(url)

    df = df.loc[::-1].reset_index(drop=True)
    dfParsed = df[['timestamp', 'open', 'close']]

    dfParsed['timestamp'] = pd.to_datetime(df['timestamp'])
    extracted = dfParsed['timestamp']
    dfParsed.set_index('timestamp', drop = True, inplace = True)

    openPrice = dfParsed['open'].values
    closePrice = dfParsed['close'].values
    intradayChange = openPrice - closePrice
    upDown = []

    for i in range(len(intradayChange)):
        if intradayChange[i] > 0:
            upDown.append(1)
        elif intradayChange[i] < 0:
            upDown.append(-1)
        else:
            upDown.append(0)
            

    dfUpDown = pd.DataFrame(upDown, columns = ['Up/Down'])
    dfUpDown.insert(0, 'Date', extracted)
    dfUpDown.set_index('Date', drop = True, inplace = True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    dfUpDownMMS = scaler.fit_transform(dfUpDown)
    dfUpDownStandard = StandardScaler().fit_transform(dfUpDown)
