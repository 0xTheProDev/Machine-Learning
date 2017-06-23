# Machine Learning by Progyan1997
# MIT License
# Program: Regression - Estimation of relation between variables

import math
import pandas
import quandl

DataFrame = quandl.get('WIKI/GOOGL')		# Getting the actual dataset from Quandl
DataFrame = DataFrame[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
DataFrame['HL_PCT'] = ( DataFrame['Adj. High'] - DataFrame['Adj. Close'] ) / DataFrame['Adj. Close'] * 100.0					# Calculating % rise of High value
DataFrame['CNG_PCT'] = ( DataFrame['Adj. Close'] - DataFrame['Adj. Open'] ) / DataFrame['Adj. Open'] * 100.0					# Calculating % change in a Day
DataFrame = DataFrame[['Adj. Close', 'HL_PCT', 'CNG_PCT', 'Adj. Volume']]
						# Features for our learning

ForeCast_col = 'Adj. Close'				# Selecting it as our prediction
DataFrame.fillna(-99999, inplace=True)			# Filling up NaN columns
ForeCast_out = int(math.ceil(0.0001 * len(DataFrame)))	# 10% of the number of Records

DataFrame['Label'] = DataFrame[ForeCast_col].shift(-ForeCast_out)	# Shifting our columns
DataFrame.dropna(inplace=True)						# Remove NaN

print(DataFrame.head())
print(DataFrame.tail())
