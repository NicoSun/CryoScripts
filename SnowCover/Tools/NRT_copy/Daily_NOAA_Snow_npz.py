'''
NOAA Daily Snow Extent / Ice Extent Data
array size: 247500 (550:450)
'''

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import matplotlib.pyplot as plt
import pandas
import CryoIO
import copy


class NOAA_Snow_Cover:


    def __init__  (self):
        self.year = 2018
        self.day_of_year = 50
        self.webpath = '/var/www/Cryoweb'
        
        self.masksload()
        
        self.CSVDatum = ['Date']
        self.IceExtent = ['IceExtent']
        self.NorthAmericaExtent =['NorthAmericaExtent']
        self.GreenlandExtent =['GreenlandExtent']
        self.EuropeExtent =['EuropeExtent']
        self.AsiaExtent =['AsiaExtent']
        
        
    def masksload(self):
        '''Loads regionmask and pixel area mask
        '''
        filename = '/home/nico/Cryoscripts/SnowCover/Masks/Pixel_area_crop.msk'
        self.pixelarea = CryoIO.openfile(filename,np.uint16)
        
        filename = '/home/nico/Cryoscripts/SnowCover/Masks/Region_Mask.msk'
        self.regionmask = CryoIO.openfile(filename,np.uint8)

        filename = '/home/nico/Cryoscripts/SnowCover/Masks/Coastmask.msk'
        self.coastmask = CryoIO.openfile(filename,np.uint8)

        filename = '/home/nico/Cryoscripts/SnowCover/Masks/Latitude_Mask.msk'
        self.Latitude_Mask = CryoIO.openfile(filename,'float32')

        
    def load_days(self):
        '''load binary data files and pass them to the calculation function
        '''
        self.stringday = str(self.day_of_year).zfill(3)
        filenameMean = '/home/nico/Cryoscripts/SnowCover/DataFiles/Mean/NOAA_Mean_{}_24km.npz'.format(self.stringday)
        filename = '/home/nico/Cryoscripts/SnowCover/DataFiles/npz/NOAA_{}{}_24km.npz'.format(self.year,self.stringday)
        
        if self.day_of_year == 1:
            self.stringday2 = 365
            filenameyesterday = '/home/nico/Cryoscripts/SnowCover/DataFiles/npz/NOAA_{}{}_24km.npz'.format(self.year-1,self.stringday2)
        else:
            self.stringday2 = str(self.day_of_year-1).zfill(3)
            filenameyesterday = '/home/nico/Cryoscripts/SnowCover/DataFiles/npz/NOAA_{}{}_24km.npz'.format(self.year,self.stringday2)
            
        snowMean = CryoIO.readnumpy(filenameMean)
        snow_map = CryoIO.readnumpy(filename)
        snowy = CryoIO.readnumpy(filenameyesterday)
            
        aaa = np.vectorize(self.calculateExtent)
        iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent,snowanomaly_map,snowchange = aaa(snow_map,self.regionmask,self.pixelarea,snowMean,snowy)

        data = [np.sum(iceextent),np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)]
        snowextent= np.sum(data[1:])
        iceextent= np.sum(data[0])
        
        self.CSVDatum.append('{}_{}'.format(self.year,self.stringday))
        self.IceExtent.append (data[0]/1e6)
        self.NorthAmericaExtent.append (data[1]/1e6)
        self.GreenlandExtent.append (data[2]/1e6)
        self.EuropeExtent.append (data[3]/1e6)
        self.AsiaExtent.append (data[4]/1e6)
        
        for x,y in enumerate(snowanomaly_map):
            if self.coastmask[x]==3:
                snowanomaly_map[x]=3
            if snowchange[x]==-2:
                snow_map[x]=6
            if snowchange[x]==2:
                snow_map[x]=7
        
        snowanomaly_value = snowextent - self.MSnow
        iceanomaly_value = iceextent - self.MSeaIce
        
        self.createmap(snow_map,snowextent,iceextent)
        self.create_anolamy_map(snowanomaly_map,snowanomaly_value,iceanomaly_value)
        

    def calculateExtent(self,snowmap,regionmask,pixelarea,snowMean,snowy):
        ''' calculates the day-month for a 366 day year'''
        iceextent = 0
        NorthAmericaExtent = 0
        GreenlandExtent = 0
        EuropeExtent = 0
        AsiaExtent = 0
        snowanomaly = snowmap-snowMean/10
        snowchange = snowmap - snowy
        
        if snowmap==3:
            iceextent = pixelarea
            snowanomaly = (snowmap-1)-snowMean/10
        if snowmap==2:
            snowanomaly = (snowmap+1)-snowMean/10
        if regionmask==3 and snowmap==4:
            NorthAmericaExtent = pixelarea
        if regionmask==4 and snowmap==4:
            GreenlandExtent = pixelarea
        if regionmask==5 and snowmap==4:
            EuropeExtent = pixelarea
        if regionmask==6 and snowmap==4:
            AsiaExtent = pixelarea
    
        return iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent,snowanomaly,snowchange
        
        
    def createmap(self,snowmap,snowextent,iceextent):
        '''displays snow cover data'''
        snowmap = snowmap.reshape(610,450)
        map1 = np.ma.masked_outside(snowmap,-0.5,2.5) # Land -> Water
        map2 = np.ma.masked_outside(snowmap,2.5,4.5) # Ice -> Snow
        map3 = np.ma.masked_outside(snowmap,6,7) # Snow extent gain/loss
        
        fig, ax = plt.subplots(figsize=(8, 10))
        cmap = plt.cm.ocean_r
        cmap2 = plt.cm.Greys
        cmap3 = plt.cm.RdBu
        
        ax.clear()
        ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='white',transform=ax.transAxes)
        ax.text(0.66, 0.03, 'Ice extent: '+'{:,}'.format(iceextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
        ax.text(0.66, 0.01, 'Snow extent: '+'{:,}'.format(snowextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
        
        ax.text(0.62, -0.02, 'Snow cover gain', fontsize=10,color='blue',transform=ax.transAxes)
        ax.text(0.82, -0.02, 'Snow cover loss', fontsize=10,color='red',transform=ax.transAxes)
        
        ax.set_title('NOAA / NSIDC IMS Snow & Ice Extent      {}-{}-{}'.format(self.year,self.month,self.day),x=0.5)
        ax.set_xlabel('cryospherecomputing.com',x=0.25)
        ax.set_ylabel('Data source: nsidc.org/data/g02156',y=0.15)
        
        ax.imshow(map1, interpolation='nearest', vmin=0, vmax=2, cmap=cmap) # Water & Land
        ax.imshow(map2, interpolation='nearest', vmin=3, vmax=5.5, cmap=cmap2) #Snow & Ice
        ax.imshow(map3, interpolation='nearest', vmin=5.6, vmax=7.4, cmap=cmap3) # Snow gain/loss
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        plt.tight_layout(pad=1)
        fig.savefig(f'{self.webpath}/Snow_Cover_Data/NOAA_Snowmap.png')
        fig.savefig('{}/Snow_Cover_Data/Images/Extent/NOAA_Snowmap_normal_{}.png'.format(self.webpath,str(self.day_of_year).zfill(3)))
        plt.draw()
        plt.close()
        
    def create_anolamy_map(self,snowmap,snowanomaly,iceanomaly):
        '''displays snow cover anomaly data'''
        snowmap = np.ma.masked_greater(snowmap, 2)
        snowmap = snowmap.reshape(610,450)
        snowmap = snowmap*100
        
        fig_anom, ax = plt.subplots(figsize=(8, 10))
        cmap_anom = copy.copy(plt.colormaps["RdBu"])
        #cmap_anom = plt.cm.RdBu
        cmap_anom.set_bad('black',0.8)
        ax.clear()
        
        ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='black',transform=ax.transAxes)
        ax.text(0.6, 0.05, 'Ice anomaly: '+'{:,}'.format(iceanomaly)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
        ax.text(0.6, 0.03, 'Snow anomaly: '+'{:,}'.format(snowanomaly)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)

        
        ax.set_title('NOAA / NSIDC IMS Snow & Ice Extent Anomaly      {}-{}-{}'.format(self.year,self.month,self.day),x=0.5)
        ax.set_xlabel('cryospherecomputing.com',x=0.25)
        ax.set_ylabel('Data source: nsidc.org/data/g02156',y=0.15)

        ax.text(1.02, 0.02, 'Snow cover anomaly in percent (Base 2000-2019)',
            transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
        axins1  = inset_axes(ax, width="5%", height="25%", loc=4)
        im1 = ax.imshow(snowmap, interpolation='nearest', vmin=-100, vmax=100, cmap=cmap_anom)
        
        
        plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[-100,0,+100])
        axins1.yaxis.set_ticks_position("left")
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        plt.tight_layout(pad=1)
        
        fig_anom.savefig(f'{self.webpath}/Snow_Cover_Data/NOAA_Snowmap_anomaly.png')
        fig_anom.savefig('{}/Snow_Cover_Data/Images/Anomaly/NOAA_Snowmap_anomaly_{}.png'.format(self.webpath,str(self.day_of_year).zfill(3)))
        plt.close()
        

    def loadCSVdata(self,doy):
        '''loads NRT data'''
        #NRT Data
        Yearcolnames = ['Date', 'IceExtent', 'NorthAmericaExtent','GreenlandExtent','EuropeExtent','AsiaExtent']
        Yeardata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/NRT_extent_data.csv', names=Yearcolnames)
        self.CSVDatum = Yeardata.Date.tolist()
        self.IceExtent = Yeardata.IceExtent.tolist()
        self.NorthAmericaExtent = Yeardata.NorthAmericaExtent.tolist()
        self.GreenlandExtent = Yeardata.GreenlandExtent.tolist()
        self.EuropeExtent = Yeardata.EuropeExtent.tolist()
        self.AsiaExtent = Yeardata.AsiaExtent.tolist()
        
        #Mean value Data
        Meancolnames = ['Date','SeaIce', 'NorthAmerica', 'Greenland', 'Europe', 'Asia']
        Meandata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/Mean_extents.csv', names=Meancolnames,header=0)
        MSeaIce = Meandata.SeaIce.tolist()
        MAmerica = Meandata.NorthAmerica.tolist()
        MGreenland = Meandata.Greenland.tolist()
        MEurope = Meandata.Europe.tolist()
        MAsia = Meandata.Asia.tolist()
        
        self.MSeaIce = int(MSeaIce[doy]*1e6)
        self.MSnow = int((MAmerica[doy] + MGreenland[doy] + MEurope[doy] + MAsia[doy])*1E6)
        
    def data_exort(self):
        CryoIO.csv_columnexport(f'{self.webpath}/Snow_Cover_Data/NRT_extent_data.csv',
            [self.CSVDatum,self.IceExtent,self.NorthAmericaExtent,self.GreenlandExtent,self.EuropeExtent,self.AsiaExtent])
        
        
    def dayloop(self,year,lastday):
        
        # turn off maps for speedup
        self.MSnow = 5e5
        self.MSeaIce = 5e5
        
        self.year = year
        for xxx in range (2,lastday+1):
            self.day_of_year = xxx
            self.load_days()
            print(xxx)
            
        self.data_exort()
        
    def automated(self,year,month,day,dayofyear):
        '''function to automate parts of the monthly update procedure'''
        self.year = year
        self.month =str(month).zfill(2)
        self.day = str(day).zfill(2)
        self.day_of_year = dayofyear

        self.loadCSVdata(self.day_of_year-1)
        self.load_days()
        
        self.data_exort()
        plt.show()



action = NOAA_Snow_Cover()
if __name__ == "__main__":
    
    action.automated(2023,9,28,270)
#     action.extentdata()
    # action.dayloop(2023,268)
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