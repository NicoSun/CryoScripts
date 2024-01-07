"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the sea ice thickness from the formatted ADS SIT data ( with File_Mangaer)
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import CryoIO

class ADS_mapping:

	def __init__  (self):
		self.masksload()
		icemap = self.landmask.reshape(900,900)
		icemap = np.rot90(icemap,k=2)[80:750,:700]
		
# 		self.labelfont = {'fontname':'Arial'}

# 		self.filepath = '/media/prussian/Cryosphere/CryosphereComputing_2.0/Past_SIT/'
		self.filepath = 'X:\CryosphereComputing_2.0\Past_SIT/'
		
		self.createfigure(icemap)
		self.createfigure_anom(icemap)

		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		self.landmask = CryoIO.openfile(landmaskfile,np.uint8)
		
	def createfigure(self,icemap):
		'''creates the plot figure (map)'''
		self.fig, self.ax = plt.subplots(figsize=(10, 8.5))
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=350,cmap = plt.cm.gist_ncar)
		self.cbar = plt.colorbar(self.cax,shrink=0.9)
		self.cbar.set_label('Thickness in cm')

		
	def createfigure_anom(self,icemap):
		'''creates the plot figure (map)'''
		self.fig2, self.ax2 = plt.subplots(figsize=(10, 8.5))
		self.cax2 = self.ax2.imshow(icemap, interpolation='nearest', vmin=-200, vmax=200,cmap = plt.cm.coolwarm_r)
		self.cbar2 = plt.colorbar(self.cax2,shrink=0.9)
		self.cbar2.set_label('Thickness anomaly in cm')

	def normalshow(self,icemap,icesum,icethickness,datestrings):
		'''used to display data on a map'''
		icemap = icemap.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		icesum = int(icesum)
		icethickness = int(icethickness)

		datestring = '{}-{}-{}'.format(datestrings[0],datestrings[1],datestrings[2])
		map1 = np.ma.masked_outside(icemap,5,600) # SIT
		map2 = np.ma.masked_outside(icemap,0,6000) # NoData -> Land -> Water
				
#		plainmap = icemap
				
		#colors = [(0.1, 0., 0.1), (0.6, 0.1, 0.1), (0.4, 0.4, 0.4)]  # NoData -> Land -> Water
		colors = [(0.4, 0.4, 0.4), (0.6, 0.1, 0.1), (0.1, 0., 0.1)]  # Water -> Land -> NoData
		cmap_name = 'my_list'
		
		cm4 = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)
		cmapice = plt.cm.gist_ncar
		
		self.ax.clear()
		self.ax.set_title('AMSR2 Thickness : {}'.format(datestring))
		self.ax.set_xlabel('Volume: '+str(icesum)+' 'r'$km^3$''  /  Thickness: '+str(icethickness)+' cm', fontsize=14)
		self.ax.set_ylabel('cryospherecomputing.com/SIT', fontsize=10,color='grey',y=0.15)
		
		self.ax.imshow(map2, interpolation='nearest',vmin=0, vmax=9900 ,cmap=cm4)
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
		self.fig.savefig('Images/SIT/AMSR2_SIT_{}.png'.format(datestring))
		if datestrings[2] == '01' or datestrings[2] == '15':
# 			self.fig.savefig('Monthly_Images/AMSR2_SIT_{}.png'.format(datestring))
			self.fig.savefig(f'{self.filepath}AMSR2_SIT_{datestring}.png')
		if datestrings[2] == '31' or datestrings[2] == '30' or datestrings[1] == '02' and datestrings[2] == '28':
			self.fig.savefig('Upload/AMSR2_SIT_Last_Day.png')

		
	def anomalyshow(self,icemap,icesum,icethickness,datestrings):
		'''used to display data on a map'''
		for x,y in enumerate(icemap):
			if self.landmask[x] > 40:
				icemap[x] = 5665
		
		icemap = icemap.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		icesum = int(icesum)
		icethickness = round(icethickness,2)
		
		datestring = '{}-{}-{}'.format(datestrings[0],datestrings[1],datestrings[2])
		map1 = np.ma.masked_outside(icemap,-300,300) # SIT
		map2 = np.ma.masked_outside(icemap,0,6000) # NoData -> Land -> Water
				
