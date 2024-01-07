from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import CryoIO
import pandas
import math
import copy

plt.style.use('dark_background')

class Simpleviewer:


    def __init__  (self):
        self.year = 2021
        self.month = 1
        self.day = 31
        self.threads = 8
        
        
        # self.masksload_25km()
        self.masksload_3km()

    def masksload_25km(self):
    
        regionmask_file = 'Masks/mask_25km/region_s_pure.msk'
        latmask_file = 'Masks/mask_25km/pss25lats_v3.dat'
        lonmask_file = 'Masks/mask_25km/pss25lons_v3.dat'

        self.latmask = CryoIO.openfile(latmask_file,np.int32) /100000
        self.lonmask = CryoIO.openfile(lonmask_file,np.int32) /100000
        self.regionmask = CryoIO.openfile(regionmask_file,np.int8)
        
    def masksload_3km(self):
    
        regionmask_file = 'Masks/mask_3km/AMSR2_sh_region.npz'
        landmask_file = 'Masks/mask_3km/AMSR2_sh_land.npz'
        latmask_file = 'Masks/mask_3km/AMSR2_sh_lat.npz'
        lonmask_file = 'Masks/mask_3km/AMSR2_sh_lon.npz'

        self.latmask = CryoIO.readnumpy(latmask_file).flatten()
        self.lonmask = CryoIO.readnumpy(lonmask_file).flatten()
        self.landmask = CryoIO.readnumpy(landmask_file).flatten()
        
        # testmap = self.regionmask / self.landmask

        # self.icemap_3km(self.landmask)

        
        
    def maincalc(self):
        
        Yearcolnames = ['iceberg', 'lat', 'lon','speed']
        speed_df = pandas.read_csv('temp/iceberg_speed.csv', names=Yearcolnames)
        
        Yearcolnames = ['index', 'lat','lon']
        # lat_lon_list = pandas.read_csv('Masks/mask_25km/lat-lonlist_coast_free.csv', names=Yearcolnames)
        lat_lon_list = pandas.read_csv('Masks/mask_3km/ocean_lat_lon_list.csv', names=Yearcolnames)
        
        self.gridindex = lat_lon_list['index']
        latitudes = lat_lon_list['lat']
        self.longitudes = lat_lon_list['lon']
        
        self.latdict = {}
        for index,value in enumerate(latitudes):
            self.latdict[self.gridindex[index]] = value
        
        speedlist = []
        for speed_index,speed in enumerate(speed_df['speed']):
            speed_lat = speed_df['lat'][speed_index]
            speed_lon = speed_df['lon'][speed_index]
            speedlist.append([speed_lat,speed_lon,speed])
            
        self.speed_array = np.zeros(len(self.latmask))
        self.duplicate = np.zeros(len(self.latmask))
        
        print('pool: ', len(speedlist), ' threads: ',self.threads)
        p = Pool(processes=self.threads)
        data = p.map(self.map_iceberg_speed, speedlist)
        p.close()

        for value in data:
            if value != None:
                self.speed_array[value[0]] += value[1]
                self.duplicate[value[0]] += 1
        

        CryoIO.savenumpy('speedmap_23_3km.npz',self.speed_array)
        CryoIO.savenumpy('duplicate_23_3km.npz',self.duplicate)

        
    def testdata(self):
        
        speed_file = 'speedmap_23_25km.npz'
        duplicate_file = 'duplicate_23_25km.npz'
        testmap = CryoIO.readnumpy(speed_file) 
        duplicate_map = CryoIO.readnumpy(duplicate_file)
        
        testmap = testmap / duplicate_map
        testmap[np.isnan(testmap)] = 0
        
        for index, value in enumerate(self.regionmask):
            if value == 11:
                testmap[index] = 111

        self.icemap_25km(testmap)

    
    
    def map_iceberg_speed(self,speed_data):

        #function finds all close longitude points
        newlon_list = []
        for index,value in enumerate(self.longitudes):
            aaa = math.isclose(speed_data[1], value, abs_tol = 0.1)
            if aaa == True:
                newlon_list.append(self.gridindex[index])
#                 print(gridindex[index])

        #function finds all close latitude points from the longitude list
        for index2,value2 in enumerate(newlon_list):
            bbb = math.isclose(speed_data[0], self.latdict[value2], abs_tol = 0.1)
            if bbb == True:
                return value2,speed_data[2]

                

    def icemap_25km(self,icemap):        
        icemap = np.ma.masked_greater(icemap, 100)
        icemap = icemap.reshape(332, 316)
        
        map1 = np.ma.masked_outside(icemap,-1,111) # Land -> Water
        map2 = np.ma.masked_outside(icemap,0.1,60) # Ice -> Snow
        
        
        cmap = copy.copy( plt.cm.Greys)
        cmap2 = copy.copy( plt.cm.jet)
        cmap.set_bad('black',0.8)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        title = fig.suptitle('Average Iceberg Speed', fontsize=14, fontweight='bold')
        
        ax.imshow(map1, interpolation='nearest', vmin=-222, vmax=111, cmap=cmap) # Water & Land
        cax = ax.imshow(map2, interpolation='nearest', vmin=0.1, vmax=30, cmap=cmap2) #Iceberg Speed
        cbar = fig.colorbar(cax).set_label('km / day')
        ax.axis('off')
        ax.text(-0.04, 0.0, 'cryospherecomputing.com',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
        ax.text(0.0, -0.04, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        fig.tight_layout(pad=1)
        # fig.savefig('images/iceberg_speed_23.png')
        plt.pause(0.01)
        
    def icemap_3km(self,icemap):        
        # icemap = np.ma.masked_greater(icemap, 100)

        
        map1 = np.ma.masked_outside(icemap,-1,111) # Land -> Water
        map2 = np.ma.masked_outside(icemap,0.1,60) # Ice -> Snow
        
        
        cmap = copy.copy( plt.cm.Greys)
        cmap2 = copy.copy( plt.cm.jet)
        cmap.set_bad('black',0.8)
        
        fig, ax = plt.subplots(figsize=(8, 8))
        title = fig.suptitle('Average Iceberg Speed', fontsize=14, fontweight='bold')
        
        cax = ax.imshow(icemap)
        # ax.imshow(map1, interpolation='nearest', vmin=-222, vmax=111, cmap=cmap) # Water & Land
        # cax = ax.imshow(map2, interpolation='nearest', vmin=0.1, vmax=30, cmap=cmap2) #Iceberg Speed
        cbar = fig.colorbar(cax).set_label('km / day')
        ax.axis('off')
        ax.text(-0.04, 0.0, 'cryospherecomputing.com',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
        ax.text(0.0, -0.04, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        fig.tight_layout(pad=1)
        # fig.savefig('images/iceberg_speed_23.png')
        plt.pause(0.01)
        
        
        
action = Simpleviewer()
# action.lat_lon_list()
action.maincalc()
# action.testdata()

