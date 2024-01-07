"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun
"""

import os
import re
import gzip
import numpy as np
import CryoIO
import netCDF4
import pandas

class AMSR_File_Manager:
    def __init__(self):
        Columns = ['A']
        csvdata = pandas.read_csv('Masks/polehole.csv', names=Columns,dtype=int)
        self.icepole = csvdata.A.tolist()
                 
        Columns = ['A']
        csvdata = pandas.read_csv('Masks/polering.csv', names=Columns,dtype=int)
        self.icepole_ring = csvdata.A.tolist()
        self.combo_list = self.icepole + self.icepole_ring

    def rename(self,year):
        filepath = f'DataFiles/north/{year}'
        
        for file in os.listdir(filepath):
            filenew = file[0:5] + '_nh' + file[5:]
    #         print(filenew)
            os.rename(os.path.join(filepath,file),os.path.join(filepath,filenew))
    
    
    def folder_create(self,year):
        os.mkdir(f'DataFiles/{year}')
        
    def fill_pole_hole(self):
        import time
        import os
        start = time.time()
        
        for year in range(2023,2024):
            filepath = f'DataFiles/north/{year}'
            for file in os.listdir(filepath):
                print(file)
                icemap = CryoIO.readnumpy(os.path.join(filepath,file))
                icemap = icemap.reshape(-1)
                icemap = self.formatdata(icemap)
                
                icemap = icemap.reshape(3300,2100)
                icemap = np.clip(icemap,a_min=0,a_max=255)
                icemap = np.array(icemap,dtype=np.uint8)
                # CryoIO.savenumpy(os.path.join(filepath,file), icemap)
        
        end = time.time()
        print(end-start)
    
    def mass_converter(self,nc,hemisphere,filename):
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
        
    def formatdata(self,icemap):
        icepolecon = []
        for val in self.icepole_ring:
            if icemap[val] < 255:
                icepolecon.append (icemap[val])
            
        icepolecon = np.mean(icepolecon)
        
        for val2 in self.combo_list:
            if icemap[val2] > 254:
                icemap[val2] = icepolecon
        return icemap
    
    def dailyupdate(self,tempdata,filenameFormatted,hemisphere,datedict):
        '''this function handels daily automated updates'''
        
        layer = 'sea ice concentration' # sea_ice_concentration,land,latitude,longitude
        
        with netCDF4.Dataset('dummy', mode='r', memory=gzip.decompress(tempdata.getbuffer())) as nc:
    
            icemap = np.array(nc[layer][0])
            icemap = np.flip(icemap,axis=1)
            icemap = np.rot90(icemap,k=2)
    
            if hemisphere == 'nh':
                icemap = icemap[200:3500,100:2200]
                icemap = icemap.flatten()
                icemap = self.formatdata(icemap)
                icemap = icemap.reshape(3300,2100)
            elif hemisphere == 'sh':
                icemap = icemap[0:2500,300:2500]
    
            icemap = np.clip(icemap,a_min=0,a_max=255)
            icemap = np.array(icemap,dtype=np.uint8)
            CryoIO.savenumpy(filenameFormatted,icemap)
            self.create_maps(icemap,hemisphere,datedict)
            
    def create_maps(self,icemap,hemi,datedict):
        import AMSR2_maps
        
        year = datedict['year']
        month = datedict['month']
        day = datedict['day']
        datestring = f'{year}-{month}-{day}'
        landmask = CryoIO.readnumpy(f'Masks/{hemi}/AMSR2_{hemi}_land.npz').flatten()
        icemean = CryoIO.readnumpy(f'DataFiles/Mean_12_23/{hemi}/AMSR2_{hemi}_Mean_{month}{day}.npz').flatten()
        icemap = icemap.flatten()
        anom_map = icemap - icemean
        print(len(landmask))
        print(len(icemean))
        print(len(icemap))
        print(len(anom_map))
        
        for index,value in enumerate(landmask):
            if value == 1:
                anom_map[index] = 222
        
        if hemi == 'nh':
            icemap = icemap.reshape(3300,2100)
            anom_map = anom_map.reshape(3300,2100)
        elif hemi == 'sh':
            icemap = icemap.reshape(2500,2200)
            anom_map = anom_map.reshape(2500,2200)
        AMSR2_maps.action.normalshow(icemap, hemi, datestring,icesum=0)
        AMSR2_maps.action.anomalyshow(anom_map, hemi, datestring,icesum=0)

action = AMSR_File_Manager()

#for year in range(2004,2019):
if __name__ == "__main__":
    print('main')
    # action.fill_pole_hole()
#     dailyupdate('DataFiles/v110/nh_SIC_LEAD_2023030112_030200.nc.gz','nh')
#    mass_converter()
    

