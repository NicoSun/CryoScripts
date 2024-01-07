import numpy as np
import pandas
from datetime import date
from datetime import timedelta
import os
import re

class Downloader:

	def __init__  (self):
		self.year = 2018
		self.month = 1
		self.day = 1
		self.daycount = 365
		
		self.today = date(self.year, self.month, self.day)
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		Columns = ['hole']
		csvdata = pandas.read_csv('Tools/2008_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		 		
		Columns = ['edge']
		csvdata = pandas.read_csv('Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		

	def move_files(self,year):
		'''this function moves data into a year folder'''
		filepath = 'DataFiles/'
		filepath_2 = f'DataFiles/{year}/'
		for file in os.listdir(filepath):		
			pattern = r'NSIDC_{}'.format(str(year))
			match = re.search(pattern,file)
			if match:
				os.rename(os.path.join(filepath,file),os.path.join(filepath_2,file))
				
	def create_folders(self,year):
		'''this function creates folders'''
		
		# Directory
		directory = "DataFiles"
		
		path = os.path.join(directory, str(year))
		os.mkdir(path)
		

action = Downloader()
#action.AWPcalc_north()

if __name__ == '__main__':
# 	action.create_folders(2000)
	for year in range (1978,2026):
		action.move_files(year)
# 		action.create_folders(year)
