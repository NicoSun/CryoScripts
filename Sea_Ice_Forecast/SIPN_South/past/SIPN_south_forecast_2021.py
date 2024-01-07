'''
This script calculates the Sea Ice Forecast. All model values have been tuned with the _tuning script.

@author: Nico Sun

'''

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
		
		self.CSVDatum = []
		self.CSVVolume =  []
		self.CSVExtent = []
		self.CSVArea = []
		self.sic_cutoff = 0.1 # thickness in meter
		self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		self.gridvolumefactor = 625*0.001
		self.base_back_radiation = 9 #default: 9
		self.base_bottommelt = 1 #default: 1
		self.icedrift_sim = 10 # (MJ)
		
		self.CSVVolumeHigh =  []
		self.CSVExtentHigh = []
		self.CSVAreaHigh = []
		
		self.CSVVolumeLow =  []
		self.CSVExtentLow = []
		self.CSVAreaLow = []
		self.starttime = time.time()
		
		
	def masksload(self):
		''' Loads NSIDC masks and Daily Solar Energy Data'''
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
		''' Starts the day loop'''
		filepath = 'X:/NSIDC_South/DataFiles/'	
		filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		countmax = self.index+self.daycount
		
		iceforecast = CryoIO.openfile(os.path.join(filepath,filename), np.uint8)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}_south.bin'.format(self.datestring)
			filenameAvg = 'Forecast_Manual/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'Forecast_Manual_SIC_change/NSIDC_SIC_Change_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'Forecast_Stdv/NSIDC_Stdv_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameDrift_error = 'analysis/icedrift_correction/SIPN2_error_{}{}.bin'.format(self.stringmonth,self.stringday)
			
			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 1 * (co2value / 338)**0.5
			
			self.bottommelt = self.base_bottommelt
			bottommelt = self.bottommelt
			bottommeltHigh = self.bottommelt * 0.9
			bottommeltLow = self.bottommelt * 1.2
			
			icedrift_error = CryoIO.openfile(filenameDrift_error,np.float16)/100
			icedrift_error = icedrift_error
					
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			if count <= 336: #change date of year to last available date
				iceforecast =CryoIO.openfile(os.path.join(filepath,filename), np.uint8)/250

				
#				self.early_recalibrate(iceforecast)
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,icedrift_error,self.iceMean,bottommelt)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecast,icedrift_error,self.iceHigh,bottommeltHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecast,icedrift_error,self.iceLow,bottommeltLow)
				
			else:
				icechange = CryoIO.openfile(os.path.join(filepath,filenameChange), np.int8)/250
				iceAvg = CryoIO.openfile(os.path.join(filepath,filenameAvg), np.uint8)/250
				iceStdv = CryoIO.openfile(os.path.join(filepath,filenameStdv), np.float16)/250
			
				iceforecast = iceforecast + icechange
				np.clip(iceforecast,0,1)
				iceforecastMean = (2*iceforecast+iceAvg)/3
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.22)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.30)
				
				iceforecastMean[iceforecastMean > 1] = 1
				iceforecastHigh[iceforecastHigh > 1] = 1
				iceforecastLow[iceforecastLow > 1] = 1
				iceforecastMean[iceforecastMean < 0] = 0
				iceforecastHigh[iceforecastHigh < 0] = 0
				iceforecastLow[iceforecastLow < 0] = 0
				
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,icedrift_error,self.iceMean,bottommelt)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecastHigh,icedrift_error,self.iceHigh,bottommeltHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecastLow,icedrift_error,self.iceLow,bottommeltLow)
			
			'''submission formatting'''
			area_low = int(areaLow)/1e6
			area_low = '{:.4f}'.format(area_low)
			
			area_mean = int(area)/1e6
			area_mean = '{:.4f}'.format(area_mean)
			
			area_high = int(areaHigh)/1e6
			area_high = '{:.4f}'.format(area_high)
			
			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(round(int((extent))/1e6,4))
			self.CSVArea.append(area_mean)
			
			self.CSVVolumeHigh.append(int(calcvolumeHigh))
			self.CSVExtentHigh.append(round(int((extentHigh))/1e6,4))
			self.CSVAreaHigh.append(area_high)
			
			self.CSVVolumeLow.append(int(calcvolumeLow))
			self.CSVExtentLow.append(round(int((extentLow))/1e6,4))
			self.CSVAreaLow.append(area_low)
			
#			visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
#			visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
			
			#save last date as arrary in mm
# 			if count >= (countmax-15):
# 			if count >330:
#				visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
# 				visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
# 				visualize.fig2.savefig('Images/{}'.format(self.datestring))
				
