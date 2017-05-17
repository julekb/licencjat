#### This script contains all steps required to analyze the data ####

output_path = 'scripttest/'  #path for output data


###### STEP 1 #######
#### getting the data from individual answers ####
print('getdata')

import getdata_script as gd

gd_path = 'scripttest/data/'	#path to the folder with .csv files

avg_data, data_all = gd.all_data(gd_path)


###### STEP 2 #######
### creating individual models
print('individual models')

import compare_models as cm

ind_models = cm.find_models(avg_data, data_all)