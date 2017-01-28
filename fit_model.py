import numpy as np
from sklearn import cross_validation, linear_model
import pandas as pd
import pickle as pkl

from math import exp, log

N = 31
path = "data_all/"

with open(path+"avg_mean_sd.pkl", 'rb') as f:
	avg_mean_sd = pkl.load(f)

with open(path+"data_all.pkl", 'rb') as f:
	data_all = pkl.load(f)

#sortowanie po bodźcu
avg_mean_sd = avg_mean_sd.sort_values('stimulus')
avg_mean_sd = avg_mena_sd.reset_index(drop=True)

for d in data_all:
	d = d.sort_values('stimulus')
	d = d.reset_index(drop=True)


X_avg = avg_mean_sd['mean']
X_avg = [[x] for x in X_avg]

#różny Y
regr_log = linear_model.LinearRegression().fit(X_avg, Y)
# regr_log.coef_


# def FitRegr_log(X, Y):
	#dopasowanie indywidualnego modelu dla konkretnej osoby

	# resultsX = []
	# resultsRegr_log = []

	# kf = corss_validation.KFold(N, n_folds=N, random_state=True)

	# for train_index, test_index in kf:
	# 	X_train, Y_train = X[train_index], Y[train_index]
	# 	X_test, Y_test = X[test_index], Y[test_index]

	# 	resultsX.append(X_test)

	# 	X_train_list = [[x] for x in X_train]

	# 	regr_log = linear_model.LinearRegression().fit(np.log(X_train_list), Y_train)
	# 	resultsRegr_log += [[float(regr_log.predict(np.log(x))) for x in X_test]]

