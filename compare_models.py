import numpy as np
import pandas as pd
import pickle as pkl

from math import exp, log

from sklearn import cross_validation, linear_model
from sklearn.neighbors import KNeighborsRegressor as KNR
from itertools import combinations, product, zip_longest
from sklearn.metrics import mean_squared_error as mse

# loading dataframe with calculated individual linear models
path = 'pkl_data/'
# with open(path+'df.pkl', 'rb') as f:
#     df_regr = pkl.load(f)
"""with open(path+'dataframeALL_regr_ey.pkl', 'rb') as f:
    df_ey = pkl.load(f)
with open(path+'dataframeALL_regr_log.pkl', 'rb') as f:
    df_log = pkl.load(f)

# different location
"""
with open(path+'avg_mean_sd.pkl', 'rb') as f:
	avg_data = pkl.load(f)
avg_data = avg_data.sort_values('stimulus')
avg_data = avg_data.reset_index(drop=True)

with open(path+'data_all.pkl', 'rb') as f:
	data_all = pkl.load(f)
for d in data_all:
	d = d.sort_values('stimulus')
	d = d.reset_index(drop=True)

# creating zero model y=x
zero = linear_model.LinearRegression()
zero.intercept_, zero.coef_ = 0, np.array(1)

participants = len(data_all)
N = len(data_all[0])
model_names = ["regr", "regr_ey", "regr_log", "nb1NN", "nb2NN", "nb3NN"]

def fit_model(X, Y):
	#### function for generating linear model for individual ####
	X = [[x] for x in X]
	regr = linear_model.LinearRegression().fit(X, Y)
	regr_ey = linear_model.LinearRegression().fit(np.exp(X), Y)
	regr_log = linear_model.LinearRegression().fit(np.log(X), Y)
	nb1NN = KNR(n_neighbors=1, algorithm='ball_tree').fit(X, Y)
	nb2NN = KNR(n_neighbors=2, algorithm='ball_tree').fit(X, Y)
	nb3NN = KNR(n_neighbors=3, algorithm='ball_tree').fit(X, Y)

	return [regr, regr_ey, regr_log, nb1NN, nb2NN, nb3NN]

def find_models():
	#### function for generating linear models for all agents/participants ####

	# creating dataframe; columns include all type of models, their inverse and remained data from cross validation for further computations
	column_names = model_names + ['inv '+name for name in model_names] + ['remain']
	multi = pd.MultiIndex.from_tuples([(i,j) for i in range(participants) for j in list(range(N))])
	df = pd.DataFrame(index=multi, columns=column_names)
	col_len = len(column_names)-1

	# fitting 'objective' model based on mean responses
	X = avg_data['mean']
	obj_Y = avg_data['stimulus']
	OBJ_models = fit_model(X, obj_Y)
	OBJ_models_inv = fit_model(obj_Y, X)

	# iteration over all agents and fitting models
	for i, agent in enumerate(data_all):
		# cross validation
		kf = cross_validation.LeaveOneOut(N)
		Y = agent['converted']
		for (train_index, test_index) in kf:
			X_train = X[train_index]
			Y_train = Y[train_index]
			models = fit_model(X, Y)
			models_inv = fit_model(Y, X)
			df.loc[i,test_index[0]][:col_len] = models+models_inv
			df.loc[i,test_index[0]][col_len] = Y[test_index]
	return df, OBJ_models, OBJ_models_inv

def save_models_script():
	#### function for saving individual linear models to pickle file ####
	ind_models, OBJ_models, OBJ_models_inv = find_models()
	with open(path+'ind_models.pkl', 'wb') as f:
		pkl.dump(ind_models, f)

	with open(path+'obj_models.pkl', 'wb') as f:
		pkl.dump([OBJ_models, OBJ_models_inv], f)
	return

def load_models_script(Return=False):
	#### loading models generated by save_models_script() ####
	with open(path+'ind_models.pkl', 'rb') as f:
		ind_models = pkl.load(f)
	with open(path+'obj_models.pkl', 'rb') as f:
		obj_models = pkl.load(f)
	if Return:
		return ind_models, obj_models
	return

def fight(A_y, B_y, A_model, A_model_inv, B_model, B_model_inv):
	#### function returning answer difference with models ####
	# A_y, B_y - answers agents A and B
	# type is model type (linear, NN)

	d_A = A_y - float(A_model.predict(float(B_model_inv.predict(B_y))))
	d_B = float(B_model.predict(float(A_model_inv.predict(A_y)))) - B_y
	return d_A, d_B

def compare_errors(ind_models):
	#### comparing communication error with and without individual model ####

	column_names = [k+' '+l for l in ['model error', 'diff'] for k in model_names]+['neighbors model error']
	multi = pd.MultiIndex.from_tuples([(i,j,k) for i in range(participants) for j in range(i+1,participants) for k in range(N)], names=['agent A', 'agent B', 'iteration'])
	df_err = pd.DataFrame(index=multi, columns=column_names)

	for i in range(participants):
		for j in range(i+1,participants):
			for k in range(N):
				A, B = ind_models.loc[i,k], ind_models.loc[j,k]
				# between agents difference without individual model
				df_err.loc[i,j,k]['no model error'] = A['remain'] - B['remain']
				for model in model_names:
					d_A, d_B = fight(A['remain'], B['remain'], A[model], A['inv '+model], B[model], B['inv '+model])
					# between agents difference with individual model
					df_err.loc[i,j,k][model+' model error'] = d_A - d_B
					# between agents difference with and without individual model
					df_err.loc[i,j,k][model+' diff'] = (A['remain']-B['remain']) - (d_A-d_B)
					# !!!! the accuracy of these calculations above needs to be revised !!!!
	return df_err

def save_errors_script():
	#### function for saving dataframe with errors ####
	ind, obj = load_models_script(True)
	df_err = compare_errors(ind)
	# with open(path+'df_err.pkl', 'wb') as f:
	# 	pkl.dump(df_err, f)
	return df_err
	