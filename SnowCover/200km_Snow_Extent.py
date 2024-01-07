'''
Climate Data Record (CDR) of Northern Hemisphere (NH) Snow Cover Extent (SCE) 


array size: 7744 (88:88)
'''
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import CryoIO

from datetime import date
from datetime import timedelta


class NOAA_Snow_Cover:


	def __init__  (self):
		self.threads = 2
		
		self.plottype = 'daily' # daily ,  mask
		self.dailyorcumu()
		self.masksload()
		self.mode = 'Mean'
		
		self.CSVDatum = ['Date']
		self.NorthAmericaExtent =['NorthAmericaExtent']
		self.GreenlandExtent =['GreenlandExtent']
		self.EuropeExtent =['EuropeExtent']
		self.AsiaExtent =['AsiaExtent']
		
		
	def masksload(self):

		filename = 'X:/SnowCover/Masks/Rutgers_Region_Mask.msk'
		self.regionmask = CryoIO.openfile(filename,np.uint8)
		
		dataset = Dataset('DataFiles/Low_resolution/nhsce_v01r01_19661004_20200706.nc')
		self.snow_arays = dataset.variables['snow_cover_extent']
		self.land = dataset.variables['land'][:]
		self.gridarea = dataset.variables['area'][:]
		self.gridarea = self.gridarea.reshape(7744)
		self.latitude = dataset.variables['latitude'][:]
		self.longitude = dataset.variables['longitude'][:]
		
#		self.maskview(self.regionmask)
#		plt.show()
		
		
	def dayloop(self):
		extent_list = []
		self.start = date(1966, 10, 4)
		loopday	= self.start
		for x in self.snow_arays:
			loopdate = f'{loopday.year}-{loopday.strftime("%V")}'
			aaa = np.array(x,dtype='uint8').reshape(7744)
#			self.dailyview(aaa,loopdate)
			extent_list.append(aaa)
			self.CSVDatum.append(loopdate)
			loopday += timedelta(weeks=1)
			
		print(len(extent_list))
#		print(filename_list)
		data = map(self.threaded, extent_list)
#		p.close()
		
		for value in data:
			self.NorthAmericaExtent.append (value[0]/1e6)
			self.GreenlandExtent.append (value[1]/1e6)
			self.EuropeExtent.append (value[2]/1e6)
			self.AsiaExtent.append (value[3]/1e6)
			
		CryoIO.csv_columnexport('CSVexport/Low_Res_extent.csv',
			[self.CSVDatum,self.NorthAmericaExtent,self.GreenlandExtent,self.EuropeExtent,self.AsiaExtent])

			
	def threaded(self,extent_map):
		
		aaa = np.vectorize(self.calculateExtent)
		NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent = aaa(extent_map,self.regionmask,self.gridarea)

		return np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)
		

	def calculateExtent(self,icemap,regionmask,pixelarea):
		NorthAmericaExtent = 0
		GreenlandExtent = 0
		EuropeExtent = 0
		AsiaExtent = 0
#		iceanomaly = icemap-icemean
		
		if regionmask==10 and icemap==1:
			NorthAmericaExtent = pixelarea
		if regionmask==20 and icemap==1:
			GreenlandExtent = pixelarea
		if regionmask==30 and icemap==1:
			EuropeExtent = pixelarea
		if regionmask==40 and icemap==1:
			AsiaExtent = pixelarea
	
		return NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent
		
		
	def dailyview(self,snowmap,date):
		snowmap = snowmap.reshape(88,88)
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title(f'Date: {date}',x=0.15)
		self.ax.set_xlabel('NOAA: Snow / Ice Extent')
#		self.cax = self.ax.imshow(snowmap, interpolation='nearest', vmin=-25, vmax=25, cmap=cmap)
		self.cax = self.ax.imshow(snowmap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
#		self.fig.savefig(self.mode)
		plt.pause(0.01)
		
		
	def maskview(self,snowmap):		
		snowmap = snowmap.reshape(88,88)
		fig = plt.figure(figsize=(4.5, 5.5))
		ax = fig.add_subplot(111)
		
		ax.imshow(snowmap, interpolation='nearest')
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.axis('off')
		ax.set_position([0, 0, 1, 1])
#		fig.savefig('Landmask.png',bbox_inches=0)
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(247500, dtype=float)
		self.icenull = self.icenull.reshape(550, 450)
		
		if self.plottype == 'daily':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=1,cmap = plt.cm.jet)
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
#			self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold',x=0.175)
			
# =============================================================================
# 		if self.plottype == 'mask':
# 			self.fig, self.ax = plt.subplots(figsize=(8, 10))
# 			self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
# 			#self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
# #			self.title = self.fig.suptitle('Mask', fontsize=14, fontweight='bold')
# =============================================================================
		
		
		
if __name__ == "__main__":
	action = NOAA_Snow_Cover()
#	action.viewloop()
#	action.masksload()
	action.dayloop()
#	action.writetofile()
#	
'''
0 Ocean
10 North America
20 Greenland
30 Europe
40 Asia
'''