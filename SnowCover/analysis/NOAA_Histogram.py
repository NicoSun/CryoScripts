"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

https://nsidc.org/data/g02156
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

stepsize = 250000

def showplot(img,bins):
	fig = plt.figure(figsize=(11, 11))
	ax = fig.add_subplot(111)
	
	ax.plot(img)
#	ax.set_xticks(bins/5)
#	ax.axes.get_yaxis().set_ticks([])
#	ax.axes.get_xaxis().set_ticks([])
	plt.tight_layout(pad=1)
	plt.show()

def csvexport(filename,filedata):
	np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')

def decompress(file):
	normalized = []
	
	
	ttt = []
	for yearcol in range(0,24):
		ttt.append(str(yearcol))
	Yeardata = pd.read_csv(file, names=ttt)
	
	lll = []
	for xxx in ttt:
		lll.append(Yeardata[xxx])
		
	kkk = np.array(lll)
	ooo = kkk.flatten()
	ooo = ooo*1e6

	print(ooo)
	binmin = -6000000#int(min(bincol))
	binmax = 7000000#int(max(bincol))
	binall = sum(ooo)
	
	bins = np.arange(binmin,binmax,stepsize)
#	print(bins)
	print(len(bins))
	
	for step in range (binmin,int(binmax),stepsize):
		count = 0
		for x,y in enumerate(ooo):
			if step-stepsize/2 < y < step+stepsize/2:
				count += 1
		normalized.append(count) #Antarctica

			
	bincsv = ["'{}'".format(x) for x in bins]
	bincsv = bincsv[::-1]
#	print(len(normalized))
	normalizedcsv = normalized[::-1]
	
	
#	csvexport('Greenland_{}.csv'.format(stepsize),[bins,normalized])
	csvexport('Z_binlist{}.csv'.format(stepsize),[bincsv])
	csvexport('Z_valuelist{}.csv'.format(stepsize),[normalizedcsv])
# 	showplot(normalized,bins)
	

#for year in range(2004,2019):
if __name__ == "__main__":
	print('main')
	decompress('Snow_anomaly.csv')
#	openimage('Panama/N008W081_DSM.tif')
#	multi_image()

