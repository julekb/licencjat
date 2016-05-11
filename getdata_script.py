import numpy as np
import pandas as pd

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

	df = df.ix[4:34]
	df = df.reset_index(drop=True)

	for i, val in enumerate(df['stimulus']):
		df.loc[i, 'stimulus'] = int(val[14:17])
	

	return df

