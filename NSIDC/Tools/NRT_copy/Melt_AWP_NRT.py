import numpy as np
import pandas
import CryoIO
from datetime import date
from datetime import timedelta

class Melt_AWP_NRT:

    def __init__ (self):
        
        self.iceMJ = 0.2
        self.initRegions()
        self.labelfont = {'fontname':'Arial'}
        self.masksload()
        self.webpath = '/var/www/Cryoweb'
        

    def masksload(self):
        '''Loads regionmask, pixel area mask, latitudemask and
        AWP values for southern latitudes
        '''
        
        filename = '/home/nico/Cryoscripts/NSIDC/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = '/home/nico/Cryoscripts/NSIDC/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
        filename= '/home/nico/Cryoscripts/NSIDC/Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.int32)/100000
        
        filename = '/home/nico/Cryoscripts/NSIDC/Masks/Max_AWP_extent.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
            
        self.latitudelist = np.loadtxt('/home/nico/Cryoscripts/NSIDC/Masks/Lattable_MJ.csv', delimiter=',')
        self.co2list = np.loadtxt('/home/nico/Cryoscripts/NSIDC/Masks/Global_CO2_forecast.csv', delimiter=',')
        self.DMI_temp = np.loadtxt('/home/nico/Cryoscripts/NSIDC/Masks/DMI_Temp_80N.csv', delimiter=',')
        
        self.DMI_temp = self.DMI_temp[79:] # start 20th March
        
#        self.maskview(self.Icemask)
#        plt.show()
        
    def dayloop(self):
        
        self.loadMeandata()
        self.AWPcumulative_map = np.zeros(len(self.regmaskf), dtype=float)
        self.AWPcumulative_EJ = np.zeros(len(self.regmaskf), dtype=float)
#        self.AWPanomaly_acumu = np.zeros(len(self.regmaskf), dtype=float)
        
        loopday = date(2023,3, 20)
        self.year = loopday.year
        self.stringmonth = str(loopday.month).zfill(2)
        self.stringday = str(loopday.day).zfill(2)
        for count in range (1,187): #120, 187
            print(self.year ,self.stringmonth, self.stringday)
            self.daycalc(count,loopday.month-1)
#            self.createmaps(count)
            loopday = loopday+timedelta(days=1)
            self.year = loopday.year
            self.stringmonth = str(loopday.month).zfill(2)
            self.stringday = str(loopday.day).zfill(2)
