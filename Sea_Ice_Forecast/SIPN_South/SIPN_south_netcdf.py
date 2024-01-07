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
		
		self.filepath = '/media/prussian/Cryosphere/NSIDC_South'
		self.filepath_SIPN = '/media/prussian/Cryosphere/Sea_Ice_Forecast'
		
		self.start = date(2022, 12, 1)
		self.loopday = self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		
		self.forecasttype = '003'
		self.forecastmetric = 'sic' #vol or sic
		self.masksload()
		
	def masksload(self):
		
		filename = f'{self.filepath}/Masks/region_s_pure.msk'
		self.regmaskf = CryoIO.openfile(filename, np.uint8)
		
		filename = f'{self.filepath}/Masks/pss25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename, np.int32)/1000
		
		filename = f'{self.filepath}/Masks/pss25lats_v3.dat'
		self.latmaskf = CryoIO.openfile(filename, np.int32)/100000
		
		filename = f'{self.filepath}/Masks/pss25lons_v3.dat'
		self.lonmaskf = CryoIO.openfile(filename, np.int32)/100000

		filename = f'{self.filepath}/Masks/region_s_pure.msk'
		self.landmask = CryoIO.openfile(filename, np.uint8)
		for x,y in enumerate(self.landmask):
			if y==11 or y==12:
				self.landmask[x] = 100
			else:
				self.landmask[x] = 0


		
	def NETCDF_creater(self):
		
		if self.forecastmetric == 'sic':
			rootgrp = Dataset("NicoSun_{}_concentration.nc".format(self.forecasttype), "w", format="NETCDF4")
		elif self.forecastmetric == 'vol':
			rootgrp = Dataset("NicoSun_{}_volume.nc".format(self.forecasttype), "w", format="NETCDF4")
		

		rootgrp.description = 'NicoSun_SIPN_south_forecast_{}'.format(self.forecasttype)

		fcstgrp = rootgrp.createGroup("forecasts")
		time = rootgrp.createDimension("time", None)
		xaxis = rootgrp.createDimension("xaxis", 332)
		yaxis = rootgrp.createDimension("yaxis", 316)
		
		times = rootgrp.createVariable("time","f4",("time",))
		latitude = rootgrp.createVariable("latitude","f4",("xaxis","yaxis",))
		longitude = rootgrp.createVariable("longitude","f4",("xaxis","yaxis",))
		areacello = rootgrp.createVariable("areacello","f4",("xaxis","yaxis",))
		sftof = rootgrp.createVariable("sftof","u1",("xaxis","yaxis",))
		
		
		
		areacello.units = "gridcell area in km^2"
		sftof.units = "land cover in precent"
		
		self.latmaskf = self.latmaskf.reshape(332, 316)
		self.lonmaskf = self.lonmaskf.reshape(332, 316)
		self.areamaskf = self.areamaskf.reshape(332, 316)
		self.landmask  = self.landmask.reshape(332, 316)
		
		latitude[:,:] = self.latmaskf
		longitude[:,:] = self.lonmaskf
		areacello[:,:] = self.areamaskf
		sftof[:,:] = self.landmask
		
		if self.forecastmetric == 'sic':
			iceconcentration = rootgrp.createVariable("siconc","u1",("time","xaxis","yaxis",))
			iceconcentration.units = "SIC in %"
		elif self.forecastmetric == 'vol':
			volume = rootgrp.createVariable("sivol","f4",("time","xaxis","yaxis",))
			volume.units = "SIT in m"
			
		x = 0
		self.daycount = 90 #  Dec-Feb(90)
		siclist = []
		vollist = []
		while x < self.daycount:
			filepath = f'temp/{self.forecasttype}'
			filename = 'SIPN2_SIC_{}_{}{}{}.bin'.format(self.forecasttype,self.year,self.stringmonth,self.stringday)
# 			filenamevol = 'SIPN2_SIT_{}_{}{}{}.bin'.format(self.forecasttype,self.year,self.stringmonth,self.stringday)
			sic_forecast_load = CryoIO.openfile(f'{filepath}/{filename}', np.uint8)/2.5
# 			vol_forecast_load = CryoIO.openfile(f'{filepath}/{filenamevol}', np.float16)
			
			
			if self.forecastmetric == 'sic':
				siclist.append(sic_forecast_load)
# =============================================================================
# 			elif self.forecastmetric == 'vol':
# 				vollist.append(vol_forecast_load)
# =============================================================================
			
			self.advanceday(1)
			x += 1
			
		if self.forecastmetric == 'sic':
			iceconcentration[0:self.daycount,:,:] = siclist
		elif self.forecastmetric == 'vol':
			volume[0:self.daycount,:,:] = vollist

			
		
#		times[:] = timelist
		
		
		rootgrp.close()
		#print ('temp shape before adding data = ', temp.shape)
		print(self.forecasttype)
		
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		
action = NETCDF()
action.NETCDF_creater()


