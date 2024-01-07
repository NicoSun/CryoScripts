from multiprocessing import Pool
import numpy as np
import os
import CryoIO

from datetime import date
from datetime import timedelta
import time

class NSIDC_prediction:

    def __init__  (self):
        self.filepath = '/media/prussian/Cryosphere/NSIDC_South'
        self.filepath_SIPN = '/media/prussian/Cryosphere/Sea_Ice_Forecast'
        
        self.start = date(2018, 11,30)
        self.loopday = self.start
        self.year = self.start.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        
        self.daycount = 1 #366year, 181summer,91 decmber-february
        
        self.masksload() 
#        self.map_create()
        
        self.CSVDatum = ['Date']
        self.CSVVolume =  ['VolumeMean']
        self.CSVExtent = ['ExtentMean']
        self.CSVArea = ['AreaMean']
        self.sic_cutoff = 0.1 # thickness in meter
        self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
        self.gridvolumefactor = 625*0.001
        self.base_back_radiation = 9 #default: 9
        self.base_bottommelt = 1.1 #default: 1
        self.base_icedrift_sim = 7.0 # (MJ)
        
        self.CSVVolumeHigh =  ['VolumeHigh']
        self.CSVExtentHigh = ['ExtentHigh']
        self.CSVAreaHigh = ['AreaHigh']
        
        self.CSVVolumeLow =  ['VolumeLow']
        self.CSVExtentLow = ['ExtentLow']
        self.CSVAreaLow = ['AreaLow']
        self.starttime = time.time()
        
        
    def masksload(self):
        ''' Loads NSIDC masks and Daily Solar Energy Data'''
        
        filename = f'{self.filepath}/Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename, np.uint8)
        
        filename = f'{self.filepath}/Masks/pss25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename, np.int32)/1000
        
        filename = f'{self.filepath}/Masks/pss25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename, np.int32)/100000
        
        filename = f'{self.filepath}/Masks/pss25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename, np.int32)/100000
        
        self.latitudelist = np.loadtxt(f'{self.filepath}/Masks/Lattable_south_MJ_all_year.csv', delimiter=',')
        self.co2list = np.loadtxt(f'{self.filepath}/Masks/Global_CO2_forecast.csv', delimiter=',')
        
    
    def prediction(self):        
        filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
        countmax = self.index+self.daycount
        
        iceforecast = CryoIO.openfile(f'{self.filepath}/DataFiles/{self.year}/{filename}', np.uint8)/250
        
        self.iceMean = np.array(self.iceLastDate, dtype=float)
        self.iceHigh = np.array(self.iceLastDate, dtype=float)
        self.iceLow = np.array(self.iceLastDate, dtype=float)
        

        for count in range (self.index,countmax,1):
            filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}_south.bin'
            filenameAvg = f'{self.filepath_SIPN}/DataFiles_s/Forecast_{submissionmonth}/Forecast_Manual/NSIDC_Mean_{self.stringmonth}{self.stringday}.npz'
            filenameChange = f'{self.filepath_SIPN}/DataFiles_s/Forecast_{submissionmonth}/Forecast_SIC_change/NSIDC_SIC_Change_{self.stringmonth}{self.stringday}.npz'
            filenameStdv = f'{self.filepath_SIPN}/DataFiles_s/Forecast_{submissionmonth}/Forecast_Stdv/NSIDC_Stdv_{self.stringmonth}{self.stringday}.npz'
            filenameDrift_error = f'analysis/icedrift_correction/SIPN2_error_{self.stringmonth}{self.stringday}.npz'
            
            #338ppm base value in 1980
            co2listindex = (self.year-1980)*12 + self.loopday.month-1
            co2value = self.co2list[co2listindex][1]
            self.back_radiation = self.base_back_radiation - 2 * co2value / 338
            self.icedrift_sim = self.base_icedrift_sim - count/111
            
            self.bottommelt = self.base_bottommelt
            bottommelt = self.bottommelt
            bottommeltHigh = self.bottommelt * 0.9
            bottommeltLow = self.bottommelt * 1.2
            
            driftcorrection = self.icedrift_sim * 1
            driftcorrectionLow = self.icedrift_sim * 0.9
            driftcorrectionHigh = self.icedrift_sim * 1.1
            
            icedrift_error = CryoIO.readnumpy(filenameDrift_error)/100
            icedrift_error = icedrift_error
                    
            #normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
            if count <= 152+40: #change date of year to last available date
                iceforecast = CryoIO.openfile(filename,np.uint8)/250
                
