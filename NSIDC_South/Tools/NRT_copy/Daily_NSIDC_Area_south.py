import numpy as np
import pandas
import matplotlib.pyplot as plt
import copy
import CryoIO
import os


class NSIDC_area:

    def __init__  (self):
        self.Cdate = CryoIO.CryoDate(2023,1,1) # initilizes a 366 day year
        self.webpath = '/var/www/Cryoweb'
        self.daycount = 366 #366year, 186summer
        
        self.CSVDatum = ['Date']
        self.CSVArea =['Area']
        self.CSVExtent = ['Extent']
        self.CSVCompaction = ['Compaction']
        
        self.tarea_anom = ['Area Anomaly']
        self.textent_anom = ['Extent Anomaly']
        
        self.plottype = 'both' #normal, anomaly, both
        self.masksload()
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
        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)

        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/pss25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
#        self.maskview(self.areamaskf)
#        plt.show()
        
        
    def dayloop(self):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        filepath = '/home/nico/Cryoscripts/NSIDC_South/DataFiles/'
        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            filename = f'{year}/NSIDC_{year}{month}{day}_south.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}_south.bin'
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
        areaanomaly = 0
        icemap_new = icemap
        icemapanomaly = 5
        
        if regionmask < 10:
            if icemap == 1.02: #value for missing data
                icemap = iceMean
            icemapanomaly = icemap - iceMean
            if 0.15 <= icemap <=1:
#                 print(icemap)
                area = icemap*areamask
                extent = areamask
            if icemap > 1:
                icemap = 5
                icemapanomaly = 5
            if icemap <=1 and icemapanomaly <=1:
                    areaanomaly = icemapanomaly*areamask
                    
        elif regionmask > 10:
            icemap_new = 5
                
        return icemap_new,icemapanomaly,area,extent,areaanomaly
        
    def maskview(self,icemap):
        '''displays loaded masks'''
        icemap = icemap.reshape(332, 316)
        plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=10, cmap=plt.cm.jet)


    def normalshow(self,icemap,icesum):
        '''displays sea ice data'''
        icemap = icemap.reshape(332, 316)
        icemap = icemap[0:310,20:310]
        icemap = np.ma.masked_greater(icemap, 1)
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        cmap = copy.copy(plt.colormaps["jet"])
        cmap.set_bad('black',0.6)
        
        self.ax.clear()
        self.ax.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
        self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
        cax = self.ax.imshow(icemap*100, interpolation='nearest', vmin=0, vmax=100,cmap = cmap)
        
        cbar = self.fig.colorbar(cax, ticks=[0,25,50,75,100],shrink=0.8).set_label('Sea Ice concentration in %')
        
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        self.ax.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 16, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        self.ax.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.fig.tight_layout(pad=1)
        self.fig.subplots_adjust(left=0.05)
        self.fig.savefig(f'{self.webpath}/NSIDC_Area/Antarctic-1.png')
    
    def anomalyshow(self,icemap,icesum):
        '''displays sea ice anomaly data'''
        icemap = icemap.reshape(332, 316)
        icemap = icemap[0:310,20:310]
        icemap = np.ma.masked_greater(icemap, 1)
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        self.ax2.clear()
        self.ax2.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
        cmap2 = copy.copy(plt.colormaps["coolwarm_r"])
        cmap2.set_bad('black',0.6)
        self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
        cax = self.ax2.imshow(icemap*100, interpolation='nearest', vmin=-75, vmax=75, cmap=cmap2)
        
        cbar = self.fig2.colorbar(cax, ticks=[-75,-50,-25,0,25,50,75],shrink=0.8).set_label('Sea Ice concentration anomaly in %')
        
        
        self.ax2.axes.get_yaxis().set_ticks([])
        self.ax2.axes.get_xaxis().set_ticks([])
        self.ax2.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(2, 16, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(205, 305,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
        
        self.ax2.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.fig2.tight_layout(pad=1)
        self.fig2.subplots_adjust(left=0.05)
        self.fig2.savefig(f'{self.webpath}/NSIDC_Area/Antarctic_anom-1.png')
    
        
    def normalandanomaly(self):
        '''creates separate figures for sea ice data'''
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 8))
        
    def csvexport(self,filename,filedata):
        np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
    
    def loadCSVdata (self,deletion):
        #NRT Data
        Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
        Yeardata = pandas.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv', names=Yearcolnames)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVArea = Yeardata.Area.tolist()
        self.CSVExtent = Yeardata.Extent.tolist()
        self.CSVCompaction = Yeardata.Compaction.tolist()
        
        if deletion > 0:
            self.CSVDatum = self.CSVDatum[:-deletion]
            self.CSVArea = self.CSVArea[:-deletion]
            self.CSVExtent = self.CSVExtent[:-deletion]
            self.CSVCompaction = self.CSVCompaction[:-deletion]
            
        
        
    def maintanance(self):
        
        xxx = 6
        while xxx > 0:
            try:
                file1 = f'{self.webpath}/NSIDC_Area/Antarctic-{xxx}.png'
                file2 = f'{self.webpath}/NSIDC_Area/Antarctic-{xxx+1}.png'
                file3 = f"{self.webpath}/NSIDC_Area/Antarctic_anom-{xxx}.png"
                file4 = f"{self.webpath}/NSIDC_Area/Antarctic_anom-{xxx+1}.png"
                
                self.rename_image(file1, file2)
                self.rename_image(file3, file4)
            except:
                print(f'no image {xxx}')
            xxx -= 1
            
            
    def rename_image(self,file1,file2):
        os.rename(file1,file2)
        
    def no_data_day(self):
        self.loadCSVdata(0)
        self.CSVDatum.append(self.CSVDatum[-1])
        self.CSVArea.append(self.CSVArea[-1])
        self.CSVExtent.append (self.CSVExtent[-1])
        self.CSVCompaction.append(self.CSVCompaction[-1])
        
        self.csvexport(f'{self.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv',
            [self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])

    
    def automated (self,day,month,year,daycount):
        self.Cdate = CryoIO.CryoDate(year,month,day)
        self.daycount = daycount
        self.maintanance()
        
        self.loadCSVdata(self.daycount-1)
        self.dayloop()
# =============================================================================
#         self.csvexport(f'{self.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv',
#             [self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])
# =============================================================================


action = NSIDC_area()
if __name__ == "__main__":
    print('main')
    #action.loadCSVdata()
    # action.automated(26,'09',2023,3) #note substract xxx days from last available day
    # action.maintanance()
    
#     action.no_data_day()
#     action.dayloop()
    action.year_reCalc()
    action.csvexport(f'{action.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv',
            [action.CSVDatum,action.CSVArea,action.CSVExtent,action.CSVCompaction])

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

arraylength: 104912 (332, 316)

#Regionmask:
2: Weddel Sea
3: Indian Ocean
4: Pacific Ocean
5: Ross Sea
6: Bellingshausen Amundsen Sea
11: Land
12: Coast
'''