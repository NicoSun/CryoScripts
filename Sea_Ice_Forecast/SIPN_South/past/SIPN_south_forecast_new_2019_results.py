from multiprocessing import Pool
import numpy as np
import os
import CryoIO

from datetime import date
from datetime import timedelta
import time

class NSIDC_prediction:

	def __init__  (self):
		self.start = date(2018, 11,30)
		self.loopday = self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		
		self.daycount = 1 #366year, 181summer,91 decmber-february
		
		self.masksload() 
#		self.map_create()
		
		self.CSVDatum = ['Date']
		self.CSVVolume =  ['VolumeMean']
		self.CSVExtent = ['ExtentMean']
		self.CSVArea = ['AreaMean']
		self.meltfactor = 1.0 # MJ reduction
		self.sic_cutoff = 0.12 # thickness in meter
		self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		self.gridvolumefactor = 625*0.001
		self.base_back_radiation = 9 #default: 9
		self.base_bottommelt = 1 #default: 1
		
		self.CSVVolumeHigh =  ['VolumeHigh']
		self.CSVExtentHigh = ['ExtentHigh']
		self.CSVAreaHigh = ['AreaHigh']
		
		self.CSVVolumeLow =  ['VolumeLow']
		self.CSVExtentLow = ['ExtentLow']
		self.CSVAreaLow = ['AreaLow']
		self.starttime = time.time()
		
		
	def masksload(self):
		filename = 'X:/NSIDC_South/Masks/region_s_pure.msk'
		self.regmaskf = CryoIO.openfile(filename, np.uint8)
		
		filename = 'X:/NSIDC_South/Masks/pss25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename, np.int32)/1000
		
		filename = 'X:/NSIDC_South/Masks/pss25lats_v3.dat'
		self.latmaskf = CryoIO.openfile(filename, np.int32)/100000
		
		filename = 'X:/NSIDC_South/Masks/pss25lons_v3.dat'
		self.lonmaskf = CryoIO.openfile(filename, np.int32)/100000
		
		self.latitudelist = np.loadtxt('X:/NSIDC_South/Masks/Lattable_south_MJ_all_year.csv', delimiter=',')
		self.co2list = np.loadtxt('X:/NSIDC_South/Masks/Global_CO2.csv', delimiter=',')
		
	
	def prediction(self):		
		filepath = 'X:/NSIDC_South/DataFiles/'	
		filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		countmax = self.index+self.daycount
		
		iceforecast = CryoIO.openfile(os.path.join(filepath,filename), np.uint8)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}_south.bin'.format(self.datestring)
			filenameAvg = 'Mean_00_19/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'Daily_change/NSIDC_SIC_Change_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'Stdv/NSIDC_Stdv_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			
			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 2 * co2value / 338
			
			self.bottommelt = self.base_bottommelt
			bottommelt = self.bottommelt * 1.05
			bottommeltHigh = self.bottommelt * 0.95
			bottommeltLow = self.bottommelt * 1.25
					
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			if count <= 330: #change date of year to last available date
				iceforecast =CryoIO.openfile(os.path.join(filepath,filename), np.uint8)/250

				
#				self.early_recalibrate(iceforecast)
				self.meltfactor = 1.4
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,self.iceMean,bottommelt)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecast,self.iceHigh,bottommeltHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecast,self.iceLow,bottommeltLow)
				
			else:
				icechange = CryoIO.openfile(os.path.join(filepath,filenameChange), np.int8)/250
				iceAvg = CryoIO.openfile(os.path.join(filepath,filenameAvg), np.uint8)/250
				iceStdv = CryoIO.openfile(os.path.join(filepath,filenameStdv), np.float16)/250
			
				iceforecast = iceforecast + icechange
				np.clip(iceforecast,0,1)
				iceforecastMean = (2*iceforecast+iceAvg)/3
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.22)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.35)
				
				iceforecastMean[iceforecastMean > 1] = 1
				iceforecastHigh[iceforecastHigh > 1] = 1
				iceforecastLow[iceforecastLow > 1] = 1
				iceforecastMean[iceforecastMean < 0] = 0
				iceforecastHigh[iceforecastHigh < 0] = 0
				iceforecastLow[iceforecastLow < 0] = 0
			
				self.meltfactor = 1
				
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,self.iceMean,bottommelt)
# =============================================================================
# 				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecastHigh,self.iceHigh,bottommeltHigh)
# 				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecastLow,self.iceLow,bottommeltLow)
# =============================================================================
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(round(int((extent))/1e6,4))
			self.CSVArea.append(round(int((area))/1e6,4))
			
