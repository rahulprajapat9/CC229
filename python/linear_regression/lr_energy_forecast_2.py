##### 1
import pandas
import quandl, math, datetime, time
import numpy as np
from sklearn import preprocessing, model_selection, svm #svm is here for regression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

dateparse = lambda dates: pandas.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')

##### 2
energy_data_df = pandas.read_csv(
	'../input/energydata_complete.csv',
	index_col='date',
	date_parser=dateparse
)

#print(list(energy_data_df))
#energy_data_df['Appliances'].plot()
#plt.show()

#print(energy_data_df['Appliances'].values)

##### 3
forecast_col = 'Appliances'

energy_data_df.fillna(-99999, inplace=True)
forecast_out = int(math.ceil(0.01*len(energy_data_df))) # predicting 1% of training length

energy_data_df['label']=energy_data_df[forecast_col].shift(-forecast_out)
energy_data_df.dropna(inplace=True)
#print(energy_data_df['label'])
#print(energy_data_df.head())

##### 4
#drop the column 'label' and take rest of them (features) as X
X = np.array(energy_data_df.drop(['label'],1))
y = np.array(energy_data_df['label'])

X = preprocessing.scale(X) #normalizing the X into -1 to 1

#model_selection.train_test_split() function (shuffles and) separates the data frames into two random data frames
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

X_lately = X[-forecast_out:]
X = X[:-forecast_out]

clf = LinearRegression()
#clf = svm.SVR() #SVM SVR classifier #default kernel is linear
#clf = svm.SVR(kernel = 'poly') #SVM SVR + kernel = poly

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

##### 5
forecast_set = clf.predict(X_lately)
print(forecast_set, accuracy, forecast_out)

energy_data_df['Forecast'] = np.nan

last_date = energy_data_df.iloc[-1].name
last_unix = time.mktime(last_date.timetuple())
one_day = 86400 #seconds in one day
next_unix = last_unix + one_day

for i in forecast_set:
	next_date = datetime.datetime.fromtimestamp(next_unix)
	next_unix += one_day
	energy_data_df.loc[next_date] = [np.nan for _ in range(len(energy_data_df.columns)-1)] + [i]
#taking each forecast_set and day, and then setting those as values in data frame;
# basically making future features as not a number; and then the last line takes all of the first columns,
# sets them to NaN; and the final col wherever the i is which is the forecast in this case

#over here 'next_date' is basically the next index

energy_data_df[forecast_col].plot()
energy_data_df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
