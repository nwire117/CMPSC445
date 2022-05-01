# -*- coding: utf-8 -*-
"""ML

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jFkNcoBsXyh8F7X0rijnnWgX4fN9F-Nj
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# use opening, closing, high, and low prices as features and check accuracy
def checkModelAccuracy(predictions, model_name, timespan = 0):
  res = 0
  if(timespan == 0):
    timespan = Y_validation.size
  for i in range(timespan):
    closing_price = float(Y_validation[i])
    prediction = float(predictions[i])
    opening_price = float(X_validation[i][0])

    prediction_diff = prediction - closing_price
    
    reach_percentage = 0.05
    margin_of_error = closing_price * reach_percentage 
    upper_limit = closing_price + margin_of_error
    lower_limit = closing_price - margin_of_error
    expected_change = closing_price - opening_price
    accuracy = 0

    # print("Opening: ", opening_price, "\nClosing: ", closing_price, "\nPrediction: ", prediction, "\nUpper Limit: ", upper_limit, "\nLower Limit: ", lower_limit, "\nExpected Change:", expected_change, "\nPrediction diff: ", prediction_diff, "\n")
    if(upper_limit > prediction and lower_limit < prediction):
      if(expected_change < 0):
        if(prediction < opening_price):
          res += 1
      else:
        if(prediction > opening_price):
          res += 1
  accuracy = (res/timespan) * 100 
  print(model_name + ": " + str(accuracy) + "%")

# use opening price as the only real feature and use the mean of other 3 features as dummy value then check accuracy
def checkModelRealWorldAccuracy(predictions, model_name, timespan = 0):
  print("\n")
  res = 0
  if(timespan == 0):
    timespan = Y_validation.size
  for i in range(timespan):
    closing_price = float(df.iloc[i]['close'])
    prediction = float(predictions[i])
    opening_price = float(df.iloc[i]['open'])

    prediction_diff = prediction - closing_price
    
    reach_percentage = 0.05
    margin_of_error = closing_price * reach_percentage 
    upper_limit = closing_price + margin_of_error
    lower_limit = closing_price - margin_of_error
    expected_change = closing_price - opening_price
    accuracy = 0

    #print("Opening: ", opening_price, "\nClosing: ", closing_price, "\nPrediction: ", prediction, "\nUpper Limit: ", upper_limit, "\nLower Limit: ", lower_limit, "\nExpected Change:", expected_change, "\nPrediction diff: ", prediction_diff, "\n")
    if(upper_limit > prediction and lower_limit < prediction):
      if(expected_change < 0):
        if(prediction < opening_price):
          res += 1
      else:
        if(prediction > opening_price):
          res += 1
  accuracy = (res/timespan) * 100 
  print(model_name + "'s Realword Performance: " + str(accuracy) + "%")

# get ticker from user
ticker = input("Enter stock symbol: ")

# import dataset from url
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=RCURB8MB4MUMOVQT&datatype=csv'
names = ['date', 'open', 'high', 'low', 'close', 'volume']
df = pd.read_csv(url, names=names, skiprows=1)

# split-out test dataset
array = df.values.astype(str)
X = array[:,[1,2,3,5]]
Y = array[:,4]

X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=.20, shuffle=False)
X_validation = X_validation.astype(float)
Y_validation = Y_validation.astype(float)

################# compare all the models of interest by accuracy ##################
print("\nValidation accuracies of the models:")
# 1) K nearest mean
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

# train the model 
knn.fit(X_train, Y_train)

# make predictions 
predictions = knn.predict(X_validation)

# check the accuracy on test data
checkModelAccuracy(predictions, 'KNN')

# 2) Gaussian Naive Bayes (NB)
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()

# train the model 
gnb.fit(X_train, Y_train)

# make predictions 
predictions = gnb.predict(X_validation)

# check the accuracy on test data
checkModelAccuracy(predictions, 'NB')

# 3) Linear Regression
from sklearn import linear_model
ln_regression = linear_model.LinearRegression()

# train the model 
ln_regression.fit(X_train, Y_train)

# make predictions 
predictions = ln_regression.predict(X_validation)

# check the accuracy on test data
checkModelAccuracy(predictions, 'Linear Regression')

##############################################

# test the chosen model
test_length = 30
prediction = []
avg_high = 0 
avg_low = 0 
avg_vol = 0
next_day = 0

for i in range(test_length):
  avg_high = df.head(i+1)['high'].mean()
  avg_low = df.head(i+1)['low'].mean()
  avg_vol = df.head(i+1)['volume'].mean()

  next_day = [[df.iloc[i]['close'], avg_high, avg_low, avg_vol]]
  prediction.append(ln_regression.predict(next_day))

checkModelRealWorldAccuracy(prediction, 'Linear Regression', test_length)

# predict next day's closing price
averaging_timespan = 7
avg_high = df.head(averaging_timespan)['high'].mean()
avg_low = df.head(averaging_timespan)['low'].mean()
avg_vol = df.head(averaging_timespan)['volume'].mean()

next_day = [[df.iloc[0]['close'], avg_high, avg_low, avg_vol]]
next_day_prediction_val = ln_regression.predict(next_day)

# get next day's predicted price of the chosen stock and return it
def getNextDayPrediction():
  return next_day_prediction_val[0]

print("\nTomorrow's price for", ticker, "will be:", getNextDayPrediction())