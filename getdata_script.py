import numpy as np
import pandas as pd
N = 31

f = "data_test.csv"

def GetData( file ):
	df = pd.read_csv(file)
	del df['view_history']
	del df['rt']
	del df['trial_type']
	del df['trial_index']
	del df['time_elapsed']
	del df['internal_node_id']
	del df['subject']
	del df['phase']

	responses = df['responses'][1:2]

	del df['responses']

	df = df.ix[4:N+3]
	df = df.reset_index(drop=True)

	df['converted'] = [0]*N

	for i, val in enumerate(df['stimulus']):
		df.loc[i, 'stimulus'] = int(val[14:17])
		df.loc[i,'converted'] = 200 * (df['sim_score'][i]-1) / 99 + 7
	
	return df

import matplotlib.pyplot as plt

def PlotData( df, name ):
	df = df.sort(['stimulus'])
	plt.plot(df['stimulus'], df['converted'], 'r-')
	plt.plot([0, 200], [0, 200], 'k-')
	plt.savefig(name+'.png')

	return

def DataAnalysis (df):

	df['deviation'] = [0]*N
	df['SD'] = [0]*N

	for i, row in df.iterrows():
		df.loc[i, 'deviation'] = row['converted']-row['stimulus']
	return df

