import os
from skimage import io
import pandas as pd

W = 800
H = 600


def GetPercentage(filename):

	img = io.imread(filename)
	n = 0
	for i in img:
		for ii in i:
			if ii[0] != 255:
				n += 1
	return n/(W*H/100)

def Script(url):
# zwraca dataframe z procentem zaczernienia obrazków w folderze url

	import glob
	filenames = glob.glob(url+"/dots*.png")
	l = len(url)
	print(filenames)

	df = pd.DataFrame()
	df['names'] = filenames
	df['stimulus'] = [int(name[6+l:9+l]) for name in filenames]
	df['percentage'] = [GetPercentage(file) for file in filenames]
	return df
