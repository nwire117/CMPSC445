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
import io
import mplfinance as mpf

def train():
    
    return "#RockyMusic"

def prediction():
    
    return "prediction complete"

def setTicker(t): 
    ticker= t
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=58O211IRNVWF6FTD&datatype=csv'
    names = ['date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(url, names=names, skiprows=1)

    df.date= pd.to_datetime(df.date)

    df = df.set_index('date')
    df = df.iloc[::-1]

    
    mpf.plot(df['2022-04'], type='candle', volume=True, tight_layout = True, title= ticker + ' price', style='yahoo', savefig ='graph.png')
    
