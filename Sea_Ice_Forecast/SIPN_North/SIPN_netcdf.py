# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:10:55 2018

@author: NicoS
"""
from netCDF4 import Dataset
import numpy as np
import os
import CryoIO

from datetime import date
from datetime import timedelta

class NETCDF:
    def __init__  (self):
        self.filepath = os.path.abspath('../../NSIDC')
        self.start = date(2023, 7, 1)
        self.loopday = self.start
        self.year = self.start.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.yearday = self.loopday.timetuple().tm_yday
        
        self.forecasttype = '001' #001, 002, 003
        self.masksload()
        
    def masksload(self):
        ''' Loads NSIDC masks and Daily Solar Energy Data'''
        
        filename = f'{self.filepath}/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = f'{self.filepath}/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000

        filename= f'{self.filepath}/Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = f'{self.filepath}/Masks/psn25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        for x,y in enumerate(self.regmaskf):
            if y==20 or y==21:
                self.regmaskf[x] = 100
            else:
                self.regmaskf[x] = 0

        
    def NETCDF_creater(self):
        
        if self.forecasttype == '001':
            forecastdescription = 'Low'
        elif self.forecasttype == '002':
            forecastdescription = 'Mean'
        elif self.forecasttype == '003':
            forecastdescription = 'High'
            
        if self.loopday.month == 6:
            month = 'June'
        elif self.loopday.month == 7:
            month = 'July'
        elif self.loopday.month == 8:
            month = 'August'
        elif self.loopday.month == 9:
            month = 'September'
        
        rootgrp = Dataset("NicoSun_2023_{}_concentration.nc".format(self.forecasttype), "w", format="NETCDF4")
        rootgrp.description = 'NicoSun_SIPN_{}_forecast_{} 1st July to 30st September'.format(month,forecastdescription)

        fcstgrp = rootgrp.createGroup("forecasts")
        time = rootgrp.createDimension("time", None)
        xaxis = rootgrp.createDimension("xaxis", 448)
        yaxis = rootgrp.createDimension("yaxis", 304)
        
        times = rootgrp.createVariable("time","f4",("time",))
        latitude = rootgrp.createVariable("latitude","f4",("xaxis","yaxis",))
        longitude = rootgrp.createVariable("longitude","f4",("xaxis","yaxis",))
        areacello = rootgrp.createVariable("areacello","f4",("xaxis","yaxis",))
        sftof = rootgrp.createVariable("sftof","u1",("xaxis","yaxis",))
        iceconcentration = rootgrp.createVariable("siconc","u1",("time","xaxis","yaxis",))
        
        areacello.units = "gridcell area in km^2"
        sftof.units = "land cover in percent"
        iceconcentration.units = "SIC in %"
        
        self.latmaskf = self.latmaskf.reshape(448, 304)
        self.lonmaskf = self.lonmaskf.reshape(448, 304)
        self.areamaskf = self.areamaskf.reshape(448, 304)
        self.regmaskf  = self.regmaskf.reshape(448, 304)
        
        latitude[:,:] = self.latmaskf
        longitude[:,:] = self.lonmaskf
        areacello[:,:] = self.areamaskf
        sftof[:,:] = self.regmaskf
        
# =============================================================================
#         icethickness = rootgrp.createVariable("icethick","f4",("xaxis","yaxis",))
#         icethickness.units = "thickness in m"
#         thickness = self.openfile('SIPN2_thickness_20200601.bin',np.float)
#         thickness  = thickness.reshape(448, 304)
#         icethickness[:,:] = thickness
# =============================================================================
        
#        iceconcentration = rootgrp.createVariable(varname="siconc{}-{}-{}".format(self.year,self.stringmonth,self.stringday),
#                 datatype="u1",dimensions=("xaxis","yaxis",))
        
            
        x = 0
        self.daycount = 92 #  June-Sep(122), July-Sep(92), Aug-Oct(92),
        icelist = []
        while x < self.daycount:
            filepath = 'temp/{}'.format(self.forecasttype)
            filename = 'SIPN2_SIC_{}_{}{}{}.npz'.format(self.forecasttype,self.year,self.stringmonth,self.stringday)
            iceforecast_load = CryoIO.readnumpy(f'{filepath}/{filename}')/2.5
            iceforecast_load = iceforecast_load.reshape(448, 304)
            
            icelist.append(iceforecast_load)
            self.advanceday(1)
            x += 1
        iceconcentration[0:self.daycount,:,:] = icelist


        
        rootgrp.close()
        #print ('temp shape before adding data = ', temp.shape)
        
    def advanceday(self,delta):    
        self.loopday = self.loopday+timedelta(days=delta)
        self.year = self.loopday.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.yearday = self.loopday.timetuple().tm_yday
        
action = NETCDF()
action.NETCDF_creater()


