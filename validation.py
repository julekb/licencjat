import numpy as np
from sklearn import cross_validation



def CrossValidation(X, Y):

	from sklearn.metrics import mean_squared_error as mse
	from sklearn import cross_validation, linear_model
	N = 30

	resultsX = []
	resultsId = []
	resultsRegr = []

	kf = cross_validation.KFold(N, n_folds=10, random_state=None)
	for train_index, test_index in kf:
		X_train, Y_train = X[train_index], Y[train_index]
		X_test, Y_test = X[test_index], Y[test_index]

		resultsX.append(X_test)
		resultsId.append(Y_test)

		X_train_list = [[x] for x in X_train]

		regr = linear_model.LinearRegression().fit(X_train_list, Y_train)
		resultsRegr += [[int(regr.predict(x)) for x in X_test]]



	return mse(resultsX, resultsId), mse(resultsX, resultsRegr)





import getdata_script as gd
df = gd.GetData(gd.f)



print(CrossValidation((df['stimulus']), (df['converted'])))