import numpy
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import mplfinance as mpf


# fix random seed for reproducibility
numpy.random.seed(7)


    
def setTicker(t): 
    ticker= t
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=58O211IRNVWF6FTD&datatype=csv'
    names = ['date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(url, names=names, skiprows=1)   
    saved_df = df
    df = df.iloc[::-1]
    data=df.filter(['close'])
    dataset = data.values

    # split into train and test sets
    train_size = math.ceil(len(dataset)*.8)


    # normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1)) 
    ds = scaler.fit_transform(dataset)

    train = ds[0:train_size,:]
    trainX= [] 
    trainY = []
    for i in range(60, len(train)):
        trainX.append(train[i-60:i,0])
        trainY.append(train[i,0])
        
    trainX,trainY = numpy.array(trainX) ,   numpy.array(trainY)

    # reshape input to be [samples, time steps, features]
    trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1],1))

    # create  LSTM network
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape= (trainX.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile and fit the model
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=4, batch_size=1)


    test = ds[train_size-60:, :]

    testX= []

    testY = dataset[train_size:,:]
    for i in range(60, len(test)):
        testX.append(test[i-60:i,0])

    testX = numpy.array(testX)

    testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))


    # make predictions
    testPredict = model.predict(testX)
    # invert prediction
    testPredict = scaler.inverse_transform(testPredict)

    # calculate root mean squared error
    testScore = numpy.sqrt(numpy.mean(testPredict - testY)**2)
    print('Test Score: %.2f RMSE' % (testScore))
    
    #plot data
    train = data[:train_size]
    valid= data[train_size:]
    valid['Predictions'] = testPredict
    print(valid)

    
   # show data 
    plt.figure(figsize=(16,8))
    plt.title("LTSM")
    plt.xlabel('Date', fontsize = 18)
    plt.ylabel("Close price", fontsize = 18)
    plt.plot(train['close'])
    plt.plot(valid[['close', 'Predictions']])
    plt.legend(['Train', 'Val', 'Predictions'], loc = 'lower right')
    plt.savefig("static/graph.png")
    