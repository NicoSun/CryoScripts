"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script decompresses and NOAA Northern Hemisphere Snow Cover Data
https://nsidc.org/data/g02156
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import io
import re


def preformat():
	'''This function saves all data in a cropped and unit8 format'''
	
	csvlist = []
#		print(os.path.join(filepath,file))
	with open('Bad_data_new2.csv') as csvfile:
		snowmap = csv.reader(csvfile, delimiter=',')
		for row in snowmap:
			csvlist.append(row)
#		del csvlist[-1]
		print(len(csvlist[0]))
		csvlist[0][0] = 0
		snowmap = np.zeros(1024*1024)
		for x,y in enumerate(csvlist[0]):
			try:
				if float(y) < 200:
					snowmap[x] = y
			except:
				pass
		snowmap = snowmap.reshape(1024,1024)
		snowmap = np.flip(snowmap,axis=1)
		snowmap = snowmap[220:830,250:700]
		snowmap = np.rot90(snowmap,k=2)
		plt.imshow(snowmap)
		plt.show()
		
def mass_converter():
	'''This function saves all data in a cropped and unit8 format'''
	
	filename = 'X:/SnowCover/Masks/Landmask.msk'
	with open(filename, 'rb') as fr:
		landmask = np.fromfile(fr, dtype='uint8')
	
	
#		print(os.path.join(filepath,file))
	csv.Dialect.skipinitialspace=True
	filepath = 'X:/SnowCover/Datafiles/badformat'
	for file in os.listdir(filepath):
		csvlist = []
		print(file)
		with open(os.path.join(filepath,file)) as csvfile:
			snowmap = csv.reader(csvfile, delimiter=',')
			for row in snowmap:
				csvlist.append(row)
			print(len(csvlist))
			if len(csvlist)==131094:
				del csvlist[0:22]
			else:
				del csvlist[0:24]
			flat_list = [item for sublist in csvlist for item in sublist]
			
			string = ''
			
			for x in flat_list:
				string = string+x
				
		data = re.sub(' +', ',', string)
		data = data[1:]
	
		text_file = io.StringIO(data)
			
	
		snowmap = np.genfromtxt(text_file,delimiter=',')
		snowmap = snowmap.reshape(1024,1024)
		snowmap = np.flip(snowmap,axis=1)
		snowmap = snowmap[220:830,250:700]
		snowmap = np.rot90(snowmap,k=2)
		snowmap_2 = snowmap.reshape(274500)
		snowmap_new = np.zeros(len(landmask))
#		print(len(snowmap_2))
		
	
		for x,y in enumerate(landmask):
			if y==2:
				snowmap_new[x] = 2
				if snowmap_2[x] == 165:
					snowmap_new[x] = 4
	
			elif y==1:
				snowmap_new[x] = 1
				if snowmap_2[x] == 164:
					snowmap_new[x] = 3
		
		snowbinary = np.array(snowmap_new,dtype='uint8')
		with open(os.path.join('X:/SnowCover/DataFiles',file[0:17]+'.bin'), 'wb') as writer:
			writer.write(snowbinary)
# =============================================================================
# 	snowmap_new = snowmap_new.reshape(610,450)
# 	plt.imshow(snowmap_new)
# 	plt.show()
# =============================================================================

year = 1997
day = 36
daycount = 1

#for year in range(2004,2019):
if __name__ == "__main__":
	print('main')
#	decompress()
	mass_converter()

#for day in range(1,366):
	#decompress(str(day).zfill(3))

#rename(year,month)
