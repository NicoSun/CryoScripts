'''
NOAA Daily Snow Extent / Ice Extent Data


array size: 247500 (550:450)
'''
from multiprocessing import Pool
import numpy as np
import CryoIO

class NOAA_Snow_Cover:


    def __init__  (self):
        self.threads = 20
        
        self.masksload()
        self.init_regionlists()
                
    def init_regionlists(self):
        self.NorthAmericaExtent = [['Greenland','Eastern Canada','Central Canada','Canadian Rockies','Northern Canada',
                    'Alaska','US NE','US SE','US MidWest','US SW','US Pacific','US Rockies']]
        self.EuropeExtent = [['North Europe','West Europe','Central Europe','Southern Europe','Eastern Europe']]
        self.AsiaExtent = [['East Siberia','Central Siberia','West Siberia','Central Asia',
                'Central Mountain Asia','Eastern Asia','Tibet','Western Asia','Persia']]

        
    def masksload(self):
        
        filename = '../Masks/Pixel_area_crop.msk'
        self.pixelarea = CryoIO.openfile(filename,np.uint16)
        
        filename = '../Masks/SubRegion_Mask.msk'
        self.SubRegion_Mask = CryoIO.openfile(filename,np.uint8)


    def listclear(self):
        '''define lists for regional calculation'''
            
        #AWP lists
            
        self.Eastern_Canada_calc = []
        self.Central_Canada_calc = []
        self.Rockies_Canada_calc = []
        self.Northern_Canada_calc = []
        self.Alaska_calc = []
        self.US_NE_calc = []
        self.US_SE_calc = []
        self.US_MW_calc = []
        self.US_SW_calc = []
        self.US_Pacific_calc = []
        self.US_Rocki_calc = []
            
        self.Greenland_calc = []
            
        self.Scandinavia_calc = []
        self.West_Europe_calc = []
        self.Cent_Europe_calc = []
        self.South_Europe_calc = []
        self.East_Europe_calc = []
            
        self.East_sib_calc = []
        self.Cent_sib_calc = []
        self.West_sib_calc = []
        self.Cent_Asia_calc = []
        self.Mount_Asia_calc = []
        self.East_Asia_calc = []
        self.Tibet_calc = []
        self.West_Asia_calc = []
        self.Persia_calc = []
        

        
    def listsappend(self):
        '''adds area corrected AWP to main lists'''
        NorthAmerica = [sum(self.Greenland_calc),sum(self.Eastern_Canada_calc),sum(self.Central_Canada_calc),sum(self.Rockies_Canada_calc),
                sum(self.Northern_Canada_calc),sum(self.Alaska_calc),sum(self.US_NE_calc),sum(self.US_SE_calc),
                sum(self.US_MW_calc),sum(self.US_SW_calc),sum(self.US_Pacific_calc),sum(self.US_Rocki_calc)]
        Europe = [sum(self.Scandinavia_calc),sum(self.West_Europe_calc),sum(self.Cent_Europe_calc),
            sum(self.South_Europe_calc),sum(self.East_Europe_calc)]
        Asia = [sum(self.East_sib_calc),sum(self.Cent_sib_calc),sum(self.West_sib_calc),sum(self.Cent_Asia_calc),sum(self.Mount_Asia_calc),
          sum(self.East_Asia_calc),sum(self.Tibet_calc),sum(self.West_Asia_calc),sum(self.Persia_calc)]
        return NorthAmerica,Europe,Asia
        

        
        
    def dayloop(self):
        for year in range(2020,2023):
            print(year)
            filename_list = []
            date_list = []
            self.init_regionlists()
            
            for day_of_year in range (1,366): #366
                stringday = str(day_of_year).zfill(3)
                filename = f'../DataFiles/{year}/NOAA_{year}{stringday}_24km.npz'
                filename_list.append(filename)
                date_list.append('{}_{}'.format(year,stringday))
            
            p = Pool(processes=self.threads)
            data = p.map(self.threaded, (filename_list))
            p.close()
            print(len(data))
            for value in data:
                self.NorthAmericaExtent.append (value[0])
                self.EuropeExtent.append (value[1])
                self.AsiaExtent.append (value[2])
            self.export_data(year)

            
    def threaded(self,filename):
        
        snow = CryoIO.readnumpy(filename)
        
        self.listclear()
        aaa = np.vectorize(self.regional_extent)
        execution = aaa(snow,self.SubRegion_Mask,self.pixelarea)

        NorthAmerica,Europe,Asia = self.listsappend()
        return NorthAmerica,Europe,Asia
        
    def regional_extent(self,snow,subregmask,areamask):
        if snow ==4:
            if subregmask == 50:
                self.Greenland_calc.append(areamask)
            #North America Regions
            elif subregmask == 10:
                self.Eastern_Canada_calc.append(areamask)
            elif subregmask == 12:
                self.Central_Canada_calc.append(areamask)
            elif subregmask == 16:
                self.Northern_Canada_calc.append(areamask)
            elif subregmask == 18:
                self.Rockies_Canada_calc.append(areamask)
            elif subregmask == 20:
                self.Alaska_calc.append(areamask)
            elif subregmask == 21:
                self.US_NE_calc.append(areamask)
            elif subregmask == 22:
                self.US_SE_calc.append(areamask)
            elif subregmask == 23:
                self.US_MW_calc.append(areamask)
            elif subregmask == 24:
                self.US_SW_calc.append(areamask)
            elif subregmask == 25:
                self.US_Pacific_calc.append(areamask)
            elif subregmask == 26:
                self.US_Rocki_calc.append(areamask)
            #Asia regions
            elif subregmask == 30:
                self.East_sib_calc.append(areamask)
            elif subregmask == 31:
                self.Cent_sib_calc.append(areamask)
            elif subregmask == 32:
                self.West_sib_calc.append(areamask)
            elif subregmask == 33:
                self.Cent_Asia_calc.append(areamask)
            elif subregmask == 34: #Central Mountain Asia
                self.Mount_Asia_calc.append(areamask)
            elif subregmask == 35: # Eastern Asia
                self.East_Asia_calc.append(areamask)
            elif subregmask == 36:
                self.Tibet_calc.append(areamask)
            elif subregmask == 37:
                self.West_Asia_calc.append(areamask)
            elif subregmask == 38:
                self.Persia_calc.append(areamask)
            #European regions
            elif subregmask == 40:
                self.Scandinavia_calc.append(areamask)
            elif subregmask == 42:
                self.West_Europe_calc.append(areamask)
            elif subregmask == 44:
                self.Cent_Europe_calc.append(areamask)
            elif subregmask == 46:
                self.South_Europe_calc.append(areamask)
            elif subregmask == 48:
                self.East_Europe_calc.append(areamask)
        return 


    def export_data(self,year):
        '''writes data to a csv files'''
        
        CryoIO.csv_rowexport(f'../CSVexport/raw/{year}_Regional_extent_NorthAmerica.csv',self.NorthAmericaExtent)
        CryoIO.csv_rowexport(f'../CSVexport/raw/{year}_Regional_extent_Europe.csv',self.EuropeExtent)
        CryoIO.csv_rowexport(f'../CSVexport/raw/{year}_Regional_extent_Asia.csv',self.AsiaExtent)

        
if __name__ == "__main__":
    action = NOAA_Snow_Cover()
#    action.viewloop()
#    action.masksload()
    action.dayloop()
#    action.export_data()
