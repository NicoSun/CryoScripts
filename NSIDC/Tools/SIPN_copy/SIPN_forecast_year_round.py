from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import os
import math

from datetime import date
from datetime import timedelta
import time


class NSIDC_prediction:

	def __init__  (self):
		self.start = date(2016, 1, 1)
		self.loopday	= self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		
		self.daycount = 1 #366year, 186summer
		
		self.masksload()
		self.map_create()
		
		self.meltfactor = 1.25 # MJ adjustment for imported heat
		self.sic_cutoff = 0.09 # thickness in meter
		self.icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		self.gridvolumefactor = 625*0.001
		self.base_back_radiation = 9
		self.base_bottommelt = 4
		
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
		
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(filename, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(mask, dtype=float)
	
		filename = 'X:/NSIDC/Masks/Max_AWP_extent.bin'
		with open(filename, 'rb') as frmsk:
			self.Icemask = np.fromfile(frmsk, dtype=np.uint8)
		
		filename = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(filename, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		filename= 'X:/NSIDC/Masks/psn25lats_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
		
		filename = 'X:/NSIDC/Masks/psn25lons_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask4 = np.fromfile(flmsk, dtype=np.uint32)
		self.lonmaskf = np.array(mask4, dtype=float)/100000
		
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ_all_year.csv', delimiter=',')
		self.co2list = np.loadtxt('X:/NSIDC/Masks/Global_CO2_forecast.csv', delimiter=',')
	
	def dayloop(self):
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(self.datestring)
		countmax = self.index+self.daycount
		
		with open(os.path.join(filepath,filename), 'rb') as frr:
			iceforecast = np.fromfile(frr, dtype=np.uint8)
		iceforecast = np.array(iceforecast, dtype=float)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		
		self.day_of_year = self.index
		self.meltmomentum = self.index

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}.bin'.format(self.datestring)
			filenameAvg = 'DataFiles/Forecast_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}.bin'.format(self.stringmonth,self.stringday)
			
			daystart = time.time()
			
			
			if self.day_of_year < 90:
				self.meltmomentum = 44
			elif self.day_of_year < 150:
				self.meltmomentum += 1.75
			elif self.day_of_year < 250:
				self.meltmomentum +=1.1
			elif self.day_of_year < 260:
				self.meltmomentum -= 5
			elif self.day_of_year < 367:
				self.meltmomentum = max(0.95*self.meltmomentum,44)
			
			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 2.8 * co2value / 338
			self.bottommelt = self.base_bottommelt * self.meltmomentum / 180
			
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			
			if count <= 99999: #change date of year to last available date
				with open(os.path.join(filepath,filename), 'rb') as frr:
					ice2 = np.fromfile(frr, dtype=np.uint8)
				iceforecast = np.array(ice2, dtype=float)/250
				iceforecast = iceforecast
				
				self.reforecast(iceforecast)
				
			else:
				with open(filenameChange, 'rb') as fr:
					icechange = np.fromfile(fr, dtype=np.int8)
				icechange = np.array(icechange, dtype=float)/250
				with open(filenameAvg, 'rb') as fr:
					iceAvg = np.fromfile(fr, dtype=np.uint8)
				iceAvg = np.array(iceAvg, dtype=float)/250
				
				with open(filenameStdv, 'rb') as frr:
					iceStdv = np.fromfile(frr, dtype=np.float16)
				iceStdv = np.array(iceStdv, dtype=float)/250
			
				iceforecast = iceforecast + icechange
				iceforecastMean = (2*iceforecast+iceAvg)/3
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.22)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.38)
				
				self.prediction(iceforecastLow,iceforecastMean,iceforecastHigh)
				print('shit')
			
			end = time.time()
			
#			print(self.bottommelt , self.back_radiation)
			print(self.loopday, self.back_radiation)
			
			if count < countmax:
				self.advanceday(1)


			
	def advanceday(self,delta):
		self.loopday = self.loopday+timedelta(days=delta)
		self.day_of_year = self.loopday.timetuple().tm_yday
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
		
	def reforecast(self,iceforecast):
		bottommelt = self.bottommelt
		
		self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,self.iceMean,bottommelt)
		
		if self.loopday.day==1 or self.loopday.day==15:
			self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
	#		self.concentrationshow(sicmap,int(area),int(extent),'Mean')
			plt.pause(0.01)
#			self.fig.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_{}.png'.format(self.datestring))
	#		self.fig2.savefig('X:/Sea_Ice_Forecast/Data_Dump/SIPN_SIC_{}.png'.format(self.datestring))
			self.ax.clear()
	#		self.ax2.clear()
		
		self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
		self.CSVVolume.append(int(calcvolume))
		self.CSVExtent.append(int(extent)/1e6)
		self.CSVArea.append(int(area)/1e6)
			
			
					
	def prediction(self,iceforecastLow,iceforecastMean,iceforecastHigh,count):
		bottommelt = self.bottommelt
		bottommeltHigh = self.bottommelt * 0.88
		bottommeltLow = self.bottommelt * 1.1
				
		self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecastMean,self.iceMean,bottommelt)
		self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecastHigh,self.iceHigh,bottommeltHigh)
		self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecastLow,self.iceLow,bottommeltLow)

		self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
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
			
# =============================================================================
# 		self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
# 		self.concentrationshow(sicmap,int(area),int(extent),'Mean')
# =============================================================================
		
		#save last date as arrary in mm
#		self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
		self.concentrationshow(sicmap,int(area),int(extent),'Mean')				
#		self.fig.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_Mean.png'.format(self.datestring))
		self.fig2.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_002_SIC.png'.format(self.datestring))
#		self.ax.clear()
		self.ax2.clear()
			
#		self.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
		self.concentrationshow(sicmapHigh,int(areaHigh),int(extentHigh),'High')
#		self.fig.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_High.png'.format(self.datestring))
		self.fig2.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_003_SIC.png'.format(self.datestring))
#		self.ax.clear()
		self.ax2.clear()
		
#		self.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
		self.concentrationshow(sicmapLow,int(areaLow),int(extentLow),'Low')
#		self.fig.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_Low.png'.format(self.datestring))
		self.fig2.savefig('X:/Sea_Ice_Forecast/All_year/Images/{}_SIPN_001_SIC.png'.format(self.datestring))
#		self.ax.clear()
		self.ax2.clear()
			
			
# =============================================================================
# 		iceLastDateMean = self.iceMean*1000
# 		iceLastDateMean = np.array(iceLastDateMean,dtype=np.uint16)
# 		iceLastDateHigh = self.iceHigh*1000
# 		iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.uint16)
# 		iceLastDateLow = self.iceLow*1000
# 		iceLastDateLow = np.array(iceLastDateLow,dtype=np.uint16)
# =============================================================================
		
		
# =============================================================================
# 		# save SIT maps
# 		exportpath = 'X:/Sea_Ice_Forecast/Data_Dump/'
# 		self.savebinaryfile('{}SIPN2_Thickness_Mean_{}.bin'.format(exportpath,self.datestring),iceLastDateMean)
# 		self.savebinaryfile('{}SIPN2_Thickness_midHigh_{}.bin'.format(exportpath,self.datestring),iceLastDateHigh)
# 		self.savebinaryfile('{}SIPN2_Thickness_midLow_{}.bin'.format(exportpath,self.datestring),iceLastDateLow)
# =============================================================================
		
# =============================================================================
# 		# save SIC maps
# 		exportpath = 'X:/Sea_Ice_Forecast/Data_Dump/'
# 		self.savebinaryfile('{}SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
# 		self.savebinaryfile('{}SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
# 		self.savebinaryfile('{}SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)
# =============================================================================
				

	def meltcalc(self,iceforecast,icearray,bottommelt):
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		
		sicmapg = np.array(self.sicmap)
		extent = 0
		area = 0
		calcvolume = 0
		thickness_change = 0
		for x in range (0,arraylength):
			if self.Icemask[x] == 1:
				pixlat = max(20,self.latmaskf[x])
				indexx = int(round((pixlat-20)*5))
				MJ_surface = self.latitudelist[indexx][self.day_of_year]*(1-min(1,max(0,iceforecast[x]))) * self.meltfactor - self.back_radiation
				
				if 0 < icearray[x] < 8.8:
					if MJ_surface > 0: #melt
						thickness_change = (MJ_surface + bottommelt) /self.icemeltenergy
						icearray[x] -= thickness_change
					else:  # freeze
						thickness_change = (MJ_surface / max(1,icearray[x]) + bottommelt)/self.icemeltenergy
						icearray[x] -= thickness_change

				if icearray[x] <= 0:
					MJ_Loss = self.back_radiation * (1 - icearray[x]) - self.back_radiation
					thickness_change = (MJ_surface + bottommelt - MJ_Loss) / self.icemeltenergy
					icearray[x] -= thickness_change
				
				if self.sic_cutoff < icearray[x] < 5:
					sicmapg[x] = min(250,(icearray[x])/0.0065)
#					sicmapg[x] = min(250,(icearray[x]**1.3)/0.008)
					extent += self.areamaskf[x]
					area += min(1,sicmapg[x]/250) * self.areamaskf[x]
					calcvolume += max(0,self.gridvolumefactor*icearray[x])
					
					
		return icearray,sicmapg,extent,area,calcvolume
		

	def thicknessshow(self,icemap,Volumevalue,extentvalue,outlooktype):		
		icemap = np.ma.masked_greater(icemap, 8)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Volumevalue = '{:,}'.format(Volumevalue)+' 'r'$km^3$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.set_title('{}_Forecast , Date: {}-{}-{}'.format(outlooktype,self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Average Forecast')
		self.ax.set_xlabel('Volume: {} / Extent: {}'.format(Volumevalue,extentvalue), fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=3, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		
		
	def concentrationshow(self,icemap,Areavalue,extentvalue,outlooktype):
		icemap = icemap/250
		icemap =np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Areavalue = '{:,}'.format(Areavalue)+' 'r'$km^2$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax2.set_title('{}_Forecast , Date: {}-{}-{}'.format(outlooktype,self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Average Forecast')
		self.ax2.set_xlabel('Area: {} / Extent: {}'.format(Areavalue,extentvalue), fontsize=14)
		self.cax2 = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
		
		
	def map_create(self):
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,0.5,1,1.5,2,2.5,3]).set_label('Sea Ice Thickness in m')
		
# =============================================================================
# 		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
# 		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
# 		self.cbar = self.fig2.colorbar(self.cax2, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
# =============================================================================
		
	def savebinaryfile(self,filename,filedata):
		with open(filename,'wb') as writecumu:
				writecumu.write(filedata)
				
	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
		
	def csvexport_by_forecasttype(self):
		
		exportpathHigh = 'X:/Sea_Ice_Forecast/All_year/'
		exportpath = 'X:/Sea_Ice_Forecast/All_year/'
		exportpathLow = 'X:/Sea_Ice_Forecast/All_year/'
		self.csvexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
# =============================================================================
# 		self.csvexport('{}_SIPN_forecast_003_{}.csv'.format(exportpathHigh,self.year),
# 				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
# 		self.csvexport('{}_SIPN_forecast_001_{}.csv'.format(exportpathLow,self.year),
# 				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])
# =============================================================================


	def csvexport_by_measure(self):
		
		exportpath = 'X:/Sea_Ice_Forecast/All_year/2019/'
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
		
		self.daycount = daycount
		
		print(thickness,'meter')
		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(self.datestring)
		
		with open(os.path.join(filepath,filename), 'rb') as fr:
			ice = np.fromfile(fr, dtype=np.uint8)
		icef = np.array(ice, dtype=float)/250
		self.iceLastDate = np.zeros(len(icef),dtype=np.float)
		self.sicmap = np.zeros(len(icef),dtype=np.uint8)
		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 15:
				self.iceLastDate[x] = 9
				self.sicmap [x] = 255
		
		for x in range (0,len(self.iceLastDate)):
			if self.Icemask[x] == 1:
				if icef[x] > 0.15:
					self.iceLastDate[x] = thickness*icef[x]*(self.latmaskf[x]/75)
			if self.regmaskf[x] < 2:
				self.iceLastDate[x] = 0


		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')
		self.dayloop()
		end = time.time()
		print(end-self.starttime)
		self.csvexport_by_forecasttype()
		plt.show()
	

# =============================================================================
# thicknesslist =[2.79,2.58,2.35,2.61,2.57,2.60,2.67,2.69,2.72,2.58,2.73,2.68,2.56,2.64,2.59,2.54,
# 				2.45,2.59,2.59,2.46,2.43,2.44,2.43,2.38,2.33,2.33,2.32,2.17,2.22,2.16,2.04,1.94,
# 				1.99,1.93,2.01,2.11,2.06,1.84,2.02,1.99] # 1980 start
# =============================================================================

# =============================================================================
# thicknesslist =[2.17,2.22,2.16,2.04,1.94,1.99,1.93,2.01,2.11,2.06,1.84,2.02,1.99] # 2007 start
# 
# 
# 
# def spawnprocess(datalist):
# 	action = NSIDC_prediction()
# 	data = action.getvolume(datalist[1],122,1,6,datalist[0]) #daycount: 122 until 30th Sep
# 	
# 	return data
# 	
# if __name__ == '__main__':
# 	datalist = []
# 	x = 0
# 	for year in range(2007,2019):
# 		datalist.append([year,thicknesslist[x]])
# 		x +=1
# 	
# 	p = Pool(processes=12)
# 	data = p.map(spawnprocess, datalist)
# 	p.close()
# =============================================================================


thicknesslist = 2.82
year = 1979
action = NSIDC_prediction()
action.getvolume(thicknesslist,366*39,1,1,year)
action.csvexport_by_forecasttype()


'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''