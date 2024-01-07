import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import CryoIO
import os

class NSIDC_area:

    def __init__  (self):
        self.Cdate = CryoIO.CryoDate(2023,1,1) # initilizes a 366 day year
        self.webpath = '/var/www/Cryoweb'
        
        self.daycount = 33 #366year, 186summer
        
        self.CSVDatum = ['Date']
        self.CSVArea =['Area']
        self.CSVExtent = ['Extent']
        self.CSVCompaction = ['Compaction']
        
        self.tarea_anom = ['Area Anomaly']
        self.textent_anom = ['Extent Anomaly']
        
        self.region_area = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
                    , ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
                    , ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
        self.region_extent = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
                    , ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
                    , ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
        
        
        self.plottype = 'both' #normal, anomaly, both
        self.masksload()
        self.initRegions()
        self.normalandanomaly()
        
        
    def year_reCalc(self):
        import datetime
        self.today = datetime.date.today()
        self.daycount = self.today.timetuple().tm_yday
        
        self.dayloop()
        
        
    def masksload(self):
        '''Loads regionmask and pixel area mask
        option to display masks is commented out
        '''
        filename = '/home/nico/Cryoscripts/NSIDC/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = '/home/nico/Cryoscripts/NSIDC/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
#        self.maskview(self.regmaskf)
#        plt.show()

    def initRegions(self):
        self.area_init = []
        self.extent_init = []
        
        for x in range(0,len(self.region_area)):
            self.area_init.append([])
            self.extent_init.append([])
            

    def appendregion(self):

        for x in range(0,len(self.region_area)):
            self.region_area[x].append(int(np.sum(self.area_init[x]))/1e6)
            
        for x in range(0,len(self.region_extent)):
            self.region_extent[x].append(int(np.sum(self.extent_init[x]))/1e6)
            
        self.initRegions()
        
        
    def dayloop(self):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        
        filepath = '/home/nico/Cryoscripts/NSIDC/DataFiles/'
        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            filename = f'{year}/NSIDC_{year}{month}{day}.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}.bin'
            print(filename)
            
            #loads data file
            ice = CryoIO.readnumpy(f'{filepath}{filename}')/250
                
            # loads the mean data file
            iceMean = CryoIO.openfile(f'{filepath}{filenameMean}',np.uint8)/250
        
            #area & extent calculation
            aaa = np.vectorize(self.calculateAreaExtent)
            icemap_new,icemapanomaly,area,extent,areaanomaly = aaa(ice,iceMean,self.areamaskf,self.regmaskf)
            
            compaction = (np.sum(area)/np.sum(extent))*100
            self.CSVDatum.append('{}/{}/{}'.format(year,month,day))
            self.CSVArea.append((np.sum(area))/1e6)
            self.CSVExtent.append (np.sum(extent)/1e6)
            self.CSVCompaction.append(round(compaction,3))
            
            self.appendregion()
            
            area_anom = np.sum(areaanomaly)/1e6

            if count == (self.daycount-1):
                self.normalshow(icemap_new,self.CSVArea[-1])
                self.anomalyshow(icemapanomaly,area_anom)
