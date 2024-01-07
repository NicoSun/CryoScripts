import numpy as np
import os
import CryoIO


class NOAA_Filler:

	def __init__  (self):
		self.year = 2001
		self.daycount = 366
		
	def dayloop(self):
			
		for day_of_year in range (1,self.daycount): 
			stringday = str(day_of_year).zfill(3)
			filename = f'DataFiles/{self.year}/NOAA_{self.year}{stringday}_24km.npz'
#			print(filename)
		
			try:
				ice = CryoIO.readnumpy(filename)

			except FileNotFoundError:
				stringdayM1 = str(day_of_year-1).zfill(3)
				filenameMinus1 = f'DataFiles/{self.year}/NOAA_{self.year}{stringdayM1}_24km.npz'
				
				iceM1 = CryoIO.readnumpy(filenameMinus1)
				CryoIO.savenumpy(filename,iceM1)
			
			except Exception as e:
				print(e)
				
			print(f'{self.year}-{stringday}')


action = NOAA_Filler()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	#action.gapyear()