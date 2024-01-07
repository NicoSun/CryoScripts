import CryoIO
import numpy as np
import os

class npz_converter:
	
	def __init__  (self):
		self.Cdate = CryoIO.CryoDate(2022,1,1) # initilizes a 366 day year
		
		self.daycount = 366 #366year

	def dayloop(self,year):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		self.year = year
		filepath = '/home/nico/Cryoscripts/NSIDC_South/DataFiles/'
		for count in range (0,self.daycount,1):
			year = self.Cdate.year
			month = self.Cdate.strMonth
			day = self.Cdate.strDay
			filename = f'{year}/NSIDC_{year}{month}{day}_south.bin'
			filename_npz = filename[:-3] + 'npz'

			icef = CryoIO.openfile(f'{filepath}{filename}', np.uint8)
			ice = np.array(icef,dtype=np.uint8)
			
			CryoIO.savenumpy(f'{filepath}{filename_npz}', ice)
			os.remove(f'{filepath}{filename}')
			self.Cdate.datecalc()
			
action = npz_converter()
action.dayloop(2021)
# =============================================================================
# for year in range(2005,2021):
# 	action.dayloop(year)
# 	print(year)
# =============================================================================
