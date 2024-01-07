'''
This script calculates the Sea Ice Forecast. All model values have been tuned with the _tuning script.

@author: Nico Sun

'''


import numpy as np
import os
import CryoIO

from datetime import date
from datetime import timedelta
import time
import SIPN_analysis


class NSIDC_prediction:

	def __init__  (self):
		self.start = date(2016, 1, 1)
		self.loopday	= self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		
		self.masksload()
		
		self.sic_cutoff = 0.09 # thickness in meter
		self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		self.gridvolumefactor = 625*0.001
		self.base_back_radiation = 6.6 #default: 6 (MJ)
		self.base_bottommelt = 3.3 #default: 3.5 (MJ)
		self.icedrift_sim = 6 # (MJ)
		self.airtemp_mod = 0.75
		
		self.CSVDatum = ['Date']
		self.CSVVolume =  ['Volume']
		self.CSVExtent = ['Extent']
		self.CSVArea = ['Area']
		
		self.CSVVolumeHigh =  ['VolumeHigh']
		self.CSVExtentHigh = ['ExtentHigh']
		self.CSVAreaHigh = ['AreaHigh']
		
		self.CSVVolumeLow =  ['VolumeLow']
		self.CSVExtentLow = ['ExtentLow']
		self.CSVAreaLow = ['AreaLow']
		
		self.CSVAlaska = ['Alaska']
		self.starttime = time.time()
		
	
	def masksload(self):
		''' Loads NSIDC masks and Daily Solar Energy Data'''
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		self.regmaskf = CryoIO.openfile(filename,np.uint32)

		filename = 'X:/NSIDC/Masks/psn25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000

		filename= 'X:/NSIDC/Masks/psn25lats_v3.dat'
		self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
		
		filename = 'X:/NSIDC/Masks/psn25lons_v3.dat'
		self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000
	
		
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ_all_year.csv', delimiter=',')
		self.co2list = np.loadtxt('X:/NSIDC/Masks/Global_CO2_forecast.csv', delimiter=',')
		self.templist = np.loadtxt('X:/NSIDC/Masks/DMI_Temp_80N.csv', delimiter=',')
		
	def prediction(self):
		''' Starts the day loop'''
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(self.datestring)
		countmax = self.index+self.daycount
		
		iceforecast = CryoIO.openfile(os.path.join(filepath,filename),np.uint8)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}.bin'.format(self.datestring)
			filenameAvg = 'X:/NSIDC/DataFiles/Forecast_Manual/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'X:/NSIDC/DataFiles/Forecast_SIC_change/NSIDC_SIC_Change_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'X:/NSIDC/DataFiles/Forecast_Stdv/NSIDC_Stdv_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameDrift_error = 'analysis/icedrift_correction/SIPN2_error_{}{}.bin'.format(self.stringmonth,self.stringday)

			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 2 * co2value / 338
			
			self.air_temp = (self.templist[count]-273) * self.airtemp_mod
			
			self.bottommelt = self.base_bottommelt * self.meltmomentum / 180
			bottommelt = self.bottommelt * 1
			bottommeltHigh = self.bottommelt * 0.9
			bottommeltLow = self.bottommelt * 1.1
			
			driftcorrection = self.icedrift_sim * 1
			driftcorrectionLow = self.icedrift_sim * 0.9
			driftcorrectionHigh = self.icedrift_sim * 1.1
			
			icedrift_error = CryoIO.openfile(filenameDrift_error,np.float16)/100
			icedrift_error = icedrift_error
			
			#fileformats: normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			
			if count <= 224: #change date of year to last available date
				iceforecast = CryoIO.openfile(os.path.join(filepath,filename),np.uint8)/250
				
				
				if 220 <= count <= 224:
					self.august_recalibrate(iceforecast)
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecast,icedrift_error,self.iceMean,count,bottommelt,driftcorrection)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecast,icedrift_error,self.iceHigh,count,bottommeltHigh,driftcorrectionHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecast,icedrift_error,self.iceLow,count,bottommeltLow,driftcorrectionLow)
				
			else:
				#load statistical data
				icechange = CryoIO.openfile(filenameChange,np.int8)/250
				iceAvg = CryoIO.openfile(filenameAvg,np.uint8)/250
				iceStdv = CryoIO.openfile(filenameStdv,np.float16)/250
			
				iceforecast = iceforecast + icechange
				iceforecastMean = (3*iceforecast+iceAvg)/4
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.1)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.3)
				
				iceforecastMean[iceforecastMean > 1] = 1
				iceforecastHigh[iceforecastHigh > 1] = 1
				iceforecastLow[iceforecastLow > 1] = 1
				iceforecastMean[iceforecastMean < 0] = 0
				iceforecastHigh[iceforecastHigh < 0] = 0
				iceforecastLow[iceforecastLow < 0] = 0
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecastMean,icedrift_error,self.iceMean,count,bottommelt,driftcorrection)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecastHigh,icedrift_error,self.iceHigh,count,bottommeltHigh,driftcorrectionHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecastLow,icedrift_error,self.iceLow,count,bottommeltLow,driftcorrectionLow)
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(int(extent)/1e6)
			self.CSVArea.append(int(area)/1e6)
			
			self.CSVVolumeHigh.append(int(calcvolumeHigh))
			self.CSVExtentHigh.append(int(extentHigh)/1e6)
			self.CSVAreaHigh.append(int(areaHigh)/1e6)
			
			self.CSVVolumeLow.append(int(calcvolumeLow))
			self.CSVExtentLow.append(int(extentLow)/1e6)
			self.CSVAreaLow.append(int(areaLow)/1e6)
			self.CSVAlaska.append((int(alaska)/1e6))
			
			if count > (countmax-82):
	#			visualize.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
				visualize.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
				visualize.fig2.savefig('Images/{}'.format(self.datestring))
			
			