# =============================================================================
#                     plt.close()
#                     plt.close()
# =============================================================================
            
            self.Cdate.datecalc()
                
    def calculateAreaExtent(self,icemap,iceMean,areamask,regionmask):
        '''area & extent calculation & remove lake ice'''
        area = 0
        extent = 0
        icemap_new = icemap
        areaanomaly = 0
        
        if regionmask < 2:
            icemap_new = 0.0
            icemapanomaly = 0.0
        if 1 < regionmask < 16:
            if icemap == 1.02: #value for missing data
                icemap = iceMean
                icemap_new = iceMean
            icemapanomaly = icemap - iceMean
            if 0.15 <= icemap <=1:
                area = icemap*areamask
                extent = areamask
                if regionmask == 2:
                    self.area_init[0].append (area)
                    self.extent_init[0].append (areamask)
                elif regionmask == 3:
                    self.area_init[1].append (area)
                    self.extent_init[1].append (areamask)
                elif regionmask == 4:
                    self.area_init[2].append (area)
                    self.extent_init[2].append (areamask)
                elif regionmask == 6:
                    self.area_init[3].append (area)
                    self.extent_init[3].append (areamask)
                elif regionmask == 7:
                    self.area_init[4].append (area)
                    self.extent_init[4].append (areamask)
                elif regionmask == 8:
                    self.area_init[5].append (area)
                    self.extent_init[5].append (areamask)
                elif regionmask == 9:
                    self.area_init[6].append (area)
                    self.extent_init[6].append (areamask)
                elif regionmask == 10:
                    self.area_init[7].append (area)
                    self.extent_init[7].append (areamask)
                elif regionmask == 11:
                    self.area_init[8].append (area)
                    self.extent_init[8].append (areamask)
                elif regionmask == 12:
                    self.area_init[9].append (area)
                    self.extent_init[9].append (areamask)
                elif regionmask == 13:
                    self.area_init[10].append (area)
                    self.extent_init[10].append (areamask)
                elif regionmask == 14:
                    self.area_init[11].append (area)
                    self.extent_init[11].append (areamask)
                elif regionmask == 15:
                    self.area_init[12].append (area)
                    self.extent_init[12].append (areamask)
        if regionmask > 16: #Land mask
            icemap_new    = 5
            icemapanomaly = 5
        if icemap <=1 and icemapanomaly <=1: #cheap anomaly calculation
                areaanomaly = icemapanomaly*areamask
                
        return icemap_new,icemapanomaly,area,extent,areaanomaly
        
    def maskview(self,icemap):
        '''displays loaded masks'''
        icemap = icemap.reshape(448, 304)
        plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=16, cmap=plt.cm.jet)


    def normalshow(self,icemap,icesum):
        '''displays sea ice data'''
        icemap = np.ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(448, 304)
        icemap = icemap[60:410,30:260]
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        cmap = copy.copy(plt.colormaps["jet"])
        cmap.set_bad('black',0.6)
        
        self.ax.clear()
        self.ax.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
        #self.ax.set_title('Minimum of Minima')
        self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
        cax = self.ax.imshow(icemap*100, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        
        cbar = self.fig.colorbar(cax, ticks=[0,25,50,75,100],shrink=0.85).set_label('Sea Ice concentration in %')
        
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        self.ax.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 16, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        self.ax.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.fig.tight_layout(pad=1)
        self.fig.subplots_adjust(left=0.05)
        self.fig.savefig(f'{self.webpath}/NSIDC_Area/Arctic-1.png')
#         plt.pause(0.01)

    
    def anomalyshow(self,icemap,icesum):
        '''creates separate figures for sea ice data'''
        icemap = np.ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(448, 304)
        icemap = icemap[60:410,30:260]
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        self.ax2.clear()
        self.ax2.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))        
        cmap2 = copy.copy(plt.colormaps["coolwarm_r"])
        cmap2.set_bad('black',0.6)
        
        self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
        cax = self.ax2.imshow(icemap*100, interpolation='nearest', vmin=-75, vmax=75, cmap=cmap2)
        
        cbar = self.fig2.colorbar(cax, ticks=[-75,-50,-25,0,25,50,75],shrink=0.85).set_label('Sea Ice concentration anomaly in %')
        
        self.ax2.axes.get_yaxis().set_ticks([])
        self.ax2.axes.get_xaxis().set_ticks([])
        self.ax2.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(2, 16, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(165, 346,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
        self.ax2.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.fig2.tight_layout(pad=1)
        self.fig2.subplots_adjust(left=0.05)
        self.fig2.savefig(f'{self.webpath}/NSIDC_Area/Arctic_anom-1.png')
#         plt.pause(0.01)
    
        
    def normalandanomaly(self):
        '''creates separate figures for sea ice data'''
        self.fig, self.ax = plt.subplots(figsize=(8, 10))
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))

    def loadCSVdata (self,deletion):
        #NRT Data
        Yearcolnames = ['Date','B','C','D','E','F']
        Yeardata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Arctic_NSIDC_Area_NRT.csv', names=Yearcolnames)

        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVArea = Yeardata.B.tolist()
        self.CSVExtent = Yeardata.C.tolist()
        self.CSVCompaction = Yeardata.D.tolist()

        if deletion > 0:
            self.CSVDatum = self.CSVDatum[:-deletion]
            self.CSVArea = self.CSVArea[:-deletion]
            self.CSVExtent = self.CSVExtent[:-deletion]
            self.CSVCompaction = self.CSVCompaction[:-deletion]
            
            
        
    def loadCSVRegiondata (self,deletion):
        Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Regional_NRT.csv', names=Yearcolnames)
        
        for x in range (0,len(Yearcolnames)):
            self.region_area[x] = Yeardata[Yearcolnames[x]].tolist()
            if deletion > 0:
                self.region_area[x] = self.region_area[x][:-deletion]
        
        
        Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata_ext = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Regional_NRT_extent.csv', names=Yearcolnames)
        
        for x in range (0,len(Yearcolnames)):
            self.region_extent[x] = Yeardata_ext[Yearcolnames[x]].tolist()
            if deletion > 0:
                self.region_extent[x] = self.region_extent[x][:-deletion]
        
        
    def exportdata(self):
        filepath = f'{self.webpath}/NSIDC_Area/Data/'
        CryoIO.csv_columnexport(f'{filepath}Arctic_NSIDC_Area_NRT.csv',
            [self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])
        CryoIO.csv_columnexport(f'{filepath}Regional_NRT.csv',self.region_area)
        CryoIO.csv_columnexport(f'{filepath}Regional_NRT_extent.csv',self.region_extent)
    
    def maintanance(self):
        xxx = 6
        while xxx > 0:
            try:
                file1 = f'{self.webpath}/NSIDC_Area/Arctic-{xxx}.png'
                file2 = f'{self.webpath}/NSIDC_Area/Arctic-{xxx+1}.png'
                file3 = f"{self.webpath}/NSIDC_Area/Arctic_anom-{xxx}.png"
                file4 = f"{self.webpath}/NSIDC_Area/Arctic_anom-{xxx+1}.png"
                
                self.rename_image(file1, file2)
                self.rename_image(file3, file4)
            except:
                print(f'no day {xxx}')
            xxx -= 1
                
            
    def rename_image(self,file1,file2):
        os.rename(file1,file2)
        
    def no_data_day(self):
        self.loadCSVdata(0)
        self.loadCSVRegiondata(0)
        
        self.CSVDatum.append(self.CSVDatum[-1])
        self.CSVArea.append(self.CSVArea[-1])
        self.CSVExtent.append (self.CSVExtent[-1])
        self.CSVCompaction.append(self.CSVCompaction[-1])
        
#         print(self.region_area[0])
        for x in range(0,len(self.region_area)):
            self.region_area[x].append(self.region_area[x][-1])
            
        for x in range(0,len(self.region_extent)):
            self.region_extent[x].append(self.region_extent[x][-1])

        self.exportdata()

    
    def automated (self,day,month,year,daycount):
        self.Cdate = CryoIO.CryoDate(year,month,day)
        self.daycount = daycount
        self.maintanance()
        
        self.loadCSVdata(self.daycount-1)
        self.loadCSVRegiondata(self.daycount-1)
        self.dayloop()
        self.exportdata()



action = NSIDC_area()
if __name__ == "__main__":
    print('main')
#     action.maintanance()
#     action.dayloop()
#     action.year_reCalc()
#     action.exportdata()
#     action.no_data_day()
#     action.automated(16,11,2022,4) #note substract xxx days from last available day
    

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

#Regionmask:
0: lakes
1: Ocean
2: Sea of Okothsk
3: Bering Sea
4: Hudson bay
5: St Lawrence
6: Baffin Bay
7: Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Achipelago
15: Central Arctic
20: Land
21: Coast
'''
