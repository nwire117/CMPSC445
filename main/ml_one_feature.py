# -*- coding: utf-8 -*-
"""ML_one_feature.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MtYaTIqQtVqcAKw3ZyL6bJLGPyQKW2Ds
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import warnings
from sklearn.exceptions import DataConversionWarning

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=DataConversionWarning)

# use opening price as the only feature and check accuracy
def checkModelAccuracy(predictions, model_name, timespan = 0):
  res = 0
  if(timespan == 0):
    timespan = Y_test.size
  for i in range(timespan):
    closing_price = float(Y_test[i])
    prediction = float(predictions[i])
    opening_price = float(X_test[i][0])

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

# get ticker from user
ticker = input("Enter stock symbol: ")

# import dataset from url
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker +'&outputsize=full&apikey=RCURB8MB4MUMOVQT&datatype=csv'
names = ['date', 'open', 'high', 'low', 'close', 'volume']
df = pd.read_csv(url, names=names, skiprows=1)

# split-out test dataset
array = df.values.astype(str)
X = array[:,1]
Y = array[:,4]
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.20, shuffle=False)
X_test = X_test.astype(float)
Y_test = Y_test.astype(float)

################# compare all the models of interest by accuracy ##################
print("\nValidation accuracies of the models:")
# 1) K nearest mean
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()

# train the model 
knn.fit(X_train, Y_train)

# make predictions 
predictions = knn.predict(X_test)

# check the accuracy on test data
checkModelAccuracy(predictions, 'KNN')

# 2) Gaussian Naive Bayes (NB)
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()

# train the model 
gnb.fit(X_train, Y_train)

# make predictions 
predictions = gnb.predict(X_test)

# check the accuracy on test data
checkModelAccuracy(predictions, 'NB')

# 3) Linear Regression
from sklearn import linear_model
ln_regression = linear_model.LinearRegression()

# train the model 
ln_regression.fit(X_train, Y_train)

# make predictions 
predictions = ln_regression.predict(X_test)

# check the accuracy on test data
checkModelAccuracy(predictions, 'Linear Regression')

##############################################

# predict next day's closing price
next_day = [[df.iloc[0]['close']]]
next_day_prediction_val = ln_regression.predict(next_day)

# get next day's predicted price of the chosen stock and return it
def getNextDayPrediction():
  return next_day_prediction_val[0][0]

print("\nTomorrow's price for", ticker, "will be:", getNextDayPrediction())