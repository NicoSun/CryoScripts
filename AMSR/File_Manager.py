"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun


"""

import os
import re
import gzip
import numpy as np
import CryoIO
import logging
import netCDF4

def rename(year):
	filepath = f'DataFiles/north/{year}'
	
	for file in os.listdir(filepath):
		filenew = file[0:5] + '_nh' + file[5:]
# 		print(filenew)
		os.rename(os.path.join(filepath,file),os.path.join(filepath,filenew))


def folder_create(year):
	os.mkdir(f'DataFiles/{year}')

def mass_converter(nc,hemisphere,filename):
	'''This function saves all data in a cropped and unit8 format'''
	layer = 'sea_ice_concentration' # sea_ice_concentration,land,latitude,longitude
	icemap = np.array(nc[layer][0])

	icemap = np.flip(icemap,axis=1)
	icemap = np.rot90(icemap,k=2)
	if hemisphere == 'nh':
		icemap = icemap[200:3500,100:2200]
	elif hemisphere == 'sh':
		icemap = icemap[0:2500,300:2500]
		filename = filename+'_sh'

	icemap = np.clip(icemap,a_min=0,a_max=255)
	icemap = np.array(icemap,dtype=np.uint8)

	np.savez_compressed(filename,Map=icemap)


def decompress():
	import h5py
	logging.basicConfig(filename='logs/filemanager.log', level=logging.INFO)
	
	hemisphere = 'sh'
	'''this function decompresses all files'''
	filepath = '/media/prussian/Cryosphere/AMSR/DataFiles/compressed_south'
	exportpath = '/media/prussian/Cryosphere/AMSR/DataFiles/south/'
	pattern = r'AMSR2'
	for file in os.listdir(filepath):
		match = re.search(pattern,file)
		if match:
			try:
				print(file[0:14])
				with gzip.open(f'{filepath}/{file}') as gz:
					nc = h5py.File(gz,'r')
					mass_converter(nc,hemisphere,os.path.join(exportpath,file[0:14]))
				logging.info(f'{file}')
			except Exception:
				logging.error(f'{file}')


def dailyupdate_old(tempfile,filenameFormatted,hemisphere):
	'''this function handels daily automated updates'''
	layer = 'sea ice concentration' # sea_ice_concentration,land,latitude,longitude

	with gzip.open(tempfile) as gz:
		with netCDF4.Dataset('dummy', mode='r', memory=gz.read()) as nc:

			icemap = np.array(nc[layer][0])
			icemap = np.flip(icemap,axis=1)
			icemap = np.rot90(icemap,k=2)

			if hemisphere == 'nh':
				icemap = icemap[200:3500,100:2200]
			elif hemisphere == 'sh':
				icemap = icemap[0:2500,300:2500]

			icemap = np.clip(icemap,a_min=0,a_max=255)
			icemap = np.array(icemap,dtype=np.uint8)

			CryoIO.savenumpy(filenameFormatted,icemap)

	os.remove(tempfile)

def dailyupdate(tempdata,filenameFormatted,hemisphere,datestring):
	'''this function handels daily automated updates'''
	import AMSR2_maps
	layer = 'sea ice concentration' # sea_ice_concentration,land,latitude,longitude
	
	with netCDF4.Dataset('dummy', mode='r', memory=gzip.decompress(tempdata.getbuffer())) as nc:

		icemap = np.array(nc[layer][0])
		icemap = np.flip(icemap,axis=1)
		icemap = np.rot90(icemap,k=2)

		if hemisphere == 'nh':
			icemap = icemap[200:3500,100:2200]
		elif hemisphere == 'sh':
			icemap = icemap[0:2500,300:2500]

		icemap = np.clip(icemap,a_min=0,a_max=255)
		icemap = np.array(icemap,dtype=np.uint8)

		CryoIO.savenumpy(filenameFormatted,icemap)
		
		AMSR2_maps.action.normalshow(icemap, hemisphere, datestring,icesum=0)


year = 1997
day = 36
daycount = 1

#for year in range(2004,2019):
if __name__ == "__main__":
	print('main')
	# decompress()
# 	dailyupdate('DataFiles/v110/nh_SIC_LEAD_2023030112_030200.nc.gz','nh')
#	mass_converter()
	

# =============================================================================
# 	for year in range(2012,2013):
# # 		folder_create(year)
# 		rename(year)
# =============================================================================
