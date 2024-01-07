import numpy as np
import matplotlib.pyplot as plt

class Mask_creater:


	def __init__  (self):
		self.year = 2016
		self.month = 10
		self.day = 21
		self.daycount = 1 #366 year 183 austral summer
		
	
	def Coastalmask(self):
	
		regionmaskfile = 'Masks/region_s_pure.msk'
		with open(regionmaskfile, 'rb') as frmsk:
			self.mask = np.fromfile(frmsk, dtype=np.uint8)
		
		self.mask = self.mask.reshape(332, 316)
		for y in range (60,280):
			for x in range (40,288):
				for yoff in range(1,5):
					for xoff in range(1,5):
						for region in range (2,7):
							if self.mask[y,x]== 12 and self.mask[y-yoff,x] == region:
								self.mask[y-yoff,x] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x] == region:
								self.mask[y+yoff,x] = 20+region
				
							if self.mask[y,x]== 12 and self.mask[y,x-xoff] == region:
								self.mask[y,x-xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y,x+xoff] == region:
								self.mask[y,x+xoff] = 20+region
								
							if self.mask[y,x]== 12 and self.mask[y-yoff,x-xoff] == region:
								self.mask[y-yoff,x-xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x+xoff] == region:
								self.mask[y+yoff,x+xoff] = 20+region
							if self.mask[y,x]== 12 and self.mask[y-yoff,x+xoff] == region:
								self.mask[y-yoff,x+xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x-xoff] == region:
								self.mask[y+yoff,x-xoff] = 20+region
		
		self.masksave('Masks/region_s_coast.msk',self.mask)
		self.maskview(self.mask)
		plt.show()
		
	def MaxExtent(self):
	
		file = 'DataFiles/Maximum/NSIDC_Max_0926_south.bin'
		with open(file, 'rb') as frmsk:
			mask = np.fromfile(frmsk, dtype=np.uint8)
			
		icemask = np.zeros(len(mask))
			
		for x,y in enumerate(mask):
			if 52 < y < 251:
				icemask[x] = 1
			if y == 253:
				icemask[x] = 3
			if y == 254:
				icemask[x] = 2
		
		export = np.array(icemask,dtype=np.uint8)
		self.masksave('Masks/Max_AWP_extent_south.bin',export)
		self.maskview(icemask)
		plt.show()
		
		
	def masksave(self,filename,export):
		with open(filename, 'wb') as msk:
			msk.write(export)

	def maskview(self,icemap):		
		icemap = icemap.reshape(332, 316)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=4, cmap=plt.cm.jet)
			
		
action = Mask_creater()
action.MaxExtent()
#action.Coastalmask()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
