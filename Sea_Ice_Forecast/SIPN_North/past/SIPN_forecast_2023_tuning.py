'''
This tuning script should be run before the main forecast script. It can compute forecasts for all past years in a short time.
This allows for finetuning the model towards different forecast metrics e.g. Extent, SIC or SIT
The raw output data is saved in a folder called anaysis. With the "SIPN_analysis" script this raw data can be better analysed 
and create a new bias correction mask.

@author: Nico Sun

'''


from multiprocessing import Pool
import numpy as np
import CryoIO
import os

from datetime import date
from datetime import timedelta
import time
# import SIPN_analysis


class NSIDC_prediction:

    def __init__  (self,icedrift=False):
        self.filepath = os.path.abspath('../../NSIDC')
        self.filepath_SIPN = os.path.abspath('..')
        self.iceDrift = icedrift
        

        
        self.masksload()
        
        self.sic_cutoff = 0.09 # thickness in meter
        self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
        self.gridvolumefactor = 625*0.001
        self.base_back_radiation = 6.6 #default: 6.6 (MJ)
        self.base_bottommelt = 3.3 #default: 3.3 (MJ)
        self.icedrift_sim = 6 # default: 6 (MJ)
        self.airtemp_mod = 0.75
        self.starttime = time.time()
        
    
    def masksload(self):
        ''' Loads NSIDC masks and Daily Solar Energy Data'''
        
        filename = f'{self.filepath}/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = f'{self.filepath}/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000

        filename= f'{self.filepath}/Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = f'{self.filepath}/Masks/psn25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000
    
        
        self.latitudelist = np.loadtxt(f'{self.filepath}/Masks/Lattable_MJ_all_year.csv', delimiter=',')
        self.co2list = np.loadtxt(f'{self.filepath_SIPN}/Global_CO2_forecast.csv', delimiter=',')
        self.templist = np.loadtxt(f'{self.filepath}/Masks/DMI_Temp_80N.csv', delimiter=',')
        
        
    def prediction(self):
        ''' Starts the day loop'''
        filename = 'NSIDC_{}.npz'.format(self.datestring)
        countmax = self.index+self.daycount
        
        iceforecast = CryoIO.readnumpy(f'{self.filepath}/DataFiles/{self.year}/{filename}')/250
