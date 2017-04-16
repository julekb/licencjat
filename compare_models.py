import numpy as np
import pandas as pd
import pickle as pkl

from math import exp, log

from sklearn import cross_validation, linear_model
from sklearn.neighbors import KNeighborsRegressor as KNR
from itertools import combinations
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

	# fitting 'objective' model based on mean responses
	X = avg_data['mean']
	obj_Y = avg_data['stimulus']
	OBJ_models = fit_model(X, obj_Y)
	OBJ_models_inv = fit_model(obj_Y, X)
	X = avg_data['mean']

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
			df.loc[i,test_index[0]][:12] = models+models_inv
			df.loc[i,test_index[0]][12] = X[test_index]
	return df, OBJ_models,OBJ_models_inv
	
def save_models_script():
	#### function for saving individual linear models to pickle file ####
	df, OBJ_models, OBJ_models_inv = find_models()
	with open(path+'ind_models.pkl', 'wb') as f:
		pkl.dump(df, f)

	with open(path+'ojb_models.pkl', 'wb') as f:
		pkl.dump([OBJ_models, OBJ_models_inv], f)

	return

def compare(df):
	#### comparing communication error with and without individual model ####

	df_columns = df.columns #['type model A', 'type model B', 'type model OBJ', 'type d_A', 'type d_B'] where type is the name of regression moel; i.e.: regr, regr_ey, regr_log
	# iteration over all rows(each row contains linear models for a pair of agents)

	column_names = ['no model error', 'model error', 'diff']
	df_err = pd.DataFrame(index=df.index, columns=column_names)

	for index, row in df.iterrows():
		stimulus = all_data[0]['converted'][index[2]]
		df_err.loc[index]['model error'] = (row[df_columns[0]].predict(stimulus) - row[df_columns[1]].predict(stimulus))[0]
		# df_err.loc(index)['no model error'] = row[df_columns[0]].predict(stimulus) - row[df_columns[1]].predict(stimulus)
		# df_err.loc(index)['model error'] = row[df_columns[0].predict[stimuli]] - row[df_columns[1].predict(stimulus)]
	return df_err
	