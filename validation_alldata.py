#python3

import numpy as np
from sklearn import cross_validation
import pandas as pd
import pickle

# CrossValidation() imports
from sklearn.metrics import mean_squared_error as mse
from sklearn import cross_validation, linear_model
from math import exp, log
from sklearn.neighbors import KNeighborsRegressor as KNR


def CrossValidation(X, Y):

	# X - lista data['stimulus']
	# Y - lista data['converted']

	resultsX = []
	resultsId = []
	resultsRegr = []
	resultsRegr_ey = []
	resultsRegr_log = []
	results1NN, results2NN, results3NN = [], [], []
	resultsY = []

	kf = cross_validation.LeaveOneOut(N)
	#kf = cross_validation.LeaveOneOut(N) #LeaveOneOut == KFold(n, n_folds=n)
	for train_index, test_index in kf:
		X_train, Y_train = X[train_index], Y[train_index]
		X_test, Y_test = X[test_index], Y[test_index]
		
		resultsX.append(X_test.values[0])
		resultsId.append(Y_test.values[0])
		resultsY.append(Y_test.values[0])

		X_train_list = [[x] for x in X_train]

		regr = linear_model.LinearRegression().fit(X_train_list, Y_train)
		resultsRegr += [[float(regr.predict(x)) for x in X_test]]

		regr_ey = linear_model.LinearRegression().fit(np.exp(X_train_list), Y_train)
		resultsRegr_ey += [[float(regr_ey.predict(np.exp(x))) for x in X_test]]
	

		regr_log = linear_model.LinearRegression().fit(np.log(X_train_list), Y_train)
		resultsRegr_log += [[float(regr_log.predict(np.log(x))) for x in X_test]]		
		
		nb1NN = KNR(n_neighbors=1, algorithm='ball_tree').fit(X_train_list, Y_train)
		results1NN += [[float(nb1NN.predict(x)[0]) for x in X_test]]

		nb2NN = KNR(n_neighbors=2, algorithm='ball_tree').fit(X_train_list, Y_train)
		results2NN += [[float(nb2NN.predict(x)[0]) for x in X_test]]

		nb3NN = KNR(n_neighbors=3, algorithm='ball_tree').fit(X_train_list, Y_train)
		results3NN += [[float(nb3NN.predict(x)[0]) for x in X_test]]


	return resultsX, resultsId, resultsY, resultsRegr, resultsRegr_ey, resultsRegr_log, results1NN, results2NN, results3NN

def PrintMSE():
	names = ["MSEId", "MSERegr", "MSERegr_ey", "MSERegr_log", "MSE1NN", "MSE2NN", "MSE3NN"]
	for i, mse in enumerate([MSEId, MSERegr, MSERegr_ey, MSERegr_log, MSE1NN, MSE2NN, MSE3NN]):
		print(names[i] + ":  ", mse)


N = 31
path = 'data_all/'

with open(path+"data_all.pkl", 'rb') as f:
	data_all = pickle.load(f)

allX, allId, allY, allRegr, allRegr_ey, allRegr_log, all1NN, all2NN, all3NN = [], [], [], [], [], [], [], [], []

for data in data_all:

	resultsX, resultsId, resultsY, resultsRegr, resultsRegr_ey, resultsRegr_log, results1NN, results2NN, results3NN = CrossValidation(data['stimulus'], data['converted'])
	allX += resultsX
	allId += resultsId
	allY += resultsY
	allRegr += resultsRegr
	allRegr_ey += resultsRegr_ey
	allRegr_log += resultsRegr_log
	all1NN += results1NN
	all2NN += results2NN
	all3NN += results3NN

MSEId, MSERegr, MSERegr_ey, MSERegr_log, MSE1NN, MSE2NN, MSE3NN = mse(allX, allId), mse(allY, allRegr), mse(allY, allRegr_ey), mse(allY, allRegr_log), mse(allY, all1NN), mse(allY, all2NN), mse(allY, all3NN)

# print(MSEId, MSERegr, MSERegr_ey, MSE_log, MSE1NN, MSE2NN, MSE3NN)


	# CV = CrossValidation((DF['stimulus']), (DF['converted']))
	# MSE2 = MSE
	# MSE = [MSE2[i] + CV[i] for i in range(len(CV))]

	# l = len(onlyfiles)
	# msn_labels = ['MSEId:', 'MSERegr:', 'MSERegr_ey:', 'MSE_log:', 'MSE1NN:', 'MSE2NN:', 'MSE3NN:']
	# for index, mse in enumerate(MSE):
	# 	print(msn_labels[index] + " ", mse/l)



	# print(CrossValidation((df['stimulus']), (df['converted'])))