#         icedrift_error = np.zeros(len(self.regmaskf))
        
        self.iceMean = np.array(self.iceLastDate, dtype=float)
        

        for count in range (self.index,countmax,1):
            filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}.npz'
            filenameChange = f'{self.filepath_SIPN}/DataFiles/Forecast_SIC_change/NSIDC_SIC_Change_{self.stringmonth}{self.stringday}.npz'
            filenameDrift_error = f'{self.filepath_SIPN}/DataFiles/drift_correction/SIPN2_error_{self.stringmonth}{self.stringday}.npz'

            #338ppm base value in 1980
            co2listindex = (self.year-1980)*12 + self.loopday.month-1
            co2value = self.co2list[co2listindex][1]
            self.back_radiation = self.base_back_radiation - 2 * co2value / 338
            
            
            self.air_temp = (self.templist[count]-273) * self.airtemp_mod
            
            self.bottommelt = self.base_bottommelt * self.meltmomentum / 180
            bottommelt = self.bottommelt
            self.MJ_adjust = bottommelt - self.back_radiation + self.air_temp
            
            if (self.iceDrift):
                icedrift_error = CryoIO.readnumpy(filenameDrift_error)/100
                icedrift_error = icedrift_error
            else:
                icedrift_error = self.sicmap # empty map with landmask
            
            
            #fileformats: normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
            iceforecast_obs = CryoIO.readnumpy(filename)/250
            if count <= 300: #change date of year to last available date, 161==10th June
                self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast_obs,icedrift_error,self.iceMean,count)

            else:
                #load statistical data
                icechange = CryoIO.readnumpy(filenameChange)/250
                iceforecast = iceforecast + icechange
                
                '''instead of pre-calculating a sea ice correlation for every year like in the real forecast
                 we simply mix the observation into the mean field as a low factor
                 '''
                iceforecastMean = (4*iceforecast+iceforecast_obs)/5
                
                iceforecastMean[iceforecastMean > 1] = 1
                iceforecastMean[iceforecastMean < 0] = 0
                
                self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,icedrift_error,self.iceMean,count)


            self.CSVVolume.append(int(calcvolume))
            self.CSVExtent.append(int(extent)/1e6)
            self.CSVArea.append(int(area)/1e6)
            
            #SIC export for error analysis
            CryoIO.savenumpy(f'analysis/predict/SIPN2_{self.datestring}.npz',sicmap)
                
            
            self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
            print(self.year,count)

            # model value adjustment over time
            self.advanceday(1)
            self.icedrift_sim = 6 + count / 150
            if count < 245:
                self.meltmomentum +=1.5
            elif 245 <= count <= 250:
                self.meltmomentum -=22 # default 22
            elif 252 <= count <= 278:
                self.meltmomentum -=12 # default 12
                
            if count == 182:
                self.airtemp_mod = 0.25
            elif count == 270:
                self.airtemp_mod = 1.1
            elif count == 280:
                self.airtemp_mod = 1.25

            
    def advanceday(self,delta):
        self.loopday = self.loopday+timedelta(days=delta)
        self.year = self.loopday.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
        
        
    def calc_driftcorrection(self,drifterror,SIT):
        ''' finetuning values for icedrift mask'''
        abs_Drifterror = abs(drifterror)
        if abs_Drifterror > 0.9:
            multi = 5
        elif abs_Drifterror > 0.82:
            multi = 3.5
        elif abs_Drifterror > 0.75:
            multi = 2.2
        elif abs_Drifterror > 0.7:
            multi = 1.5
        else:
            multi = 1
            
        if SIT < 0.1 and drifterror < 0: #0.1,0
            multi = multi * 2 # icefree area accelerated re-freeze
        elif SIT > 0.44 and drifterror < 0: #0.1,0
            multi = multi *0.25 # already refrozen, but still error
        elif SIT > 0.3 and drifterror > 0.5: # 0.5,0
            multi = multi * 2 # thick ice speed up melt if overpredict ice
            
        return multi
        

    def meltcalc(self,iceforecast,icedrift_error,icearray,count):
        ''' main melting algorithm '''
        arraylength = len(iceforecast)
        np.seterr(divide='ignore', invalid='ignore')
        
        sicmapg = np.array(self.sicmap)
        extent = 0
        area = 0
        calcvolume = 0
        for x in range (0,arraylength):
            if  1 < self.regmaskf[x] < 16:
                if icearray[x] < 5:
                    pixlat = max(20,self.latmaskf[x])
                    indexx = int(round((pixlat-20)*5))
                    if (self.iceDrift):
                        driftcorrection = self.icedrift_sim
                        driftcorrection = driftcorrection * self.calc_driftcorrection(icedrift_error[x],icearray[x])
                        MJ = self.latitudelist[indexx][count+1]*(1-min(1,max(0,iceforecast[x]))) + self.MJ_adjust + driftcorrection * icedrift_error[x]
                    else:
                        MJ = self.latitudelist[indexx][count+1]*(1-min(1,max(0,iceforecast[x]))) + self.MJ_adjust
                    
                    MJ_in_thick = MJ/self.icemeltenergy #energy in thickness
                    thicknesschange = MJ_in_thick
                    if icearray[x] > 0.5 and MJ_in_thick < 0: # low ice growth for thick ice
                        thicknesschange = MJ_in_thick * (3-icearray[x])/3 
                    icearray[x] = max(-3,icearray[x]-thicknesschange)
                    calcvolume += max(0,self.gridvolumefactor*icearray[x])
                if self.sic_cutoff < icearray[x] < 5:
                    sicmapg[x] = min(250,(icearray[x])/0.0065)