# =============================================================================
# 			self.CSVVolumeHigh.append(int(calcvolumeHigh))
# 			self.CSVExtentHigh.append(round(int((extentHigh))/1e6,4))
# 			self.CSVAreaHigh.append(round(int((areaHigh))/1e6,4))
# 			
# 			self.CSVVolumeLow.append(int(calcvolumeLow))
# 			self.CSVExtentLow.append(round(int((extentLow))/1e6,4))
# 			self.CSVAreaLow.append(round(int((areaLow))/1e6,4))
# =============================================================================
			
#			visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
#			visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
			
			#save last date as arrary in mm
			if count >= (countmax-15):
# 			if count >330:
#				visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
				visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
				visualize.fig2.savefig('Images/{}'.format(self.datestring))
				
# =============================================================================
# #				SIPN_analysis_south.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
# 				SIPN_analysis_south.concentrationshow(sicmapHigh,int(areaHigh),int(extentHigh),'High')
# 
# #				SIPN_analysis_south.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
# 				SIPN_analysis_south.concentrationshow(sicmapLow,int(areaLow),int(extentLow),'Low')
# =============================================================================
				
				
# =============================================================================
# 				iceLastDateMean = self.iceMean*1000
# 				iceLastDateMean = np.array(iceLastDateMean,dtype=np.uint16)
# 				iceLastDateHigh = self.iceHigh*1000
# 				iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.uint16)
# 				iceLastDateLow = self.iceLow*1000
# 				iceLastDateLow = np.array(iceLastDateLow,dtype=np.uint16)
# =============================================================================

# =============================================================================
# 			# save SIT maps
# 			exportpath = 'X:/Sea_Ice_Forecast/Data_Dump/'
# 			CryoIO.savebinaryfile('{}001/SIPN2_Thickness_Mean_{}.bin'.format(exportpath,self.datestring),iceLastDateMean)
# 			CryoIO.savebinaryfile('{}002/SIPN2_Thickness_midHigh_{}.bin'.format(exportpath,self.datestring),iceLastDateHigh)
# 			CryoIO.savebinaryfile('{}003/SIPN2_Thickness_midLow_{}.bin'.format(exportpath,self.datestring),iceLastDateLow)
# =============================================================================
			
# =============================================================================
# 			# save SIC maps
# 			exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2020-21_Submission/'
# 			CryoIO.savebinaryfile('{}001/SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
# 			CryoIO.savebinaryfile('{}002/SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
# 			CryoIO.savebinaryfile('{}003/SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)
# =============================================================================

			#SIC export for error analysis