# =============================================================================
# #				SIPN_analysis_south.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
# 				SIPN_analysis_south.concentrationshow(sicmapHigh,int(areaHigh),int(extentHigh),'High')
# 
# #				SIPN_analysis_south.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
# 				SIPN_analysis_south.concentrationshow(sicmapLow,int(areaLow),int(extentLow),'Low')
# =============================================================================
				
			# convert SIT for binary export
			iceLastDateMean = self.iceMean
			iceLastDateMean = np.array(iceLastDateMean,dtype=np.float16)
			iceLastDateHigh = self.iceHigh
			iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.float16)
			iceLastDateLow = self.iceLow
			iceLastDateLow = np.array(iceLastDateLow,dtype=np.float16)

			# save binary SIT maps
			exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2021-22_Submission/'
			CryoIO.savebinaryfile('{}001/SIPN2_SIT_001_{}.bin'.format(exportpath,self.datestring),iceLastDateLow)
			CryoIO.savebinaryfile('{}002/SIPN2_SIT_002_{}.bin'.format(exportpath,self.datestring),iceLastDateMean)
			CryoIO.savebinaryfile('{}003/SIPN2_SIT_003_{}.bin'.format(exportpath,self.datestring),iceLastDateHigh)
			
			
			# save binary SIC maps
			exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2021-22_Submission/'
			CryoIO.savebinaryfile('{}001/SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
			CryoIO.savebinaryfile('{}002/SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
			CryoIO.savebinaryfile('{}003/SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)

# =============================================================================
# 			#SIC export for error analysis
# 			CryoIO.savebinaryfile('analysis/predict/SIPN2_{}.bin'.format(self.datestring),sicmap)
# =============================================================================
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,self.yearday, self.base_back_radiation)
#			print(count)
			if count < countmax:
				self.advanceday(1)
			
	def advanceday(self,delta):	
		self.icedrift_sim = max(7,self.icedrift_sim - 0.04)
		self.base_back_radiation += 0.01
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
	def early_recalibrate(self,iceobserved):
		''' optional recalibration with latest observed SIC data'''
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
					
	def calc_driftcorrection(self,drifterror,SIT):
		''' finetuning values for icedrift mask'''
		if abs(drifterror) > 0.9:
			multi = 4
		elif abs(drifterror) > 0.82:
			multi = 3
		elif abs(drifterror) > 0.75:
			multi = 2
		elif abs(drifterror) > 0.7:
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

	def meltcalc(self,iceforecast,icedrift_error,icearray,bottommelt):
		''' main melting algorithm '''
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		
		sicmapg = np.array(np.zeros(len(icearray),dtype=np.uint8))
		extent = 0
		area = 0
		calcvolume = 0
		for x in range (0,arraylength):
			if self.regmaskf[x] < 11:
				if self.latmaskf[x] < -56:
					pixlat = min(-40,self.latmaskf[x])
					indexx = int(round((pixlat+40)*(-5)))
					
					''' finetuning values for icedrift mask'''
					driftcorrection = self.icedrift_sim
					if self.latmaskf[x] > -65: #higher correction in Weddell Sea
						driftcorrection = driftcorrection * 2.5
					elif self.latmaskf[x] > -70: #higher correction in Weddell Sea
						driftcorrection = driftcorrection * 2
					driftcorrection = driftcorrection * self.calc_driftcorrection(icedrift_error[x],icearray[x])
					
					MJ = self.latitudelist[indexx][self.yearday]*(1-iceforecast[x])-self.back_radiation + bottommelt + driftcorrection * icedrift_error[x]
					icearray[x] = max(-2,icearray[x]-MJ/self.icemeltenergy)
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
		''' Exporting values option 1 '''
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2021-22_Submission/'
		CryoIO.csv_columnexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
		CryoIO.csv_columnexport('{}_SIPN_forecast_003_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
		CryoIO.csv_columnexport('{}_SIPN_forecast_001_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])

	def csvexport_by_measure(self):
		''' Export values option 2 '''
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2021-22_Submission/'
# =============================================================================
# 		CryoIO.csv_columnexport('{}__SIPN_forecast_Volume{}.csv'.format(exportpath,self.year),
# 				[self.CSVDatum,self.CSVVolumeLow,self.CSVVolume,self.CSVVolumeHigh])
# =============================================================================
		CryoIO.csv_columnexport('{}__SIPN_forecast_Area{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAreaLow,self.CSVArea,self.CSVAreaHigh])
		CryoIO.csv_columnexport('{}__SIPN_forecast_Extent{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVExtentLow,self.CSVExtent,self.CSVExtentHigh])
		
	def csvexport_submission_format(self):
		''' Exporting values option 3 '''
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2021-22_Submission/'
		import csv
		with open(f'{exportpath}NicoSun_001_total-area.txt', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows([self.CSVAreaLow])
		with open(f'{exportpath}NicoSun_002_total-area.txt', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows([self.CSVArea])
		with open(f'{exportpath}NicoSun_003_total-area.txt', 'w', newline='') as f:
			writer = csv.writer(f)
			writer.writerows([self.CSVAreaHigh])

		
		
	def getvolume (self,thickness,daycount,day,month,year):
		''' first day initialisation '''
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
		
# 		filename = 'X:/NSIDC_south/DataFiles/NSIDC_{}_south.bin'.format(lastday)
		filename = 'SIPN_init_20211130_south.bin'
		
		self.iceLastDate = CryoIO.openfile(filename, np.uint8)/250

		# Landmask initialisation
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 7:
				self.iceLastDate[x] = 9
		
		# thickness initialisation
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] < 7:
				if 0.25 < self.iceLastDate[x] <= 1 and self.latmaskf[x] < -56:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]
				elif 0.1 < self.iceLastDate[x] < 0.25 and self.latmaskf[x] < -56:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]+0.05
				else:
					self.iceLastDate[x] = 0
			if self.regmaskf[x] < 1:
				self.iceLastDate[x] = 0

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')

		self.prediction()  # start dayloop
		end = time.time()
		print(end-self.starttime)
# 		self.csvexport_by_forecasttype()
# 		self.csvexport_by_measure()
# =============================================================================
# 		self.thicknessshow(self.iceLastDate,5,4,'end')
# 		self.concentrationshow(ice,5,4,'end')
# =============================================================================
#		plt.show()
		

	
if __name__ == '__main__':
	
# =============================================================================
# import SIPN_analysis_south
# visualize = SIPN_analysis_south.NSIDC_analysis()
# visualize.conmap_create()
# =============================================================================
	thickness = 1.44
	year = 2021
	month = 11
	day = 30
	daycount = 91 # 91 days
	# runs single year forecast
	action = NSIDC_prediction()
	action.getvolume(thickness,daycount,day,month,year) 
	action.csvexport_by_measure()
	action.csvexport_submission_format()

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