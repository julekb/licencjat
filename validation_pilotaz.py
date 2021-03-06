#python3


import numpy as np
from sklearn import cross_validation
import pandas as pd



def cross_validation(X, Y):

	from sklearn.metrics import mean_squared_error as mse
	from sklearn import cross_validation, linear_model
	from math import exp, log
	from sklearn.neighbors import NearestNeighbors as NN
	from sklearn.neighbors import KNeighborsClassifier as KNC
	from sklearn.neighbors import KNeighborsRegressor as KNR

	N = 31

	resultsX = []
	resultsId = []
	resultsRegr = []
	resultsRegr_ey = []
	resultsRegr_log = []
	results1NN, results2NN, results3NN = [], [], []
	resultsY = []

	


	kf = cross_validation.KFold(N, n_folds=10, random_state=True)
	#kf = cross_validation.LeaveOneOut(N) #LeaveOneOut == KFold(n, n_folds=n)
	for train_index, test_index in kf:
		X_train, Y_train = X[train_index], Y[train_index]
		X_test, Y_test = X[test_index], Y[test_index]
		print(X_train, X_test)

		resultsX.append(X_test)
		resultsId.append(Y_test)
		resultsY.append(Y_test)

		X_train_list = [[x] for x in X_train]

		regr = linear_model.LinearRegression().fit(X_train_list, Y_train)
		resultsRegr += [[float(regr.predict(x)) for x in X_test]]

		regr_ey = linear_model.LinearRegression().fit(np.exp(X_train_list), Y_train)
		resultsRegr_ey += [[float(regr_ey.predict(np.exp(x))) for x in X_test]]
		# X_regr_ey = []
		# for x in X_test:
		# 	x_regr = float(regr_ey.predict(x))
		# 	if (x_regr >= 1):
		# 		X_regr_ey.append(log(x_regr))
		# 	else:
		# 		X_regr_ey.append(1)

		# resultsRegr_ey += [X_regr_ey]
		# resultsRegr_ey += [[log(float(regr_ey.predict(x))) for x in X_test]]
		# resultsRegr_ey += [[log(abs(float(regr_ey.predict(x)))) for x in X_test]]


		regr_log = linear_model.LinearRegression().fit(np.log(X_train_list), Y_train)
		resultsRegr_log += [[float(regr_log.predict(np.log(x))) for x in X_test]]		
		#Y_train = np.asarray(Y_train, dtype="|S6")
		nb1NN =KNR(n_neighbors=1, algorithm='ball_tree').fit(X_train_list, Y_train)
		results1NN += [[float(nb1NN.predict(x)[0]) for x in X_test]]

		nb2NN =KNR(n_neighbors=2, algorithm='ball_tree').fit(X_train_list, Y_train)
		results2NN += [[float(nb2NN.predict(x)[0]) for x in X_test]]

		nb3NN =KNR(n_neighbors=3, algorithm='ball_tree').fit(X_train_list, Y_train)
		results3NN += [[float(nb3NN.predict(x)[0]) for x in X_test]]

	


	#return [mse(resultsX, resultsId), mse(resultsX, resultsRegr), mse(resultsX, resultsRegr_ey), mse(resultsX, resultsRegr_log), mse(resultsX, results1NN), mse(resultsX, results2NN), mse(resultsX, results3NN)]
	return [mse(resultsX, resultsId), mse(resultsY, resultsRegr), mse(resultsY, resultsRegr_ey), mse(resultsY, resultsRegr_log), mse(resultsY, results1NN), mse(resultsY, results2NN), mse(resultsY, results3NN)]





import getdata_script as gd
from os import listdir
from os.path import isfile, join
# df = gd.GetData(gd.f)


MSEId, MSERegr, MSERegr_ey, MSE_log, MSE1NN, MSE2NN, MSE3NN = 0, 0, 0, 0, 0, 0, 0
MSE = [0, 0, 0, 0, 0, 0, 0]
path = 'data_all/'
#onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
#path = ''
onlyfiles1 = ['aaa', 'data_test.csv']

onlyfiles = ['pilotaz'+str(i+1)+'.csv' for i in range(5)]
print(onlyfiles)

for file in onlyfiles:
	DF = gd.get_data(path+file)
	
	CV = cross_validation((DF['stimulus']), (DF['converted']))
	MSE2 = MSE
	MSE = [MSE2[i] + CV[i] for i in range(len(CV))]

l = len(onlyfiles)
msn_labels = ['MSEId:', 'MSERegr:', 'MSERegr_ey:', 'MSE_log:', 'MSE1NN:', 'MSE2NN:', 'MSE3NN:']
for index, mse in enumerate(MSE):
	print(msn_labels[index] + " ", mse/l)



	# print(cross_validation((df['stimulus']), (df['converted'])))