# =============================================================================
# 			#save last date as arrary in mm
# 			if count == (countmax-15):
# #			if count >210:
# #				SIPN_analysis.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
# 				SIPN_analysis.concentrationshow(sicmap,int(area),int(extent),'Mean')
# 				
# #				SIPN_analysis.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
# 				SIPN_analysis.concentrationshow(sicmapHigh,int(areaHigh),int(extentHigh),'High')
# 
# #				SIPN_analysis.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
# 				SIPN_analysis.concentrationshow(sicmapLow,int(areaLow),int(extentLow),'Low')
# =============================================================================
				
# =============================================================================
# 				# convert SIT into millimeter
# 				iceLastDateMean = self.iceMean*1000
# 				iceLastDateMean = np.array(iceLastDateMean,dtype=np.uint16)
# 				iceLastDateHigh = self.iceHigh*1000
# 				iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.uint16)
# 				iceLastDateLow = self.iceLow*1000
# 				iceLastDateLow = np.array(iceLastDateLow,dtype=np.uint16)
# =============================================================================
			
			
# =============================================================================
# 			# save binary SIT maps
# 			exportpath = 'X:/Sea_Ice_Forecast/Data_Dump/'
# 			CryoIO.savebinaryfile('{}001/SIPN2_Thickness_Mean_{}.bin'.format(exportpath,self.datestring),iceLastDateMean)
# 			CryoIO.savebinaryfile('{}002/SIPN2_Thickness_midHigh_{}.bin'.format(exportpath,self.datestring),iceLastDateHigh)
# 			CryoIO.savebinaryfile('{}003/SIPN2_Thickness_midLow_{}.bin'.format(exportpath,self.datestring),iceLastDateLow)
# =============================================================================
			
			# save binary SIC maps
			exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/'
			CryoIO.savebinaryfile('{}001/SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
			CryoIO.savebinaryfile('{}002/SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
			CryoIO.savebinaryfile('{}003/SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)
			
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,count)
#			print(self.meltmomentum)
			
# =============================================================================
# 			# optional image export
# 			if count == (countmax-1):
# #				SIPN_analysis.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
# 				SIPN_analysis.concentrationshow(sicmap,int(area),int(extent),'Mean')
# #				SIPN_analysis.fig.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_{}.png'.format(self.datestring))
# 				SIPN_analysis.fig2.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_SIC_{}.png'.format(self.datestring))
# #				SIPN_analysis.ax.clear()
# 				SIPN_analysis.ax2.clear()
# =============================================================================

			# model value adjustment over time
			if count < countmax:
				self.advanceday(1)
				self.icedrift_sim = 6 + count / 150
				if count < 245:
					self.meltmomentum +=1.5
				elif 245 <= count <= 250:
					self.meltmomentum -=22
				elif 252 <= count <= 278:
					self.meltmomentum -=12
					
				if count == 182:
					self.airtemp_mod = 0.25
				elif count == 270:
					self.airtemp_mod = 1.11
				elif count == 280:
					self.airtemp_mod = 1.33

			
	def advanceday(self,delta):
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
		
	def august_recalibrate(self,iceobserved):
		''' optional recalibration in August with latest observed SIC data'''
		thickness = 1.37
		for x in range (0,len(iceobserved)):
			if 1 < self.regmaskf[x] < 16:
				if iceobserved[x] > 0.15:
					iceobserved[x] = thickness*iceobserved[x]*(self.latmaskf[x]/75)
				else:
					iceobserved[x] = 0
				self.iceMean[x] = (2*self.iceMean[x]+iceobserved[x])/3
				self.iceHigh[x] = (2*self.iceHigh[x]+iceobserved[x])/3
				self.iceLow[x] = (2*self.iceLow[x]+iceobserved[x])/3
					
		return
	
	def calc_driftcorrection(self,drifterror,SIT):
		''' finetuning values for icedrift mask'''
		if abs(drifterror) > 0.9:
			multi = 5
		elif abs(drifterror) > 0.82:
			multi = 3.5
		elif abs(drifterror) > 0.75:
			multi = 2.2
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


	def meltcalc(self,iceforecast,icedrift_error,icearray,count,bottommelt,basedriftcorrection):
		''' main melting algorithm '''
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		MJ_adjust = bottommelt - self.back_radiation
		
		sicmapg = np.array(self.sicmap)
		extent = 0
		area = 0
		alaska = 0
		calcvolume = 0
		for x in range (0,arraylength):
			if  1 < self.regmaskf[x] < 16:
				if icearray[x] < 5:
					pixlat = max(20,self.latmaskf[x])
					indexx = int(round((pixlat-20)*5))
					driftcorrection = basedriftcorrection
					driftcorrection = driftcorrection * self.calc_driftcorrection(icedrift_error[x],icearray[x])

					MJ = self.latitudelist[indexx][count+1]*(1-min(1,max(0,iceforecast[x]))) + MJ_adjust + driftcorrection * icedrift_error[x]
					MJ_in_thick = MJ/self.icemeltenergy #energy in thickness
					thicknesschange = MJ_in_thick
					if icearray[x] > 0.5 and MJ_in_thick < 0: # low ice growth for thick ice
						thicknesschange = MJ_in_thick * (3-icearray[x])/3 
					icearray[x] = max(-3,icearray[x]-thicknesschange)
					calcvolume += max(0,self.gridvolumefactor*icearray[x])
				if self.sic_cutoff < icearray[x] < 5:
					sicmapg[x] = min(250,(icearray[x])/0.0065)
#					sicmapg[x] = min(250,(icearray[x]**1.3)/0.008)
					extent += self.areamaskf[x]
					area += min(1,sicmapg[x]/250) * self.areamaskf[x]
					if self.regmaskf[x] == 12 or self.regmaskf[x] == 13:
						alaska += self.areamaskf[x]
					
					
		return icearray,sicmapg,extent,area,calcvolume,alaska

		
	def csvexport_by_forecasttype(self):
		''' Exporting values option 1 '''
		exportpathHigh = 'X:/Sea_Ice_Forecast/SIPN_north/'
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/'
		exportpathLow = 'X:/Sea_Ice_Forecast/SIPN_north/'
		CryoIO.csv_columnexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
		CryoIO.csv_columnexport('{}_SIPN_forecast_003_{}.csv'.format(exportpathHigh,self.year),
				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
		CryoIO.csv_columnexport('{}_SIPN_forecast_001_{}.csv'.format(exportpathLow,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])
		
		CryoIO.csv_columnexport('{}_SIPN_forecast_066_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAlaska])

	def csvexport_by_measure(self):
		''' Export values option 2 '''
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/'
		CryoIO.csv_columnexport('{}__SIPN_forecast_Volume{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVVolume,self.CSVVolumeHigh])
		CryoIO.csv_columnexport('{}__SIPN_forecast_Area{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAreaLow,self.CSVArea,self.CSVAreaHigh])
		CryoIO.csv_columnexport('{}__SIPN_forecast_Extent{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVExtentLow,self.CSVExtent,self.CSVExtentHigh])
		
		CryoIO.csv_columnexport('{}_SIPN_forecast_066_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAlaska])
		
		
	def getvolume (self,thickness,daycount,day,month,year):
		''' first day initialisation '''
		self.daycount = daycount
		self.start = date(year,month,day)
		self.loopday	= self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		self.meltmomentum = self.index
				
		print(thickness,'meter')
		
		filename = 'X:/NSIDC/DataFiles/NSIDC_{}.bin'.format(self.datestring)
		
		self.iceLastDate = CryoIO.openfile(filename,np.uint8)/250
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

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')
		self.prediction() # start dayloop
		end = time.time()
		print(end-self.starttime)
#		CryoIO.csv_columnexport_by_forecasttype()
#		plt.show()
		return self.CSVArea,self.CSVExtent
	



visualize = SIPN_analysis.NSIDC_analysis()
#visualize.thickmap_create()
visualize.conmap_create()
thickness = 2.00
year = 2021
action = NSIDC_prediction()
action.getvolume(thickness,153,1,6,year)
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

monthly CO2 data
https://gml.noaa.gov/ccgg/trends/data.html
'''