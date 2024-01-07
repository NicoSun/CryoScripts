"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun
The script downloads 80N temperature data from the DMI
ftp://ftp.dmi.dk/plus80N_temperatureindex/
"""

import urllib.request
import datetime
import csv
import FDD_year
import FDD_Season
import Temp_graph

class Downloader:

	def __init__  (self):
		'''initializes the current date'''
		self.today = datetime.date.today() - datetime.timedelta(days=1)
		self.day = self.today.day
		self.month = self.today.month
		self.year = self.today.year


	def download(self):
		'''downloads the latest temp data file'''
		#response = urllib.request.urlopen('http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_'+str(self.year)+'.png')
		response = urllib.request.urlopen('ftp://ftp.dmi.dk/plus80N_temperatureindex/meanT'+str(self.year)+'_running.txt')
		data = response.read()
			
		filename = 'X:/DMI/DMI_80N_'+str(self.year)+'.csv'
		file_ = open(filename, 'wb')
		file_.write(data)
		file_.close()
			
		#http://ocean.dmi.dk/arctic/plots/meanTarchive/meanT_2016.png
		print('Download done')
			
	def listappend(self):
		'''creates a new csv file from the downloaded file (sometimes the DMI failes to provide data for a date and
		 this function then duplicates the last available date. With some days missing the graph would become too short and greatly distorted in shape.
		 After a full year it's recommended to use interpolated values for missing dates)'''
		with open('DMI_80N_'+str(self.year)+'.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ')
			spamreader = list(spamreader)
	
		fields=[spamreader[-1][0],spamreader[-1][1],spamreader[-1][2]]
		with open('ZZZ_80N_List.csv', 'a',newline='') as f:
			writer = csv.writer(f)
			writer.writerow(fields)
			
	def Tempcalc(self):
		'''starts the FDD calculation'''
		self.download()
		self.listappend()
		Temp_graph.tempcalc.automated(self.year,self.month,self.day)
		FDD_year.fddcalc.automated(self.year,self.month,self.day)
		
		if self.month < 6 or self.month > 8:
			FDD_Season.fddcalc.automated(self.year,self.month,self.day)
		
		print(self.day,self.month,self.year)

action = Downloader()
action.Tempcalc()
#action.getday()
