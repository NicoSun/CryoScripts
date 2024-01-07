import numpy as np
import pandas
import CryoIO
import matplotlib.pyplot as plt

from datetime import date
from datetime import timedelta

class AWP_calc_daily:

    def __init__ (self):
        self.webpath = '/var/www/Cryoweb'
        self.iceMJ = 0.15
        # self.labelfont = {'fontname':'Arial'}
        self.masksload()
        self.dailyorcumu()
        self.initRegions()


    def masksload(self):
        '''Loads regionmask, pixel area mask, latitudemask and
        AWP values for southern latitudes
        '''
        
        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)
        
        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/pss25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
        
        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/pss25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.int32)/100000
        
        filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/Max_AWP_extent_south.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        #latitudes [-40 to -80, step = 0.2]
        self.latitudelist = np.loadtxt('/home/nico/Cryoscripts/NSIDC_South/Masks/Lattable_south_MJ.csv', delimiter=',')
        
#        self.maskview(self.latmaskf)
#        plt.show()
        
    def maskview(self,icemap):
        '''displays loaded masks'''
        icemap = icemap.reshape(332, 316)
        plt.imshow(icemap, interpolation='nearest', vmin=-90, vmax=40, cmap=plt.colormaps['jet'])
        
    def initRegions(self):
        self.CSVDatum = ['Date']
        self.CSVDaily = ['Daily MJ/m2']
        self.CSVCumu = ['Accumulated MJ/m2']
        
        self.Wed = ['Weddel Sea']
        self.Ind = ['Indian Ocean']
        self.Pac = ['Pacific Ocean']
        self.Ross = ['Ross Sea']
        self.Bell = ['Bell-Amun Sea']
        
        self.Wed_daily = ['Weddel Sea Daily']
        self.Ind_daily = ['Indian Ocean']
        self.Pac_daily = ['Pacific Ocean']
        self.Ross_daily = ['Ross Sea']
        self.Bell_daily = ['Bell-Amun Sea']
        
    def clearRegionLists(self):
        #define lists for regional area calculation
        self.Wed_calc = []
        self.Ind_calc = []
        self.Pac_calc = []
        self.Ross_calc = []
        self.Bel_calc = []
        
        self.Wed_daily_calc = []
        self.Ind_daily_calc = []
        self.Pac_daily_calc = []
        self.Ross_daily_calc = []
        self.Bel_daily_calc = []
        
        self.Wed_area = []
        self.Ind_area = []
        self.Pac_area = []
        self.Ross_area = []
        self.Bel_area = []
        
    def appendRegionLists(self):
        #append regional lists
        self.Wed.append  (round((np.sum(self.Wed_calc)/np.sum(self.Wed_area)),3))
        self.Ind.append  (round((np.sum(self.Ind_calc)/np.sum(self.Ind_area)),3))
        self.Pac.append  (round((np.sum(self.Pac_calc)/np.sum(self.Pac_area)),3))
        self.Ross.append  (round((np.sum(self.Ross_calc)/np.sum(self.Ross_area)),3))
        self.Bell.append  (round((np.sum(self.Bel_calc)/np.sum(self.Bel_area)),3))
        
        #append daily regional lists
        self.Wed_daily.append  (round((np.sum(self.Wed_daily_calc)/np.sum(self.Wed_area)),3))
        self.Ind_daily.append  (round((np.sum(self.Ind_daily_calc)/np.sum(self.Ind_area)),3))
        self.Pac_daily.append  (round((np.sum(self.Pac_daily_calc)/np.sum(self.Pac_area)),3))
        self.Ross_daily.append  (round((np.sum(self.Ross_daily_calc)/np.sum(self.Ross_area)),3))
        self.Bell_daily.append  (round((np.sum(self.Bel_daily_calc)/np.sum(self.Bel_area)),3))
        
    def dayloop(self):
        
        self.loadMeandata()
        self.AWPcumulative = np.zeros(len(self.regmaskf), dtype=float)
        self.AWPanomaly_acumu = np.zeros(len(self.regmaskf), dtype=float)
        
        loopday = date(2023, 9, 22)
        self.year = loopday.year
        self.stringmonth = str(loopday.month).zfill(2)
        self.stringday = str(loopday.day).zfill(2)
        for count in range (1,7): # 182 Antarctic summer (because start at 1)
            print(self.year ,self.stringmonth, self.stringday)
            self.daycalc(count)
        
            loopday = loopday+timedelta(days=1)
            self.year = loopday.year
            self.stringmonth = str(loopday.month).zfill(2)
            self.stringday = str(loopday.day).zfill(2)
        self.save_data()
        self.createMaps(count)
        
    def daycalc(self,DayofYear):
        '''for loop to load binary data files and pass them to the calculation function
        '''

