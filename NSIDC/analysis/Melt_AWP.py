from multiprocessing import Pool
import numpy as np
import CryoIO

import time

class Melt_AWP_calc:

    def __init__ (self):
        
        self.iceMJ = 0.2
        self.datum = ['Date']

        self.Daily_all_regions = ['Daily MJ/m2']
        self.Accu_all_regions = ['Accumulated MJ/m2']
        
        self.regions_D = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
                    , ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
                    , ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
        self.regions_A = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
                    , ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
                    , ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
        
        self.Daily_central_regions = ['Daily MJ/m2']
        self.Accu_central_regions = ['Accumulated MJ/m2']
        
        self.masksload()
        self.initRegions()
    
        self.starttime = time.time()

    def masksload(self):
        filename = '../Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = '../Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
        filename= '../Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = '../Masks/Max_AWP_extent.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        self.latitudelist = np.loadtxt('../Masks/Lattable_MJ.csv', delimiter=',')
        self.co2list = np.loadtxt('../Masks/Global_CO2.csv', delimiter=',')
        self.DMI_temp = np.loadtxt('../Masks/DMI_Temp_80N.csv', delimiter=',')
        
        self.DMI_temp = self.DMI_temp[79:] # start 20th March

        
    def initRegions(self):
        self.AWP_D_init = []
        self.AWP_A_init = []
        
        for x in range(0,len(self.regions_A)):
            self.AWP_D_init.append([])
            self.AWP_A_init.append([])
            
    def appendregion(self):
        central_arctic_daily = 0
        central_arctic = 0
        
        for x in range(0,len(self.regions_A)):
            regionA = np.sum(self.AWP_A_init[x])/1E6
            regionD = np.sum(self.AWP_D_init[x])/1E6
            self.regions_A[x].append(round(regionA,0))
            self.regions_D[x].append(round(regionD,0))
            
            if x > 5: # only count region after Barents Sea
                central_arctic += regionA
                central_arctic_daily += regionD
        
        self.Accu_central_regions.append(round(central_arctic,0))
        self.Daily_central_regions.append(round(central_arctic_daily,0))
        
        self.initRegions()
        
        
    def dayloop(self,year=2023):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        self.Cdate = CryoIO.CryoDate(year,3,20)
        self.daycount = 187 # 187summer
        filepath = '../DataFiles/'
        AWPdaily_map = np.zeros(len(self.regmaskf), dtype=float)
        AWPcumulative_map = np.zeros(len(self.regmaskf), dtype=float)
        AWPcumulative_EJ = np.zeros(len(self.regmaskf), dtype=float)


        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            filename = f'{year}/NSIDC_{year}{month}{day}.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}.npz'
            
            #loads data file
            ice = CryoIO.readnumpy(f'{filepath}{filename}')/250
            iceMean = CryoIO.readnumpy(f'{filepath}{filenameMean}')/250
            
            #338ppm base value in 1980
            co2listindex = (year-1979)*12 + self.Cdate.month-1
            co2value =  self.co2list[co2listindex][1]
            co2_adjust = (0.43+co2value**0.9/300)
                
            self.back_radiation = (((0.000000056703*self.DMI_temp[count]**4)*0.25)*0.0864)/co2_adjust
            
            #calculate the map
            aaa = np.vectorize(self.energycalc)
            AWPdaily_map,AWPcumulative_map,AWPdaily_EJ,AWPcumulative_EJ = aaa(
                    count,ice,iceMean,AWPdaily_map,AWPcumulative_map,AWPcumulative_EJ,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
            
            #append pan Arctic lists
            self.datum.append('{}/{}/{}'.format(year,month,day))
            self.Daily_all_regions.append ((np.nansum(AWPdaily_EJ))/1e6)
            self.Accu_all_regions.append ((np.nansum(AWPcumulative_EJ))/1e6)
            
            #append Regions
            self.appendregion()
            print(year ,month, day)
            self.Cdate.datecalc()
            
        end = time.time()
        print(end-self.starttime)
        self.export_data()
        CryoIO.savenumpy(f'Melt_AWP/final_data/Melt_AWP_energy_{year}.npz',AWPcumulative_map)

        
#        plt.show()
        
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
            self.AWP_D_init[0].append (AWPdaily_areaweighted)
            self.AWP_A_init[0].append (AWPcumulative_areaweighted)
        elif regmaskf == 3:
            self.AWP_D_init[1].append (AWPdaily_areaweighted)
            self.AWP_A_init[1].append (AWPcumulative_areaweighted)
        elif regmaskf == 4:
            self.AWP_D_init[2].append (AWPdaily_areaweighted)
            self.AWP_A_init[2].append (AWPcumulative_areaweighted)
        elif regmaskf == 6:
            self.AWP_D_init[3].append (AWPdaily_areaweighted)
            self.AWP_A_init[3].append (AWPcumulative_areaweighted)
        elif regmaskf == 7:
            self.AWP_D_init[4].append (AWPdaily_areaweighted)
            self.AWP_A_init[4].append (AWPcumulative_areaweighted)
        elif regmaskf == 8:
            self.AWP_D_init[5].append (AWPdaily_areaweighted)
            self.AWP_A_init[5].append (AWPcumulative_areaweighted)
        elif regmaskf == 9:
            self.AWP_D_init[6].append (AWPdaily_areaweighted)
            self.AWP_A_init[6].append (AWPcumulative_areaweighted)
        elif regmaskf == 10:
            self.AWP_D_init[7].append (AWPdaily_areaweighted)
            self.AWP_A_init[7].append (AWPcumulative_areaweighted)
        elif regmaskf == 11:
            self.AWP_D_init[8].append (AWPdaily_areaweighted)
            self.AWP_A_init[8].append (AWPcumulative_areaweighted)
        elif regmaskf == 12:
            self.AWP_D_init[9].append (AWPdaily_areaweighted)
            self.AWP_A_init[9].append (AWPcumulative_areaweighted)
        elif regmaskf == 13:
            self.AWP_D_init[10].append (AWPdaily_areaweighted)
            self.AWP_A_init[10].append (AWPcumulative_areaweighted)
        elif regmaskf == 14:
            self.AWP_D_init[11].append (AWPdaily_areaweighted)
            self.AWP_A_init[11].append (AWPcumulative_areaweighted)
        elif regmaskf == 15:
            self.AWP_D_init[12].append (AWPdaily_areaweighted)
            self.AWP_A_init[12].append (AWPcumulative_areaweighted)
        
    
    def export_data(self):
        CryoIO.csv_columnexport(f'Melt_AWP/csv/_melt_AWP_{self.Cdate.year}.csv',
                [self.datum,self.Daily_all_regions,self.Accu_all_regions,self.Daily_central_regions,self.Accu_central_regions])
        CryoIO.csv_columnexport(f'Melt_AWP/csv/_melt_AWP_regional_{self.Cdate.year}.csv',self.regions_A)
        CryoIO.csv_columnexport(f'Melt_AWP/csv/_melt_AWP_regional_daily_{self.Cdate.year}.csv',self.regions_D)

    
def spawnprocess(year):
    action = Melt_AWP_calc()
    data = action.dayloop(year)
    
    return data
    
if __name__ == '__main__':
    yearlist = []
    for year in range(1979,2001):
        yearlist.append(year)
    
    p = Pool(processes=22)
    data = p.map(spawnprocess, yearlist)
    p.close()
    

# action = Melt_AWP_calc()
# action.dayloop(2000)


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