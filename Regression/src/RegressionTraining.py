# Machine Learning by Progyan1997
# MIT License
# Program: Regression - Estimation of relation between variables

import datetime
import math
from matplotlib import style
import matplotlib.pyplot as plot
import numpy
import pandas
import quandl
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

style.use('ggplot')				# Defining a graph

DataFrame = quandl.get('WIKI/GOOGL')		# Getting the actual dataset from Quandl
DataFrame = DataFrame[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
DataFrame['HL_PCT'] = ( DataFrame['Adj. High'] - DataFrame['Adj. Close'] ) / DataFrame['Adj. Close'] * 100.0					# Calculating % rise of High value
DataFrame['CNG_PCT'] = ( DataFrame['Adj. Close'] - DataFrame['Adj. Open'] ) / DataFrame['Adj. Open'] * 100.0					# Calculating % change in a Day
DataFrame = DataFrame[['Adj. Close', 'HL_PCT', 'CNG_PCT', 'Adj. Volume']]
						# Features for our learning

ForeCast_col = 'Adj. Close'				# Selecting it as our prediction
DataFrame.fillna(-99999, inplace=True)			# Filling up NaN columns
ForeCast_out = int(math.ceil(0.005 * len(DataFrame)))	# 0.5% of the number of Records

DataFrame['Label'] = DataFrame[ForeCast_col].shift(-ForeCast_out)	# Shifting our columns

X = numpy.array(DataFrame.drop(['Label'], 1))	# Features: Everything except `label` col(1)
X = preprocessing.scale(X)			# Normalize the dataset features
X_Lately = X[-ForeCast_out:]			# Dataset that are to be predicted
X = X[:-ForeCast_out]				# Dataset that are used for prediction

DataFrame.dropna(inplace=True)			# Remove NaN
y = numpy.array(DataFrame['Label'])		# Labels: Selecting `label` column

X_Train, X_Test, y_Train, y_Test = cross_validation.train_test_split(X, y, test_size = 0.5)
					# Train data and Test data from 20% of dataset

Classifier = LinearRegression()			# Define a classifier by Linear Regression
						# also, Classifier = svm.SVR()
Classifier.fit(X_Train, y_Train)		# Import Training data to the classifier
accuracy = Classifier.score(X_Test, y_Test)	# Testing the accuracy of the classifier
ForeCast_set = Classifier.predict(X_Lately)	# Predicting the data

# print(ForeCast_set, accuracy, ForeCast_out)

DataFrame['Forecast'] = numpy.nan		# Creating a new column filled with NaN

Last_Date = DataFrame.iloc[-1].name		# Creating Date-Time against each entry
Last_TimeStamp = Last_Date.timestamp()
Next_TimeStamp = Last_TimeStamp + 86400

for i in ForeCast_set:
	Next_Date = datetime.datetime.fromtimestamp(Next_TimeStamp)
	Next_TimeStamp += 86400
	DataFrame.loc[Next_Date] = [numpy.nan for _ in range(len(DataFrame.columns) - 1)] + [i]

DataFrame['Adj. Close'].plot()			# Ploting the curve of Price (estimated & 
DataFrame['Forecast'].plot()			# actual) against Date axis
plot.legend(loc = 4)
plot.xlabel('Date')
plot.ylabel('Price')
plot.show()