# 			CryoIO.savebinaryfile('predict/SIPN2_{}.bin'.format(self.datestring),sicmap)
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,self.yearday, self.latitudelist[150][self.yearday])
#			print(count)
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
					
				

	def meltcalc(self,iceforecast,icearray,bottommelt):
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		
		sicmapg = np.array(np.zeros(len(icearray),dtype=np.uint8))
		extent = 0
		area = 0
		calcvolume = 0
		for x in range (0,arraylength):
			if self.regmaskf[x] < 11:
				if 0 < icearray[x] < 5: # speedup calculation
					pixlat = min(-40,self.latmaskf[x])
					indexx = int(round((pixlat+40)*(-5)))
					MJ = self.latitudelist[indexx][self.yearday]*(1-iceforecast[x])*self.meltfactor-self.back_radiation + bottommelt
					icearray[x] = max(0,icearray[x]-MJ/self.icemeltenergy)
					calcvolume = calcvolume + self.gridvolumefactor*icearray[x]
					if self.sic_cutoff < icearray[x] < 5:
						sicmapg[x] = min(250,(icearray[x]/0.006))
						extent += self.areamaskf[x]
						area += min(1,sicmapg[x]/250) * self.areamaskf[x]
					
					
		return icearray,sicmapg,extent,area,calcvolume
		
		
	def csvexport_by_forecasttype(self):
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2020-21_Submission/'
		CryoIO.csv_columnexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
		CryoIO.csv_columnexport('{}_SIPN_forecast_003_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
		CryoIO.csv_columnexport('{}_SIPN_forecast_001_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])

	def csvexport_by_measure(self):
		
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2020-21_Submission/'
		CryoIO.csv_columnexport('{}__SIPN_forecast_Volume{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVVolume,self.CSVVolumeHigh])
		CryoIO.csv_columnexport('{}__SIPN_forecast_Area{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAreaLow,self.CSVArea,self.CSVAreaHigh])
		CryoIO.csv_columnexport('{}__SIPN_forecast_Extent{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVExtentLow,self.CSVExtent,self.CSVExtentHigh])
		
		
	def getvolume (self,thickness,daycount,day,month,year):
		self.daycount = daycount
		self.start = date(year,month,day)
		self.loopday	= self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		lastday = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		self.yearday = self.loopday.timetuple().tm_yday

		
		print(thickness,'meter')
		
		filename = 'X:/NSIDC_south/DataFiles/NSIDC_{}_south.bin'.format(lastday)
		
		self.iceLastDate = CryoIO.openfile(filename, np.uint8)/250

		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 7:
				self.iceLastDate[x] = 9
		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] < 7:
				if 0.15 < self.iceLastDate[x] <= 1 and self.latmaskf[x] < -55:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]
				else:
					self.iceLastDate[x] = 0
			if self.regmaskf[x] < 1:
				self.iceLastDate[x] = 0

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')

		self.prediction()
		end = time.time()
		print(end-self.starttime)
#		self.csvexport_by_forecasttype()
# =============================================================================
# 		self.thicknessshow(self.iceLastDate,5,4,'end')
# 		self.concentrationshow(ice,5,4,'end')
# =============================================================================
#		plt.show()
		
# 1980-2016
thicknesslist_1980 = [1.427,1.438,1.410,1.398,1.386,1.390,1.454,1.577,1.340,1.400,1.566,1.390
				 ,1.488,1.550,1.475,1.379,1.526,1.404,1.394,1.390,1.422,1.589,1.344,1.470,
				 1.555,1.407,1.553,1.414,1.521,1.446,1.465,1.408,1.537,1.626,1.609,1.624,1.538,1.517,1518]


thicknesslist_2000 = [1.422,1.589,1.444,1.470, 1.555,1.407,1.553,1.414,1.521,1.446,1.465,1.408,1.537,1.626,1.609,1.624,1.538,1.517,1.518]

# =============================================================================
# def spawnprocess(datalist):
# 	action = NSIDC_prediction()
# 	data = action.getvolume(datalist[1],122,1,12,datalist[0]) #daycount: 91 until 28th Feb
# 	
# 	return data
# 	
# if __name__ == '__main__':
# 	datalist = []
# 	x = 0
# 	for year in range(2000,2019):
# #		datalist.append([year,thicknesslist_2000[x]])
# 		datalist.append([year,1.475])
# 		x +=1
# 	
# 	p = Pool(processes=12)
# 	data = p.map(spawnprocess, datalist)
# 	p.close()
# =============================================================================

import SIPN_analysis_south
visualize = SIPN_analysis_south.NSIDC_analysis()
visualize.conmap_create()

	
action = NSIDC_prediction()
action.getvolume(1.48,91,30,11,2019)
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
'''