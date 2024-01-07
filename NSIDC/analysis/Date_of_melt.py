import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import CryoIO

class NSIDC_area:

	def __init__  (self):
		self.start = date(2000, 3, 29)
		self.month = self.start.month
		self.day = self.start.day
		self.daycount = 161 #161 (April-August)
		self.decade = 1980
		#01/04 day 92
		#31/08 day 244
				
		self.masksload()
		
		
	def masksload(self):
	
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		self.regmaskf = CryoIO.openfile(filename,np.uint32)
		
		
	def dayloop(self):		
		loopday	= self.start	
		self.day_of_year	= self.start.timetuple().tm_yday
		
		data = []
		
		for year in range(self.decade,self.decade+10):
			filename = 'DataFiles/NSIDC_{}0329.bin'.format(year)
			icef = CryoIO.openfile(filename,np.uint8)
			data.append(icef)
				
		iceminyear = np.asarray(data).min(0)
		icemeanyear = np.asarray(data).mean(0)
		icemaxyear = np.asarray(data).max(0)
				
				
		#assigns day 500 for ice covered sea and day 0 for ice free sea
		for y in range (0,len(iceminyear)):
			if  iceminyear[y] > 37:
				iceminyear[y] = 500
			else:
				iceminyear[y] = 0
				
			if  icemeanyear[y] > 37:
				icemeanyear[y] = 500
			else:
				icemeanyear[y] = 0
				
			if  icemaxyear[y] > 37:
				icemaxyear[y] = 500
			else:
				icemaxyear[y] = 0
		
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			data = []
			
			for year in range(self.decade,self.decade+10):
				filename = 'DataFiles/NSIDC_{}{}{}.bin'.format(year,self.stringmonth,self.stringday)
				icef = CryoIO.openfile(filename,np.uint8)
				data.append(icef)
				
			icemin = np.asarray(data).min(0)
			icemedian = np.asarray(data).mean(0)
			icemax = np.asarray(data).max(0)

			#melt date calculation
			aaa = np.vectorize(self.meltdate)
			iceminyear,icemeanyear,icemaxyear= aaa(iceminyear,icemeanyear,icemaxyear,icemin,icemedian,icemax,self.regmaskf)
			
				
			if count < self.daycount:
				loopday = loopday+timedelta(days=1)
				self.month = loopday.month
				self.day = loopday.day
				self.day_of_year = loopday.timetuple().tm_yday
			print('Date: {} , DayofYear: {}'.format(loopday,self.day_of_year))
			
		#mask out land cover
		for x in range (0,len(iceminyear)):
			if self.regmaskf[x] > 16:
				iceminyear[x] = 999
				icemeanyear[x] = 999
				icemaxyear[x] = 999
			elif self.regmaskf[x] < 2:
				iceminyear[x] = 0
				icemeanyear[x] = 0
				icemaxyear[x] = 0
			else:
				if iceminyear[x] == 500:
					iceminyear[x] = -2
				if icemeanyear[x] == 500:
					icemeanyear[x] = -2
				if icemaxyear[x] == 500:
					icemaxyear[x] = -2
								
		self.normalshow(iceminyear,'min')
		self.normalshow(icemeanyear,'mean')
		self.normalshow(icemaxyear,'max')
