import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler
import mplfinance as mpf
import io
import IPython.display as IPydisplay

'''
apikey: 58O211IRNVWF6FTD

'''
ticker = input("Enter stock symbol: ")


url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=58O211IRNVWF6FTD&datatype=csv'
names = ['date','open', 'high', 'low', 'close', 'volume']
df = pd.read_csv(url, names=names, skiprows=1)

df.date= pd.to_datetime(df.date)

df = df.set_index('date')
df = df.iloc[::-1]

cancan = io.BytesIO()

mpf.plot(df['2022-04'], type='candle', volume=True, tight_layout = True, title= ticker + ' price', style='yahoo', savefig = cancan)
cancan.seek(0)
IPydisplay.Image(cancan.read())

