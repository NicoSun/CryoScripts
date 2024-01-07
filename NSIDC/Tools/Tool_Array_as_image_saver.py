import numpy as np
import matplotlib.pyplot as plt
import CryoIO
import copy

class Simpleviewer:


	def __init__  (self):
		self.year = 2020
		self.month = 1
		self.day = 1
		self.daycount = 12 #  13 months
		self.mode = 'Max' #Min, Max
		
		self.masksload()
		self.dailyorcumu()
		
		# options Max,Min,Mean
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		self.regmaskf = CryoIO.openfile(filename,np.uint32)
		
		filename = 'X:/NSIDC/Masks/psn25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
		
	
	def viewloop(self):
# =============================================================================
# 		months = ['zero','Jan','Feb','Mar','Apr','May','Jun','Jul', 'Aug', 'Sep','Oct','Nov','Dec']
# 		if self.mode == 'Min':
# 			header = "NSIDC Combined Low SIC"
# 		elif self.mode == 'Max':
# 			header = "NSIDC Combined High SIC"
# 			
# 		if self.day == 1:
# 			day = "1st"
# 		elif self.day == 15:
# 			day = "15th"
# =============================================================================
		
		for count in range (0,self.daycount,1): 
			stringmonth = str(self.month).zfill(2)
			stringday = str(self.day).zfill(2)
			filename = 'DataFiles/NSIDC_{}{}{}.bin'.format(self.year,stringmonth,stringday)
# 			filename = f'DataFiles/{self.mode}/NSIDC_{self.mode}_{stringmonth}{stringday}.bin'
			
			ice = CryoIO.openfile(filename,np.uint8)/250
			
			#area & extent calculation
			aaa = np.vectorize(self.calculateAreaExtent)
			area,extent = aaa(ice,self.areamaskf,self.regmaskf)
			
			area = np.sum(area)
			extent = np.sum(extent)
			
# 			xlabel = f'{header} {months[self.month]} {day}'
			xlabel = f'Date: {self.year}/{stringmonth}/{stringday}'
			filename = f'temp/NSIDC_{self.year}{stringmonth}{stringday}_north.png'
			self.dailyloop(ice,area,extent, xlabel, filename)

			self.month += 1
			if self.month == 13:
				self.month = 1
				self.year += 1
			
# 		plt.show()
		
	def calculateAreaExtent(self,icemap,areamask,regionmask):
		'''area & extent calculation & remove lake ice'''
		area = 0
		extent = 0

		if 1 < regionmask < 16:
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask

				
		return area,extent
		
	def dailyloop(self,icemap,area,extent, xlabel,filename):
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[30:430,10:290]
		cmap = copy.copy(plt.cm.get_cmap("jet"))
		cmap.set_bad('black',0.8)
		
		self.ax.clear()
		self.ax.set_xlabel(xlabel)
		self.ax.xaxis.set_label_position('top') 
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax.text(0.55, 0.05, 'Area: '+'{:,}'.format(area)+' 'r'$km^2$', fontsize=10,color='white',transform=self.ax.transAxes)
		self.ax.text(0.55, 0.03, 'Extent: '+'{:,}'.format(extent)+' 'r'$km^2$', fontsize=10,color='white',transform=self.ax.transAxes)
		
		self.ax.text(2, 8, 'cryospherecomputing.tk', fontsize=8,color='white',fontweight='bold')
		self.ax.text(200, 8, 'data source: NSIDC', fontsize=8,color='white',fontweight='bold')
				
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=0)
		self.fig.savefig(filename)
#		plt.pause(0.01)
		
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		self.fig, self.ax = plt.subplots(figsize=(5.8, 7))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100],shrink=0.9).set_label('Ice concentration in %')
#			self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold',x=0.175)
			
		
		
		
		
action = Simpleviewer()
action.viewloop()
#action.masksload()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
