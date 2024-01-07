import numpy as np
import CryoIO
import matplotlib.pyplot as plt

class NSIDC_area:

	def __init__  (self):
		self.Cdate = CryoIO.CryoDate(2022,1,1) # initilizes a 366 day year
		
		self.daycount = 366 #366year, 186summer
		
		self.macro_region = [['Date'],['Area'],['Extent'],['Compaction']]
		
		self.region_area = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
					, ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
					, ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
		self.region_extent = [['Sea_of_Okhotsk'], ['Bering_Sea'], ['Hudson_Bay'], ['Baffin_Bay'], ['East_Greenland_Sea']
					, ['Barents_Sea'], ['Kara_Sea'], ['Laptev_Sea'], ['East_Siberian_Sea'], ['Chukchi_Sea']
					, ['Beaufort_Sea'], ['Canadian_Archipelago'], ['Central_Arctic']]
		
		self.masksload()
		self.initRegions()
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		filepath = './'
		filename = f'{filepath}/Masks/Arctic_region_mask.bin'
		self.regmaskf = CryoIO.openfile(filename,np.uint32)

		filename = f'{filepath}/Masks/psn25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
		
# 		self.maskview(self.regmaskf)
# 		plt.show()

	def initRegions(self):
		self.area_init = []
		self.extent_init = []
		
		for x in range(0,len(self.region_area)):
			self.area_init.append([])
			self.extent_init.append([])
			

	def appendregion(self):

		for x in range(0,len(self.region_area)):
			self.region_area[x].append(int(np.sum(self.area_init[x]))/1e6)
			
		for x in range(0,len(self.region_extent)):
			self.region_extent[x].append(int(np.sum(self.extent_init[x]))/1e6)
			
		self.initRegions()
		
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		filepath = './DataFiles/'
		for count in range (0,self.daycount,1):
			year = self.Cdate.year
			month = self.Cdate.strMonth
			day = self.Cdate.strDay
			filename = f'{year}/NSIDC_{year}{month}{day}.npz'
			filenameMean = f'Mean_00_19/NSIDC_Mean_{month}{day}.bin'
			print(filename)
			
			#loads data file
			ice = CryoIO.readnumpy(f'{filepath}{filename}')/250
		
			#area & extent calculation
			aaa = np.vectorize(self.calculateAreaExtent)
			area,extent = aaa(ice,self.areamaskf,self.regmaskf)
			
			compaction = (np.sum(area)/np.sum(extent))*100
			self.macro_region[0].append('{}/{}/{}'.format(year,month,day))
			self.macro_region[1].append((np.sum(area))/1e6)
			self.macro_region[2].append (np.sum(extent)/1e6)
			self.macro_region[3].append(round(compaction,3))
			
			self.appendregion()
			self.Cdate.datecalc()
				
					
	def calculateAreaExtent(self,icemap,areamask,regionmask):
		'''area & extent calculation & ignore lake ice'''
		area = 0
		extent = 0
		
		if 1 < regionmask < 16:
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
				if regionmask == 2:
					self.area_init[0].append (area)
					self.extent_init[0].append (areamask)
				elif regionmask == 3:
					self.area_init[1].append (area)
					self.extent_init[1].append (areamask)
				elif regionmask == 4:
					self.area_init[2].append (area)
					self.extent_init[2].append (areamask)
				elif regionmask == 6:
					self.area_init[3].append (area)
					self.extent_init[3].append (areamask)
				elif regionmask == 7:
					self.area_init[4].append (area)
					self.extent_init[4].append (areamask)
				elif regionmask == 8:
					self.area_init[5].append (area)
					self.extent_init[5].append (areamask)
				elif regionmask == 9:
					self.area_init[6].append (area)
					self.extent_init[6].append (areamask)
				elif regionmask == 10:
					self.area_init[7].append (area)
					self.extent_init[7].append (areamask)
				elif regionmask == 11:
					self.area_init[8].append (area)
					self.extent_init[8].append (areamask)
				elif regionmask == 12:
					self.area_init[9].append (area)
					self.extent_init[9].append (areamask)
				elif regionmask == 13:
					self.area_init[10].append (area)
					self.extent_init[10].append (areamask)
				elif regionmask == 14:
					self.area_init[11].append (area)
					self.extent_init[11].append (areamask)
				elif regionmask == 15:
					self.area_init[12].append (area)
					self.extent_init[12].append (areamask)
				
		return area,extent
	
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(448, 304)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=16, cmap=plt.cm.jet)
# 		plt.savefig('aaa.png')

		
	def exportdata(self):
		filepath = './CSVdata/regional_raw/'
# 		CryoIO.csv_columnexport(f'{filepath}NSIDC_Area.csv_{self.Cdate.year}',self.macro_region)
		CryoIO.csv_columnexport(f'{filepath}Regional_area_{self.Cdate.year-1}.csv',self.region_area)
		CryoIO.csv_columnexport(f'{filepath}Regional_extent_{self.Cdate.year-1}.csv',self.region_extent)
	

		


action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	action.dayloop()
# 	action.exportdata()

	

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