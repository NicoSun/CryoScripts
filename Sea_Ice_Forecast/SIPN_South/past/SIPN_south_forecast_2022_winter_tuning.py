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

from datetime import date
from datetime import timedelta
import time


class NSIDC_prediction:

    def __init__(self):
        self.filepath = '/media/prussian/Cryosphere/NSIDC_South'
        self.filepath_SIPN = '/media/prussian/Cryosphere/Sea_Ice_Forecast'

        self.start = date(2018, 11, 30)
        self.loopday = self.start
        self.year = self.start.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)

        self.daycount = 1  # 366year, 181summer,91 decmber-february

        self.masksload()
#		self.map_create()

        self.sic_cutoff = 0.1  # thickness in meter
        # Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
        self.icemeltenergy = 333.55*1000*0.92/1000
        self.gridvolumefactor = 625*0.001
        self.base_back_radiation = 9  # default: 9
        self.base_bottommelt = 1.1  # default: 1
        self.base_icedrift_sim = 7.0 # default: 9 (MJ)

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

        self.latitudelist = np.loadtxt(
            f'{self.filepath}/Masks/Lattable_south_MJ_all_year.csv', delimiter=',')
        self.co2list = np.loadtxt(
            f'{self.filepath}/Masks/Global_CO2_forecast.csv', delimiter=',')

    def prediction(self):
        ''' Starts the day loop'''
        filename = 'NSIDC_{}{}{}_south.bin'.format(
            self.year, self.stringmonth, self.stringday)
        countmax = self.index+self.daycount

        iceforecast = CryoIO.openfile(f'{self.filepath}/DataFiles/{self.year}/{filename}', np.uint8)/250
        icedrift_error = np.zeros(len(self.regmaskf))

        self.iceMean = np.array(self.iceLastDate, dtype=float)

        for count in range(self.index, countmax, 1):
            filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}_south.bin'
            filenameChange = f'{self.filepath_SIPN}/DataFiles_s/Forecast_SIC_change/NSIDC_SIC_Change_{self.stringmonth}{self.stringday}.bin'
            filenameDrift_error = f'analysis/icedrift_correction/SIPN2_error_{self.stringmonth}{self.stringday}.npz'

            # 338ppm base value in 1980
            co2listindex = (self.year-1980)*12 + self.loopday.month-1
            co2value = self.co2list[co2listindex][1]
            self.back_radiation = self.base_back_radiation - 2 * co2value / 338

            self.MJ_adjust = self.base_bottommelt - self.back_radiation
            self.icedrift_sim = self.base_icedrift_sim - count/111

            icedrift_error = CryoIO.readnumpy(filenameDrift_error)/100
            icedrift_error = icedrift_error

            # fileformats: normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
            iceforecast_obs = CryoIO.openfile(filename, np.uint8)/250
            if count <= 161:  # change date of year to last available date
                self.iceMean, sicmap, extent, area, calcvolume = self.meltcalc(
                    iceforecast_obs, icedrift_error, self.iceMean)

            else:
                icechange = CryoIO.openfile(filenameChange, np.int8)/250
                iceforecast = iceforecast + icechange

                '''instead of pre-calculating a sea ice correlation for every year like in the real forecast
				 we simply mix the observation into the mean field as a low factor
				 '''

                iceforecastMean = (3*iceforecast+iceforecast_obs)/4

                iceforecastMean[iceforecastMean > 1] = 1
                iceforecastMean[iceforecastMean < 0] = 0

                self.iceMean, sicmap, extent, area, calcvolume = self.meltcalc(iceforecastMean, icedrift_error, self.iceMean)

            self.CSVVolume.append(int(calcvolume))
            self.CSVExtent.append(round(int((extent))/1e6, 4))
            self.CSVArea.append(round(int((area))/1e6, 4))

            # SIC export for error analysis
# 			CryoIO.savenumpy('analysis/predict/SIPN2_{}.npz'.format(self.datestring),sicmap)
            CryoIO.savenumpy(f'analysis/predict/SIPN2_{self.datestring}.npz', sicmap)

            self.CSVDatum.append('{}/{}/{}'.format(self.year, self.stringmonth, self.stringday))
            print(self.year, self.yearday, self.icedrift_sim)
