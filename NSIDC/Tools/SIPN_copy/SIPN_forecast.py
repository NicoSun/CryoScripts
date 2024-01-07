from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import os

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
		
		self.daycount = 1 #366year, 186summer
		
		self.masksload()
		
		self.sic_cutoff = 0.09 # thickness in meter
		self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		self.gridvolumefactor = 625*0.001
		self.base_back_radiation = 6 #default: 6 (MJ)
		self.base_bottommelt = 3.3 #default: 3.3 (MJ)
		self.icedrift_sim = 2 # (MJ)
		
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
		
	
	def openfile(self,filename,fileformat):
		with open((filename), 'rb') as fr:
			data = np.fromfile(fr, dtype=fileformat)
			data = np.array(data, dtype=float)
		return data
	
	def masksload(self):
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		self.regmaskf = self.openfile(filename,np.uint32)

		filename = 'X:/NSIDC/Masks/psn25area_v3.dat'
		self.areamaskf = self.openfile(filename,np.uint32)/1000

		filename= 'X:/NSIDC/Masks/psn25lats_v3.dat'
		self.latmaskf = self.openfile(filename,np.uint32)/100000
		
		filename = 'X:/NSIDC/Masks/psn25lons_v3.dat'
		self.lonmaskf = self.openfile(filename,np.uint32)/100000
	
		
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ_all_year.csv', delimiter=',')
		self.co2list = np.loadtxt('X:/NSIDC/Masks/Global_CO2_forecast.csv', delimiter=',')
		
	def prediction(self):		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(self.datestring)
		countmax = self.index+self.daycount
		
		iceobserved = self.openfile(os.path.join(filepath,filename),np.uint8)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}.bin'.format(self.datestring)
			filenameAvg = 'X:/NSIDC/DataFiles/Forecast_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'X:/NSIDC/DataFiles/Forecast_SIC_change/NSIDC_SIC_Change_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'X:/NSIDC/DataFiles/Forecast_Stdv/NSIDC_Stdv_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameDrift_error = 'icedrift_correction/SIPN2_error_{}{}.bin'.format(self.stringmonth,self.stringday)

			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 2 * co2value / 338
			
			self.bottommelt = self.base_bottommelt * self.meltmomentum / 180
			bottommelt = self.bottommelt * 1
			bottommeltHigh = self.bottommelt * 0.9
			bottommeltLow = self.bottommelt * 1.1
			
			icedrift_error = self.openfile(filenameDrift_error,np.float16)/100
			icedrift_error = icedrift_error
			
			
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			
			if count <= 300: #change date of year to last available date
				iceforecast = self.openfile(os.path.join(filepath,filename),np.uint8)/250
				
				
# =============================================================================
# 				if 220 <= count <= 225:
# 					self.august_recalibrate(iceforecast)
# =============================================================================
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecast,icedrift_error,self.iceMean,count,bottommelt)
# =============================================================================
# 				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecast,icedrift_error,self.iceHigh,count,bottommeltHigh)
# 				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecast,icedrift_error,self.iceLow,count,bottommeltLow)
# =============================================================================
				
			else:
				#load statistical data
				icechange = self.openfile(filenameChange,np.int8)/250
				iceAvg = self.openfile(filenameAvg,np.uint8)/250
				iceStdv = self.openfile(filenameStdv,np.float16)/250
			
				iceforecast = iceforecast + icechange
				iceforecastMean = (3*iceforecast+iceAvg)/4
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.2)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.38)
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecastMean,icedrift_error,self.iceMean,count,bottommelt)
# =============================================================================
# 				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecastHigh,icedrift_error,self.iceHigh,count,bottommeltHigh)
# 				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecastLow,icedrift_error,self.iceLow,count,bottommeltLow)
# =============================================================================
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(int(extent)/1e6)
			self.CSVArea.append(int(area)/1e6)
			
