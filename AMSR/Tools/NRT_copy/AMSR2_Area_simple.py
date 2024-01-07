import numpy as np
import matplotlib.pyplot as plt
import os
import CryoIO

from datetime import date
from datetime import timedelta

from multiprocessing import Pool

import logging

niceValue = os.nice(15)


class NSIDC_area:

	def __init__  (self):
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		self.CSVCompaction = ['Compaction']
		
		self.hemi = 'nh'
		self.threads = 24
		
		self.masksload()
		logging.basicConfig(filename=f'logs/areatest_{self.hemi}.log', level=logging.INFO)
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		filepath = '/media/prussian/Cryosphere/AMSR/Masks/'
		
		filename = f'AMSR2_{self.hemi}_land.npz'
		self.landmask = CryoIO.readnumpy(f'{filepath}{filename}').flatten()

# =============================================================================
# 		self.maskview(self.landmask)
# 		plt.show()
# =============================================================================

		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		
		self.start = date(2012,7,4) #first data date(2012, 7, 4)
		self.end = date(2023,4,16)
		self.daycount = (self.end - self.start).days
		loopday	= self.start
		
		filename_list = []
		for count in range (0,self.daycount,1):
			datestring = loopday.strftime('%Y%m%d')
			if self.hemi == 'nh':
				filepath = f'DataFiles/north/{loopday.year}/'
			else:
				filepath = f'DataFiles/south/{loopday.year}/'
			filename = f'AMSR2_{self.hemi}_v110_{datestring}.npz'
			filelocation = f'{filepath}{filename}'
			filename_list.append(filelocation)
			
			self.CSVDatum.append(loopday)
			loopday += timedelta(days=1)
			
		p = Pool(processes=self.threads)
		data = p.map(self.threaded, filename_list)
		p.close()
		
		for x in range(0,len(data)):
			area = data[x][0]/1e6
			extent = data[x][1]/1e6
			self.CSVArea.append(area)
			self.CSVExtent.append (extent)
			
			compaction = (area/extent)*100
			self.CSVCompaction.append(round(compaction,3))
			
			
	def threaded(self,filename):
		
		area = extent = 0
		#loads data file
		try:
			#loads data file
			ice = CryoIO.readnumpy(filename).flatten()
			ice = np.ma.masked_greater(ice, 100)
			ice = np.ma.masked_less(ice, 15)
			area = ice * 9.76/100
			extent = ice/ice * 9.76
		except:
			logging.info(filename)
			
		return np.sum(area), np.sum(extent)
# =============================================================================
# 			#area & extent calculation
# 			aaa = np.vectorize(self.calculateAreaExtent)
# 			area,extent = aaa(ice,self.landmask)
# =============================================================================
			

			
	def calculateAreaExtent(self,icemap,landmask,areamask=9.76):
		'''area & extent calculation & remove lake ice'''
		area = 0
		extent = 0

		if 14 < icemap < 101:
			area = icemap*areamask/100
			extent = areamask

		return area,extent
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		if self.hemi == 'nh':
			icemap = icemap.reshape(3300, 2100)
		else:
			icemap = icemap.reshape(2500, 2200)
		plt.imshow(icemap, interpolation='nearest', vmin=-180, vmax=180, cmap=plt.cm.jet)

		
	def exportdata(self):
		CryoIO.csv_columnexport(f'AMSR2_test_{self.hemi}.csv',
			[self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction])

	
	def automated (self,day,month,year,daycount):
		self.year = year
		self.month = month
		self.day = day
		self.daycount = daycount
		self.maintanance()
		
		self.loadCSVdata(self.daycount-1)
		self.loadCSVRegiondata(self.daycount-1)
		self.dayloop()
		self.exportdata()



action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
# 	action.dayloop()
# 	action.exportdata()
# 	action.automated(30,12,2021,3) #note substract xxx days from last available day

	

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
