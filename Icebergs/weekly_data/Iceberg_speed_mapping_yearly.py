import numpy as np
import matplotlib.pyplot as plt
import CryoIO
import pandas
import math
import copy

class Simpleviewer:


    def __init__  (self):
        self.year = 2021
        self.month = 1
        self.day = 31
        
        self.dailyorcumu()
        self.masksload()
    

    def masksload(self):
    
        regionmask_file = 'Masks/region_s_pure.msk'
        latmask_file = 'Masks/pss25lats_v3.dat'
        lonmask_file = 'Masks/pss25lons_v3.dat'

        self.latmask = CryoIO.openfile(latmask_file,np.int32) /100000
        self.lonmask = CryoIO.openfile(lonmask_file,np.int32) /100000
        self.regionmask = CryoIO.openfile(regionmask_file,np.int8)

# =============================================================================
#         testmap = self.regionmask.reshape(332,316)
#         self.maskview(testmap)
#         plt.show()
# =============================================================================
        
        
    def maincalc(self):
        
        Yearcolnames = ['iceberg', 'lat', 'lon','speed']
        speedlist = pandas.read_csv(f'temp/{self.year}_all.csv', names=Yearcolnames)
        
        Yearcolnames = ['index', 'lat','lon']
        lat_lon_list = pandas.read_csv('Masks/lat-lonlist_coast_free.csv', names=Yearcolnames)
        
#         print(lat_lon_list['lat'][0])

        # mask = self.region_calc(mask) # create sub regions
#         self.lat_lon_list() # export lat/lon values
        speedmap, duplicate = self.map_iceberg_speed(speedlist,lat_lon_list)

        CryoIO.savebinaryfile('Masks/2022_iceberg.dat',speedmap)
        CryoIO.savebinaryfile('Masks/2022_duplicate.dat',duplicate)
        self.testdata()

        
    def testdata(self):
        
        regionmask_file = 'Masks/2022_iceberg.dat'
        duplicate_file = 'Masks/2022_duplicate.dat'
        testmap = CryoIO.openfile(regionmask_file,float) / 7
        duplicate_map = CryoIO.openfile(duplicate_file,float)
        
        testmap = testmap / duplicate_map
        testmap[np.isnan(testmap)] = 0
        
        for index, value in enumerate(self.regionmask):
            if value == 11:
                testmap[index] = 255
                
            
        self.maskview(testmap)


    def lat_lon_list(self):

        latlist = []
        lonlist = []
        for index,value in enumerate(self.regionmask):
            if value == 11:
                continue
            if self.latmask[index] > -50:
                continue
            else:
                latlist.append([index,self.latmask[index]])
                lonlist.append([index,self.lonmask[index]])
                
        CryoIO.csv_rowexport('latlist.csv', latlist)
        CryoIO.csv_rowexport('lonlist.csv', lonlist)

        return
    
    
    def map_iceberg_speed(self,speedlist,lat_lon_list):

        speed_array = np.zeros(len(self.latmask))
        duplicate = np.zeros(len(self.latmask))
        
        gridindex = lat_lon_list['index']
        latitudes = lat_lon_list['lat']
        longitudes = lat_lon_list['lon']
        
        latdict = {}
        for index,value in enumerate(latitudes):
            latdict[gridindex[index]] = value
        
        for speed_index,speed in enumerate(speedlist['speed']):
            speed_lat = speedlist['lat'][speed_index]
            speed_lon = speedlist['lon'][speed_index]
            print(speed_index)
        
            newlon_list = []
            for index,value in enumerate(longitudes):
                aaa = math.isclose(speed_lon, value, abs_tol = 0.1)
                if aaa == True:
                    newlon_list.append(gridindex[index])
    #                 print(gridindex[index])
            for index2,value2 in enumerate(newlon_list):
                
                bbb = math.isclose(speed_lat, latdict[value2], abs_tol = 0.25)
                if bbb == True:
                    speed_array[value2] += speed
                    duplicate[value2] += 1
                

        return speed_array, duplicate

    def maskview(self,icemap):        
        self.ax.clear()
        icemap = np.ma.masked_greater(icemap, 100)
        icemap = icemap.reshape(332, 316)
        icemap = icemap[20:300,30:300]
        
        map1 = np.ma.masked_outside(icemap,-1,111) # Land -> Water
        map2 = np.ma.masked_outside(icemap,0.1,60) # Ice -> Snow
        
        
        cmap = copy.copy( plt.cm.Greys)
        cmap2 = copy.copy( plt.cm.jet)
        cmap.set_bad('black',0.8)
        
        #self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
        #self.ax.set_xlabel(': '+str(icesum)+' Wh/m2')
        self.ax.imshow(map1, interpolation='nearest', vmin=-222, vmax=25, cmap=cmap) # Water & Land
        cax = self.ax.imshow(map2, interpolation='nearest', vmin=0.1, vmax=25, cmap=cmap2) #Snow & Ice
        self.cbar = self.fig.colorbar(cax).set_label('km / day')
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        self.ax.text(-0.04, 0.0, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.ax.text(0.0, -0.04, '2022',
            transform=self.ax.transAxes,color='grey', fontsize=10)
        self.fig.tight_layout(pad=1)
        
#         self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=1, vmax=40 , cmap = cmap2)
        self.fig.savefig(f'iceberg_speed_{self.year}.png')
        plt.pause(0.01)
        
        
    def dailyorcumu(self):        
        plt.style.use('dark_background')
        self.icenull = np.zeros(104912, dtype=float)
        self.icenull = self.icenull.reshape(332, 316)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
#         self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
        self.title = self.fig.suptitle(f'Iceberg location and Speed {self.year}', fontsize=14, fontweight='bold')
            
        
        
        
action = Simpleviewer()
# action.lat_lon_list()
action.maincalc()
# action.testdata()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