#         filename = '/home/nico/Cryoscripts/NSIDC_South/DataFiles/{}/NSIDC_{}{}{}_south.bin'.format(self.year,self.year,self.stringmonth,self.stringday)
        filename = f'/home/nico/Cryoscripts/NSIDC_South/DataFiles/{self.year}/NSIDC_{self.year}{self.stringmonth}{self.stringday}_south.npz'
        filenameMean = f'/home/nico/Cryoscripts/NSIDC_South/DataFiles/Mean_00_19/NSIDC_Mean_{self.stringmonth}{self.stringday}_south.bin'
        
#         ice = CryoIO.openfile(filename,np.uint8)/250
        ice = CryoIO.readnumpy(filename)/250
        iceMean = CryoIO.openfile(filenameMean,np.uint8)/250
        
        self.clearRegionLists()
#        print(DayofYear)
        #calculate the map
        aaa = np.vectorize(self.energycalc)
        self.AWPdaily,self.AWPcumulative,self.AWPanomaly,self.AWPanomaly_acumu,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(DayofYear,ice,
            iceMean,self.AWPcumulative,self.AWPanomaly_acumu,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
            
        #append pan Arctic lists
        self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
        self.CSVDaily.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
        self.CSVCumu.append (round(np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea),3))
        
        self.appendRegionLists()
        
    def energycalc(self,DayofYear,ice,iceMean,AWPcumulative,AWPanomaly_acumu,icemask,regmaskf,areamask,latmask):
        '''AWP energy calculation & Regional breakdown'''
        AWPdaily_areaweighted = np.nan
        AWPdaily_oceanarea = np.nan
        AWPcumulative_areaweighted = np.nan
        AWPcumulative_oceanarea = np.nan
        AWPanomaly = np.nan
        anomalymap = iceMean - ice
        
        if regmaskf < 7:
            if ice == 1.02: #value for missing data
                ice = iceMean
                anomalymap = iceMean - ice
            pixlat = min(-40,latmask)
            indexx = int(round((pixlat+40)*(-5)))
            MJ = self.latitudelist[indexx][DayofYear]
            AWPdaily = ((1-ice) * MJ) + self.iceMJ * MJ * ice
            AWPcumulative = AWPcumulative + AWPdaily
            AWPanomaly = anomalymap * MJ * 0.8
            AWPanomaly_acumu = AWPanomaly_acumu + AWPanomaly
            if icemask == 1:
                AWPdaily_areaweighted = AWPdaily * areamask
                AWPdaily_oceanarea = areamask
                AWPcumulative_areaweighted = AWPcumulative * areamask
                AWPcumulative_oceanarea = areamask
                    
                if regmaskf == 2:
                    self.Wed_daily_calc.append(AWPdaily_areaweighted)
                    self.Wed_calc.append(AWPcumulative_areaweighted)
                    self.Wed_area.append(areamask)
                elif regmaskf == 3:
                    self.Ind_daily_calc.append (AWPdaily_areaweighted)
                    self.Ind_calc.append (AWPcumulative_areaweighted)
                    self.Ind_area.append (areamask)
                elif regmaskf == 4:
                    self.Pac_daily_calc.append (AWPdaily_areaweighted)
                    self.Pac_calc.append (AWPcumulative_areaweighted)
                    self.Pac_area.append (areamask)
                elif regmaskf == 5:
                    self.Ross_daily_calc.append (AWPdaily_areaweighted)
                    self.Ross_calc.append (AWPcumulative_areaweighted)
                    self.Ross_area.append (areamask)
                elif regmaskf == 6:
                    self.Bel_daily_calc.append (AWPdaily_areaweighted)
                    self.Bel_calc.append (AWPcumulative_areaweighted)
                    self.Bel_area.append (areamask)

        else:
            AWPdaily = 9999.9
            AWPcumulative = 9999.9
            
        return AWPdaily,AWPcumulative,AWPanomaly,AWPanomaly_acumu,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea
        

    def normalshow(self,icemap,icesum):
        '''displays daily AWP data'''
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        icemap = np.ma.masked_greater(icemap, 9000)
                
        cbarmax = min(32,int(np.amax(icemap)))
        
        self.ax.clear()
        self.ax.set_xlabel('Pan Antarctic Mean: '+str(icesum)+' [MJ / 'r'$m^2$]')
        cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=cbarmax, cmap=self.cmap)
        
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        self.ax.set_title('Albedo-Warming Potential',loc='left')
        self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
        
        self.ax.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        self.ax.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.2)
        
        cbar = self.fig.colorbar(cax, ticks=[0,cbarmax*0.25,cbarmax*0.5,cbarmax*0.75
            ,cbarmax]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]')
        
        self.fig.tight_layout()
#         plt.pause(0.01)
        self.fig.savefig(f'{self.webpath}/AWP/South_AWP_Map1.png')
        
        
    def cumulativeshow(self,icemap,icesum):
        '''displays cumulative AWP data'''
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        icemap = np.ma.masked_greater(icemap, 9000)
        
        cbarmax = min(5000,int(np.amax(icemap)))
        
        self.ax2.clear()
        self.ax2.set_xlabel('Pan Antarctic Mean: '+str(int(icesum))+' [MJ / 'r'$m^2$]')
        cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=cbarmax, cmap=self.cmap)
        
        self.ax2.axes.get_yaxis().set_ticks([])
        self.ax2.axes.get_xaxis().set_ticks([])
        self.ax2.set_title('Accumulated AWP',loc='left')
        self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
        
        self.ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        self.ax2.set_ylabel('cryospherecomputing.com/awp-south',y=0.2)
        
        
        cbar = self.fig2.colorbar(cax, ticks=[0,int(cbarmax*0.25),int(cbarmax*0.5),int(cbarmax*0.75)
        ,cbarmax]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]')
        
        self.fig2.tight_layout()
#         plt.pause(0.01)
        self.fig2.savefig(f'{self.webpath}/AWP/South_AWP_Map2.png')
        
    def anomalyshow(self,icemap,icesum):
        '''displays anomaly AWP data'''
        
        for x,y in enumerate(self.regmaskf):
            if y > 8:
                icemap[x] = 99
        
        icemap = np.ma.masked_outside(icemap,-50,50) 
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        
        lowestAWP = np.amin(icemap)
        highestAWP = np.amax(icemap)
        
        cbarmax = int(max(abs(lowestAWP),highestAWP,10))        
        
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_subplot(111)

        cax = ax.imshow(icemap, interpolation='nearest', vmin=-cbarmax, vmax=cbarmax, cmap=self.cmap)
        cbar = fig.colorbar(cax, ticks=[-cbarmax,-0.5*cbarmax,0,0.5*cbarmax,
            cbarmax]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.set_xlabel('Pan Antarctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]')
        ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.2)
        ax.set_title('Albedo-Warming Potential Anomaly',loc='left')
        ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
        
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.text(185, 285,'Anomaly Base: 2000-2019', fontsize=9,color='black',fontweight='bold')
        fig.tight_layout()
#         plt.pause(0.01)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Map3.png')
        plt.close()
        
    def anomalyshow_accu(self,icemap,icesum):
        '''displays anomaly AWP data'''
        
        for x,y in enumerate(self.regmaskf):
            if y > 8:
                icemap[x] = 9999
        
        icemap = np.ma.masked_outside(icemap,-5000,5000) 
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        
        lowestAWP = np.amin(icemap)
        highestAWP = np.amax(icemap)
        
        cbarmax = int(min(abs(lowestAWP),highestAWP,1000))
        
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_subplot(111)

        cax = ax.imshow(icemap, interpolation='nearest', vmin=-cbarmax, vmax=cbarmax, cmap=self.cmap)
        cbar = fig.colorbar(cax, ticks=[-cbarmax,-0.5*cbarmax,0,0.5*cbarmax,
            cbarmax]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.set_xlabel('Pan Antarctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]')
        ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.2)
        ax.set_title('Accumulated AWP Anomaly',loc='left')
        ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
        
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.text(185, 285,'Anomaly Base: 2000-2019', fontsize=9,color='black',fontweight='bold')
        fig.tight_layout()
