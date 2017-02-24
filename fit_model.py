
import numpy as np
import pandas as pd
import pickle as pkl

from math import exp, log

from sklearn import cross_validation, linear_model
from sklearn.neighbors import KNeighborsRegressor as KNR
from itertools import combinations
from sklearn.metrics import mean_squared_error as mse


path = "data_all/"

with open(path+'avg_mean_sd.pkl', 'rb') as f:
	avg_data = pkl.load(f)

# with open(path+"data_all.pkl", 'rb') as f:
with open(path+'pilot_data.pkl', 'rb') as f: #testowo mniejszy plik
	data_all = pkl.load(f)

def fit_model(X, Y):
	# funkcja zwracająca dopasowanie różnych modeli
	X = [[x] for x in X]
	regr = linear_model.LinearRegression().fit(X, Y)
	regr_ey = linear_model.LinearRegression().fit(np.exp(X), Y)
	regr_log = linear_model.LinearRegression().fit(np.log(X), Y)
	nb1NN = KNR(n_neighbors=1, algorithm='ball_tree').fit(X, Y)
	nb2NN = KNR(n_neighbors=2, algorithm='ball_tree').fit(X, Y)
	nb3NN = KNR(n_neighbors=3, algorithm='ball_tree').fit(X, Y)

	return regr, regr_ey, regr_log, nb1NN, nb2NN, nb3NN
def fight(A_y, B_y, model_obj=False, model_obj_inv=False, A_model=False, A_model_inv=False, B_model=False, B_model_inv=False, k=0):
	"""funkcja zwracająca różnicę odpowiedzi bez lub z indywidualnymi modelami
	A_y, B_y - odpowiedzi agentów A i B
	model_obj - model 'odniesienia/obiektywny', A_model, B_model - podele dopasowane do agentów A i B
	jeśli modele indywidualne modele to NN, to k >= 3"""
	if A_model == False:
		return float(A_y - B_y)
	else:
		d_A = A_y - float(A_model.predict(float(B_model_inv.predict(B_y))))
		# d_B = B_model.predict(A_model_inv.predict(A_y)) - B_y
		return d_A		
# sortowanie po bodźcu
avg_data = avg_data.sort_values('stimulus')
avg_data = avg_data.reset_index(drop=True)

for d in data_all:
	d = d.sort_values('stimulus')
	d = d.reset_index(drop=True)

# dopasowanie 'obiektywnego' modelu percepcyjnego na podstawie średnich odpowiedzi

obj_X = avg_data['mean']
obj_Y = avg_data['stimulus']
OBJ_models = fit_model(obj_X, obj_Y)
OBJ_models_inv = fit_model(obj_Y, obj_X)
X = avg_data['mean']

err = []
err_mod = [[] for i in range(6)]
model_names = ["regr", "regr_ey", "regr_log", "nb1NN", "nb2NN", "nb3NN"]
#parowanie każdy z każdym, dopasowanie indywidualnego modelu i symulacja

N = len(data_all[0])

for A_data, B_data in combinations(data_all, 2):

	kf = cross_validation.LeaveOneOut(N)
	A_Y, B_Y = A_data['converted'], B_data['converted']
	

	for train_index, test_index in kf:
		X_train, A_Y_train, B_Y_train = X[train_index], A_Y[train_index], B_Y[train_index]
		X_test, A_Y_test, B_Y_test = X[test_index], A_Y[test_index], B_Y[test_index]
		
		#dopasowanie indywidualnego modelu dla uczestnika A i B
		
		A_models = fit_model(X_train, A_Y_train)
		A_models_inv = fit_model(A_Y_train, X_train)
		B_models = fit_model(X_train, B_Y_train)
		B_models_inv = fit_model(B_Y_train, X_train)

		err.append(fight(A_Y_test, B_Y_test))

		for k, model in enumerate(model_names):
				# deprecation warning
				err_mod[k].append(fight(float(A_Y_test), float(B_Y_test), OBJ_models[k], OBJ_models_inv[k], A_models[k], A_models_inv[k], B_models[k], B_models_inv[k]))

for k, model in enumerate(model_names):
	print(model+" mse:", mse([0 for i in err_mod[k]], err_mod[k]))
print("zero mse:", mse([0 for i in err], err))