#            
        self.export_data()
        self.createmaps()
        
    def initRegions(self):
        
        self.CSVDatum = ['Date']
        self.CSVDaily = ['Daily EJ']
        self.CSVAccu = ['Accumulated EJ']
        
        self.CSVDaily_central = ['Central Daily EJ']
        self.CSVAccu_central = ['Central Accumulated EJ']
        
        self.SoO = ['Sea of Okhotsk']
        self.Bers = ['Bering Sea']
        self.HB = ['Hudson Bay']
        self.BB = ['Baffin Bay']
        self.EG = ['East Greenland Sea']
        self.BaS = ['Barents Sea']
        self.KS = ['Kara Sea']
        self.LS = ['Laptev Sea']
        self.ES = ['East Siberian Sea']
        self.CS = ['Chukchi Sea']
        self.BeaS = ['Beaufort Sea']
        self.CA = ['Canadian Archipelago']
        self.AB = ['Central Arctic']
        
        self.SoO_daily = ['Sea of Okhotsk']
        self.Bers_daily = ['Bering Sea']
        self.HB_daily = ['Hudson Bay']
        self.BB_daily = ['Baffin Bay']
        self.EG_daily = ['East Greenland Sea']
        self.BaS_daily = ['Barents Sea']
        self.KS_daily = ['Kara Sea']
        self.LS_daily = ['Laptev Sea']
        self.ES_daily = ['East Siberian Sea']
        self.CS_daily = ['Chukchi Sea']
        self.BeaS_daily = ['Beaufort Sea']
        self.CA_daily = ['Canadian Archipelago']
        self.AB_daily = ['Central Arctic']
        
    def clearRegionLists(self):
        self.SoO_daily_calc = []
        self.SoO_calc = []
        self.Bers_daily_calc = []
        self.Bers_calc = []
        self.HB_daily_calc = []
        self.HB_calc = []
        self.BB_daily_calc = []
        self.BB_calc = []
        self.EG_daily_calc = []
        self.EG_calc = []
        self.BaS_daily_calc = []
        self.BaS_calc = []
        self.KS_daily_calc = []
        self.KS_calc = []
        self.LS_daily_calc = []
        self.LS_calc = []
        self.ES_daily_calc = []
        self.ES_calc = []
        self.CS_daily_calc = []
        self.CS_calc = []
        self.BeaS_daily_calc = []
        self.BeaS_calc = []
        self.CA_daily_calc = []
        self.CA_calc = []
        self.AB_daily_calc = []
        self.AB_calc = []
        
    def appendRegionLists(self):
        #append regional lists
        self.SoO.append (round(np.sum(self.SoO_calc),0)/1e6)
        self.Bers.append (round(np.sum(self.Bers_calc),0)/1e6)
        self.HB.append (round(np.sum(self.HB_calc),0)/1e6)
        self.BB.append (round(np.sum(self.BB_calc),0)/1e6)
        self.EG.append (round(np.sum(self.EG_calc),0)/1e6)
        self.BaS.append (round(np.sum(self.BaS_calc),0)/1e6)
        self.KS.append (round(np.sum(self.KS_calc),0)/1e6)
        self.LS.append (round(np.sum(self.LS_calc),0)/1e6)
        self.ES .append (round(np.sum(self.ES_calc),0)/1e6)
        self.CS.append (round(np.sum(self.CS_calc),0)/1e6)
        self.BeaS.append (round(np.sum(self.BeaS_calc),0)/1e6)
        self.CA.append (round(np.sum(self.CA_calc),0)/1e6)
        self.AB.append (round(np.sum(self.AB_calc),0)/1e6)
    
        #append daily regional lists
        self.SoO_daily.append (round(np.sum(self.SoO_daily_calc),0)/1e6)
        self.Bers_daily.append (round(np.sum(self.Bers_daily_calc),0)/1e6)
        self.HB_daily.append (round(np.sum(self.HB_daily_calc),0)/1e6)
        self.BB_daily.append (round(np.sum(self.BB_daily_calc),0)/1e6)
        self.EG_daily.append (round(np.sum(self.EG_daily_calc),0)/1e6)
        self.BaS_daily.append (round(np.sum(self.BaS_daily_calc),0)/1e6)
        self.KS_daily.append (round(np.sum(self.KS_daily_calc),0)/1e6)
        self.LS_daily.append (round(np.sum(self.LS_daily_calc),0)/1e6)
        self.ES_daily.append (round(np.sum(self.ES_daily_calc),0)/1e6)
        self.CS_daily.append (round(np.sum(self.CS_daily_calc),0)/1e6)
        self.BeaS_daily.append (round(np.sum(self.BeaS_daily_calc),0)/1e6)
        self.CA_daily.append (round(np.sum(self.CA_daily_calc),0)/1e6)
        self.AB_daily.append (round(np.sum(self.AB_daily_calc),0)/1e6)
        
    def appendCentalArctic(self):
        #create a single central Arctic list from regions
        central_arctic_daily = [np.sum(self.AB_daily_calc),np.sum(self.CA_daily_calc),np.sum(self.BeaS_daily_calc),np.sum(self.CS_daily_calc),
                    np.sum(self.ES_daily_calc),np.sum(self.LS_daily_calc),np.sum(self.KS_daily_calc)]
        
        
        central_arctic = [np.sum(self.AB_calc),np.sum(self.CA_calc),np.sum(self.BeaS_calc),np.sum(self.CS_calc),np.sum(self.ES_calc),
                        np.sum(self.LS_calc),np.sum(self.KS_calc)]
        
        #append central Arctic Lists
        self.CSVDaily_central.append (int(np.nansum(central_arctic_daily))/1e6)
        self.CSVAccu_central.append  (int(np.nansum(central_arctic))/1e6)
        
        
    def daycalc(self,DayofYear,month):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        AWPdaily_map = np.zeros(len(self.regmaskf), dtype=float)

        filepath = '/home/nico/Cryoscripts/NSIDC/DataFiles/'
        filename = f'{filepath}/{self.year}/NSIDC_{self.year}{self.stringmonth}{self.stringday}.npz'
        filenameMean = f'{filepath}/Mean_00_19/NSIDC_Mean_{self.stringmonth}{self.stringday}.bin'
            
        ice = CryoIO.readnumpy(filename)/250
        iceMean = CryoIO.openfile(filenameMean,np.uint8)/250
        
        #338ppm base value in 1980
        co2listindex = (self.year-1980)*12 + month
        co2value =  self.co2list[co2listindex][1]
        co2_adjust = (0.43+co2value**0.9/300)
        
            
        self.back_radiation = (((0.000000056703*self.DMI_temp[DayofYear]**4)*0.25)*0.0864)/co2_adjust