#			print(count)
            if count < countmax:
                self.advanceday(1)

    def advanceday(self, delta):
        self.loopday = self.loopday+timedelta(days=delta)
        self.year = self.loopday.year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.yearday = self.loopday.timetuple().tm_yday
        self.datestring = '{}{}{}'.format(
            self.year, self.stringmonth, self.stringday)

    def calc_driftcorrection(self, drifterror, SIT, pixlat):
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

    def meltcalc(self, iceforecast, icedrift_error, icearray):
        ''' main melting algorithm '''
        arraylength = len(iceforecast)
        np.seterr(divide='ignore', invalid='ignore')

        sicmapg = np.array(np.zeros(len(icearray), dtype=np.uint8))
        extent = 0
        area = 0
        calcvolume = 0
        for x in range(0, arraylength):
            if self.regmaskf[x] < 11:
                if self.latmaskf[x] < -54:
                    pixlat = min(-40, self.latmaskf[x])
                    indexx = int(round((pixlat+40)*(-5)))
                    driftcorrection = self.icedrift_sim
                    driftcorrection = driftcorrection * self.calc_driftcorrection(icedrift_error[x], icearray[x], pixlat)

                    MJ = self.latitudelist[indexx][self.yearday]*(1-iceforecast[x]) + self.MJ_adjust + driftcorrection * icedrift_error[x]
                    icearray[x] = max(-1, icearray[x]-MJ/self.icemeltenergy)
                    calcvolume = calcvolume + self.gridvolumefactor*icearray[x]
                    if self.sic_cutoff < icearray[x] < 5:
                        sicmapg[x] = min(250, (icearray[x]/0.006))
                        extent += self.areamaskf[x]
                        area += min(1, sicmapg[x]/250) * self.areamaskf[x]
                else:
                    icearray[x] = 0
                    sicmapg[x] = 0

        return icearray, sicmapg, extent, area, calcvolume

    def csvexport_by_forecasttype(self):
        ''' Exporting values '''
        CryoIO.csv_columnexport('_SIPN_forecast_002_{}.csv'.format(self.year), [self.CSVDatum, self.CSVVolume, self.CSVArea, self.CSVExtent])

    def getvolume(self, thickness, daycount, day, month, year):
        ''' first day initialisation '''
        self.daycount = daycount
        self.start = date(year, month, day)
        self.loopday = self.start
        self.year = year
        self.stringmonth = str(self.loopday.month).zfill(2)
        self.stringday = str(self.loopday.day).zfill(2)
        self.datestring = '{}{}{}'.format(
            self.year, self.stringmonth, self.stringday)
        self.index = self.loopday.timetuple().tm_yday
        self.yearday = self.loopday.timetuple().tm_yday

        print(thickness, 'meter')
        self.CSVDatum = ['Date']
        self.CSVVolume = [f'Volume_{year}']
        self.CSVExtent = [f'Extent_{year}']
        self.CSVArea = [f'Area_{year}']

        filename = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}_south.bin'

        self.iceLastDate = CryoIO.openfile(filename, np.uint8)/250

        # Landmask initialisation
        for x in range(0, len(self.iceLastDate)):
            if self.regmaskf[x] > 7:
                self.iceLastDate[x] = 9

        # thickness initialisation
        for x in range(0, len(self.iceLastDate)):
            if self.regmaskf[x] < 7:
                if 0.25 < self.iceLastDate[x] <= 1 and self.latmaskf[x] < -54:
                    self.iceLastDate[x] = thickness*self.iceLastDate[x]
                elif 0.1 < self.iceLastDate[x] < 0.25 and self.latmaskf[x] < -54:
                    self.iceLastDate[x] = thickness*self.iceLastDate[x]+0.05
                else:
                    self.iceLastDate[x] = -0.4
            if self.regmaskf[x] < 1:
                self.iceLastDate[x] = 0


#		self.normalshow(self.iceLastDate,volume,area,'Mean')

        self.prediction()
        end = time.time()
        print(end-self.starttime)
        return self.CSVArea, self.CSVExtent


def spawnprocess(datalist):
    action = NSIDC_prediction()
    # daycount: 91 until 28th Feb
    data = action.getvolume(datalist[1], 120, 1, 6, datalist[0])

    return data


if __name__ == '__main__':
    datalist = []
    x = 0
    thickness = 1.5
    for year in range(1998, 2022):
        datalist.append([year, thickness])
        x += 1

    p = Pool(processes=24)
    data = p.map(spawnprocess, datalist)
    p.close()

    area = []
    extent = []
    for x in data:
        area.append(x[0])
        extent.append(x[1])

    action = NSIDC_prediction()
    CryoIO.csv_columnexport('_area.csv', area)
    CryoIO.csv_columnexport('_extent.csv', extent)

# =============================================================================
# import SIPN_analysis_south
# visualize = SIPN_analysis_south.NSIDC_analysis()
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
