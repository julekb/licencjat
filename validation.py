#python3


import numpy as np
from sklearn import cross_validation



def CrossValidation(X, Y):

	from sklearn.metrics import mean_squared_error as mse
	from sklearn import cross_validation, linear_model
	from math import exp, log
	from sklearn.neighbors import NearestNeighbors as NN
	from sklearn.neighbors import KNeighborsClassifier as KNC

	N = 30

	resultsX = []
	resultsId = []
	resultsRegr = []
	resultsRegr_ey = []
	results1NN, results2NN, results3NN = [], [], []

	


	kf = cross_validation.KFold(N, n_folds=10, random_state=True)
	for train_index, test_index in kf:
		X_train, Y_train = X[train_index], Y[train_index]
		X_test, Y_test = X[test_index], Y[test_index]

		resultsX.append(X_test)
		resultsId.append(Y_test)

		X_train_list = [[x] for x in X_train]

		regr = linear_model.LinearRegression().fit(X_train_list, Y_train)
		resultsRegr += [[float(regr.predict(x)) for x in X_test]]

		regr_ey = linear_model.LinearRegression().fit(X_train_list, [exp(y) for y in Y_train])
		resultsRegr_ey += [[log(float(regr_ey.predict(x))) for x in X_test]]
		
		Y_train = np.asarray(Y_train, dtype="|S6")
		nb1NN =KNC(n_neighbors=1, algorithm='ball_tree').fit(X_train_list, Y_train)
		results1NN += [[float(nb1NN.predict(x)[0]) for x in X_test]]

		nb2NN =KNC(n_neighbors=2, algorithm='ball_tree').fit(X_train_list, Y_train)
		results2NN += [[float(nb2NN.predict(x)[0]) for x in X_test]]

		nb3NN =KNC(n_neighbors=3, algorithm='ball_tree').fit(X_train_list, Y_train)
		results3NN += [[float(nb3NN.predict(x)[0]) for x in X_test]]

	


	return mse(resultsX, resultsId), mse(resultsX, resultsRegr), mse(resultsX, resultsRegr_ey), mse(resultsX, results1NN), mse(resultsX, results2NN), mse(resultsX, results3NN)





import getdata_script as gd
df = gd.GetData(gd.f)



print(CrossValidation((df['stimulus']), (df['converted'])))