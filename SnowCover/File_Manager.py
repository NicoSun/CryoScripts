"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script decompresses and NOAA Northern Hemisphere Snow Cover Data
https://nsidc.org/data/g02156
"""

import os
import io
import re
import gzip
import numpy as np
import CryoIO



def create_folders(year):
	'''this function creates folders'''
	
	# Directory
	directory = "DataFiles"
	
	path = os.path.join(directory, str(year))
	os.mkdir(path)
	
def move_files(year):
	'''this function moves data into a year folder'''
	filepath = 'DataFiles/'
	filepath_2 = f'DataFiles/{year}/'
	for file in os.listdir(filepath):		
		pattern = r'NOAA_{}'.format(str(year))
		match = re.search(pattern,file)
		if match:
			os.rename(os.path.join(filepath,file),os.path.join(filepath_2,file))
			
def convert_npz(year):
	'''this function moves data into a year folder'''
	filepath_bin = '/media/prussian/WD/SnowCover/'
	filepath_npz = f'DataFiles/{year}/'
	for file in os.listdir(filepath_bin):		
		pattern = r'NOAA_{}'.format(str(year))
		match = re.search(pattern,file)
		if match:
			newfilename = file[0:17]
			newfilename = f'{newfilename}.npz'
			print(newfilename)
			snow_map = CryoIO.openfile(os.path.join(filepath_bin,file),np.uint8)
			
			CryoIO.savenumpy(os.path.join(filepath_npz,newfilename),snow_map)
# 			os.remove(os.path.join(filepath,file))


def mass_converter(text_file,filename):
	'''This function saves all data in a cropped and unit8 format'''
	snow = np.genfromtxt(text_file,skip_header =30,delimiter=1)
	snowmap = np.flip(snow,axis=1)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
	snowbinary = np.array(snowmap).reshape(-1)

	year = filename[5:9]
	file_convert = f'DataFiles/{year}/{filename}.npz'
	CryoIO.savenumpy(file_convert,snowbinary)

		
def decompress(year):
	'''this function decompresses all files'''
	filepath = 'DataFiles/gzip_files/'
	pattern = f'NOAA_{year}'
	for file in os.listdir(filepath):		
		match = re.search(pattern,file)
		if match:
			print(os.path.join(filepath,file))
# 			print(os.path.join('DataFiles/gzip_files',file[0:17]))
			with gzip.open(os.path.join(filepath,file), mode='rb') as fr:
				file_content = fr.read()
			text_file = io.BytesIO(file_content)
# 			try:
			mass_converter(text_file,file[0:17])
# 			except:
# 				print(file[0:17])
				
def dailyupdate(filenameformatted):
	'''this function handels daily automated updates'''
	with gzip.open(os.path.join('DataFiles/gzip_files',filenameformatted), mode='rb') as fr:
		file_content = fr.read()
				

	text_file = io.BytesIO(file_content)
	snow = np.genfromtxt(text_file,skip_header =30,delimiter=1)
	snowmap = np.flip(snow,axis=1)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
	snowbinary = np.array(snowmap,dtype='uint8')
	with open(os.path.join('DataFiles',filenameformatted[0:17]+'.bin'), 'wb') as writer:
		writer.write(snowbinary)
#	os.remove(os.path.join('X:/SnowCover/DataFiles/gzip_files',filenameformatted[0:17]+'.asc'))


year = 1997
day = 36
daycount = 1

#for year in range(2004,2019):
if __name__ == "__main__":
	print('main')

	for year in range (2021,2022):
# 		create_folders(year)
# 		move_files(year)
# 		convert_npz(year)
		decompress(year)
	

#for day in range(1,366):
	#decompress(str(day).zfill(3))

#rename(year,month)
