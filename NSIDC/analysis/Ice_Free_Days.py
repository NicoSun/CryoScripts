from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import CryoIO



class NSIDC_IcefreeDays:

	def __init__  (self):
		self.root = '../'
		self.masksload()
		
	def masksload(self):
		filename = f'{self.root}Masks/Arctic_region_mask.bin'
		self.regmask = CryoIO.openfile(filename,np.uint32)


	def dayloop(self,year):
		self.Cdate = CryoIO.CryoDate(year,1,1) # initilizes a 366 day year
		
		icefreecount = np.zeros(len(self.regmask))
		filepath = '../DataFiles/'
		for count in range (0,366):
			year = self.Cdate.year
			month = self.Cdate.strMonth
			day = self.Cdate.strDay
			filename = f'{year}/NSIDC_{year}{month}{day}.npz'
			ice = CryoIO.readnumpy(f'{filepath}{filename}') # !!!don't divide by 250!!!
				
			# loads the mean data file
# 			filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}.bin'
# 			iceMean = CryoIO.openfile(f'{filepath}{filenameMean}',np.uint8)/250


			aaa = np.vectorize(self.daycalc)
			icefreecount= aaa(icefreecount,ice)
			self.Cdate.datecalc()
			print('Date: {}-{}-{}'.format(year,month,day))
			
		self.normalshow(icefreecount,year)
# 		CryoIO.savenumpy(f'{self.root}temp/Icefreedays_{year}.npz', icefreecount)

# 		plt.show()
		
	
	def daycalc(self,icefreecount,ice):
		'''calculates icefree days'''
	
		if ice < 37:
			icefreecount += 1
		elif ice > 250:
			icefreecount = 400
		return icefreecount
			
		
	def normalshow(self,icemap,year):
		icemap = icemap.reshape(448, 304)
				
		cmap = plt.cm.magma_r # plt.cm.jet
		cmap.set_bad('black',0.66)
		
		map1 = np.ma.masked_outside(icemap,0,370) 
		
		fig = plt.figure(figsize=(7, 8))
		ax = fig.add_subplot(111)

		cax = ax.imshow(map1, interpolation='nearest', vmin=0, vmax=300, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[0,50,100,150,200,250,300]).set_label('Ice Free Days')
		
		ax.imshow(map1, interpolation='nearest', vmin=0, vmax=300, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_title('Arctic Ice Free Days: {}'.format(year),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		ax.set_xlabel('cryospherecomputing.com/IceFreeDays',x=0.50)
		ax.set_ylabel('nsidc.org/data/NSIDC-0051',y=0.15)
		fig.tight_layout()

		fig.savefig(f'{self.root}temp/images/Arctic_IceFreeDays_{year}.png')
		plt.close()

	def anomalyshow(self,icemap,year):
		cmap = plt.cm.RdBu # plt.cm.jet
		cmap.set_bad('black',0.66)
		
		for x,y in enumerate(self.regmask):
			if y > 15:
				icemap[x] = 400
		
		icemap = np.ma.masked_outside(icemap,-300,370) 
		icemap = icemap.reshape(448, 304)
		fig = plt.figure(figsize=(7, 8))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=-100, vmax=100, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[-100,-50,0,50,100]).set_label('Ice Free Days Anomaly')
		
		ax.imshow(icemap, interpolation='nearest', vmin=-100, vmax=100, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_title('Arctic Ice Free Days Anomaly: {}'.format(year),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 16, r'Anomaly Base: 2000-19', fontsize=10,color='black',fontweight='bold')
		ax.set_xlabel('cryospherecomputing.com/IceFreeDays',x=0.50)
		ax.set_ylabel('nsidc.org/data/NSIDC-0051',y=0.15)
		fig.tight_layout()

		fig.savefig(f'{self.root}temp/images/Arctic_IceFreeDays__anom_{year}.png')
		plt.close()
		
	def calcanomaly(self):
		
		icemean = np.zeros(len(self.regmask))
		icedict = {}

		for year in range(1979,2023):
			filename = f'{self.root}temp/Icefreedays_{year}.npz'
			ice = CryoIO.readnumpy(filename)
			icedict[year] = ice
				
			if 1999 < year < 2020:
				icemean += ice/20
				
		for key,value in icedict.items():
			print(key)
			iceanomaly = icemean - value
			self.anomalyshow(iceanomaly,key)

# 		plt.show()
		


# =============================================================================
# def spawnprocess(datalist):
# 	action = NSIDC_IcefreeDays()
# 	data = action.dayloop(datalist[0])
# 	
# 	return data
# 	
# if __name__ == '__main__':
# 	datalist = []
# 	for year in range(1979,2023):
# 		datalist.append([year])
# 	
# 	p = Pool(processes=23)
# 	data = p.map(spawnprocess, datalist)
# 	p.close()
# =============================================================================

if __name__ == '__main__':
	action = NSIDC_IcefreeDays()
	action.calcanomaly()
# 	action.dayloop(2020)
	
'''
Values are coded as follows:

0-250  concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''