import numpy as np
import pandas as pd
N = 31

#f = "data_test.csv"
# def PrepareData( file):
# 	df = pd.read_csv(file)
def test(a):
	return(a)


def GetData( file ):
	df = pd.read_csv(file)
	# print(df.columns)
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
	df['deviation'] = [0]*N


	for i, val in enumerate(df['stimulus']):
		if (isinstance(val, str)):
			df.loc[i, 'stimulus'] = int(val[14:17])
			df.loc[i,'converted'] = 200 * (df['sim_score'][i]-1) / 99 + 7
			df.loc[i, 'deviation'] = df.loc[i, 'converted'] - df.loc[i, 'stimulus']
	
	return df



import matplotlib.pyplot as plt

def PlotData( df, name ):
	df = df.sort(['stimulus'])
	plt.plot(df['stimulus'], df['converted'], 'r-')
	plt.plot([0, 200], [0, 200], 'k-')
	plt.savefig(name+'.png')

	return

def PlotAllData( d, name ):
	for df in d:
		# df = df.sort(['stimulus'])
		plt.plot(df.sort(['stimulus'])['stimulus'], df.sort(['stimulus'])['converted'], 'r-')
		plt.plot([0, 200], [0, 200], 'k-')
	plt.savefig(name+'.png')

	return

def DataAnalysis (df):

	df['deviation'] = [0]*N

	

	for i, row in df.iterrows():
		# df.loc[i, 'deviation'] = row['converted']-row['stimulus']
		row['deviation'] = row['converted']-row['stimulus']
		# df.loc[i, 'SD'] = 
	return df


def VarDev():
	import glob
	filenames = glob.glob("badanie1*.csv")
	data = []
	df = pd.DataFrame()

	sum_dev = []
	sum_sdev = []
	for name in filenames:
		temp = GetData(name)
		# print(abs(temp['deviation']))
		dev = sum(abs(temp['deviation']))

		# print(dev)
		sum_dev.append((dev))
		sum_sdev.append(dev*dev)

		# print(temp['deviation'])
		# print(sum_dev)

		# sum_sd = 
	df['sum_dev'] = sum_dev
	df['sum_sdev'] = sum_sdev
	df['name'] = filenames
	

	# print("sum dev")
	# for s in sum_dev:
	# 	print(s)



	return df


def AllData():
	import glob
	filenames = glob.glob("badanie1*.csv")
	data = []
	for name in filenames:
		data.append(GetData(name))

	final = pd.DataFrame()
	final['stimulus'] = data[1]['stimulus']

	i = len(data)


	m = []
	sd = []
	for i in range(31):
		m.append(np.mean([x for x in [xx.loc[i, 'converted'] for xx in data]]))
		sd.append(np.std([x for x in [xx.loc[i, 'converted'] for xx in data]]))
	final['mean'] = m
	final['SD'] = sd

	PlotAllData(data, 'alldata')
	# for d in data[1:]:
	# 	for j in range(31):
	# 		mean.loc[j, 'converted'] += d.loc[j, 'converted']
	# 		mean.loc[j, 'deviation'] += d.loc[j, 'deviation']
	# # mean['deviation'] = mean['converted'] - mean['stimulus']

	# # mean['SD']=

	# for j in range(31):
	# 	mean.loc[j, 'converted'] /= i
	# 	mean.loc[j, 'deviation'] /= i
		# for d in data:
		# 	mean.loc[j, 'SD'] += (d['deviation']-mean['deviation'][j])^2



	return final