#        print(self.back_radiation)
        
        #define lists for regional area calculation
        self.clearRegionLists()
            
        #calculate the map
        aaa = np.vectorize(self.energycalc)
        self.AWPdaily_map,self.AWPcumulative_map,self.AWPdaily_EJ,self.AWPcumulative_EJ = aaa(
                DayofYear,ice,iceMean,AWPdaily_map,self.AWPcumulative_map,self.AWPcumulative_EJ,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
            

        #append pan Arctic lists
        self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
        self.CSVDaily.append ((np.nansum(self.AWPdaily_EJ))/1e6)
        self.CSVAccu.append ((np.nansum(self.AWPcumulative_EJ))/1e6)
        
        #append central Arctic
        self.appendCentalArctic()
        #append Regions
        self.appendRegionLists()
        
        
    def energycalc(self,count,ice,iceMean,AWPdaily_map,AWPcumulative_map,AWPcumulative_EJ,icemask,regmaskf,areamask,latmask):
        '''AWP energy calculation & Regional breakdown'''
        AWPdaily_EJ = 0
        
        if regmaskf < 2:
            AWPdaily_map = 0.0
            AWPcumulative_map = 0.0
        
        elif regmaskf > 16:
            AWPdaily_map = -1
            AWPcumulative_map = -1
        
        elif icemask == 1:
            AWPdaily_map = 0.0
            AWPcumulative_map = AWPcumulative_map
            
            if ice == 1.02: #value for missing data
                ice = iceMean
            if ice > 0.25:
                pixlat = max(40,latmask)
                indexx = int(round((pixlat-40)*5))
                MJ = self.latitudelist[indexx][count+1]
                AWPdaily_MJ = ((1-ice) * MJ) + self.iceMJ * MJ * ice - self.back_radiation
                
                
                AWPdaily_map = AWPdaily_MJ * areamask
                AWPcumulative_map = AWPcumulative_map + AWPdaily_map
                
                AWPdaily_EJ = AWPdaily_map
                AWPcumulative_EJ += AWPdaily_map
                self.regioncalc(regmaskf,AWPdaily_map,AWPcumulative_map)
                
            elif ice <= 0.25:
                AWPdaily_map = 0
                AWPcumulative_map = AWPcumulative_map
                self.regioncalc(regmaskf,AWPdaily_map,AWPcumulative_map)
                
            
        return AWPdaily_map,AWPcumulative_map,AWPdaily_EJ,AWPcumulative_EJ
        

    def regioncalc(self,regmaskf,AWPdaily_areaweighted,AWPcumulative_areaweighted):
        if regmaskf == 2:
            self.SoO_daily_calc.append  (AWPdaily_areaweighted)
            self.SoO_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 3:
            self.Bers_daily_calc.append  (AWPdaily_areaweighted)
            self.Bers_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 4:
            self.HB_daily_calc.append  (AWPdaily_areaweighted)
            self.HB_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 6:
            self.BB_daily_calc.append  (AWPdaily_areaweighted)
            self.BB_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 7:
            self.EG_daily_calc.append  (AWPdaily_areaweighted)
            self.EG_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 8:
            self.BaS_daily_calc.append  (AWPdaily_areaweighted)
            self.BaS_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 9:
            self.KS_daily_calc.append  (AWPdaily_areaweighted)
            self.KS_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 10:
            self.LS_daily_calc.append  (AWPdaily_areaweighted)
            self.LS_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 11:
            self.ES_daily_calc.append  (AWPdaily_areaweighted)
            self.ES_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 12:
            self.CS_daily_calc.append  (AWPdaily_areaweighted)
            self.CS_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 13:
            self.BeaS_daily_calc.append  (AWPdaily_areaweighted)
            self.BeaS_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 14:
            self.CA_daily_calc.append  (AWPdaily_areaweighted)
            self.CA_calc.append  (AWPcumulative_areaweighted)
        elif regmaskf == 15:
            self.AB_daily_calc.append  (AWPdaily_areaweighted)
            self.AB_calc.append  (AWPcumulative_areaweighted)
        
        
    def createmaps(self):
        import Melt_AWP_Graphs_NRT
        datestring = '{}-{}-{}'.format(self.year,self.stringmonth,self.stringday)
        
        Melt_AWP_Graphs_NRT.action.IceMelt_NRT(self.AWPdaily_map,self.CSVDaily[-1],datestring)
        Melt_AWP_Graphs_NRT.action.IceMelt_NRT_accu(self.AWPcumulative_map,self.CSVAccu[-1],datestring)
        Melt_AWP_Graphs_NRT.action.automated(self.year,datestring)

                
    def export_data(self):
        CryoIO.csv_columnexport(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT.csv',
                [self.CSVDatum,self.CSVDaily,self.CSVAccu,self.CSVDaily_central,self.CSVAccu_central])
        CryoIO.csv_columnexport(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional.csv',
                [self.CSVDatum,self.SoO,self.Bers,self.HB,self.BB,self.EG,self.BaS,
                self.KS,self.LS,self.ES,self.CS,self.BeaS,self.CA,self.AB])
        CryoIO.csv_columnexport(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional_daily.csv',
                [self.CSVDatum,self.SoO_daily,self.Bers_daily,self.HB_daily,self.BB_daily,self.EG_daily,self.BaS_daily,self.KS_daily,
                 self.LS_daily,self.ES_daily,self.CS_daily,self.BeaS_daily,self.CA_daily,self.AB_daily])
        
        #save binary accumulative files
        CryoIO.savebinaryfile(f'{self.webpath}/Melt_AWP/Arctic_IceMelt_Accu.bin',self.AWPcumulative_map)
        CryoIO.savebinaryfile(f'{self.webpath}/Melt_AWP/Arctic_IceMelt_EJ.bin',self.AWPcumulative_EJ)

    
    def loadNRTdata (self):
        Yearcolnames = ['Date','B','C','D','E']
        Yeardata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT.csv', names=Yearcolnames)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVDaily = Yeardata.B.tolist()
        self.CSVAccu = Yeardata.C.tolist()
        self.CSVDaily_central = Yeardata.D.tolist()
        self.CSVAccu_central = Yeardata.E.tolist()
        
    def loadMeandata (self):
        AWP_mean = ['A','B','C','D']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_mean.csv', names=AWP_mean)
        self.AWP_Daily_mean = Climatedata.A.tolist()
        self.AWP_Accu_mean = Climatedata.B.tolist()

    
    
    def loadCSVRegiondata (self):
        Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional.csv', names=Yearcolnames)
        self.SoO = Yeardata.Sea_of_Okhotsk.tolist()
        self.Bers = Yeardata.Bering_Sea.tolist()
        self.HB = Yeardata.Hudson_Bay.tolist()
        self.BB = Yeardata.Baffin_Bay.tolist()
        self.EG = Yeardata.East_Greenland_Sea.tolist()
        self.BaS = Yeardata.Barents_Sea.tolist()
        self.KS = Yeardata.Kara_Sea.tolist()
        self.LS = Yeardata.Laptev_Sea.tolist()
        self.ES = Yeardata.East_Siberian_Sea.tolist()
        self.CS = Yeardata.Chukchi_Sea.tolist()
        self.BeaS = Yeardata.Beaufort_Sea.tolist()
        self.CA = Yeardata.Canadian_Archipelago.tolist()
        self.AB = Yeardata.Central_Arctic.tolist()
        
        Yearcolnames_daily = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata_daily = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily)
        self.SoO_daily = Yeardata_daily.Sea_of_Okhotsk.tolist()
        self.Bers_daily = Yeardata_daily.Bering_Sea.tolist()
        self.HB_daily = Yeardata_daily.Hudson_Bay.tolist()
        self.BB_daily = Yeardata_daily.Baffin_Bay.tolist()
        self.EG_daily = Yeardata_daily.East_Greenland_Sea.tolist()
        self.BaS_daily = Yeardata_daily.Barents_Sea.tolist()
        self.KS_daily = Yeardata_daily.Kara_Sea.tolist()
        self.LS_daily = Yeardata_daily.Laptev_Sea.tolist()
        self.ES_daily = Yeardata_daily.East_Siberian_Sea.tolist()
        self.CS_daily = Yeardata_daily.Chukchi_Sea.tolist()
        self.BeaS_daily = Yeardata_daily.Beaufort_Sea.tolist()
        self.CA_daily = Yeardata_daily.Canadian_Archipelago.tolist()
        self.AB_daily = Yeardata_daily.Central_Arctic.tolist()
    
    
    def automated (self,year,month,stringday):
        self.year = year
        self.stringmonth = str(month).zfill(2)
        self.stringday = stringday
        
        print(self.year,self.stringmonth,self.stringday)
        self.loadNRTdata()
        self.loadMeandata()
        self.loadCSVRegiondata()
        self.DayofYear = len(self.CSVDaily)
        
        #load accumulative files
        self.AWPcumulative_map = CryoIO.openfile(f'{self.webpath}/Melt_AWP/Arctic_IceMelt_Accu.bin',np.float)
        self.AWPcumulative_EJ = CryoIO.openfile(f'{self.webpath}/Melt_AWP/Arctic_IceMelt_EJ.bin',np.float)
        
#        print(self.AWP_Daily_mean[index])
        self.daycalc(self.DayofYear,month)
        self.export_data()
        self.createmaps()


action = Melt_AWP_NRT()
    

    
if __name__ == '__main__':
#    action.automated(2019,7,'17')
    action.dayloop()
#     action.export_data()
    


'''
#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

Region mask
0: Lakes
1: Ocean
2: Sea of Okhotsk
3: Bering Sea
4: Hudson Bay
5: St Lawrence
6: Baffin Bay
7: East Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Archipelago
15: Central Arctic
20: Land
21: Coast

Max Ice Extent:
0: Ocean
1: Ice
2: Land
3: Coast
'''