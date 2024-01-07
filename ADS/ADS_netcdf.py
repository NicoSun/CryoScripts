# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:10:55 2018

@author: NicoS
"""
from netCDF4 import Dataset
import numpy as np
import CryoIO

from datetime import date
from datetime import timedelta

class NETCDF:
	def __init__  (self):
		self.start = date(2018, 12, 1)
		self.loopday = self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		
		self.daycount = 30
		
		self.mode = 'Low'
		self.masksload()
		
		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		self.landmask = CryoIO.openfile(landmaskfile,np.uint8)

		latlonmaskfile = 'Masks/latlon_low.map'
		latlonmask = CryoIO.openfile(latlonmaskfile,np.uint16)
		self.latmaskf = 0.01*latlonmask[:810000] 
		self.lonmaskf = 0.01*latlonmask[810000:]
		
	def NETCDF_creater(self):
		months = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		
		rootgrp = Dataset("Upload/ADS_AMSR2_SIT_{}.nc".format(months[self.loopday.month-1]), "w", format="NETCDF4")
#		rootgrp = Dataset("ADS_AMSR2_SIT_{}.nc".format(self.loopday), "w", format="NETCDF4")
		rootgrp.description = 'calculated by NicoSun using ADS thickness data 10km grid'

		fcstgrp = rootgrp.createGroup("forecasts")
		time = rootgrp.createDimension("time", None)
		xaxis = rootgrp.createDimension("xaxis", 900)
		yaxis = rootgrp.createDimension("yaxis", 900)
		
#		times = rootgrp.createVariable("time","f4",("time",))
		latitude = rootgrp.createVariable("Latitude","f4",("xaxis","yaxis",))
		longitude = rootgrp.createVariable("Longitude","f4",("xaxis","yaxis",))
		Landmask = rootgrp.createVariable("Landmask","u1",("xaxis","yaxis",))
		icecthickness = rootgrp.createVariable("SIT","u2",("time","xaxis","yaxis",),zlib=True)
		
		Landmask.units = "land cover in precent"
		
		self.latmaskf = self.latmaskf.reshape(900, 900)
		self.lonmaskf = self.lonmaskf.reshape(900, 900)
		self.landmask  = self.landmask.reshape(900, 900)
		
		latitude[:,:] = self.latmaskf
		longitude[:,:] = self.lonmaskf
		Landmask[:,:] = self.landmask
		
		icecthickness.units = "SIT in cm"
			
		x = 0
		icelist = []
		while x < self.daycount:
			filename = 'X:/ADS/Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			icethickness_load = CryoIO.openfile(filename,np.uint16)
			icethickness_load = icethickness_load.reshape(900, 900)
			
			icelist.append(icethickness_load)
			self.advanceday(1)
			x += 1
		icecthickness[0:self.daycount,:,:] = icelist

			
		
#		times[:] = timelist
		
		
		rootgrp.close()
		#print ('temp shape before adding data = ', temp.shape)
		
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		
	def automated (self,day,month,year,daycount):
		self.start = date(year, month, day)
		self.loopday = self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.daycount = daycount
		self.NETCDF_creater()
		
		
action = NETCDF()
if __name__ == "__main__":
	#action.NETCDF_creater()
	action.automated(1,7,2020,31)



