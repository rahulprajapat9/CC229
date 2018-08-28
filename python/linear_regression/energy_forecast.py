##### 1
import pandas
import quandl, math, datetime, time
import numpy as np
from sklearn import preprocessing, model_selection, svm #svm is here for regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


def svc_param_selection(X, y, nfolds):
    Cs = [0.001, 0.01, 0.1, 1, 10]
    gammas = [0.001, 0.01, 0.1, 1]
    param_grid = {'C': Cs, 'gamma' : gammas}
    grid_search = model_selection.GridSearchCV(svm.SVC(kernel='rbf'), param_grid, cv=nfolds)
    grid_search.fit(X, y)
    grid_search.best_params_
    return grid_search.best_params_


dateparse = lambda dates: pandas.datetime.strptime(dates, '%Y-%m-%d %H:%M:%S')

# 1. read_input
# https://archive.ics.uci.edu/ml/datasets/Appliances+energy+prediction
energy_data_df = pandas.read_csv(
	'../input/energydata_complete.csv',
	index_col='date',
	date_parser=dateparse
)

# 2. organize_input
energy_data_df.fillna(-99999, inplace=True)

for lag in range(5):

	print('\n\n\n -------- Running iteration for lag = {} --------'.format(lag))

	energy_data_df['label'] = energy_data_df['Appliances'].shift(-lag)
	energy_data_df.dropna(inplace=True)

	X = np.array(energy_data_df.drop(['Appliances','label','rv1','rv2'],1))
	y = np.array(energy_data_df['label'])

	X = preprocessing.scale(X)

	train_frac = 0.8
	traintest= int(math.ceil(train_frac*len(X)))

	X_train = X[:traintest]
	X_test = X[traintest:]
	y_train = y[:traintest]
	y_test = y[traintest:]

	# 3. analyze_ts
	# granger causality test, cross correlation or ...

	# 4. forecast_ts

	#print('finding optimal value for C and gamma...')
	#svc_params = svc_param_selection(X_train, y_train, None)
	#print(svc_params) # --> {'C': 0.001, 'gamma': 0.001}
	#print('above are the optimal values of C and gamma')
	#time.sleep(55)

	#for model in [LinearRegression(), svm.SVR(), svm.SVR(kernel = 'poly'), svm.SVC()]:
	for model in [svm.SVC(C=100, gamma=0.001)]:

		rgr = model
		#rgr = svm.SVR() #SVM SVR classifier #default kernel is linear
		#rgr = svm.SVR(kernel = 'poly') #SVM SVR + kernel = poly
		#rgr = svm.SVC()

		rgr.fit(X_train, y_train)

		#print('Coefficients: \n', rgr.coef_)

		# 5. evaluate_results
		accuracy = rgr.score(X_test, y_test)

		y_test_predict = rgr.predict(X_test)

		RMSE = np.power(mean_squared_error(y_test, y_test_predict), 1./2,)
		print('\nFor model {}, \n R2_value = {}\n RMSE = {}\n'.format(model,accuracy,RMSE))

		plot = 1
		if plot:
			from matplotlib import pyplot
			pyplot.plot(y_test_predict)
			pyplot.plot(y_test)
			pyplot.show()