#                self.early_recalibrate(iceforecast)
                
                self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,icedrift_error,self.iceMean,bottommelt,driftcorrection)
                self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecast,icedrift_error,self.iceHigh,bottommeltHigh,driftcorrectionHigh)
                self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecast,icedrift_error,self.iceLow,bottommeltLow,driftcorrectionLow)
                
            else:
                icechange = CryoIO.readnumpy(filenameChange)/250
                iceAvg = CryoIO.readnumpy(filenameAvg)/250
                iceStdv = CryoIO.readnumpy(filenameStdv)/250
            
                iceforecast = iceforecast + icechange
                np.clip(iceforecast,0,1)
                iceforecastMean = (3*iceforecast+iceAvg)/4
                iceforecastHigh = np.array(iceforecastMean + iceStdv*0.22)
                iceforecastLow = np.array(iceforecastMean - iceStdv*0.30)
                
                iceforecastMean[iceforecastMean > 1] = 1
                iceforecastHigh[iceforecastHigh > 1] = 1
                iceforecastLow[iceforecastLow > 1] = 1
                iceforecastMean[iceforecastMean < 0] = 0
                iceforecastHigh[iceforecastHigh < 0] = 0
                iceforecastLow[iceforecastLow < 0] = 0
                
                
                self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,icedrift_error,self.iceMean,bottommelt,driftcorrection)
                self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecastHigh,icedrift_error,self.iceHigh,bottommeltHigh,driftcorrection)
                self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecastLow,icedrift_error,self.iceLow,bottommeltLow,driftcorrection)
            

            self.CSVVolume.append(int(calcvolume))
            self.CSVExtent.append(round(int((extent))/1e6,4))
            self.CSVArea.append(round(int((area))/1e6,4))
            
            self.CSVVolumeHigh.append(int(calcvolumeHigh))
            self.CSVExtentHigh.append(round(int((extentHigh))/1e6,4))
            self.CSVAreaHigh.append(round(int((areaHigh))/1e6,4))
            
            self.CSVVolumeLow.append(int(calcvolumeLow))
            self.CSVExtentLow.append(round(int((extentLow))/1e6,4))
            self.CSVAreaLow.append(round(int((areaLow))/1e6,4))
            
# =============================================================================
#             if count > (countmax-82):
#     #            visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
#                 visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
#                 visualize.fig2.savefig('Images/{}'.format(self.datestring))
# =============================================================================
            

            
            self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
            print(self.year,self.yearday, self.icedrift_sim)