#		plainmap = icemap
		cbarmax = 200# min(250,int(np.amax(icemap)))
				
		colors = [(0.1, 0., 0.1), (0, 0.4, 0), (0.4, 0.4, 0.4)]  # NoData -> Land -> Water
		#colors = [(0.4, 0.4, 0.4), (0.6, 0.1, 0.1), (0.1, 0., 0.1)]  # Water -> Land -> NoData
		cmap_name = 'my_list'
		
		cm4 = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)
		cmap2 = plt.cm.coolwarm_r
		
		self.ax2.clear()
		self.ax2.set_title('AMSR2 Thickness Anomaly: {}'.format(datestring))
		self.ax2.set_xlabel('Volume: '+str(icesum)+' 'r'$km^3$''  /  Thickness: '+str(icethickness)+' cm', fontsize=14)
		self.ax2.set_ylabel('cryospherecomputing.com/SIT', fontsize=10,color='grey',y=0.15)
		
		self.ax2.imshow(map2, interpolation='nearest',vmin=5000, vmax=6000 ,cmap=cm4)
		self.ax2.imshow(map1, interpolation='nearest',vmin=-cbarmax, vmax=cbarmax, cmap=cmap2)

		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 18, r'Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 38, r'Map & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=0)
		self.fig2.subplots_adjust(left=0.03)
		self.fig2.subplots_adjust(right=1.05)
		self.fig2.savefig('Images/Anomaly/AMSR2_SIT_Anomaly_{}.png'.format(datestring))
		if datestrings[2] == '01' or datestrings[2] == '15':
# 			self.fig2.savefig('Monthly_Images/AMSR2_SIT_Anomaly_{}.png'.format(datestring))
			self.fig2.savefig(f'{self.filepath}AMSR2_SIT_Anomaly_{datestring}.png')
		if datestrings[2] == '31' or datestrings[2] == '30' or datestrings[1] == '02' and datestrings[2] == '28':
			self.fig2.savefig('Upload/AMSR2_SIT_Last_Day_Anomaly.png')
		
	def viewloop(self,daycount):
		'''used to display raw & calculated data on a map'''
		from datetime import date
		from datetime import timedelta
		
		loopday	= date(2012,7,3)
		self.year = loopday.year
		self.stringmonth = str(loopday.month).zfill(2)
		self.stringday = str(loopday.day).zfill(2)
		
		for count in range (0,daycount,1): 
			filenameMean_test = 'temp/AMSR2_SIT_Mean_{}{}.dat'.format(self.stringmonth,self.stringday)
			#filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			#filename = 'Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'Datafiles/Mean/ADS_Mean_{}{}.dat'.format(self.stringmonth,self.stringday)
			
			icenMean = CryoIO.openfile(filenameMean,np.uint16)
# 			icenewdate = CryoIO.openfile(filename,np.uint16)/10
			#icenMean = CryoIO.openfile(filenameMean_test,np.int32)
			print(count)
			
			self.normalshow(icenMean,1,1,[count,1])
			#self.anomalyshow(icenMean,1,1,[1,1])
#			map1 = np.ma.masked_outside(iceread,0,400)
			#print(round((100*count/daycount),2),' % \r', end="")
			if count < daycount:
				loopday += timedelta(days=1)
				self.year = loopday.year
				self.stringmonth = str(loopday.month).zfill(2)
				self.stringday = str(loopday.day).zfill(2)
				
		plt.show()
			


action = ADS_mapping()
if __name__ == "__main__":
	action.viewloop(3)
	print('main')

'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5665
water: 5776
melt: 1000.1-1000.4
unknown: 654X/655X

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''