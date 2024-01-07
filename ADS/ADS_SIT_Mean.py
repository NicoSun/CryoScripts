"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the sea ice thickness from the formatted ADS SIT data ( with File_Mangaer)
"""
import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
import time
import CryoIO

class ADS_data:

	def __init__  (self):
		'''initializes the melt algorithm'''
		self.start = date(2012, 7, 3)
		self.year = self.start.year
		self.stringmonth = str(self.start.month).zfill(2)
		self.stringday = str(self.start.day).zfill(2)
		self.daycount = 3833 #total length: 3833 (end 2022)
		
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
		
		
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		self.landmask = CryoIO.openfile(landmaskfile,np.uint8)

		latlonmaskfile = 'Masks/latlon_low.map'
		latlonmask = CryoIO.openfile(latlonmaskfile,np.uint16)
		self.latmaskf = 0.01*latlonmask[:810000] 
		self.lonmaskf = 0.01*latlonmask[810000]
		
		
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
	
	def csvdata(self,icethickess,datestring):
		icevolume = []
		icethickness = []
		
		#restricts the final thickness and volume data to north of 50N
		for x,y in enumerate(icethickess):
			if  0 < y < 501 and self.latmaskf[x] > 50:
				icevolume.append  ((y/1e5)*100)
				icethickness.append (y)
				
		volume = np.sum(icevolume)
		thickness = np.sum(icethickness)/len(icethickness)
		
		return volume,thickness,datestring
		
	def dayloop(self,icethickess):
		'''main melt algorithm'''
		loopday	= self.start
		
		freezedays = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
#		meltcount = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
#		freezecount = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days

		#2012 first melt day calibration
		for x,y in enumerate(icethickess):
			if 1000 < y < 1001:
				freezedays[x] = -1
				icethickess[x] = 50
			elif y > 5500: #no data == icefree , icefree == zero thickness
				icethickess[x] = 0

		self.starttime = time.time()
		meandict = {}

# 		for count in range (0,self.daycount,1): 
		while self.year < 2023:
			datestring = '{}{}'.format(self.stringmonth,self.stringday)
			filepath = f'DataFiles/compressed/{self.year}{self.stringmonth}/'
			filename = 'ADS_SIT_{}{}{}.gz'.format(self.year,self.stringmonth,self.stringday)
			
			icenewdate = CryoIO.loadgzip(f'{filepath}{filename}',np.uint16)/10

			aaaaa = np.vectorize(self.calculateThickness)
			icethickess,freezedays = aaaaa(self.landmask,icenewdate,icethickess,freezedays)

			#calculate pole hole
			icethickess = self.polehole(icethickess)

			try:
				meandict[datestring] += icethickess
			except KeyError:
				meandict[datestring] = icethickess
			
			loopday += timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)

			print('Date: {}'.format(loopday))
		
		self.end = time.time()
		self.CSVDatum.append (self.end-self.starttime)
		self.CSVVolume.append ('seconds')
		self.CSVThickness.append (str((self.end-self.starttime)/self.daycount)+'seconds/day')

			
		for item in meandict:
			CryoIO.savenumpy(f'temp/AMSR2_SIT_Mean_{item}.npz',meandict[item])
		#self.normalshow(icethickess,1,1,1)

		
	def calculateThickness(self,landmask,icenewdate,icethickess,freezedays):
		#new day contains thickness data
		if landmask < 40:
			if icenewdate < 501:
				#old day is ice free
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
			elif 5770 < icenewdate < 5780:
				icethickess = 0
				freezedays = 0
					
			#new day shows melt and old day is ice-free (first refreeze)
			elif  1000 < icenewdate < 1002 and icethickess == 0:
				icethickess = self.first_freeze_thickness*(1-(icenewdate-1000))
				freezedays = 1
				
			# melt & freeze algorithm
			elif  1000 < icenewdate < 1001 and 0 < icethickess < 501:
				#calculates melting
				if freezedays < 1:
					icethickess = max(self.min_melt_thickness,icethickess*(1-((icenewdate-1000)/self.meltrate)))
					freezedays = -1						
					
				#calculates freezing after first refreeze	
				elif freezedays > 0 :
					icethickess = min(50,icethickess+icethickess*((icenewdate-1000)/(self.freezerate*freezedays**0.5)))
					freezedays += 1 # refreeze days
					#freezecount += 1
		else:
			icethickess = 5665

		return icethickess,freezedays

			
	def loadfirstday (self,year,month,day):
		'''used only to automate monthly updates'''
		self.year = year
		self.stringmonth = str(month).zfill(2)
		self.stringday = str(day).zfill(2)
		self.daycount = 3833 # Jul 2012- Dec 2022

		self.start = date(year, month, day)

		#for 2012 start date
		filename = 'DataFiles/compressed/201703/ADS_SIT_20170303.gz'
		icethickess =CryoIO.loadgzip(filename,np.uint16)/10
		
		self.dayloop(icethickess)
		CryoIO.csv_columnexport('temp/_AMSR2_V1.5.csv',[self.CSVDatum,self.CSVVolume,self.CSVThickness])


	def meanlalala(self):
		loopday = date(2016, 1, 1)
		self.year = loopday.year
		self.stringmonth = str(loopday.month).zfill(2)
		self.stringday = str(loopday.day).zfill(2)
		years = 12
		
		for count in range (0,366): 
			filename = 'temp/AMSR2_SIT_Mean_{}{}.npz'.format(self.stringmonth,self.stringday)
			filename_out = 'DataFiles/Mean/ADS_Mean_{}{}.npz'.format(self.stringmonth,self.stringday)
			ice = CryoIO.readnumpy(filename)
			
			if count <= 183: # 184 days Jan-July
				ice = ice/ (years-1)
			elif count > 183: # 182 Days Jul - December
				ice = ice/(years)
			
			ice_new = self.polehole(ice)

			export = np.array(ice_new, dtype=np.uint16)
			CryoIO.savenumpy(filename_out, export)
			
			print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
			loopday += timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)


action = ADS_data()
if __name__ == "__main__":
	print('main')
# 	action.loadfirstday(2012,7,3)
	action.meanlalala()
# =============================================================================
# 	try:
# 		action.dayloop('icethickness')
# 		CryoIO.csv_columnexport('_AMSR2_sea_ice_volume_V1.55.csv',[action.CSVDatum,action.CSVVolume,action.CSVThickness])
# 	except:
# 		CryoIO.csv_columnexport('_AMSR2_sea_ice_volume_V1.55.csv',[action.CSVDatum,action.CSVVolume,action.CSVThickness])
# =============================================================================

#0.864s/day single thread


'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5665
water: 5776
melt: 1000.1-1000.4
unknown: 654X/655X

landmask set as 40%

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''