#            print(count)
            if count < countmax:
                self.advanceday(1)
            
    def advanceday(self,delta):    
        self.loopday = self.loopday+timedelta(days=delta)
        self.year = self.loopday.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.yearday = self.loopday.timetuple().tm_yday
        self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
        
    def early_recalibrate(self,iceobserved):
        thickness = 1.3
        for x in range (0,len(iceobserved)):
            if self.regmaskf[x] < 7:
                if 0.15 < iceobserved[x] <= 1:
                    iceobserved[x] = thickness*iceobserved[x]
                else:
                    iceobserved[x] = 0
                    
                self.iceMean[x] = (self.iceMean[x]+iceobserved[x])/2
                self.iceHigh[x] = (self.iceHigh[x]+iceobserved[x])/2
                self.iceLow[x] = (self.iceLow[x]+iceobserved[x])/2
                    
        return

    def calc_driftcorrection(self,drifterror,SIT,pixlat):
        ''' finetuning values for icedrift mask'''
        abs_Drifterror = abs(drifterror)

        multi = 1
        if pixlat > -55:  # lower correction in high latitudes
            multi = 0.6
        elif pixlat > -65:  # lower correction in high latitudes
            multi = 0.77

        if abs_Drifterror > 0.9:
            aaa = 2.5
        elif 0.3 < abs_Drifterror < 0.9:
            aaa = 1 + abs_Drifterror
        else:
            aaa = 1
        multi = multi * aaa
        if SIT < 0.05 and drifterror < 0:  # 0.1,0
            multi = multi * 2  # icefree area accelerated re-freeze
        elif SIT > 0.44 and drifterror < 0:  # 0.1,0
            multi = multi * 0.2  # already refrozen, but still error
        elif SIT < 0.5 and drifterror > 0.3:  # 0.5,0
            multi = multi*0.75  # thin ice slow down melt if overpredict ice

        return multi

    def meltcalc(self,iceforecast,icedrift_error,icearray,bottommelt,basedriftcorrection):
        arraylength = len(iceforecast)
        np.seterr(divide='ignore', invalid='ignore')
        driftcorrection = basedriftcorrection
        
        sicmapg = np.array(np.zeros(len(icearray),dtype=np.uint8))
        extent = 0
        area = 0
        calcvolume = 0
        for x in range (0,arraylength):
            if self.regmaskf[x] < 11:
                if self.latmaskf[x] < -54:
                    pixlat = min(-40,self.latmaskf[x])
                    indexx = int(round((pixlat+40)*(-5)))
                    driftcorrection = self.icedrift_sim
                    driftcorrection = driftcorrection * self.calc_driftcorrection(icedrift_error[x], icearray[x], pixlat)
                    
                        
                    MJ = self.latitudelist[indexx][self.yearday]*(1-iceforecast[x])-self.back_radiation + bottommelt + driftcorrection * icedrift_error[x]
                    icearray[x] = max(-1,icearray[x]-MJ/self.icemeltenergy)
                    calcvolume = calcvolume + self.gridvolumefactor*icearray[x]
                    if self.sic_cutoff < icearray[x] < 5:
                        sicmapg[x] = min(250,(icearray[x]/0.006))
                        extent += self.areamaskf[x]
                        area += min(1,sicmapg[x]/250) * self.areamaskf[x]
                else:
                    icearray[x] = 0
                    sicmapg[x] = 0
                    
        return icearray,sicmapg,extent,area,calcvolume
        
        
    def csvexport_by_forecasttype(self):
        CryoIO.csv_columnexport(f'temp/_SIPN_forecast_002_{self.year}.csv',
                [self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
        CryoIO.csv_columnexport('temp/_SIPN_forecast_003_{self.year}.csv',
                [self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
        CryoIO.csv_columnexport('temp/_SIPN_forecast_001_{self.year}.csv',
                [self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])

    def csvexport_by_measure(self):
        
        CryoIO.csv_columnexport(f'temp/__SIPN_forecast_Volume{self.year}.csv',
                [self.CSVDatum,self.CSVVolumeLow,self.CSVVolume,self.CSVVolumeHigh])
        CryoIO.csv_columnexport(f'temp/__SIPN_forecast_Area{self.year}.csv',
                [self.CSVDatum,self.CSVAreaLow,self.CSVArea,self.CSVAreaHigh])
        CryoIO.csv_columnexport(f'temp/__SIPN_forecast_Extent{self.year}.csv',
                [self.CSVDatum,self.CSVExtentLow,self.CSVExtent,self.CSVExtentHigh])
        
        
    def getvolume (self,thickness,daycount,day,month,year):
        self.daycount = daycount
        self.start = date(year,month,day)
        self.loopday    = self.start
        self.year = year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
        self.index = self.loopday.timetuple().tm_yday
        self.yearday = self.loopday.timetuple().tm_yday

        
        print(thickness,'meter')
        
        filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}_south.bin'
        
        self.iceLastDate = CryoIO.openfile(filename, np.uint8)/250

        
        for x in range (0,len(self.iceLastDate)):
            if self.regmaskf[x] > 7:
                self.iceLastDate[x] = 9
        
        for x in range (0,len(self.iceLastDate)):
            if self.regmaskf[x] < 7:
                if 0.25 < self.iceLastDate[x] <= 1 and self.latmaskf[x] < -55:
                    self.iceLastDate[x] = thickness*self.iceLastDate[x]
                elif 0.1 < self.iceLastDate[x] < 0.25 and self.latmaskf[x] < -55:
                    self.iceLastDate[x] = thickness*self.iceLastDate[x]+0.05
                else:
                    self.iceLastDate[x] = -0.4
            if self.regmaskf[x] < 1:
                self.iceLastDate[x] = 0

        
#        self.normalshow(self.iceLastDate,volume,area,'Mean')

        self.prediction()
        end = time.time()
        print(end-self.starttime)
#         self.csvexport_by_forecasttype()
#         self.csvexport_by_measure()
# =============================================================================
#         self.thicknessshow(self.iceLastDate,5,4,'end')
#         self.concentrationshow(ice,5,4,'end')
# =============================================================================
#        plt.show()
        
# =============================================================================
# 
# visualize = SIPN_analysis.NSIDC_analysis()
# #visualize.thickmap_create()
# visualize.conmap_create()
# =============================================================================
thickness = 1.5
year = 2022
submissionmonth = '07'
action = NSIDC_prediction()
action.getvolume(thickness,122,1,6,year)
# action.csvexport_by_forecasttype()
action.csvexport_by_measure()

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

arraylength: 104912 (332, 316)

#Regionmask:
2: Weddel Sea
3: Indian Ocean
4: Pacific Ocean
5: Ross Sea
6: Bellingshausen Amundsen Sea
11: Land
12: Coast

monthly CO2 data
https://gml.noaa.gov/ccgg/trends/data.html
'''