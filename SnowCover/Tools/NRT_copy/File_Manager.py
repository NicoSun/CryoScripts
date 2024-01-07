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

def convert_npz(year):
	'''this function moves data into a year folder'''
	filepath_bin = 'DataFiles/'
	filepath_npz = f'DataFiles/npz/'
	for file in os.listdir(filepath_bin):		
		pattern = r'NOAA_{}'.format(str(year))
		match = re.search(pattern,file)
		if match:
			newfilename = file[0:17]
			newfilename = f'{newfilename}.npz'
			print(newfilename)
			snow_map = CryoIO.openfile(os.path.join(filepath_bin,file),np.uint8)
			
			CryoIO.savenumpy(os.path.join(filepath_npz,newfilename),snow_map)


def mass_converter(text_file,filename):
	'''This function saves all data in a cropped and unit8 format'''
	snow = np.genfromtxt(text_file,skip_header =30,delimiter=1)
	snowmap = np.flip(snow,axis=1)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
	snowbinary = np.array(snowmap).reshape(-1)
	
	file_convert = f'DataFiles/npz/{filename}.npz'
	CryoIO.savenumpy(file_convert,snowbinary)
		
def decompress():
	'''this function decompresses all files'''
	filepath = 'DataFiles/gzip_files'
	pattern = r'NOAA'
	for file in os.listdir(filepath):		
		match = re.search(pattern,file)
		if match:
			#print(os.path.join(filepath,file))
			print(os.path.join('DataFiles/gzip_files',file[0:17]+'.dat'))
			with gzip.open(os.path.join(filepath,file), mode='rb') as fr:
				file_content = fr.read()
			text_file = io.BytesIO(file_content)
			mass_converter(text_file,file[0:17])
				
def dailyupdate(filenameformatted):
	'''this function handels daily automated updates'''
	filename = filenameformatted[0:17]
	with gzip.open(os.path.join('/home/nico/Cryoscripts/SnowCover/DataFiles/gzip_files',filenameformatted), mode='rb') as fr:
		file_content = fr.read()
				
	text_file = io.BytesIO(file_content)
	snow = np.genfromtxt(text_file,skip_header =30,delimiter=1)
	snowmap = np.flip(snow,axis=1)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
# =============================================================================
# 	snowbinary = np.array(snowmap,dtype='uint8')
# 	with open(os.path.join('/home/nico/Cryoscripts/SnowCover/DataFiles/bin',filename+'.bin'), 'wb') as writer:
# 		writer.write(snowbinary)
# =============================================================================
		
	snowbinary = np.array(snowmap).reshape(-1)
	file_convert = f'/home/nico/Cryoscripts/SnowCover/DataFiles/npz/{filename}.npz'
	CryoIO.savenumpy(file_convert,snowbinary)
#	os.remove(os.path.join('X:/SnowCover/DataFiles/gzip_files',filenameformatted[0:17]+'.asc'))


year = 1997
day = 36
daycount = 1

#for year in range(2004,2019):
if __name__ == "__main__":
	print('main')
#	decompress()
# 	dailyupdate('NOAA_2023073_24km_v1.3.asc.gz')
#	mass_converter()
	convert_npz(2023)

#for day in range(1,366):
	#decompress(str(day).zfill(3))

#rename(year,month)
