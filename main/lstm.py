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
from pandas.tseries.offsets import DateOffset


# fix random seed for reproducibility
numpy.random.seed(7)


    
def setTicker(t): 
    ticker = t
       
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=58O211IRNVWF6FTD&datatype=csv'
    names = ['date', 'open', 'high', 'low', 'close', 'volume']
    df = pd.read_csv(url, names=names, skiprows=1)   
    saved_df = df
    df = df.iloc[::-1]
    df['date'] = pd.to_datetime(df['date'])
    #df['date'] = df['date'].dt.date
    
    df = df.set_index('date')
  
    data=df.filter(['close'])
    dataset = data.values
    
        # split into train and test sets
    train_size = math.ceil(len(dataset)*.4)
        
    
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
    model.fit(trainX, trainY, epochs=1, batch_size=1)
    
    
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
        
    pred_list = []
    batch = test[-60:].reshape((1, 60, 1))
    for i in range(5):   
        pred_list.append(model.predict(batch)[0]) 
        batch = numpy.append(batch[:,1:,:],[[pred_list[i]]],axis=1)
    
    add_dates = [df.index[-1] + pd.DateOffset(days = x) for x in range(0,6) ]
    future_dates = pd.DataFrame(index=add_dates[1:],columns=df.columns)
    
    df_predict = pd.DataFrame(scaler.inverse_transform(pred_list),
                              index=future_dates[-5:].index, columns=['Future Prediction'])
    
    df_proj = df.join(df_predict, how = 'outer')
    
    df_proj.index = df_proj.index.strftime('%m-%d-%Y')
    
    print(df_proj.tail(12))
        
        # calculate root mean squared error
    testScore = numpy.sqrt(numpy.mean(testPredict - testY)**2)
    print('Test Score: %.2f RMSE' % (testScore))
     
       
    #plot data
    train = data[:train_size]
    valid= data[train_size:]
    valid['Predictions'] = testPredict
    print(valid)
    
    valid.index = valid.index.strftime('%m-%d-%Y')
    train.index = train.index.strftime('%m-%d-%Y')
    
    newest= len(df_proj)
    print(newest)
    start = newest-30
        
    # show data 
    plt.figure(figsize=(16,8))
    plt.title("LSTM")
    plt.xlabel('Date', fontsize = 18)
    plt.ylabel("Close price", fontsize = 18)
    plt.plot(train['close'])
    val, = plt.plot(valid['close'], 'b', label = 'Val')
    pred, = plt.plot(valid['Predictions'], 'm', label = 'Predictions')
    f_pred, = plt.plot(df_proj['Future Prediction'], 'g', label = 'Future Predictions')
    plt.xlim(start, newest)
    plt.xticks( numpy.arange(start, newest, 2))
    plt.xticks(rotation = 45)
    plt.legend([val, pred, f_pred], ['Val', 'Prediction', 'Future Predictions'], loc = 'upper right')
    plt.savefig("static/graph.png")

    