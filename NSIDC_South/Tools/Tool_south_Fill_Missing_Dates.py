import numpy as np
import os
from datetime import date
from datetime import timedelta
import CryoIO

class NSIDC_Filler:

	def __init__  (self):
		self.start = date(2022,11, 9)
		self.year = self.start.year
		self.month = self.start.month
		self.day = self.start.day
		
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		self.daycount = 1 #366year, 186summer
		###Missing:1987-12-03 to 1988-01-12
		
	def dayloop(self):
		self.loopday	= self.start
		
		filename = '/home/nico/Cryoscripts/NSIDC_South/Masks/region_s_pure.msk'
		self.regmask = CryoIO.openfile(filename,np.uint8)
			
		for count in range (0,self.daycount,1): 
			filepath = f'DataFiles/{self.year}'
			filename = f'NSIDC_{self.year}{self.stringmonth}{self.stringday}_south.npz'
		
			try:
				ice = CryoIO.openfile(os.path.join(filepath,filename),np.uint8)
			except FileNotFoundError:
				
				#longgap_code
				ice = self.longgap(filepath,count)
			
# =============================================================================
# 				filenamePlus1 = 'NSIDC_{}_south.bin'.format(self.calcday(1))
# 				filenameMinus1 = 'NSIDC_{}_south.bin'.format(self.calcday(-1))
# 				
# 				iceP1 = CryoIO.openfile(os.path.join(filepath,filenamePlus1),np.uint8)
# 				iceM1 = CryoIO.openfile(os.path.join(filepath,filenameMinus1),np.uint8)
# 				
# 				ice = np.add(iceP1 , iceM1) *0.5
# 				ice = np.array(ice, dtype=np.uint8)
# =============================================================================
	
				CryoIO.savebinaryfile(os.path.join(filepath,filename), ice)

			except Exception as e:
				print(e)
				
			print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
			self.advanceday(1)
			
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.month = self.loopday.month
		self.day = self.loopday.day
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		return '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
	def calcday(self,delta):	
		loopday = self.loopday+timedelta(days=delta)
		year = loopday.year
		month = loopday.month
		day = loopday.day
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		return '{}{}{}'.format(year,stringmonth,stringday)
	
	def longgap(self,filepath,count):
		
		filenamePlus1 = 'NSIDC_20221108_south.bin'
		filenameMinus1 = 'NSIDC_20221110_south.bin'
		
		iceP1 = CryoIO.openfile(os.path.join(filepath,filenamePlus1),np.uint8)
		iceM1 = CryoIO.openfile(os.path.join(filepath,filenameMinus1),np.uint8)
				
		
		ice = np.zeros(len(iceP1),dtype=float)
		for x in range (0,len(iceP1)):
			if self.regmask[x] < 10:
				ice[x] = iceM1[x]+(iceP1[x]-iceM1[x])*((count)/(self.daycount))
			elif self.regmask[x] > 9:
				ice[x] = 255

		ice = np.array(ice,dtype=np.uint8)
		return ice

	def gapyear(self):
		self.year = 2023
		self.month = 2
		self.day = 29
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
			
		filepath = f'/home/nico/Cryoscripts/NSIDC_South/DataFiles/{self.year}'
		filename = 'NSIDC_{}{}{}_south.npz'.format(self.year,self.stringmonth,self.stringday)
		
		filenamePlus1 = 'NSIDC_{}0301_south.npz'.format(self.year)
		filenameMinus1 = 'NSIDC_{}0228_south.npz'.format(self.year)
		
		iceP1 = CryoIO.readnumpy(os.path.join(filepath,filenamePlus1))
		iceM1 = CryoIO.readnumpy(os.path.join(filepath,filenameMinus1))
				
		ice = np.add(iceP1 , iceM1) *0.5
		ice = np.array(ice, dtype=np.uint8) 
			
		CryoIO.savenumpy(os.path.join(filepath,filename), ice)
			
				
		print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))	

action = NSIDC_Filler()
if __name__ == "__main__":
	print('main')
# 	action.dayloop()
	action.gapyear()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA