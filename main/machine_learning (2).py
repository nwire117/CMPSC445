# -*- coding: utf-8 -*-
"""Machine_learning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jFkNcoBsXyh8F7X0rijnnWgX4fN9F-Nj
"""

import pandas as pd
from sklearn.model_selection import train_test_split

ticker = input("Enter stock symbol: ")

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=RCURB8MB4MUMOVQT&datatype=csv'
names = ['date', 'open', 'high', 'low', 'close', 'volume']
dataset = pd.read_csv(url, names=names, skiprows=1)

# split-out test dataset
array = dataset.values.astype(str)
X = array[:,1:5]
Y = array[:,4]

# train the model
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.40)


# K nearest mean
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

# train the model 
knn.fit(X_train, Y_train)

# make predictions 
predictions = knn.predict(X_test)

# check the accuracy on test data
res = 0
for i in range(60):
  closing_price = float(Y_test.item(i))
  prediction = float(predictions.item(i))
  opening_price = float(X_test[i].item(0))

  prediction_diff = prediction - closing_price
  reach_percentage = 0.1
  tmp = (closing_price - opening_price) * reach_percentage

  if(tmp < 0):
    if(prediction_diff > tmp):
      res += 1
  else:
    if(prediction_diff < tmp):
      res += 1
  accuracy = (res/60) * 100 
print(str(accuracy) + "%")