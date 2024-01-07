import numpy as np
import numpy.ma as ma
import time
import matplotlib.pyplot as plt
from matplotlib import cm

class Simpleviewer:


	def __init__  (self):
		self.year = 2020
		self.month = 12
		self.day = 1
		self.daycount = 6 #366 year 183 austral summer
		
		self.plottype = 'daily' # daily ,  mask
		self.dailyorcumu()
			
	
	def viewloop(self):
	
		for count in range (0,self.daycount,1): 
			stringmonth = str(self.month).zfill(2)
			stringday = str(self.day).zfill(2)
			filename = 'DataFiles/NSIDC_{}{}{}_south.bin'.format(self.year,stringmonth,stringday)
#			filenamemax = 'DataFiles/Maximum/NSIDC_Max_{}{}_south.bin'.format(stringmonth,stringday)
#			filenamemin = 'DataFiles/Minimum/NSIDC_Min_{}{}_south.bin'.format(stringmonth,stringday)
#			filenamemean = 'DataFiles/Daily_Mean/NSIDC_Mean_{}{}_south.bin'.format(stringmonth,stringday)
		
			try:
				with open(filename, 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
			except:
				print('N/A:',self.year,self.month,self.day)


			ice = ice / 250.
			self.dailyloop(ice)

			self.day = self.day+1
			count = count+1
			if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
				self.day=1
				self.month = self.month+1
			elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
				self.day=1
				self.month = self.month+1
			elif self.day==30 and self.month==2:
				self.day=1
				self.month = self.month+1
			elif  self.day==32 and self.month == 12:
				self.day = 1
				self.month = 1
				self.year = self.year+1
			
		plt.show()

	def masksload(self):
	
		self.regionmask = 'Masks/region_s_pure.msk'
		with open(self.regionmask, 'rb') as frmsk:
			#hdr = frmsk.read(300)
			self.regionmask = np.fromfile(frmsk, dtype=np.uint8)
		
		self.areamask = 'Masks/pss25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
			self.mask2 = np.fromfile(famsk, dtype=np.int32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /(1000)
		
		self.latmask = 'Masks/pss25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
			self.mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(self.mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000
		
		self.maskview(self.regionmask)
		plt.show()
		
		
	def dailyloop(self,icemap):
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
		icemap = np.ma.masked_greater(icemap, 1)
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		self.ax.clear()
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		#self.ax.set_xlabel('NSIDC Area: '+str(icesum)+' Ice concentration')
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1,cmap = plt.cm.jet)
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		plt.pause(1.01)
		
		
	def maskview(self,icemap):		
		icemap = icemap.reshape(332, 316)
		self.ax.clear()
		#self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		#self.ax.set_xlabel(': '+str(icesum)+' Wh/m2')
		self.cax = self.ax.imshow(icemap, interpolation='nearest')
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		if self.plottype == 'daily':
			self.fig, self.ax = plt.subplots(figsize=(8, 8))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=1,cmap = plt.cm.jet)
			self.cbar = self.fig.colorbar(self.cax, ticks=[0, 0.5, 1]).set_label('Ice concentration')
			self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold')
			
		if self.plottype == 'mask':
			self.fig, self.ax = plt.subplots(figsize=(8, 8))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
			#self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
			self.title = self.fig.suptitle('Mask', fontsize=14, fontweight='bold')
			
		
		
		
action = Simpleviewer()
action.viewloop()
# action.masksload()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
