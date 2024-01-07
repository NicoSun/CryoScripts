from multiprocessing import Pool
import numpy as np
import time
import CryoIO


def test():
	p = Pool(processes=5)
	data = p.map(action.threaded, action.filename_list)

class NSIDC_area:

	def __init__  (self):
		self.Cdate = CryoIO.CryoDate(2022,1,1) # initilizes a 366 day year
		
		self.daycount = 36 #366days * 41years
		self.threads = 6
		
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.masksload()


	def masksload(self):
		fielpath = '/home/nico/Cryoscripts/NSIDC/'
		filename = f'{fielpath}Masks/Arctic_region_mask.bin'
		self.regmaskf = CryoIO.openfile(filename,np.uint32)

		filename = f'{fielpath}Masks/psn25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000
		
	def calculateAreaExtent(self,icemap,areamask,regionmask):
		area = 0
		extent = 0

		if  1 < regionmask < 16:
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
		return area,extent
		
	def dayloop(self):
		self.start = time.time()
		self.filepath = '/home/nico/Cryoscripts/NSIDC/DataFiles/'
		filename_list = []
		for count in range (0,self.daycount,1): 
			year = self.Cdate.year
			month = self.Cdate.strMonth
			day = self.Cdate.strDay
			
			filename = f'{year}/NSIDC_{year}{month}{day}.npz'
#			filename_mean = 'Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			
			filename_list.append(filename)

			self.CSVDatum.append('{}/{}/{}'.format(year,month,day))
			print(year,month,day)
			self.Cdate.datecalc()
					
		p = Pool(processes=self.threads)
		data = p.map(self.threaded, filename_list)
		p.close()
#		print(data)
		
		for x in range(0,len(data)):
			self.CSVArea.append(data[x][0]/1e6)
			self.CSVExtent.append (data[x][1]/1e6)
		
		self.end = time.time()
		self.CSVDatum.append (round(self.end-self.start,3))
		self.CSVArea.append (' seconds ')
		self.CSVExtent.append (str(round((self.end-self.start)/self.daycount,3))+' seconds/day')
		
	def threaded(self,filename):
		file = f'{self.filepath}{filename}'
		ice = CryoIO.readnumpy(file)/250
			
		area=[]
		extent = []
		
		aaa = np.vectorize(self.calculateAreaExtent)
		area,extent = aaa(ice,self.areamaskf,self.regmaskf)

		return np.sum(area),np.sum(extent)
		
			
	def exportdata(self):
		filepath = '/home/nico/Cryoscripts/NSIDC/temp/'
		CryoIO.csv_columnexport(f'{filepath}NSIDC_Area_multithread.csv',
			[self.CSVDatum,self.CSVArea,self.CSVExtent])

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	action.exportdata()
# 	test()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

'''
#regionmask
0; Lakes
1: open ocean
2-15: Arctic regions
20: Land
21: coast
'''