'''
NOAA Daily Snow Extent / Ice Extent Data
array size: 247500 (550:450)
'''

import numpy as np
import matplotlib.pyplot as plt
import CryoIO


class NOAA_Snow_Cover:


    def __init__  (self):
        self.masksload()
        self.createMap()
        
        self.CSVDatum = ['Date']
        self.IceExtent = ['IceExtent']
        self.NorthAmericaExtent =['NorthAmericaExtent']
        self.GreenlandExtent =['GreenlandExtent']
        self.EuropeExtent =['EuropeExtent']
        self.AsiaExtent =['AsiaExtent']
        
        
    def masksload(self):
        '''Loads regionmask and pixel area mask
        '''
        filename = 'Masks/Pixel_area_crop.msk'
        self.pixelarea = CryoIO.openfile(filename,np.uint16)
        
        filename = 'Masks/Region_Mask.msk'
        self.regionmask = CryoIO.openfile(filename,np.uint8)

        filename = 'Masks/Coastmask.msk'
        self.coastmask = CryoIO.openfile(filename,np.uint8)

        

    def calculateExtent(self,snowmap,regionmask,pixelarea):
        ''' calculates the day-month for a 366 day year'''
        iceextent = 0
        NorthAmericaExtent = 0
        GreenlandExtent = 0
        EuropeExtent = 0
        AsiaExtent = 0
        
        if snowmap==3:
            iceextent = pixelarea
        if regionmask==3 and snowmap==4:
            NorthAmericaExtent = pixelarea
        if regionmask==4 and snowmap==4:
            GreenlandExtent = pixelarea
        if regionmask==5 and snowmap==4:
            EuropeExtent = pixelarea
        if regionmask==6 and snowmap==4:
            AsiaExtent = pixelarea
    
        return iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent
        
        
    def createmap(self,snowmap,snowextent,iceextent):
        '''displays snow cover data'''
        snowmap = snowmap.reshape(610,450)
        map1 = np.ma.masked_outside(snowmap,-0.5,2.5) # Land -> Water
        map2 = np.ma.masked_outside(snowmap,2.5,4.5) # Ice -> Snow
        
        cmap = plt.cm.ocean_r
        cmap2 = plt.cm.Greys
        
        self.ax.clear()
        self.ax.text(0.46, 0.01, 'cryospherecomputing.com', fontsize=11,color='white',transform=self.ax.transAxes)
        self.ax.text(0.80, 0.01, 'Map: Nico Sun', fontsize=11,color='white',transform=self.ax.transAxes)
        
        self.ax.text(0.65, 0.28, 'Ice extent: '+'{:,}'.format(iceextent)+' 'r'$km^2$', fontsize=11,color='white',transform=self.ax.transAxes)
        self.ax.text(0.65, 0.26, 'Snow extent: '+'{:,}'.format(snowextent)+' 'r'$km^2$', fontsize=11,color='white',transform=self.ax.transAxes)
        
        self.ax.set_title('NOAA / NSIDC IMS Snow & Ice Extent      {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay),x=0.5)
        self.ax.set_ylabel('Data source: nsidc.org/data/g02156',y=0.15)
        
        self.ax.imshow(map1, interpolation='nearest', vmin=0, vmax=2, cmap=cmap) # Water & Land
        self.ax.imshow(map2, interpolation='nearest', vmin=3, vmax=5, cmap=cmap2) #Snow & Ice
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        self.fig.tight_layout(pad=0.5)
        self.fig.savefig('temp/past/NOAA_Snowmap_{}{}{}.png'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
#         plt.draw()
#         plt.close()
        
    
    def createMap(self):
        '''creates separate figures for sea ice data'''
        self.fig, self.ax = plt.subplots(figsize=(8, 10))
    
    def dayloop(self):
        '''function to automate parts of the monthly update procedure'''
        self.Cdate = CryoIO.CryoDate(1998,1,1)
        
        for year in range(1998,2023):
            for day_of_year in range (1,366): #366
                stringday = str(day_of_year).zfill(3)
                filename = f'DataFiles/{year}/NOAA_{year}{stringday}_24km.npz'
                snow_map = CryoIO.readnumpy(filename)
                
                aaa = np.vectorize(self.calculateExtent)
                iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent = aaa(snow_map,self.regionmask,self.pixelarea)

                data = [np.sum(iceextent),np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)]
                snowextent= np.sum(data[1:])
                iceextent= np.sum(data[0])
                
                self.CSVDatum.append('{}_{}'.format(year,stringday))
                self.IceExtent.append (data[0]/1e6)
                self.NorthAmericaExtent.append (data[1]/1e6)
                self.GreenlandExtent.append (data[2]/1e6)
                self.EuropeExtent.append (data[3]/1e6)
                self.AsiaExtent.append (data[4]/1e6)
                
                if self.Cdate.day == 1 or self.Cdate.day == 15:
                    self.createmap(snow_map,snowextent,iceextent)
                    print('{}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
                self.Cdate.datecalc()

                
        # CryoIO.csv_columnexport('SnowCover.csv',
        #     [self.CSVDatum,self.IceExtent,self.NorthAmericaExtent,self.GreenlandExtent,self.EuropeExtent,self.AsiaExtent])
                
        # plt.show()





action = NOAA_Snow_Cover()
if __name__ == "__main__":
    
    action.dayloop()
#    action.extentdata()
#    action.writetofile()
#
'''
region_coding
1: Ocean
3: North America
4: Greenland
5: Europe
6: Asia
'''

'''
snowmap encoding
1: Ocean
2: Land
3: Ice
4: Snow
'''