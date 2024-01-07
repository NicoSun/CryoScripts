import numpy as np
import matplotlib.pyplot as plt
import CryoIO
import copy

class NSIDC_area:

    def __init__ (self,year=2022):
        self.Cdate = CryoIO.CryoDate(year,1,1) # initilizes a 366 day year
        self.root = './'
        self.daycount = 366 #366year, 186summer
        
        self.CSVDatum = ['Date']
        self.CSVArea =['Area']
        self.CSVExtent = ['Extent']
        self.CSVCompaction = ['Compaction']
        
        self.masksload()
        self.mode = 'past' #min , max, past
        
        
    def masksload(self):
        '''Loads regionmask and pixel area mask
        option to display masks is commented out
        '''
        filename = 'Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(f'{self.root}{filename}',np.uint32)

        filename = 'Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(f'{self.root}{filename}',np.uint32)/1000
        
#        self.maskview(self.regmaskf)
#        plt.show()
        
        
    def dayloop(self):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            if self.mode == 'past':
                filename = f'{year}/NSIDC_{year}{month}{day}.npz'
            elif self.mode == 'max':
                filename = f'Max/NSIDC_Max_{month}{day}.npz'
            elif self.mode == 'min':
                filename = f'Min/NSIDC_Min_{month}{day}.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}.npz'
            
            ice = CryoIO.readnumpy(f'{self.root}DataFiles/{filename}')/250
                
            # loads the mean data file
            iceMean = CryoIO.readnumpy(f'{self.root}DataFiles/{filenameMean}')/250
        
            #area & extent calculation
            aaa = np.vectorize(self.calculateAreaExtent)
            icemap_new,icemapanomaly,area,extent,areaanomaly = aaa(ice,iceMean,self.areamaskf,self.regmaskf)
            
            self.CSVDatum.append('{}/{}/{}'.format(year,month,day))
            self.CSVArea.append((np.sum(area))/1e6)
            self.CSVExtent.append (np.sum(extent)/1e6)
            self.CSVCompaction.append((np.sum(area)/np.sum(extent))*100)
            
            area_anom = np.sum(areaanomaly)/1e6
            
            #optional data show
            if day == '01' or day == '15':
                self.normalshow(icemap_new)
                print(year,month,day)
#            self.anomalyshow(icemapanomaly,area_anom)
            
            self.Cdate.datecalc()
            
        # plt.show()
            
                
                
    def calculateAreaExtent(self,icemap,iceMean,areamask,regionmask):
        '''area & extent calculation & remove lake ice'''
        area = 0
        extent = 0
        icemap_new = icemap
        icemapanomaly = icemap - iceMean
        areaanomaly = 0
        
        if regionmask < 2:
            icemap_new = 0.0
            icemapanomaly = 0.0
        if 1 < regionmask < 16:
            if icemap == 1.02: #value for missing data
                icemap = iceMean
                icemap_new = iceMean
            if 0.15 <= icemap <=1:
                area = icemap*areamask
                extent = areamask
        if regionmask > 16:
            icemap_new    = 5
            icemapanomaly = 5
        if icemap <=1 and icemapanomaly <=1: #cheap anomaly calculation
                areaanomaly = icemapanomaly*areamask
                
        return icemap_new,icemapanomaly,area,extent,areaanomaly
    
        
    def maskview(self,icemap):
        '''displays loaded masks'''
        icemap = icemap.reshape(448, 304)
        plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=16, cmap=plt.cm.jet)


    def normalshow(self,icemap):
        '''displays sea ice data'''
        icemap = np.ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(448, 304)
        icemap = icemap[40:420,10:290]
        icesum_area = '{0:,}'.format(round(self.CSVArea[-1] * 1000000))
        icesum_extent = '{0:,}'.format(round(self.CSVExtent[-1] * 1000000))
        
        cmap = copy.copy(plt.colormaps["jet"])
        cmap.set_bad('black',0.6)
        
        year = self.Cdate.year
        month = self.Cdate.strMonth
        day = self.Cdate.strDay
        self.fig, self.ax = plt.subplots(figsize=(6, 8))
        self.ax.clear()
        if self.mode == 'past':
            self.ax.set_title(f'Date: {year}-{month}-{day}', fontsize=11)
        elif self.mode == 'max':
            self.ax.set_title(f'NSIDC Combined High SIC: {month}-{day}', fontsize=11)
        elif self.mode == 'min':
            self.ax.set_title(f'NSIDC Combined Low SIC: {month}-{day}', fontsize=11)
        
        self.cax = self.ax.imshow(icemap*100, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        
        plt.axis('off')
        self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100],fraction=0.03,pad=-0.10,anchor=(0,0.85)).set_label('Ice concentration in %')
        
        self.ax.text(160, 8, r'cryospherecomputing.com', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        
        self.ax.text(160, 360, f'Area {icesum_area} km\N{SUPERSCRIPT TWO}', fontsize=11,color='white')
        self.ax.text(160, 370, f'Extent {icesum_extent} km\N{SUPERSCRIPT TWO}', fontsize=11,color='white')
        
        self.fig.tight_layout(pad=-1)

        self.fig.subplots_adjust(left=0.02,bottom=-0.02,right=0.88)
        
        if self.mode == 'past':
            self.fig.savefig(f'temp/past/NSIDC_{year}{month}{day}_north.png')
        elif self.mode == 'max':
            self.fig.savefig(f'temp/max/NSIDC_Max_{month}{day}_north.png')
        elif self.mode == 'min':
            self.fig.savefig(f'temp/min/NSIDC_Min_{month}{day}_north.png')
        # plt.pause(0.01)
        plt.close()
    
    def anomalyshow(self,icemap,icesum):
        '''displays sea ice anomaly data'''
        icemap = icemap.reshape(448, 304)
        icemap = np.ma.masked_greater(icemap, 1)
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        self.ax2.clear()
        self.ax2.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
        
        cmap2 = copy.copy(plt.colormaps["coolwarm_r"])
        cmap2.set_bad('black',0.6)
        
        self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
        self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-0.5, vmax=0.5, cmap=cmap2)
        
        self.ax2.axes.get_yaxis().set_ticks([])
        self.ax2.axes.get_xaxis().set_ticks([])
        self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(-0.04, 0.48, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
        self.fig2.tight_layout(pad=1)
        self.fig2.subplots_adjust(left=0.05)
        #self.fig2.savefig('Animation/MaxofMax_anom'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
        #self.fig2.savefig('Animation/MaxofMax_anom'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
        plt.pause(0.01)
    
        
        
    def exportdata(self,dataset):
        filepath = '/home/nico/Cryoscripts/NSIDC/temp/'
        CryoIO.csv_columnexport(f'{filepath}NSIDC_Area_{dataset}.csv',
            [self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])
                
    
for year in range (2010,2023):
    action = NSIDC_area(year)
    action.dayloop()


if __name__ == "__main__":
    print('main')
    # action = NSIDC_area()
    # action.dayloop()
#     action.exportdata('00-19')



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