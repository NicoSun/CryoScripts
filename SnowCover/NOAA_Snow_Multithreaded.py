'''
NOAA Daily Snow Extent / Ice Extent Data


array size: 247500 (550:450)
'''
from multiprocessing import Pool
import numpy as np
import CryoIO

class NOAA_Snow_Cover:


    def __init__  (self):
        self.threads = 8
        
        self.plottype = 'daily' # daily ,  mask
        self.dailyorcumu()
        self.masksload()
        self.mode = 'Mean'
        
        self.CSVDatum = ['Date']
        self.IceExtent = ['IceExtent']
        self.NorthAmericaExtent =['NorthAmericaExtent']
        self.GreenlandExtent =['GreenlandExtent']
        self.EuropeExtent =['EuropeExtent']
        self.AsiaExtent =['AsiaExtent']
        
        
    def masksload(self):
    
        filename = '../Masks/Pixel_area_crop.msk'
        self.pixelarea = CryoIO.openfile(filename,np.uint16)
        
        filename = '../Masks/Region_Mask.msk'
        self.regionmask = CryoIO.openfile(filename,np.uint8)
        
        filename = '../Masks/Latitude_Mask.msk'
        self.Latitude_Mask = CryoIO.openfile(filename,'float32')

            
        
    def dayloop(self):
        filename_list = []
        filename_listmean = []
        for year in range(2019,2020):
            for day_of_year in range (1,366): #366
                stringday = str(day_of_year).zfill(3)
#                filenameMean = '../DataFiles/Mean/NOAA_Mean_{}_24km.npz'.format(stringday)
#                filenameMax = '../DataFiles/Max/NOAA_Max_{}_24km.npz'.format(str(day_of_year).zfill(3))
                filename = '../Datafiles/{}/NOAA_{}{}_24km.npz'.format(year,year,stringday)
                filename_list.append(filename)
#                filename_listmean.append(filenameMean)
                self.CSVDatum.append('{}_{}'.format(year,stringday))
            
            
            
#        print(filename_list)
        p = Pool(processes=self.threads)
        data = p.map(self.threaded, filename_list)
        p.close()
        
        for value in data:
            self.IceExtent.append (value[0]/1e6)
            self.NorthAmericaExtent.append (value[1]/1e6)
            self.GreenlandExtent.append (value[2]/1e6)
            self.EuropeExtent.append (value[3]/1e6)
            self.AsiaExtent.append (value[4]/1e6)
            
        CryoIO.csv_columnexport('temp/NRT_extent_data.csv',
            [self.CSVDatum,self.IceExtent,self.NorthAmericaExtent,self.GreenlandExtent,self.EuropeExtent,self.AsiaExtent])

            
    def threaded(self,filename):
        
#        snowMean = CryoIO.openfile(filenameMean,np.float16)
        snow = CryoIO.readnumpy(filename)
            
            
        aaa = np.vectorize(self.calculateExtent)
        iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent = aaa(snow,self.regionmask,self.pixelarea)

        return np.sum(iceextent),np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)
        

    def calculateExtent(self,icemap,regionmask,pixelarea):
        iceextent = 0
        NorthAmericaExtent = 0
        GreenlandExtent = 0
        EuropeExtent = 0
        AsiaExtent = 0
#        iceanomaly = icemap-icemean
        
        if icemap==3:
            iceextent = pixelarea
        if regionmask==3 and icemap==4:
            NorthAmericaExtent = pixelarea
        if regionmask==4 and icemap==4:
            GreenlandExtent = pixelarea
        if regionmask==5 and icemap==4:
            EuropeExtent = pixelarea
        if regionmask==6 and icemap==4:
            AsiaExtent = pixelarea
    
        return iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent
        
        
if __name__ == "__main__":
    action = NOAA_Snow_Cover()
    # action.masksload()
#     action.dayloop()
#    action.writetofile()
#    