#                    sicmapg[x] = min(250,(icearray[x]**1.3)/0.008)
                    extent += self.areamaskf[x]
                    area += min(1,sicmapg[x]/250) * self.areamaskf[x]
                    
                    
        return icearray,sicmapg,extent,area,calcvolume

        
    def csvexport_by_forecasttype(self):
        ''' Exporting values '''
        CryoIO.csv_columnexport('_SIPN_forecast_002_{}.csv'.format(self.year),
                [self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])

        
    def getvolume (self,thickness,daycount,year,month=6,day=1):
        ''' first day initialisation '''
        self.daycount = daycount
        self.start = date(year,month,day)
        self.loopday = self.start
        self.year = year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
        self.index = self.loopday.timetuple().tm_yday
        self.meltmomentum = self.index
                
        print(thickness,'meter')
        self.CSVDatum = ['Date']
        self.CSVVolume =  [f'Volume_{year}']
        self.CSVExtent = [f'Extent_{year}']
        self.CSVArea = [f'Area_{year}']
        
        filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}.npz'
        
        self.iceLastDate = CryoIO.readnumpy(filename)/250
        self.sicmap = np.zeros(len(self.iceLastDate),dtype=np.uint8)
        
        # Landmask initialisation
        for x in range (0,len(self.iceLastDate)):
            if self.regmaskf[x] > 15:
                self.iceLastDate[x] = 9
                self.sicmap [x] = 255
        
        # thickness initialisation
        for x in range (0,len(self.iceLastDate)):
            if 1 < self.regmaskf[x] < 16:
                if self.iceLastDate[x] > 0.15:
                    self.iceLastDate[x] = thickness*self.iceLastDate[x]*(self.latmaskf[x]/75)
            if self.regmaskf[x] < 2:
                self.iceLastDate[x] = 0

        
        #SIT export for SIPN analysis
#        CryoIO.savebinaryfile('SIPN2_thickness_20200601.bin',self.iceLastDate)
        
#        self.normalshow(self.iceLastDate,volume,area,'Mean')
        self.prediction() # start dayloop
        end = time.time()
        print(end-self.starttime)
#         self.csvexport_by_forecasttype()
#        plt.show()
        return self.CSVArea,self.CSVExtent
    

# =============================================================================
# thicknesslist =[2.79,2.58,2.35,2.61,2.57,2.60,2.67,2.69,2.72,2.58,2.73,2.68,2.56,2.64,2.59,2.54,
#                 2.45,2.59,2.59,2.46,2.43,2.44,2.43,2.38,2.33,2.33,2.32,2.17,2.22,2.16,2.04,1.94,
#                 1.99,1.93,2.01,2.11,2.06,1.84,2.02,1.99] # 1980 start
# =============================================================================


def spawnprocess(datalist):
    action = NSIDC_prediction(icedrift=False)
    area,extent = action.getvolume(datalist[1],153,datalist[0]) #daycount: 122 until 30th Sep, 153 until Oct
    
    return area,extent
    
if __name__ == '__main__':
    datalist = []
    x = 0
    thickness = 2
    for year in range(2006,2023):
        datalist.append([year,thickness])
        x +=1
    
    p = Pool(processes=23)
    data = p.map(spawnprocess, datalist)
    print(f'Years calculated: {len(data)}')
    p.close()
    
    area = []
    extent = []
    for x in data:
        area.append(x[0])
        extent.append(x[1])
        
    CryoIO.csv_columnexport('temp/area.csv',area)
    CryoIO.csv_columnexport('temp/extent.csv',extent)


# =============================================================================
# visualize = SIPN_analysis.NSIDC_analysis()
# #visualize.thickmap_create()
# visualize.conmap_create()
# =============================================================================



'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

monthly CO2 data
https://gml.noaa.gov/ccgg/trends/data.html
'''