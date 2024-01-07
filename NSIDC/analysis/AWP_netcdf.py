# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:10:55 2018

@author: NicoS
"""
from netCDF4 import Dataset
import numpy as np
import CryoIO


class NETCDF:
    def __init__  (self):
        self.masksload()
        
    def masksload(self):

        filename = '../Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
        filename= '../Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename= '../Masks/psn25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = '../Masks/Max_AWP_extent.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        filename = '../Masks/Arctic_region_mask.bin'
        self.landmask = CryoIO.openfile(filename,np.uint32)
        
        for x,y in enumerate(self.landmask):
            if y==20 or y==21:
                self.landmask[x] = 100
            else:
                self.landmask[x] = 0

        
    def NETCDF_creater(self):
        nc = Dataset("AWP_Arctic.nc", "w", format="NETCDF4")
        nc.description = 'Nico Sun , CryospheComputing.com,  Arctic Albedo Warming Potential (AWP)'


        fcstgrp = nc.createGroup("AWP")
        year = nc.createDimension("year", None)
        year = nc.createDimension("map", 2)
        xaxis = nc.createDimension("xaxis", 448)
        yaxis = nc.createDimension("yaxis", 304)
        
        latitude = nc.createVariable("latitude","f4",("xaxis","yaxis",))
        longitude = nc.createVariable("longitude","f4",("xaxis","yaxis",))
        areacello = nc.createVariable("areacello","f4",("xaxis","yaxis",))
        land_mask = nc.createVariable("land_mask","u1",("xaxis","yaxis",))
        AWP_cumu = nc.createVariable(varname="AWP_Accumulated",
             datatype="f4",dimensions=("year","xaxis","yaxis",))
        
        
        areacello.units = "gridcell area in km^2"
        land_mask.units = "land cover in precent"
        AWP_cumu.units = "AWP in MJ/m2"
        
        
        self.latmaskf = self.latmaskf.reshape(448, 304)
        self.lonmaskf = self.lonmaskf.reshape(448, 304)
        self.areamaskf = self.areamaskf.reshape(448, 304)
        self.landmask  = self.landmask.reshape(448, 304)
        
        latitude[:,:] = self.latmaskf
        longitude[:,:] = self.lonmaskf
        areacello[:,:] = self.areamaskf
        land_mask[:,:] = self.landmask
        

        AWP_special = nc.createVariable(varname="AWP Icefree and Mean",
         datatype="f4",dimensions=("map","xaxis","yaxis",))
        filepath = 'AWP/final_data/'
        
        filename = f'{filepath}AWP_energy_icefree.npz'
        AWP_cumu_load = CryoIO.readnumpy(filename)
        AWP_special[0,:,:] = AWP_cumu_load
        
        filename = f'{filepath}AWP_energy_Mean.npz'
        AWP_cumu_load = CryoIO.readnumpy(filename)
        AWP_special[1,:,:] = AWP_cumu_load
        
        icelist = []
        for year in range(1979,2023):
            filename = f'{filepath}AWP_energy_{year}.npz'
            AWP_cumu_load = CryoIO.readnumpy(filename)
            AWP_cumu_load = AWP_cumu_load.reshape(448, 304)
            icelist.append(AWP_cumu_load)
            
        AWP_cumu[0:,:,:] = icelist

        nc.close()



action = NETCDF()
action.NETCDF_creater()