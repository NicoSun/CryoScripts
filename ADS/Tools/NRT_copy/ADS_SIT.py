"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the sea ice thickness from the formatted ADS SIT data ( with File_Mangaer)
"""
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
import time
import CryoIO
import gzip

import ADS_SIT_maps



class ADS_data:

	def __init__  (self):
		'''initializes the melt algorithm'''
		self.start = date(2012, 7, 3)
		self.year = self.start.year
		self.stringmonth = str(self.start.month).zfill(2)
		self.stringday = str(self.start.day).zfill(2)
		self.daycount = 5 #total length: 3620 (May 2022)
		
		self.CSVDatum = ['Date']
		self.CSVVolume =['Volume']
		self.CSVThickness =['Thickness']
		
		#melt melt algorithm hyperparameters
		self.meltrate = 5
		self.freezerate = 2.2
		self.first_freeze_thickness = 20 # centimeter*(1-melt percentage)
		self.min_melt_thickness = 25 #cm 
		self.thicknesschange = 6.6 #cm per day
		self.max_thickness = 400 #cm
		
		#Poleholelist
		Columns = ['hole']
		csvdata = pd.read_csv('Tools/zzz_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		
		Columns = ['edge']
		csvdata = pd.read_csv('Tools/zzz_poleholeEdge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		
		Columns = ['A','B','C']
		csvdata = pd.read_csv('Tools/zzz_SIT_Mean.csv', names=Columns)
		self.anom_date = csvdata.A.tolist()
		self.mean_volume = csvdata.B.tolist()
		self.mean_thickness = csvdata.C.tolist()
		
		self.meandict = {}
		
		for index,value in enumerate(self.anom_date):
			self.meandict[value] = [self.mean_volume[index],self.mean_thickness[index]]
		
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		
	def loadgzip(self,filename):
		with gzip.open(filename, mode='rb') as fr:
			from_gzipped = np.frombuffer(fr.read(), dtype=np.uint16)
		return from_gzipped
		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		self.landmask = CryoIO.openfile(landmaskfile,np.uint8)

		latlonmaskfile = 'Masks/latlon_low.map'
		latlonmask = CryoIO.openfile(latlonmaskfile,np.uint16)
		self.latmaskf = 0.01*latlonmask[:810000] 
		self.lonmaskf = 0.01*latlonmask[810000]
		
		regionmaskfile = 'Masks/Regionmask.map'
		self.regionmask = CryoIO.openfile(regionmaskfile,np.uint8)
		
		
	def polehole(self,ice):
		'''calculates the pole hole'''
		#polehole calc
		icepolecon = []
		
		for val in self.icepoleedge:
			icepolecon.append(min(self.max_thickness,ice[val]))
		#
		icepolecon = np.mean(icepolecon)
		for val2 in self.icepole:
			ice[val2] = icepolecon
		
		return ice
	
	def csvdata(self,icethickess,iceanom,datestrings):
		dictstring = '2016-{}-{}'.format(datestrings[1],datestrings[2])
		datestring = '{}-{}-{}'.format(datestrings[0],datestrings[1],datestrings[2])
		
		Regions_vol = {}
		Regions_thick = {}

		Regions_vol['total'] = []
		Regions_vol['SoO'] = []
		Regions_vol['BerS'] = []
		Regions_vol['Hudson'] = []
		Regions_vol['Baffin'] = []
		Regions_vol['Green'] = []
		Regions_vol['Barents'] = []
		Regions_vol['Kara'] = []
		Regions_vol['Laptev'] = []
		Regions_vol['EastS'] = []
		Regions_vol['Chuck'] = []
		Regions_vol['BeaS'] = []
		Regions_vol['Canada'] = []
		Regions_vol['Central'] = []

		
		Regions_thick['total'] = []
		Regions_thick['SoO'] = []
		Regions_thick['BerS'] = []
		Regions_thick['Hudson'] = []
		Regions_thick['Baffin'] = []
		Regions_thick['Green'] = []
		Regions_thick['Barents'] = []
		Regions_thick['Kara'] = []
		Regions_thick['Laptev'] = []
		Regions_thick['EastS'] = []
		Regions_thick['Chuck'] = []
		Regions_thick['BeaS'] = []
		Regions_thick['Canada'] = []
		Regions_thick['Central'] = []


		#restricts the final thickness and volume data to north of 50N
		for index,value in enumerate(icethickess):
			if 0 < value < 501 and 10 < self.regionmask[index] < 60:
				gridvolume = value/1e5*100
				Regions_vol['total'].append  (gridvolume)
				Regions_thick['total'].append (value)
				if 0 < value < 501 and self.regionmask[index]==20:
					Regions_vol['SoO'].append(gridvolume)
					Regions_thick['SoO'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==22:
					Regions_vol['BerS'].append(gridvolume)
					Regions_thick['BerS'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==24:
					Regions_vol['Hudson'].append(gridvolume)
					Regions_thick['Hudson'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==26:
					Regions_vol['Baffin'].append(gridvolume)
					Regions_thick['Baffin'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==28:
					Regions_vol['Green'].append(gridvolume)
					Regions_thick['Green'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==30:
					Regions_vol['Barents'].append(gridvolume)
					Regions_thick['Barents'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==32:
					Regions_vol['Kara'].append(gridvolume)
					Regions_thick['Kara'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==34:
					Regions_vol['Laptev'].append(gridvolume)
					Regions_thick['Laptev'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==36:
					Regions_vol['EastS'].append(gridvolume)
					Regions_thick['EastS'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==40:
					Regions_vol['Chuck'].append(gridvolume)
					Regions_thick['Chuck'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==42:
					Regions_vol['BeaS'].append(gridvolume)
					Regions_thick['BeaS'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==44:
					Regions_vol['Canada'].append(gridvolume)
					Regions_thick['Canada'].append(value)
				elif 0 < value < 501 and self.regionmask[index]==46:
					Regions_vol['Central'].append(gridvolume)
					Regions_thick['Central'].append(value)
		
		
		Voldict = {}
		Thickdict = {}
		
		for region in Regions_vol:
			Voldict[region] = np.sum(Regions_vol[region])
		
		for region in Regions_thick:
			Thickdict[region] = np.sum(Regions_thick[region])/len(Regions_thick[region])
			
		volume = Voldict['total']
		thickness = Thickdict['total']
		
		anomvolume = volume - float(self.meandict[dictstring][0])
		anomthickness = thickness - float(self.meandict[dictstring][1])
		
		ADS_SIT_maps.action.normalshow(icethickess,volume,thickness,datestrings)
		ADS_SIT_maps.action.anomalyshow(iceanom,anomvolume,anomthickness,datestrings)
		
		return Voldict,Thickdict,datestring
		
	def dayloop(self,icethickess,freezedays):
		'''main melt algorithm'''
		loopday	= self.start
		
# =============================================================================
# 		#for 2012 start date
# 		filename = 'DataFiles/2017/ADS_SIT_20170303.dat'
# 		icethickess = CryoIO.openfile(filename,np.uint16)/10
# 		freezedays = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
# 		
# 		#2012 first melt day calibration
# 		for x,y in enumerate(icethickess):
# 			if 1000 < y < 1001:
# 				freezedays[x] = -1
# 				icethickess[x] = 50
# 			elif y > 5500: #no data == icefree , icefree == zero thickness
# 				icethickess[x] = 0
# =============================================================================

		self.starttime = time.time()
		future = []		
		executor = ProcessPoolExecutor(max_workers=6)
		for count in range (0,self.daycount,1):
			filepath = f'DataFiles/compressed/{self.year}{self.stringmonth}/'
# 			datestring = '{}-{}-{}'.format(self.year,self.stringmonth,self.stringday)
			filename = 'ADS_SIT_{}{}{}.gz'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'DataFiles/Mean/ADS_Mean_{}{}.dat'.format(self.stringmonth,self.stringday)
			
			icenewdate = self.loadgzip(f'{filepath}{filename}')/10
			icenMean = CryoIO.openfile(filenameMean,np.uint16)
			
			aaaaa = np.vectorize(self.calculateThickness)
			icethickess,freezedays = aaaaa(self.landmask,icenewdate,icethickess,freezedays)
			#calculate pole hole
			icethickess = self.polehole(icethickess)
			
			iceanom = icethickess - icenMean
			
			#calculate volume/thickness data per region in extra thread
			future.append(executor.submit(self.csvdata, icethickess,iceanom,[self.year,self.stringmonth,self.stringday]))
			
			
			#export daily data as png & binary for NETCDF conversion
			NETCDF_export = np.array(icethickess, dtype=np.uint16)
			CryoIO.savebinaryfile('Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),NETCDF_export)
			if count == (self.daycount-1):
				SIT_export = np.array(icethickess, dtype=np.int32)
				CryoIO.savebinaryfile('DataFiles/NRT/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),SIT_export)
				CryoIO.savebinaryfile('DataFiles/NRT/AMSR2_FreezeDays_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),freezedays)
				
			
			print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
			loopday += timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
				
#			print('Date: {}'.format(loopday))

		aaa = future[-1].result()
		#print(future[-1].result())
		
		finaldict = {}
		finaldict_thick = {}
		for xxx in future[-1].result()[0]:
			finaldict[xxx] = [xxx]
			finaldict_thick[xxx] = [xxx]
		
		
		for xxx in future:
			for yyy in xxx.result()[1]:
				finaldict[yyy].append(xxx.result()[0][yyy])
				finaldict_thick[yyy].append(xxx.result()[1][yyy])
			self.CSVVolume.append (xxx.result()[0]['total'])
			self.CSVThickness.append (xxx.result()[1]['total'])
			self.CSVDatum.append(xxx.result()[2])
		
		#print(finaldict)
		megalist = []
		megalist_thick = []
		megalist.append(self.CSVDatum)
		megalist_thick.append(self.CSVDatum)
		
		for xxx in finaldict:
			megalist.append(finaldict[xxx])
		for xxxx in finaldict_thick:
			megalist_thick.append(finaldict_thick[xxxx])
		CryoIO.csv_columnexport('temp/_ADS_Region_Vol.csv',megalist)
		CryoIO.csv_columnexport('temp/_ADS_Region_Thick.csv',megalist_thick)
			

		#save last available date
		self.end = time.time()
		self.CSVDatum.append (self.end-self.starttime)
		self.CSVVolume.append ('seconds')
		self.CSVThickness.append (str((self.end-self.starttime)/self.daycount)+'seconds/day')	

		#plt.show()
		
	def calculateThickness(self,landmask,icenewdate,icethickess,freezedays):
		if landmask < 40:
		#new day contains thickness data
			if icenewdate < 501:
				#old day is ice free or melt was estimates
				if icethickess == 0: 
					icethickess = min(self.max_thickness,icenewdate)
					freezedays = 0
				#landmask has shifted in the data
				if 5660 < icethickess < 5670:
					icethickess = self.min_melt_thickness
	
				#old day is not ice free
				else:
					icethickess = max(icethickess-self.thicknesschange,min(self.max_thickness,icethickess+self.thicknesschange,icenewdate))
					freezedays = 0
	
			#new day is ice free
			elif 5700 < icenewdate < 5800:
				icethickess = 0
				freezedays = 0
					
			#new day shows melt and old day is ice-free (first refreeze)
			elif  1000 < icenewdate < 1002 and icethickess == 0:
				icethickess = self.first_freeze_thickness*(1-(icenewdate-1000))
				freezedays = 1
				
			# melt & freeze algorithm				
			elif  1000 < icenewdate < 1002 and 0 < icethickess < 501:	
				#calculates melting
				if freezedays < 1:
					icethickess = max(self.min_melt_thickness,icethickess*(1-((icenewdate-1000)/self.meltrate)))
					#meltcount += 5*(icenewdate-1000) # 0.2 melt == one melt day (0.2*5=1), 0.4 melt == 2 melt days
					freezedays = -1						
					
				#calculates freezing after first refreeze	
				elif freezedays > 0 :
					icethickess = min(50,icethickess+icethickess*((icenewdate-1000)/(self.freezerate*freezedays**0.5)))
					freezedays += 1 # refreeze days
		else:
			icethickess = 5665
				
		return icethickess,freezedays

	def automated (self,year,month,day,daycount):
		'''used only to automate monthly updates'''
		self.year = year
		self.stringmonth = str(month).zfill(2)
		self.stringday = str(day).zfill(2)
		self.daycount = daycount

		self.start = date(year, month, day)
		prevdate = self.start-timedelta(days=1)
		prevyear = prevdate.year
		prevmonth = prevdate.month
		prevday = prevdate.day
		
		lastmonthdata = 'DataFiles/NRT/AMSR2_SIT_{}{}{}.dat'.format(prevyear,str(prevmonth).zfill(2),str(prevday).zfill(2))
		lastmonth_freeze = 'DataFiles/NRT/AMSR2_FreezeDays_{}{}{}.dat'.format(prevyear,str(prevmonth).zfill(2),str(prevday).zfill(2))
		icethickess = CryoIO.openfile(lastmonthdata,np.int32)
		freezedays = CryoIO.openfile(lastmonth_freeze,float)
		
		self.dayloop(icethickess,freezedays)
		CryoIO.csv_columnexport('temp/_AMSR2_sea_ice_volume_V1.6.csv',[self.CSVDatum,self.CSVVolume,self.CSVThickness])

action = ADS_data()


if __name__ == "__main__":
	print('main')
# 	action.dayloop('icethickness','freezedays')
# 	CryoIO.csv_columnexport('_AMSR2_sea_ice_volume_V1.66.csv',[action.CSVDatum,action.CSVVolume,action.CSVThickness])
#	action.viewloop(1)
	action.automated(2023,4,1,30) #,year,month,startday,daycount

'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5664.8
water: 5775.9
melt: 1000.1-1000.4
unknown: 654X/655X

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''