from multiprocessing import Pool
import numpy as np
import CryoIO

import time

class AWP_calc:

    def __init__ (self):
        
        self.iceMJ = 0.15
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
        
#        self.maskview(self.regmaskf)
#        plt.show()
        
        
    def initRegions(self):
         self.AWP_D_init = []
         self.AWP_A_init = []
         self.AWP_Area_init = []
         
         for x in range(0,len(self.regions_A)):
             self.AWP_D_init.append([])
             self.AWP_A_init.append([])
             self.AWP_Area_init.append([])
             
    def appendregion(self):
         for x in range(0,len(self.regions_A)):
             regionA = np.sum(self.AWP_A_init[x])
             regionD = np.sum(self.AWP_D_init[x])
             regionArea = np.sum(self.AWP_Area_init[x])
             self.regions_A[x].append(round(regionA/regionArea,3))
             self.regions_D[x].append(round(regionD/regionArea,3))
         
         self.initRegions()
        
    def dayloop(self,year=2023):
        '''for loop to load binary data files and pass them to the calculation function
        '''
        self.Cdate = CryoIO.CryoDate(year,9,22)
        self.daycount = 181 # 181 southern summer
        filepath = '../DataFiles/'
        AWPdaily = np.zeros(len(self.regmaskf), dtype=float)
        AWPcumulative = np.zeros(len(self.regmaskf), dtype=float)

        for count in range (0,self.daycount,1):
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            filename = f'{year}/NSIDC_{year}{month}{day}_south.npz'
            filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}_south.npz'
            
            #loads data file
            ice = CryoIO.readnumpy(f'{filepath}{filename}')/250
            iceMean = CryoIO.readnumpy(f'{filepath}{filenameMean}')/250
            
            #calculate the map
            aaa = np.vectorize(self.energycalc)
            AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(
                    count,ice,iceMean,AWPcumulative,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
            
            #append pan Arctic lists
            self.datum.append('{}/{}/{}'.format(year,month,day))
            self.Daily_all_regions.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
            self.Accu_all_regions.append (round(np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea),3))
            
            self.appendregion()
            print(year ,month, day)
            self.Cdate.datecalc()
        
        end = time.time()
        print(end-self.starttime)
        
        # year = 'icefree'
        self.export_data(year)
        CryoIO.savenumpy(f'AWP/final_data/AWP_energy_{year}_south.npz',AWPcumulative)
        
        
    def energycalc(self,count,ice,iceMean,AWPcumulative,icemask,regmaskf,areamask,latmask):
        '''AWP energy calculation & Regional breakdown'''
        AWPdaily_areaweighted = np.nan
        AWPdaily_oceanarea = np.nan
        AWPcumulative_areaweighted = np.nan
        AWPcumulative_oceanarea = np.nan
        
        if regmaskf < 7:
            if ice == 1.02: #value for missing data
                ice = iceMean
            pixlat = min(-40,latmask)
            indexx = int(round((pixlat+40)*(-5)))
            MJ = self.latitudelist[indexx][count+1]
            AWPdaily = ((1-ice) * MJ) + self.iceMJ * MJ * ice
            AWPcumulative = AWPcumulative + AWPdaily
            if icemask == 1:
                AWPdaily_areaweighted = AWPdaily * areamask
                AWPdaily_oceanarea = areamask
                AWPcumulative_areaweighted = AWPcumulative * areamask
                AWPcumulative_oceanarea = areamask
                
                if regmaskf == 2:
                    self.AWP_D_init[0].append (AWPdaily_areaweighted)
                    self.AWP_A_init[0].append (AWPcumulative_areaweighted)
                    self.AWP_Area_init[0].append(areamask)
                elif regmaskf == 3:
                    self.AWP_D_init[1].append (AWPdaily_areaweighted)
                    self.AWP_A_init[1].append (AWPcumulative_areaweighted)
                    self.AWP_Area_init[1].append(areamask)
                elif regmaskf == 4:
                    self.AWP_D_init[2].append (AWPdaily_areaweighted)
                    self.AWP_A_init[2].append (AWPcumulative_areaweighted)
                    self.AWP_Area_init[2].append(areamask)
                elif regmaskf == 5:
                    self.AWP_D_init[3].append (AWPdaily_areaweighted)
                    self.AWP_A_init[3].append (AWPcumulative_areaweighted)
                    self.AWP_Area_init[3].append(areamask)
                elif regmaskf == 6:
                    self.AWP_D_init[4].append (AWPdaily_areaweighted)
                    self.AWP_A_init[4].append (AWPcumulative_areaweighted)
                    self.AWP_Area_init[4].append(areamask)
                    
        else:
            AWPdaily = 9999.9
            AWPcumulative = 9999.9
            
        return AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea

    def export_data(self,year):
        CryoIO.csv_columnexport(f'AWP/csv/_AWP_{year}_south.csv',
                [self.datum,self.Daily_all_regions,self.Accu_all_regions])
        CryoIO.csv_columnexport(f'AWP/csv/_AWP_regional_{year}_south.csv',self.regions_A)
        CryoIO.csv_columnexport(f'AWP/csv/_AWP_regional_daily_{year}_south.csv',self.regions_D)

    
    
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
#     p = Pool(processes=22)
#     data = p.map(spawnprocess, yearlist)
#     p.close()
# =============================================================================



action = AWP_calc()
action.dayloop(2020)


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