# 		self.combograph(iceminyear,icemeanyear,icemaxyear)

		
	def meltdate(self,iceminyear,icemeanyear,icemaxyear,icemin,icemedian,icemax,regmask):
		'''checks for icefree staus'''
		if 1 < regmask < 16:
			if icemin < 37 and iceminyear == 500:
				iceminyear =  self.day_of_year
			if icemedian < 37 and icemeanyear == 500:
				icemeanyear = self.day_of_year
			if icemax < 37 and icemaxyear == 500:
				icemaxyear = self.day_of_year
		
		return iceminyear,icemeanyear,icemaxyear

	def normalshow(self,icemap,code):
		icemap = icemap.reshape(448, 304)
				
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(icemap,80,320) 
		map2 = np.ma.masked_outside(icemap,-3,+2) 
		
		fig = plt.figure(figsize=(7, 8.5))
		ax = fig.add_subplot(111)
		
		if code == 'min':
			ax.set_title(f'{self.decade}s Earliest Melt Date') 
			ax.set_xlabel('white = never icefree', fontsize=14)
		elif code == 'mean':
			ax.set_title(f'{self.decade}s Mean Melt Date') 
			ax.set_xlabel('white = usually not icefree', fontsize=14)
		elif code == 'max':
			ax.set_title(f'{self.decade}s Latest Melt Date')
			ax.set_xlabel('white = not always icefree', fontsize=14)

		cax = ax.imshow(map1, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Apr','May','Jun','Jul','Aug','Sep'])
		
		ax.imshow(map2, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		fig.tight_layout(pad=0)
		fig.subplots_adjust(left=0.05)
		
		if code == 'min':
			fig.savefig(f'temp/{self.decade}s_001_Melt_Date.png')
		elif code == 'mean':
			fig.savefig(f'temp/{self.decade}s_002_Melt_Date.png')
		elif code == 'max':
			fig.savefig(f'temp/{self.decade}s_003_Melt_Date.png')

	
	
	def combograph (self,early,median,late):
		
# =============================================================================
# 		with open('Special_Animation/Earliest_Melt_Date.bin', 'rb') as aaa:
# 			early = np.fromfile(aaa, dtype=np.float)
# 				
# 		with open('Special_Animation/Median_Melt_Date.bin', 'rb') as bbb:
# 			median = np.fromfile(bbb, dtype=np.float)
# 				
# 		with open('Special_Animation/Latest_Melt_Date.bin', 'rb') as ccc:
# 			late = np.fromfile(ccc, dtype=np.float)
# =============================================================================
		
		early = early.reshape(448, 304)
		median = median.reshape(448, 304)
		late = late.reshape(448, 304)
		
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(early,90,250) 
		map11 = np.ma.masked_outside(early,-3,+2)
		map2 = np.ma.masked_outside(median,90,250) 
		map21 = np.ma.masked_outside(median,-3,+2)
		map3 = np.ma.masked_outside(late,90,250) 
		map31 = np.ma.masked_outside(late,-3,+2)
		
		
		fig = plt.figure(figsize=(17, 8))
		fig.suptitle('Arctic Melt Dates', fontsize=14, fontweight='bold')
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)
		
		
		
		ax1.set_title('Earliest Melt Date')
		ax1.imshow(map1, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax1.imshow(map11, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax2.set_title('Median Melt Date')
		ax2.imshow(map2, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax2.imshow(map21, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax3.set_title('Latest Melt Date')
		cax = ax3.imshow(map3, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax3.imshow(map31, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		cbar = fig.colorbar(cax, ticks=[91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Apr','May','Jun','Jul','Aug','Sep'])
		
		
		ax1.set_xlabel('white: never ice free', fontsize=14)
		ax2.set_xlabel('white: usually not ice free', fontsize=14)
		ax3.set_xlabel('white: not always ice free', fontsize=14)
		
		ax1.axes.get_yaxis().set_ticks([])
		ax2.axes.get_yaxis().set_ticks([])
		ax3.axes.get_yaxis().set_ticks([])
		ax1.axes.get_xaxis().set_ticks([])
		ax2.axes.get_xaxis().set_ticks([])
		ax3.axes.get_xaxis().set_ticks([])

		fig.text(0.02, 0.95, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.02, 0.92, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.66, 0.03, 'cryospherecomputing.com',)
		
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.88)
		fig.subplots_adjust(bottom=0.1)
		fig.savefig('temp/Combo_Melt_Date.png')
		plt.show()
		
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	action.dayloop()
# 	action.combograph()
	

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

#Regionmask:
0: lakes
1: Ocean
2: Sea of Okothsk
3: Bering Sea
4: Hudson bay
5: St Lawrence
6: Baffin Bay
7: Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Achipelago
15: Central Arctic
20: Land
21: Coast
'''