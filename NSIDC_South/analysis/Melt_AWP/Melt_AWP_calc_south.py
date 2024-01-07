from multiprocessing import Pool
import numpy as np
import CryoIO

import time

class AWP_calc:

    def __init__ (self):
        
        self.iceMJ = 0.2
        self.datum = ['Date']
        
        self.Daily_all_regions = ['Daily MJ/m2']
        self.Accu_all_regions = ['Accumulated MJ/m2']
        
        self.regions_D = [['Weddel_Sea'], ['Indian_Ocean'], ['Pacific_Ocean'], ['Ross_Sea'], ['Bell_Amun_Sea']]
        self.regions_A = [['Weddel_Sea'], ['Indian_Ocean'], ['Pacific_Ocean'], ['Ross_Sea'], ['Bell_Amun_Sea']]
        
        self.masksload()
        self.initRegions()
        
        self.starttime = time.time()
        

    def masksload(self):
        '''Loads regionmask, pixel area mask, latitudemask and
        AWP values for southern latitudes
        '''
        
        filename = '../Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)
        
        filename = '../Masks/pss25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
        filename = '../Masks/pss25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.int32)/100000
        
        filename = '../Masks/Max_AWP_extent_south.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        #latitudes [-40 to -80, step = 0.2]
        self.latitudelist = np.loadtxt('../Masks/Lattable_south_MJ.csv', delimiter=',')
        self.co2list = np.loadtxt('../Masks/Global_CO2.csv', delimiter=',')
        self.DMI_temp = np.loadtxt('../Masks/Melt_AWP_Temp.csv', delimiter=',')
        
        
    def initRegions(self):
         self.AWP_D_init = []
         self.AWP_A_init = []
         
         for x in range(0,len(self.regions_A)):
             self.AWP_D_init.append([])
             self.AWP_A_init.append([])
             
    def appendregion(self):
         for x in range(0,len(self.regions_A)):
             regionA = np.sum(self.AWP_A_init[x])/1E3
             regionD = np.sum(self.AWP_D_init[x])/1E3
             self.regions_A[x].append(round(regionA,0))
             self.regions_D[x].append(round(regionD,0))
         
         self.initRegions()
        
    def dayloop(self,year=2023):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        self.Cdate = CryoIO.CryoDate(year,9,22)
        self.daycount = 181 # 181 southern summer
        filepath = '../DataFiles/'
        AWPcumulative_map = np.zeros(len(self.regmaskf), dtype=float)
        AWPcumulative_EJ = 0.0

        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            filename = f'{year}/NSIDC_{year}{month}{day}_south.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}_south.npz'
            
            #loads data file
            ice = CryoIO.readnumpy(f'{filepath}{filename}')/250
            iceMean = CryoIO.readnumpy(f'{filepath}{filenameMean}')/250
            
            #338ppm base value in 1980
            co2listindex = (year-1979)*12 + self.Cdate.month-1
            co2value =  self.co2list[co2listindex][1]
            co2_adjust = (0.55+co2value**0.88/333) # 300ppm = 1, 420pp = 1.15
            
            self.back_radiation = ((0.000000056703*self.DMI_temp[count]**4)*0.025)/co2_adjust
            print(self.back_radiation)
            
            #calculate the map
            aaa = np.vectorize(self.energycalc)
            AWPcumulative_map,AWPdaily_EJ = aaa(count,ice,iceMean,AWPcumulative_map,
                self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
            
            #append pan Arctic lists
            self.datum.append('{}/{}/{}'.format(year,month,day))
            Daily_EJ = np.nansum(AWPdaily_EJ)/1e6
            AWPcumulative_EJ += Daily_EJ
            
            self.Daily_all_regions.append (Daily_EJ)
            self.Accu_all_regions.append (AWPcumulative_EJ)
            
            self.appendregion()
            print(year ,month, day)
            self.Cdate.datecalc()
        
        end = time.time()
        print(end-self.starttime , ' seconds')
        
# =============================================================================
#         self.export_data(year)
#         CryoIO.savenumpy(f'Melt_AWP/final_data/Melt_AWP_energy_{year}_south.npz',AWPcumulative_map)
# =============================================================================
        
        
    def energycalc(self,count,ice,iceMean,AWPcumulative_map,icemask,regmaskf,areamask,latmask):
        '''AWP energy calculation & Regional breakdown'''
        AWPdaily_EJ = 0
        
        if icemask == 1:
            AWPdaily_map = 0.0
            
            if ice == 1.02: #value for missing data
                ice = iceMean
            
            if ice > 0.25:
                pixlat = min(-40,latmask)
                indexx = int(round((pixlat+40)*(-5)))
                MJ = self.latitudelist[indexx][count+1]
                AWPdaily_MJ = ((1-ice) * MJ) + self.iceMJ * MJ * ice - self.back_radiation
                
                
                AWPdaily_map = AWPdaily_MJ * areamask
                AWPcumulative_map += AWPdaily_map
                
                AWPdaily_EJ = AWPdaily_map

            if regmaskf == 2:
                self.AWP_D_init[0].append (AWPdaily_map)
                self.AWP_A_init[0].append (AWPcumulative_map)
            elif regmaskf == 3:
                self.AWP_D_init[1].append (AWPdaily_map)
                self.AWP_A_init[1].append (AWPcumulative_map)
            elif regmaskf == 4:
                self.AWP_D_init[2].append (AWPdaily_map)
                self.AWP_A_init[2].append (AWPcumulative_map)
            elif regmaskf == 5:
                self.AWP_D_init[3].append (AWPdaily_map)
                self.AWP_A_init[3].append (AWPcumulative_map)
            elif regmaskf == 6:
                self.AWP_D_init[4].append (AWPdaily_map)
                self.AWP_A_init[4].append (AWPcumulative_map)
                    
        else:
            AWPdaily_map = 0.0
        
        if regmaskf > 8:
            AWPdaily_map = -1
            AWPcumulative_map = -1
            
        return AWPcumulative_map,AWPdaily_EJ

    def export_data(self,year):
        CryoIO.csv_columnexport(f'Melt_AWP/csv/Melt_AWP_{year}_south.csv',
                [self.datum,self.Daily_all_regions,self.Accu_all_regions])
        CryoIO.csv_columnexport(f'Melt_AWP/csv/Melt_AWP_regional_{year}_south.csv',self.regions_A)
        CryoIO.csv_columnexport(f'Melt_AWP/csv/Melt_AWP_regional_daily_{year}_south.csv',self.regions_D)

    
    
# =============================================================================
# def spawnprocess(year):
#     action = AWP_calc()
#     data = action.dayloop(year)
#     
#     return data
#     
# if __name__ == '__main__':
#     yearlist = []
#     for year in range(1979,2023):
#         yearlist.append(year)
#     
#     p = Pool(processes=23)
#     data = p.map(spawnprocess, yearlist)
#     p.close()
# =============================================================================



action = AWP_calc()
action.dayloop(2022)


'''
#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

arraylength: 104912 (332, 316)

Pixel Value    Antarctic Region
2    Weddell Sea
3    Indian Ocean
4    Pacific Ocean
5    Ross Sea
6    Bellingshausen Amundsen Sea
11    Land
12    Coast

Max Ice Extent:
0: Ocean
1: Ice
2: Land
3: Coast
'''