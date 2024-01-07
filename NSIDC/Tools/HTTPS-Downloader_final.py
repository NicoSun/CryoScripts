import requests
from io import BytesIO
import numpy as np
import pandas
import datetime
from datetime import timedelta
import time
import CryoIO


class Downloader:

	def __init__  (self):
		self.daycount = 365
		self.start = datetime.date(2022,1,1)
		self.date = self.start
		self.year = self.date.year
		self.stringmonth = str(self.date.month).zfill(2)
		self.stringday = str(self.date.day).zfill(2)
		
		self.urllist = []
		self.namelist = []
		
		
		Columns = ['hole']
		csvdata = pandas.read_csv('NSIDC/Tools/2008_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		 		
		Columns = ['edge']
		csvdata = pandas.read_csv('NSIDC/Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		

	def dayloop(self):
		
		self.session = requests.Session()
		
		for count in range (0,self.daycount,1): #372
			
			self.create_url_list()
#			time.sleep(1)

			#day advance
			self.date = self.date+timedelta(days=1)
			self.year = self.date.year
			self.stringmonth = str(self.date.month).zfill(2)
			self.stringday = str(self.date.day).zfill(2)
			print(self.date)
		
#		print(self.namelist)
		self.download()
			
	def create_url_list(self):
		newfilename =  f'NSIDC/DataFiles/{self.year}/NSIDC_{self.year}{self.stringmonth}{self.stringday}.npz'
		newfilename_south =  f'NSIDC_South/DataFiles/{self.year}/NSIDC_{self.year}{self.stringmonth}{self.stringday}_south.npz'
		
#		newfilename = 'test/NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
#		newfilename_south = 'test/NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		
		folder_n = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/north/daily/{}/'.format(self.year)
		folder_s = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/{}/'.format(self.year)
		file_north = 'nt_{}{}{}_f17_v01_n.bin'.format(self.year,self.stringmonth,self.stringday)
		file_south = 'nt_{}{}{}_f17_v01_s.bin'.format(self.year,self.stringmonth,self.stringday)
		
		url_n = folder_n + file_north
		url_s = folder_s + file_south
		
		self.urllist.append(url_n)
		self.urllist.append(url_s)
		
		self.namelist.append(newfilename)
		self.namelist.append(newfilename_south)
		


	def download(self):
		
		# get the requested data, note that the auth. Login credentials have to be in .netrc file
#		username, password = 'name@email.com', 'password'
		
		for index, url in enumerate(self.urllist):
		
			resp = self.session.get(url, stream=True)
			
			f = BytesIO(resp.content)
			
			icemap = f.getbuffer()
			icemap = np.frombuffer(icemap[300:],dtype=np.uint8)
			
			if len(icemap) > 136000:
				icemap = self.formatdata(icemap)
					
			CryoIO.savenumpy(self.namelist[index], icemap)
			
		
			
	def formatdata(self,icemap):
	
		icepolecon = []
		for val in self.icepoleedge:
			icepolecon.append (icemap[val])
			
		icepolecon = np.mean(icepolecon)
		
		for val2 in self.icepole:
			icemap[val2] = icepolecon
	
		return icemap
			

action = Downloader()
action.dayloop()
#action.binarytest()