# =============================================================================
# 			self.CSVVolumeHigh.append(int(calcvolumeHigh))
# 			self.CSVExtentHigh.append(int(extentHigh)/1e6)
# 			self.CSVAreaHigh.append(int(areaHigh)/1e6)
# 			
# 			self.CSVVolumeLow.append(int(calcvolumeLow))
# 			self.CSVExtentLow.append(int(extentLow)/1e6)
# 			self.CSVAreaLow.append(int(areaLow)/1e6)
# 			self.CSVAlaska.append((int(alaska)/1e6))
# =============================================================================
			
#			SIPN_analysis.action.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean',self.datestring)
#			SIPN_analysis.action.concentrationshow(sicmap,int(area),int(extent),'Mean',self.datestring)
			
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
# 			self.savebinaryfile('{}001/SIPN2_Thickness_Mean_{}.bin'.format(exportpath,self.datestring),iceLastDateMean)
# 			self.savebinaryfile('{}002/SIPN2_Thickness_midHigh_{}.bin'.format(exportpath,self.datestring),iceLastDateHigh)
# 			self.savebinaryfile('{}003/SIPN2_Thickness_midLow_{}.bin'.format(exportpath,self.datestring),iceLastDateLow)
# =============================================================================
			
# =============================================================================
# 			# save SIC maps
# 			exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/'
# 			self.savebinaryfile('{}001/SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
# 			self.savebinaryfile('{}002/SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
# 			self.savebinaryfile('{}003/SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)
# =============================================================================
			
			#SIC export for error analysis
			self.savebinaryfile('predict/SIPN2_{}.bin'.format(self.datestring),sicmap)
				
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,count)
#			print(self.meltmomentum)
			
# =============================================================================
# 			if count == (countmax-1):
# #				self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
# 				self.concentrationshow(sicmap,int(area),int(extent),'Mean')
# #				self.fig.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_{}.png'.format(self.datestring))
# 				self.fig2.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_SIC_{}.png'.format(self.datestring))
# #				self.ax.clear()
# 				self.ax2.clear()
# =============================================================================

			if count < countmax:
				self.advanceday(1)
				self.icedrift_sim = 6 * count / 150
				if count < 245:
					self.meltmomentum +=1.3
				elif 245 <= count <= 252:
					self.meltmomentum -=25
				elif 252 <= count <= 275:
					self.meltmomentum -=10
					self.icedrift_sim = 14

			
	def advanceday(self,delta):
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
		
	def august_recalibrate(self,iceobserved):
		thickness = 1.4
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


	def meltcalc(self,iceforecast,icedrift_error,icearray,count,bottommelt):
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		driftcorrection = self.icedrift_sim
		
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
					if icearray[x] < 0.1 and icedrift_error[x] < 0:
						driftcorrection = self.icedrift_sim *2 # icefree area accelerated re-freeze
					elif icearray[x] < 0.5 and icedrift_error[x] > 0.2:
						driftcorrection = self.icedrift_sim *0.66 # thin ice slow down melt if overpredict ice
					MJ = self.latitudelist[indexx][count+1]*(1-min(1,max(0,iceforecast[x]))) - self.back_radiation + bottommelt + driftcorrection * icedrift_error[x]
					thicknesschange = MJ/self.icemeltenergy #thickness_change
					icearray[x] = max(-2,icearray[x]-thicknesschange)
					calcvolume += max(0,self.gridvolumefactor*icearray[x])
				if self.sic_cutoff < icearray[x] < 5:
					sicmapg[x] = min(250,(icearray[x])/0.0065)
#					sicmapg[x] = min(250,(icearray[x]**1.3)/0.008)
					extent += self.areamaskf[x]
					area += min(1,sicmapg[x]/250) * self.areamaskf[x]
					if self.regmaskf[x] == 12 or self.regmaskf[x] == 13:
						alaska += self.areamaskf[x]
					
					
		return icearray,sicmapg,extent,area,calcvolume,alaska
		

		
		
	def savebinaryfile(self,filename,filedata):
		with open(filename,'wb') as writer:
				writer.write(filedata)
				
	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
		
	def csvexport_by_forecasttype(self):
		
		exportpathHigh = 'X:/Sea_Ice_Forecast/SIPN_north/'
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/'
		exportpathLow = 'X:/Sea_Ice_Forecast/SIPN_north/'
		self.csvexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
		self.csvexport('{}_SIPN_forecast_003_{}.csv'.format(exportpathHigh,self.year),
				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
		self.csvexport('{}_SIPN_forecast_001_{}.csv'.format(exportpathLow,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])
		
		self.csvexport('{}_SIPN_forecast_066_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAlaska])

	def csvexport_by_measure(self):
		
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_north/2019/'
		self.csvexport('{}__SIPN_forecast_Volume{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVVolume,self.CSVVolumeHigh])
		self.csvexport('{}__SIPN_forecast_Area{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVAreaLow,self.CSVArea,self.CSVAreaHigh])
		self.csvexport('{}__SIPN_forecast_Extent{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVExtentLow,self.CSVExtent,self.CSVExtentHigh])
		
		
	def getvolume (self,thickness,daycount,day,month,year):
		self.daycount = daycount
		self.start = date(year,month,day)
		self.loopday	= self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		self.meltmomentum = self.index
		
		self.daycount = daycount
		
		print(thickness,'meter')
		
		filepath = 'X:/NSIDC/DataFiles/'
		filename = 'NSIDC_{}.bin'.format(self.datestring)
		
		self.iceLastDate = self.openfile(os.path.join(filepath,filename),np.uint8)/250
		self.sicmap = np.zeros(len(self.iceLastDate),dtype=np.uint8)
		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 15:
				self.iceLastDate[x] = 9
				self.sicmap [x] = 255
		
		for x in range (0,len(self.iceLastDate)):
			if 1 < self.regmaskf[x] < 16:
				if self.iceLastDate[x] > 0.15:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]*(self.latmaskf[x]/75)
			if self.regmaskf[x] < 2:
				self.iceLastDate[x] = 0

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')
		self.prediction()
		end = time.time()
		print(end-self.starttime)
#		self.csvexport_by_forecasttype()
#		plt.show()
		return self.CSVArea,self.CSVExtent
	

# =============================================================================
# thicknesslist =[2.79,2.58,2.35,2.61,2.57,2.60,2.67,2.69,2.72,2.58,2.73,2.68,2.56,2.64,2.59,2.54,
# 				2.45,2.59,2.59,2.46,2.43,2.44,2.43,2.38,2.33,2.33,2.32,2.17,2.22,2.16,2.04,1.94,
# 				1.99,1.93,2.01,2.11,2.06,1.84,2.02,1.99] # 1980 start
# =============================================================================

thicknesslist =[2.17,2.22,2.16,2.04,1.94,1.99,1.93,2.01,2.11,2.06,1.84,2.02,1.99,2.07] # 2007 start



def spawnprocess(datalist):
	action = NSIDC_prediction()
	area,extent = action.getvolume(datalist[1],122,1,6,datalist[0]) #daycount: 122 until 30th Sep
	
	return area,extent
	
if __name__ == '__main__':
	datalist = []
	x = 0
	for year in range(2007,2020):
		datalist.append([year,thicknesslist[x]])
		x +=1
	
	p = Pool(processes=13)
	data = p.map(spawnprocess, datalist)
	print(len(data))
	p.close()
	
	area = []
	extent = []
	for x in data:
		area.append(x[0])
		extent.append(x[1])
		
	action = NSIDC_prediction()
	action.csvexport('area.csv',area)
	action.csvexport('extent.csv',extent)


# =============================================================================
# SIPN_analysis.action.thickmap_create()
# thicknesslist = 2.07
# year = 2019
# action = NSIDC_prediction()
# action.getvolume(thicknesslist,122,1,6,year)
# #action.csvexport_by_forecasttype()
# =============================================================================


'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''