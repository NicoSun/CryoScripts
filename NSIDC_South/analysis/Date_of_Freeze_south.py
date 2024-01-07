import numpy as np
import matplotlib.pyplot as plt
import CryoIO
from datetime import date
from datetime import timedelta

class NSIDC_area:

	def __init__  (self):
		self.start = date(2012, 3, 11)
		self.month = self.start.month
		self.day = self.start.day
		self.daycount = 175 #155 (Mar-Aug)
		self.decade = 2010
		
		self.masksload()
		
		
	def masksload(self):
	
		regionmaskfile = 'Masks/region_s_pure.msk'
		self.regmaskf = CryoIO.openfile(regionmaskfile,np.uint8)

	def dayloop(self):
		loopday	= self.start
		self.day_of_year = self.start.timetuple().tm_yday

		data = []
		
		for year in range(self.decade,self.decade+10):
			filename = 'DataFiles/NSIDC_{}0301_south.bin'.format(year)
			icef = CryoIO.openfile(filename,np.uint8)
			data.append(icef)
				
		iceminyear = np.asarray(data).min(0)
		icemeanyear = np.asarray(data).mean(0)
		icemaxyear = np.asarray(data).max(0)
				
				
		#assigns day 500 for ice covered sea and day 0 for ice free sea
		for y in range (0,len(iceminyear)):
			if  iceminyear[y] > 37:
				iceminyear[y] = 11
			else:
				iceminyear[y] = 500
				
			if  icemeanyear[y] > 37:
				icemeanyear[y] = 11
			else:
				icemeanyear[y] = 500
				
			if  icemaxyear[y] > 37:
				icemaxyear[y] = 11
			else:
				icemaxyear[y] = 500

		
		for count in range (0,self.daycount):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			data = []
			
			for year in range(self.decade,self.decade+10):
				filename = 'DataFiles/NSIDC_{}{}{}_south.bin'.format(year,self.stringmonth,self.stringday)
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
			if self.regmaskf[x] > 10:
				iceminyear[x] = 999
				icemeanyear[x] = 999
				icemaxyear[x] = 999
			elif self.regmaskf[x] < 2:
				iceminyear[x] = 0
				icemeanyear[x] = 0
				icemaxyear[x] = 0
			else:
				if iceminyear[x] == 500:
					iceminyear[x] = 0
				if icemeanyear[x] == 500:
					icemeanyear[x] = 0
				if icemaxyear[x] == 500:
					icemaxyear[x] = 0
					
				if iceminyear[x] == 11:
					iceminyear[x] = -2
				if icemeanyear[x] == 11:
					icemeanyear[x] = -2
				if icemaxyear[x] == 11:
					icemaxyear[x] = -2
				
		self.normalshow(iceminyear,'min')
		self.normalshow(icemeanyear,'mean')
		self.normalshow(icemaxyear,'max')
						
			
	def meltdate(self,iceminyear,icemeanyear,icemaxyear,icemin,icemedian,icemax,regmask):
		'''checks for icefree staus'''
		if regmask < 10:
			if icemin > 37 and self.day_of_year < iceminyear:
				iceminyear =  self.day_of_year
			if icemedian > 37 and self.day_of_year < icemeanyear:
				icemeanyear = self.day_of_year
			if icemax > 37 and self.day_of_year < icemaxyear:
				icemaxyear = self.day_of_year
		
		return iceminyear,icemeanyear,icemaxyear
		


	def normalshow(self,icemap,code):
		icemap = icemap.reshape(332, 316)
				
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(icemap,55,300) 
		map2 = np.ma.masked_outside(icemap,-3,+2) 
		
		fig = plt.figure(figsize=(7, 7))
		ax = fig.add_subplot(111)

		cax = ax.imshow(map1, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[60,91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Mar', 'Apr','May','Jun','Jul','Aug','Sep'])
		
		ax.imshow(map2, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		if code == 'min':
			ax.set_title(f'{self.decade}s Latest Freeze Date')
			ax.set_xlabel('white = never icefree', fontsize=14)
		elif code == 'mean':
			ax.set_title(f'{self.decade}s Mean Freeze Date') 
			ax.set_xlabel('white = usually not icefree', fontsize=14)
		elif code == 'max':
			ax.set_title(f'{self.decade}s Earliest Freeze Date') 
			ax.set_xlabel('white = not always icefree', fontsize=14)
		
		
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		fig.tight_layout(pad=0)
		fig.subplots_adjust(left=0.05)
		
		if code == 'min':
			fig.savefig(f'temp/{self.decade}s_001_Freeze_Date.png')
		elif code == 'mean':
			fig.savefig(f'temp/{self.decade}s_002_Freeze_Date.png')
		elif code == 'max':
			fig.savefig(f'temp/{self.decade}s_003_Freeze_Date.png')

	
	
	def combograph (self,early,median,late):
		
		early = early.reshape(332, 316)
		median = median.reshape(332, 316)
		late = late.reshape(332, 316)
		
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(late,55,300) 
		map11 = np.ma.masked_outside(late,-3,+2)
		map2 = np.ma.masked_outside(median,55,300) 
		map21 = np.ma.masked_outside(median,-3,+2)
		map3 = np.ma.masked_outside(early,55,300) 
		map31 = np.ma.masked_outside(early,-3,+2)
		
		
		fig = plt.figure(figsize=(18, 7))
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)
		
		fig.subplots_adjust(left=0.03, right=0.97, wspace=0.05)
		fig.suptitle('Antarctic Freeze Days',fontweight='bold',fontsize=14)

		ax1.set_title('Earliest Freeze Date')
		ax1.imshow(map1, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax1.imshow(map11, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax2.set_title('Median Freeze Date')
		ax2.imshow(map2, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax2.imshow(map21, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax3.set_title('Latest Freeze Date')
		cax = ax3.imshow(map3, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax3.imshow(map31, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax1.set_xlabel('white: never ice free', fontsize=14)
		ax2.set_xlabel('white: usually not ice free', fontsize=14)
		ax3.set_xlabel('white: not always ice free', fontsize=14)

		ax1.axes.get_yaxis().set_ticks([])
		ax1.axes.get_xaxis().set_ticks([])
		ax2.axes.get_yaxis().set_ticks([])
		ax2.axes.get_xaxis().set_ticks([])
		ax3.axes.get_yaxis().set_ticks([])
		ax3.axes.get_xaxis().set_ticks([])
		
		ax1.text(0.02, 0.96, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		ax1.text(0.02, 0.93, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		ax3.text(0.02, 0.02, 'https://sites.google.com/site/cryospherecomputing/analysis',transform=ax1.transAxes)
		
		
		fig.tight_layout(pad=-3)
		
		cbar = fig.colorbar(cax, ticks=[60,91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Mar', 'Apr','May','Jun','Jul','Aug','Sep'])
		
		fig.subplots_adjust(top=0.85)
		fig.subplots_adjust(bottom=0.1)
		fig.subplots_adjust(right=0.98)
		
#		fig.savefig('csvexport/Combo_South_Freeze_Date.png')
		
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	action.dayloop()
#	action.combograph()
	
'''
Values are coded as follows:

0-250  concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''