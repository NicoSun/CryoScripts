import CryoIO
import numpy as np
import netCDF4
import csv

class Mask_maker:
    
    def __init__  (self):
        self.masksload_3km()
        
    def masksload_25km(self):
    
        regionmask_file = 'Masks/mask_25km/region_s_pure.msk'
        latmask_file = 'Masks/mask_25km/pss25lats_v3.dat'
        lonmask_file = 'Masks/mask_25km/pss25lons_v3.dat'

        self.latmask = CryoIO.openfile(latmask_file,np.int32) /100000
        self.lonmask = CryoIO.openfile(lonmask_file,np.int32) /100000
        self.regionmask = CryoIO.openfile(regionmask_file,np.int8)
        
    def masksload_3km(self):
    
        landmask_file = 'Masks/mask_3km/AMSR2_sh_land.npz'
        latmask_file = 'Masks/mask_3km/AMSR2_sh_lat.npz'
        lonmask_file = 'Masks/mask_3km/AMSR2_sh_lon.npz'

        self.latmask = CryoIO.readnumpy(latmask_file).flatten()
        self.lonmask = CryoIO.readnumpy(lonmask_file).flatten()
        self.landmask = CryoIO.readnumpy(landmask_file).flatten()
    
    def make_lat_lon_list(self):

        lat_lon_list = []
        for index,value in enumerate(self.landmask):
            if value ==1:
                #if land ignore
                continue
            if self.latmask[index] > -46:
                #if high latitudes ignore
                continue
            else:
                lat = round(self.latmask[index],2)
                lon = round(self.lonmask[index],2)
                lat_lon_list.append([index,lat,lon])
        
        with open('Masks/mask_3km/ocean_lat_lon_list.csv', 'w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(lat_lon_list)


        return
    
    def read_netcdf(self):
        import matplotlib.pyplot as plt
        
        
        layer = 'latitude' # sea_ice_concentration,land,latitude,longitude
        with netCDF4.Dataset('Masks/mask_3km/aaa.nc', mode='r',) as nc:
            # print(nc.variables)
            print(nc)
            icemap = np.array(nc[layer])
            
            icemap = np.flip(icemap,axis=1)
            icemap = np.rot90(icemap,k=2)
            
            # CryoIO.savenumpy('Masks/mask_3km/AMSR2_sh_region.npz',icemap)
            CryoIO.savenumpy('Masks/mask_3km/AMSR2_sh_lat.npz',icemap)
            # CryoIO.savenumpy('Masks/mask_3km/AMSR2_sh_lon.npz',icemap)
            # CryoIO.savenumpy('Masks/mask_3km/AMSR2_sh_land.npz',icemap)
            
if __name__ == '__main__':
    action = Mask_maker()
    # action.read_netcdf()
    action.make_lat_lon_list()