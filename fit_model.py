
import numpy as np
import pandas as pd
import pickle as pkl

from math import exp, log

from sklearn import cross_validation, linear_model
from sklearn.neighbors import KNeighborsRegressor as KNR

N = 31
path = "data_all/"

with open(path+"avg_mean_sd.pkl", 'rb') as f:
	avg_data = pkl.load(f)

with open(path+"data_all.pkl", 'rb') as f:
# with open(path+"pilot_data.pkl", 'rb') as f: #testowo mniejszy plik
	data_all = pkl.load(f)

def fit_model(X, Y):
	# funkcja zwracająca dopasowanie różnych modeli
	regr = linear_model.LinearRegression().fit(X, Y)
	regr_ey = linear_model.LinearRegression().fit(np.exp(X), Y)
	regr_log = linear_model.LinearRegression().fit(np.log(X), Y)
	nb1NN = KNR(n_neighbors=1, algorithm='ball_tree').fit(X, Y)
	nb2NN = KNR(n_neighbors=2, algorithm='ball_tree').fit(X, Y)
	nb3NN = KNR(n_neighbors=3, algorithm='ball_tree').fit(X, Y)

	return regr, regr_ey, regr_log, nb1NN, nb2NN, nb3NN
def fight(A_y, B_y, model_obj=False, A_model=False, B_model=False, k=0):
	# funkcja zwracająca różnicę odpowiedzi bez lub z indywidualnymi modelami
	# A_y, B_y - odpowiedzi agentów A i B
	# model_obj - model 'odniesienia/obiektywny', A_model, B_model - podele dopasowane do agentów A i B
	# jeśli modele indywidualne modele to NN, to k >= 3
	if A_model == False:
		return float(A_y - B_y)
	else if k < 3:
		A_x = float((A_y - A_model.predict(0))/A_model.coef_)
		B_x = float((B_y - B_model.predict(0))/B_model.coef_)
	
		return float(model_obj.predict(A_x) - model_obj.predict(B_x))
	else: # k >= 3, czyli model NN
	# zwrca środek przedziału, który jest najbliżej y
		
# #sortowanie po bodźcu
# avg_mean_sd = avg_mean_sd.sort_values('stimulus')
# avg_mean_sd = avg_mena_sd.reset_index(drop=True)

# for d in data_all:
# 	d = d.sort_values('stimulus')
# 	d = d.reset_index(drop=True)


# dopasowanie 'obiektywnego' modelu percepcyjnego na podstawie średnich odpowiedzi

# tutaj trochę bez sensu bo stimulus sie nie zmienia!!!
obj_X = [[x] for x in avg_data['stimulus']]
obj_Y = avg_data['mean']
OBJ_models = fit_model(obj_X, obj_Y)

err = 0
err_mod = [0]*6
model_names = ["regr", "regr_ey", "regr_log", "nb1NN", "nb2NN", "nb3NN"]
#parowanie każdy z każdym, dopasowanie indywidualnego modelu i symulacja
# dobieranie uczestnika A
for i, A_data in enumerate(data_all[:-1]):		#:-1 bo ostatni już i tak nie miałby z kim się sparować
	X, A_Y = A_data['stimulus'], A_data['converted']
	kf = cross_validation.LeaveOneOut(N)

	# dobieranie uczestnika B
	for B_data in data_all[i+1:]:
		B_Y = B_data['converted']

		for train_index, test_index in kf:
			X_train, A_Y_train, B_Y_train = X[train_index], A_Y[train_index], B_Y[train_index]
			X_test, A_Y_test, B_Y_test = X[test_index], A_Y[test_index], B_Y[test_index]
			X_train = [[x] for x in X_train]
			
			#dopasowanie indywidualnego modelu dla uczestnika A
			# A_models = [A_regr, A_regr_ey, A_regr_log, A_nb1NN, A_nb2NN, A_nb3NN]
			A_models = fit_model(X_train, A_Y_train)
			# dopasowanie indywidualnego modelu dla uczestnika B
			# B_models = [B_regr, B_regr_ey, B_regr_log, B_nb1NN, B_nb2NN, B_nb3NN]
			B_models = fit_model(X_train, B_Y_train)
			err += abs(fight(A_Y_test, B_Y_test))

			for k, model in enumerate(model_names):
				if k<3:
					err_mod[k] += abs(fight(A_Y_test, B_Y_test, OBJ_models[k], A_models[k], B_models[k]))
				else:
					continue

for k, model in enumerate(model_names):
	print(model, err_mod[k])
print("zero ", err)


#różny Y