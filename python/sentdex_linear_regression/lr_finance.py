##### 1
import pandas as pd
import quandl, math, datetime, time
import numpy as np
from sklearn import preprocessing, model_selection, svm #svm is here for regression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

df = quandl.get('WIKI/GOOGL')

df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']] # showing the data availabe

#### 2
df['HL_PCT'] = (df['Adj. High']-df['Adj. Close'])/df['Adj. Close']*100.0
df['PCT_change'] = (df['Adj. Close']-df['Adj. Open'])/df['Adj. Open']*100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']] # assembling all features at one place

#print(df['Adj. Close'].values) --> converts automatically into numpy array

##### 3
forecast_col = 	'Adj. Close'
#print(len(df['Adj. Close']))
#print(df['Adj. Close'])
df.fillna(-99999, inplace=True) # just filling the NaN values with -99999

forecast_out = int(math.ceil(0.01*len(df))) # just getting a number

df['label']=df[forecast_col].shift(-forecast_out) # just shifting the column by mentioned value. Essentially making room for values which we are going to predict in next lec
df.dropna(inplace=True)
#print(df['label'])
#print(df.head())

##### 4
X = np.array(df.drop(['label'],1)) #drop the column 'label' and take rest of them (features) as X
y = np.array(df['label']) #np.array converts a data frame (/matrix) into an array

X = preprocessing.scale(X) #normalizing the X into -1 to 1
# This can guarantee stable convergence of weight and biases

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2) #model_selection.train_test_split() function (shuffles and) separates the data frames into two random data frames

X_lately = X[-forecast_out:] #rows that we have to predict
X = X[:-forecast_out] #data frame raws which are already there

clf = LinearRegression() #Regression classifier
#documentation about linear regression model : http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
#detailed parameters: n_jobs --> meaning number of CPU threads
#like --> clf = LinearRegression(n_jobs = 10) --> and processing will be fast, essentially parallel processing (-1 for full power of CPUs)

#clf = svm.SVR() #SVM SVR classifier #default kernel is linear
#clf = svm.SVR(kernel = 'poly') #SVM SVR + kernel = poly
clf.fit(X_train, y_train) #train this classifier 
accuracy = clf.score(X_test, y_test) #test this classifier

##### 5
forecast_set = clf.predict(X_lately) #predicting the outcome (y) for NaN set of features (X)
#most IMP
print(forecast_set, accuracy, forecast_out)

df['Forecast'] = np.nan #create a new col labeled as 'Forecast' and fill in 'nan' values

#generating the dates, because prediction doesnt know about date and time stamps
last_date = df.iloc[-1].name #last date starts from -1
#last_unix = last_date.timestamp()
last_unix = time.mktime(last_date.timetuple())
one_day = 86400 #seconds in one day
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += one_day
	df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i] #taking each forecast_set and day, and then setting those as values in data frame; basically making future features as not a number; and then the last line takes all of the first columns, sets them to NaN; and the final col wherever the i is which is the forecast in this case

#over here 'next_date' is basically the next index

df[forecast_col].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
