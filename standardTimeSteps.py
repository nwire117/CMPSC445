# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:31:39 2022

@author: Jason
"""

import math
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
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

'''
Use these variables to change any of the parameters.
Cannot add layers yet, work in progress

'''

sizeOfDataset = 5           # 1-100 percent of total data, more takes longer
trainingSize = 67           # 1-100 percent of dataset
lookBack = 5                # 1-100 percent of training data
lstmNeurons = 4             # any number, but more is not always better
denseNeurons = 2            # any number, does not need to be used, higher is not always better
numEpochs = 100             # any number, higher is better, but also longer

'''
This is only used for testing, can be removed for final submission
'''
# fix random seed for reproducibility
np.random.seed(7)

#ticker = input("Enter ticker: ")


#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=RCURB8MB4MUMOVQT&datatype=csv'
#names = ['date', 'open', 'high', 'low', 'close', 'volume']

df = pd.read_csv('daily_aapl.csv')

df = df.loc[::-1].reset_index(drop=True)
dfParsed = df[['timestamp', 'open', 'close']]

dfParsed['timestamp'] = pd.to_datetime(df['timestamp'])
extracted = dfParsed['timestamp']
dfParsed.set_index('timestamp', drop = True, inplace = True)

openPrice = dfParsed['open'].values
closePrice = dfParsed['close'].values
intradayChange = openPrice - closePrice
dfIntradayChange=pd.DataFrame(intradayChange, columns=['Change'])

dfIntradayChange.insert(0, 'Date', extracted)
dfIntradayChange.set_index('Date', drop = True, inplace = True)
upDown = []

dfIntradayChangeAbridged = dfIntradayChange[int(len(dfIntradayChange) * ((100-sizeOfDataset)/100)):]

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

'''
plt.plot(intradayChange)
plt.xlabel("intradayChange")
plt.show()
'''

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dfMMS = scaler.fit_transform(dfIntradayChangeAbridged)
dfStandard = StandardScaler().fit_transform(dfIntradayChangeAbridged)

'''
plt.plot(dfMMS)
plt.xlabel("dfMMS")
plt.show()

plt.plot(dfStandard)
plt.xlabel("dfStandard")
plt.show()
'''

# split into train and test sets
train_size = int(len(dfStandard) * (trainingSize/100))
test_size = len(dfStandard) - train_size
train, test = dfStandard[0:train_size,:], dfStandard[train_size:len(dfStandard),:]
print(len(train), len(test))

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

# reshape into X=t and Y=t+1
look_back = lookBack
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

# create and fit the LSTM network
batch_size = 1
model = tf.keras.Sequential()
#model.add(LSTM(16, batch_input_shape=(batch_size, look_back, 1), stateful=True, return_sequences=True))
model.add(LSTM(int(lstmNeurons), batch_input_shape=(batch_size, look_back, 1), stateful=True))
model.add(Dense(int(denseNeurons)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
for i in range(int(numEpochs)):
	model.fit(trainX, trainY, epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
	model.reset_states()

# make predictions
trainPredict = model.predict(trainX, batch_size=batch_size)
model.reset_states()
testPredict = model.predict(testX, batch_size=batch_size)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))

# shift train predictions for plotting
trainPredictPlot = np.empty_like(dfStandard)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = np.empty_like(dfStandard)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dfStandard)-1, :] = testPredict

# plot baseline and predictions
plt.plot(scaler.inverse_transform(dfStandard))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.xlabel("dfStandard lookback5")
plt.show()

