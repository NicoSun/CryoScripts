"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the sea ice thickness from the formatted ADS SIT data ( with File_Mangaer)
"""
from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas
import matplotlib.pyplot as plt
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
		self.daycount = 5 #total length: 3103 (end 2020)
		
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
		csvdata = pandas.read_csv('Tools/zzz_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		
		Columns = ['edge']
		csvdata = pandas.read_csv('Tools/zzz_poleholeEdge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		
		
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		self.createfigure()
		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		self.landmask = CryoIO.openfile(landmaskfile,np.uint8)

		latlonmaskfile = 'Masks/latlon_low.map'
		latlonmask = CryoIO.openfile(latlonmaskfile,np.uint16)
		self.latmaskf = 0.01*latlonmask[:810000] 
		self.lonmaskf = 0.01*latlonmask[810000]
		
		
	def createfigure(self):
		'''creates the plot figure (map)'''
		icemap = self.landmask.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		
		self.fig, self.ax = plt.subplots(figsize=(10, 8.5))
		#self.fig = plt.figure(figsize=(18, 8))
		#self.ax = self.fig.add_subplot(121)
		#self.ax2 = self.fig.add_subplot(122)
		
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=350,cmap = plt.cm.gist_ncar)
		self.cbar = plt.colorbar(self.cax,shrink=0.9)
		self.cbar.set_label('Thickness in cm')
		#self.normalshow(self.latmaskf,1,2)
		#plt.show()
		
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
	
	def csvdata(self,icethickess,date):
		icevolume = []
		icethickness = []
		
		#restricts the final thickness and volume data to north of 50N
		for x,y in enumerate(icethickess):
			if  0 < y < 501 and self.latmaskf[x] > 50:
				icevolume.append  ((y/1e5)*100)
				icethickness.append (y)
				
		volume = np.sum(icevolume)
		thickness = np.sum(icethickness)/len(icethickness)
		
		self.normalshow(icethickess,volume,thickness,date)
		
		return volume,thickness,date
		
	def dayloop(self,icethickess,freezedays):
		'''main melt algorithm'''
		loopday	= self.start
		
# =============================================================================
# 		#for 2012 start date
# 		filename = 'Datafiles/ADS_SIT_20170303.dat'
# 		icethickess = CryoIO.openfile(filename,np.uint16)/10
# 		freezedays = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
# 		
# 		#2012 first melt day calibration
# 		for x,y in enumerate(icethickess):
# 			if 1000 < y < 1001:
# 				freezedays[x] = -1
# 				icethickess[x] = 50
# =============================================================================
		
# =============================================================================
# 		filename = 'AMSR2_SIT_20191005.dat'
# 		icethickess =CryoIO.openfile(filename,np.float)/10
# =============================================================================
		future = []
		self.starttime = time.time()
		executor = ProcessPoolExecutor(max_workers=22)
		for count in range (0,self.daycount,1): 
			filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			
# 			try:
			icenewdate = CryoIO.openfile(filename,np.uint16)/10
# 			except:
# 				print('Date: {} not available'.format(loopday))
			
			aaaaa = np.vectorize(self.calculateThickness)
			icethickess,freezedays = aaaaa(self.landmask,icenewdate,icethickess,freezedays)
			#calculate pole hole
			icethickess = self.polehole(icethickess)
			
			#calculate volume data in extra thread
			future.append(executor.submit(self.csvdata, icethickess,date))

			
			#export daily data as png & binary for NETCDF conversion
			#self.normalshow(icethickess,self.CSVVolume[-1],self.CSVThickness[-1],loopday.day)
# =============================================================================
# 			NETCDF_export = np.array(icethickess, dtype=np.uint16)
# 			CryoIO.savebinaryfile('Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),NETCDF_export)
# =============================================================================
			if count == (self.daycount-1):
				CryoIO.savebinaryfile('Upload/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),icethickess)
				CryoIO.savebinaryfile('Upload/AMSR2_FreezeDays_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),freezedays)
				
			
# 			print(round((100*count/self.daycount),2),' % \r', end="")
			print(count)
			loopday = loopday+timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
				
#			print('Date: {}'.format(loopday))

		print(future[-1].result())
		for x in future:
			self.CSVVolume.append (x.result()[0])
			self.CSVThickness.append (x.result()[1])
			self.CSVDatum.append(x.result()[2])

		#save last available date
		self.fig.savefig('Upload/AMSR2_SIT_Last_Day.png')
		CryoIO.savebinaryfile('Upload/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday),icethickess)
		self.end = time.time()
		self.CSVDatum.append (self.end-self.starttime)
		self.CSVVolume.append ('seconds')
		self.CSVThickness.append (str((self.end-self.starttime)/self.daycount)+'seconds/day')	

		plt.show()
		
	def calculateThickness(self,landmask,icenewdate,icethickess,freezedays):
		icenewdate = icenewdate
		freezedays = freezedays
		#new day contains thickness data
		if icenewdate < 501:
			#old day is ice free or melt was estimates
			if icethickess > 5700: 
				icethickess = min(self.max_thickness,icenewdate)
				freezedays = 0
			#landmask has shifted in the data

			#old day is not ice free
			else:
				icethickess = max(icethickess-self.thicknesschange,min(self.max_thickness,icethickess+self.thicknesschange,icenewdate))
				freezedays = 0

		#new day is ice free
		elif 5700 < icenewdate < 5800:
			icethickess = icenewdate
			freezedays = 0
				
		#new day shows melt and old day is ice-free (first refreeze)
		elif  1000 < icenewdate < 1002 and icethickess > 5700:
			icethickess = self.first_freeze_thickness*(1-(icenewdate-1000))
			freezedays = 1
			
		# melt & freeze algorithm				
		elif  1000 < icenewdate < 1002 and icethickess < 501:	
			#calculates melting
			if freezedays < 1:
				icethickess = max(self.min_melt_thickness,icethickess*(1-((icenewdate-1000)/self.meltrate)))
				#meltcount += 5*(icenewdate-1000) # 0.2 melt == one melt day (0.2*5=1), 0.4 melt == 2 melt days
				freezedays = -1						
				
			#calculates freezing after first refreeze	
			elif freezedays > 0 :
				icethickess = min(50,icethickess+icethickess*((icenewdate-1000)/(self.freezerate*freezedays**0.5)))
				freezedays += 1 # refreeze days
				
		return icethickess,freezedays


	def normalshow(self,icemap,icesum,icethickness,day):	
		'''used to display data on a map'''
		from matplotlib.colors import LinearSegmentedColormap
		icemap = icemap.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		#icemap = icemap[180:600,200:600]
		icesum = int(icesum)
		icethickness = int(icethickness)

		
		map1 = np.ma.masked_outside(icemap,0,600) # SIT
		map2 = np.ma.masked_outside(icemap,0,6000) # NoData -> Land -> Water
				
#		plainmap = icemap
				
		colors = [(0.1, 0., 0.1), (0.6, 0.1, 0.1), (0.4, 0.4, 0.4)]  # NoData -> Land -> Water
		cmap_name = 'my_list'
		
		cm4 = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)
		cmapice = plt.cm.gist_ncar_r
		
		self.ax.clear()
		self.ax.set_title('AMSR2 Snow & Ice Volume:  {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		self.ax.set_xlabel('Volume: '+str(icesum)+' 'r'$km^3$''  /  Thickness: '+str(icethickness)+' cm', fontsize=14,**self.labelfont)
		self.ax.set_ylabel('cryospherecomputing.tk/SIT', fontsize=10,color='grey',y=0.15)
		
		self.ax.imshow(map2, interpolation='nearest',vmin=5500, vmax=5800 ,cmap=cm4)
		self.ax.imshow(map1, interpolation='nearest',vmin=0, vmax=350, cmap=cmapice)
		#self.ax.imshow(plainmap, interpolation='nearest',cmap=cmapice)
		#self.ax.imshow(plainmap, interpolation='nearest',vmin=0, vmax=100,cmap=cmapice)		
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 18, r'Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 38, r'Map & Melt-Algorithm: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig.tight_layout(pad=0)
		self.fig.subplots_adjust(left=0.03)
		self.fig.subplots_adjust(right=1.05)
		self.fig.savefig('Images/AMSR2_SIT_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		if day==1 or day==15:
			self.fig.savefig('Monthly_Images/AMSR2_SIT_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
			self.fig.savefig('X:/CC_Webpage/ADS_Images/AMSR2_SIT_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		
		#plt.pause(0.01)
		
	def viewloop(self,daycount):
		'''used to display raw & calculated data on a map'''
		loopday	= self.start
		for count in range (0,daycount,1): 
			#filename = 'Images/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			#filename = 'Analysis/AMSR2_meltcount_2012.dat'.format(self.year,self.stringmonth,self.stringday)
#			filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			filename = 'Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			
			try:
				iceread = CryoIO.openfile(filename,np.uint16)
			except:
				print('Date: {} not available'.format(loopday))
				
			self.normalshow(iceread,1,1,1)
#			map1 = np.ma.masked_outside(iceread,0,400)
			#print(round((100*count/daycount),2),' % \r', end="")
			if count < daycount:
				loopday = loopday+timedelta(days=1)
				self.year = loopday.year
				self.month = loopday.month
				self.day = loopday.day
				
		plt.show()
			
	def automated (self,day,month,year,daycount):
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
		
		lastmonthdata = 'Upload/AMSR2_SIT_{}{}{}.dat'.format(prevyear,str(prevmonth).zfill(2),str(prevday).zfill(2))
		lastmonth_freeze = 'Upload/AMSR2_FreezeDays_{}{}{}.dat'.format(prevyear,str(prevmonth).zfill(2),str(prevday).zfill(2))
		icethickess = CryoIO.openfile(lastmonthdata,float)
		freezedays = CryoIO.openfile(lastmonth_freeze,float)
		
		self.dayloop(icethickess,freezedays)
		CryoIO.csv_columnexport('_AMSR2_sea_ice_volume_V1.5.csv',[self.CSVDatum,self.CSVVolume,self.CSVThickness])

action = ADS_data()
if __name__ == "__main__":
	print('main')
# 	action.dayloop('icethickness')
#	action.viewloop(1)
	action.automated(1,12,2020,31) #start-day,month,year,daycount

'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5664.8
water: 5775.9
unknown: 654X/655X

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''