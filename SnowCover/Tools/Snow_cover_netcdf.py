# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:10:55 2018

@author: NicoS
"""
from netCDF4 import Dataset
import numpy as np
import os


class NETCDF:
	def __init__  (self):
		self.masksload()
		
	def masksload(self):
	
		filename = 'X:/SnowCover/Masks/Region_Mask.msk'
		with open(filename, 'rb') as fr:
			self.regionmask = np.fromfile(fr, dtype='uint8')
		filename = 'X:/SnowCover/Masks/Pixel_area_crop.msk'
		with open(filename, 'rb') as fr:
			self.pixelarea = np.fromfile(fr, dtype='uint16')
		filename = 'X:/SnowCover/Masks/Latitude_Mask.msk'
		with open(filename, 'rb') as fr:
			self.Latitude_Mask = np.fromfile(fr, dtype='float32')
		filename = 'X:/SnowCover/Masks/Longitude_Mask.msk'
		with open(filename, 'rb') as fr:
			self.Longitude_Mask = np.fromfile(fr, dtype='float32')

		


		
	def NETCDF_creater(self):
		rootgrp = Dataset("Snow_cover_days.nc", "w", format="NETCDF4")
		rootgrp.description = 'total days covered by snow'
		rootgrp.history = "Created by Nico Sun 2018-11-27"
		
		fcstgrp = rootgrp.createGroup("Snow Days")
		year = rootgrp.createDimension("year", None)
		xaxis = rootgrp.createDimension("xaxis", 610)
		yaxis = rootgrp.createDimension("yaxis", 450)

		latitude = rootgrp.createVariable("latitude","f4",("xaxis","yaxis",))
		longitude = rootgrp.createVariable("longitude","f4",("xaxis","yaxis",))
		areacello = rootgrp.createVariable("areacello","f4",("xaxis","yaxis",))
		region = rootgrp.createVariable("Region","u1",("xaxis","yaxis",))
		
		areacello.units = "gridcell area in km^2"
		
		
		self.Latitude_Mask = self.Latitude_Mask.reshape(610,450)
		self.Longitude_Mask = self.Longitude_Mask.reshape(610,450)
		self.pixelarea = self.pixelarea.reshape(610,450)
		self.regionmask  = self.regionmask.reshape(610,450)
		
		latitude[:,:] = self.Latitude_Mask
		longitude[:,:] = self.Longitude_Mask
		areacello[:,:] = self.pixelarea
		region[:,:] = self.regionmask
		
		self.year = 1997
		self.yearcount = 21
		filepath = 'X:/SnowCover/netcdf'
		x = 0
		while x < self.yearcount:
			Snow_Day = rootgrp.createVariable(varname="{}".format(self.year),
				 datatype="i2",dimensions=("xaxis","yaxis",))
			Snow_Day.units = "Days"

			filename = 'Snow_cover_days_{}.bin'.format(self.year)
			with open(os.path.join(filepath,filename), 'rb') as fr:
				Snow_Day_load = np.fromfile(fr, dtype='uint16')
				Snow_Day_load = Snow_Day_load.reshape(610,450)
				Snow_Day[:,:] = Snow_Day_load
			
			x += 1
			self.year += 1

		rootgrp.close()
		#print ('temp shape before adding data = ', temp.shape)
		


action = NETCDF()
action.NETCDF_creater()