#         plt.pause(0.01)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Map4.png')
        plt.close()
        
    def dailyorcumu(self):
        '''creates separate figures for sea ice data'''
        self.fig, self.ax = plt.subplots(figsize=(8, 7))
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 7))
        
        import copy
        self.cmap = copy.copy(plt.colormaps["coolwarm"])
        self.cmap.set_bad('black',0.75)
        
    def createMaps(self,count):
        '''creates Maps'''
        self.normalshow(self.AWPdaily,self.CSVDaily[-1])
        self.cumulativeshow(self.AWPcumulative,round(self.CSVCumu[-1],0))
        
        AWP_Daily_mean = self.AWP_Daily_mean[count]
        AWP_Accu_mean = self.AWP_Accu_mean[count]
        AWP_Daily_anom = self.CSVDaily[-1] - float(AWP_Daily_mean)
        AWP_Accu_anom = self.CSVCumu[-1] - float(AWP_Accu_mean)
        self.anomalyshow(self.AWPanomaly,round(AWP_Daily_anom,2))
        self.anomalyshow_accu(self.AWPanomaly_acumu,round(AWP_Accu_anom,2))
        
        
    def save_data(self):
        CryoIO.csv_columnexport(f'{self.webpath}/AWP_data/South_AWP_NRT.csv',
                [self.CSVDatum,self.CSVDaily,self.CSVCumu])
        CryoIO.csv_columnexport(f'{self.webpath}/AWP_data/South_AWP_NRT_regional.csv',
                [self.CSVDatum,self.Wed,self.Ind,self.Pac,self.Ross,self.Bell])
        CryoIO.csv_columnexport(f'{self.webpath}/AWP_data/South_AWP_NRT_regional_daily.csv',
                [self.CSVDatum,self.Wed_daily,self.Ind_daily,self.Pac_daily,self.Ross_daily,self.Bell_daily])
        
        #save binary accumulative files
        CryoIO.savebinaryfile(f'{self.webpath}/AWP_data/South_AWP_Accu.bin',self.AWPcumulative)
        CryoIO.savebinaryfile(f'{self.webpath}/AWP_data/South_AWP_Accu_anom.bin',self.AWPanomaly_acumu)
    
    def loadCSVdata (self):
        Yearcolnames = ['Date','B','C']
        Yeardata = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT.csv', names=Yearcolnames)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVDaily = Yeardata.B.tolist()
        self.CSVCumu = Yeardata.C.tolist()

    def loadMeandata (self):
        AWP_mean = ['Date','A','B']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_mean.csv', names=AWP_mean)
        self.AWP_Daily_mean = Climatedata.A.tolist()
        self.AWP_Accu_mean = Climatedata.B.tolist()

    
    def loadCSVRegiondata (self):
        Yearcolnames = ['A', 'B', 'C', 'D', 'E', 'F']
        Yeardata = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT_regional.csv', names=Yearcolnames)
        self.datum = Yeardata.A.tolist()
        self.Wed = Yeardata.B.tolist()
        self.Ind = Yeardata.C.tolist()
        self.Pac = Yeardata.D.tolist()
        self.Ross = Yeardata.E.tolist()
        self.Bell = Yeardata.F.tolist()
        
        Yearcolnames_daily = ['A', 'B', 'C', 'D', 'E', 'F']
        Yeardata_daily = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily)
        self.datum = Yeardata_daily.A.tolist()
        self.Wed_daily = Yeardata_daily.B.tolist()
        self.Ind_daily = Yeardata_daily.C.tolist()
        self.Pac_daily = Yeardata_daily.D.tolist()
        self.Ross_daily = Yeardata_daily.E.tolist()
        self.Bell_daily = Yeardata_daily.F.tolist()

    
    
    def automated (self,year,stringmonth,stringday):
        self.year = year
        self.stringmonth = stringmonth
        self.stringday = stringday
        
        print(self.year,self.stringmonth,self.stringday)
        self.loadCSVdata()
        self.loadCSVRegiondata()
        self.loadMeandata()
        
        #load accumulative files
        self.AWPcumulative = CryoIO.openfile(f'{self.webpath}/AWP_data/South_AWP_Accu.bin',float)
        self.AWPanomaly_acumu = CryoIO.openfile(f'{self.webpath}/AWP_data/South_AWP_Accu_anom.bin',float)
        
        index = len(self.CSVDaily)
#        print(self.AWP_Daily_mean[index])
        self.daycalc(index)
        self.createMaps(index)
        self.save_data()
        
        import Antarctic_Daily_AWP_Graphs
        Antarctic_Daily_AWP_Graphs.action.automated(self.year,stringmonth,stringday)


action = AWP_calc_daily()
    

    
if __name__ == '__main__':
      # action.automated(2023,'09','26')
      action.dayloop()
    


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