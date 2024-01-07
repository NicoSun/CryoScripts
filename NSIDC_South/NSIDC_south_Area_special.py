import numpy as np
import csv
import matplotlib.pyplot as plt
import CryoIO


class NSIDC_area_south:

    def __init__  (self,year=2022):
        self.Cdate = CryoIO.CryoDate(year,1,1) # initilizes a 366 day year
        self.root = './'
        self.daycount = 366 #366year, 186summer
        
        self.CSVDatum = ['Date']
        self.CSVArea =['Area']
        self.CSVExtent = ['Extent']
        self.CSVCompaction = ['Compaction']
        
        self.masksload()

        

    def masksload(self):
        '''Loads regionmask and pixel area mask
        option to display masks is commented out
        '''
        filename = 'Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)

        filename = 'Masks/pss25area_v3.dat'
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
            # filenameMax = f'Max/NSIDC_Max_{month}{day}_south.npz'
            # filenameMin = f'Min/NSIDC_Min_{month}{day}_south.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}_south.npz'
            
            
            #loads data file
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

            if day == '01' or day == '15':
                self.normalshow(icemap_new)
                print(year,month,day)
                 
            self.Cdate.datecalc()
        plt.show()
                
                
                    
    def calculateAreaExtent(self,icemap,iceaveragef,areamask,regionmask):
        '''area & extent calculation & remove lake ice'''
        area = 0
        extent = 0
        icemap_new = icemap
        areaanomaly = 0
        icemapanomaly = 1.1
        
        if regionmask < 10:
            icemapanomaly = icemap - iceaveragef
            if 0.15 <= icemap <=1:
                area = icemap*areamask
                extent = areamask
            if icemap > 1:
                icemapanomaly = 1.1
            if icemap <=1 and icemapanomaly <=1:
                    areaanomaly = icemapanomaly*areamask
                
        return icemap_new,icemapanomaly,area,extent,areaanomaly
        
    def maskview(self,icemap):
        '''displays loaded masks'''
        icemap = icemap.reshape(332, 316)
        plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=10, cmap=plt.cm.jet)

                

    def normalshow(self,icemap):        
        icemap = np.ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(332, 316)
        icemap = icemap[0:310,20:316]
        icesum_area = '{0:,}'.format(round(self.CSVArea[-1] * 1000000))
        icesum_extent = '{0:,}'.format(round(self.CSVExtent[-1] * 1000000))
        
        cmap = plt.cm.jet
        cmap.set_bad('black',0.6)
        
        year = self.Cdate.year
        month = self.Cdate.strMonth
        day = self.Cdate.strDay
        
        self.fig, self.ax = plt.subplots(figsize=(7.8,8))
        self.ax.clear()
        # self.ax.set_title(f'NSIDC Combined Min SIC: {month}-{day}', fontsize=11) #Maximum of Maxima, Minimum of Minima
        self.ax.set_title(f'Date: {year}-{month}-{day}', fontsize=11)
        self.cax = self.ax.imshow(icemap*100, interpolation='nearest', vmin=0, vmax=100,cmap=cmap)
        self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100],fraction=0.03,pad=-0.58,anchor=(0,0.36)).set_label('Ice concentration in %')

        
        plt.axis('off')
        self.ax.text(210, 8, r'cryospherecomputing.com', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
        self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        
        self.ax.text(88, 170, f'Area {icesum_area} km\N{SUPERSCRIPT TWO}', fontsize=11,color='white')
        self.ax.text(88, 180, f'Extent {icesum_extent} km\N{SUPERSCRIPT TWO}', fontsize=11,color='white')
        
        self.fig.tight_layout(pad=-1)
        self.fig.subplots_adjust(left=0.02,bottom=-0.02,right=0.63)
        self.fig.savefig(f'temp/past/NSIDC_{year}{month}{day}_south.png')
        # plt.pause(0.01)
        plt.close()
        
    def anomalyshow(self,icemap,icesum):        
        icemap = icemap.reshape(332, 316)
        icesum = round(icesum,3)
        self.ax2.clear()
        self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
        cmap2 = plt.cm.coolwarm_r
        cmap2.set_bad('black',0.6)
        self.ax2.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
        self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-0.75, vmax=0.75, cmap=cmap2)
        
        self.ax2.axes.get_yaxis().set_ticks([])
        self.ax2.axes.get_xaxis().set_ticks([])
        self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.fig2.tight_layout(pad=1)
        #self.fig2.savefig('Animation/MaxofMax_anom'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
        plt.pause(0.01)    
        
        
    def exportdata(self):
        filename = f"{self.year-1}.csv" # self.name
        CryoIO.csv_columnexport(filename, [self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])

for year in range (1979,2023):
    action = NSIDC_area_south(year)
    action.dayloop()
        

if __name__ == "__main__":
    print('main')
    action = NSIDC_area_south()
    action.dayloop()
    # action.exportdata()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA