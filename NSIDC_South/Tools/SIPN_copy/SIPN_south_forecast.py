from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import os

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
		with open(filename, 'rb') as frmsk:
			mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(mask, dtype=float)
		
		filename = 'X:/NSIDC_South/Masks/pss25area_v3.dat'
		with open(filename, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.int32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		filename = 'X:/NSIDC_South/Masks/pss25lats_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
		
		filename = 'X:/NSIDC_South/Masks/pss25lons_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask4 = np.fromfile(flmsk, dtype=np.int32)
		self.lonmaskf = np.array(mask4, dtype=float)/100000
		
		self.latitudelist = np.loadtxt('X:/NSIDC_South/Masks/Lattable_south_MJ_all_year.csv', delimiter=',')
		self.co2list = np.loadtxt('X:/NSIDC_South/Masks/Global_CO2.csv', delimiter=',')
		
	
	def prediction(self):		
		filepath = 'X:/NSIDC_South/DataFiles/'	
		filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		countmax = self.index+self.daycount
		
		with open(os.path.join(filepath,filename), 'rb') as frr:
			iceforecast = np.fromfile(frr, dtype=np.uint8)
		iceforecast = np.array(iceforecast, dtype=float)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}_south.bin'.format(self.datestring)
			filenameAvg = 'DataFiles/Mean_00_19/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			
			#338ppm base value in 1980
			co2listindex = (self.year-1980)*12 + self.loopday.month-1
			co2value = self.co2list[co2listindex][1]
			self.back_radiation = self.base_back_radiation - 2 * co2value / 338
			
			self.bottommelt = self.base_bottommelt
			bottommelt = self.bottommelt * 1.05
			bottommeltHigh = self.bottommelt * 0.95
			bottommeltLow = self.bottommelt * 1.25
					
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16
			if count <= 300: #change date of year to last available date
				with open(os.path.join(filepath,filename), 'rb') as frr:
					ice2 = np.fromfile(frr, dtype=np.uint8)
				iceforecast = np.array(ice2, dtype=float)/250
				
#				self.early_recalibrate(iceforecast)
				self.meltfactor = 1.4
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,self.iceMean,bottommelt)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecast,self.iceHigh,bottommeltHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecast,self.iceLow,bottommeltLow)
				
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
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.35)
				
				iceforecastMean[iceforecastMean > 1] = 1
				iceforecastMean[iceforecastMean < 0] = 0
				iceforecastHigh[iceforecastHigh > 1] = 1
				iceforecastHigh[iceforecastHigh < 0] = 0
				iceforecastLow[iceforecastLow > 1] = 1
				iceforecastLow[iceforecastLow < 0] = 0
				
				self.meltfactor = 1
				
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,self.iceMean,bottommelt)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecastHigh,self.iceHigh,bottommeltHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecastLow,self.iceLow,bottommeltLow)
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(round(int((extent))/1e6,4))
			self.CSVArea.append(round(int((area))/1e6,4))
			
			self.CSVVolumeHigh.append(int(calcvolumeHigh))
			self.CSVExtentHigh.append(round(int((extentHigh))/1e6,4))
			self.CSVAreaHigh.append(round(int((areaHigh))/1e6,4))
			
			self.CSVVolumeLow.append(int(calcvolumeLow))
			self.CSVExtentLow.append(round(int((extentLow))/1e6,4))
			self.CSVAreaLow.append(round(int((areaLow))/1e6,4))
			
#			self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
#			self.concentrationshow(sicmap,int(area),int(extent),'Mean')
			
# =============================================================================
# 			#save last date as arrary in mm
# 			if count == (countmax-15):
# #			if count >210:
# 				self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
# #				self.concentrationshow(sicmap,int(area),int(extent),'Mean')				
# #				self.fig.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_Mean.png'.format(self.datestring))
# 				self.fig2.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_002_SIC.png'.format(self.datestring))
# #				self.ax.clear()
# 				self.ax2.clear()
# 				
# #				self.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
# 				self.concentrationshow(sicmapHigh,int(areaHigh),int(extentHigh),'High')
# #				self.fig.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_High.png'.format(self.datestring))
# 				self.fig2.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_003_SIC.png'.format(self.datestring))
# #				self.ax.clear()
# 				self.ax2.clear()
# 				
# #				self.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
# 				self.concentrationshow(sicmapLow,int(areaLow),int(extentLow),'Low')
# #				self.fig.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_Low.png'.format(self.datestring))
# 				self.fig2.savefig('X:/Sea_Ice_Forecast/SIPN_south/Images/{}_SIPN_001_SIC.png'.format(self.datestring))
# #				self.ax.clear()
# 				self.ax2.clear()
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
			
			# save SIC maps
			exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2019-20_submission/'
			self.savebinaryfile('{}001/SIPN2_SIC_001_{}.bin'.format(exportpath,self.datestring),sicmapLow)
			self.savebinaryfile('{}002/SIPN2_SIC_002_{}.bin'.format(exportpath,self.datestring),sicmap)
			self.savebinaryfile('{}003/SIPN2_SIC_003_{}.bin'.format(exportpath,self.datestring),sicmapHigh)
			
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
		

	def thicknessshow(self,icemap,Volumevalue,extentvalue,outlooktype):		
		icemap = np.ma.masked_greater(icemap, 5)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Volumevalue = '{:,}'.format(Volumevalue)+' 'r'$km^3$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
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
#		self.fig.savefig('X:/Sea_Ice_Forecast/SIPN_south/SIPN_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(1.01)
		
	def concentrationshow(self,icemap,Areavalue,extentvalue,outlooktype):
		icemap = icemap/250
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Areavalue = '{:,}'.format(Areavalue)+' 'r'$km^2$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax2.clear()
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
#		self.fig2.savefig('X:/Sea_Ice_Forecast/SIPN_south/SIPN_SIC_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(0.01)
		
	def map_create(self):
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 8))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,0.5,1,1.5,2,2.5,3]).set_label('Sea Ice Thickness in m')
		
# =============================================================================
# 		self.fig2, self.ax2 = plt.subplots(figsize=(8, 8))
# 		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
# 		self.cbar = self.fig2.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
# =============================================================================
			
	def savebinaryfile(self,filename,filedata):
		with open(filename,'wb') as writer:
				writer.write(filedata)
				
	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
		
	def csvexport_by_forecasttype(self):
		
		exportpathHigh = 'X:/Sea_Ice_Forecast/SIPN_south/2019-20_submission/'
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2019-20_submission/'
		exportpathLow = 'X:/Sea_Ice_Forecast/SIPN_south/2019-20_submission/'
		self.csvexport('{}_SIPN_forecast_002_{}.csv'.format(exportpath,self.year),
				[self.CSVDatum,self.CSVVolume,self.CSVArea,self.CSVExtent])
		self.csvexport('{}_SIPN_forecast_003_{}.csv'.format(exportpathHigh,self.year),
				[self.CSVDatum,self.CSVVolumeHigh,self.CSVAreaHigh,self.CSVExtentHigh])
		self.csvexport('{}_SIPN_forecast_001_{}.csv'.format(exportpathLow,self.year),
				[self.CSVDatum,self.CSVVolumeLow,self.CSVAreaLow,self.CSVExtentLow])


	def csvexport_by_measure(self):
		
		exportpath = 'X:/Sea_Ice_Forecast/SIPN_south/2019-20_submission/'
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
		lastday = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		self.yearday = self.loopday.timetuple().tm_yday
		
		self.daycount = daycount
		
		print(thickness,'meter')
		
		filepath = 'X:/NSIDC_south/DataFiles/'	
		filename = 'NSIDC_{}_south.bin'.format(lastday)
		
		with open(os.path.join(filepath,filename), 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
		self.iceLastDate = np.array(ice, dtype=float)/250
		
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