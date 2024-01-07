from ftplib import FTP
import numpy as np


class Downloader:

	def __init__  (self):
		'''initializes date'''
		self.year = 2018
		self.month = 1
		self.day = 1
		self.daycount = 1 #year
		self.mode = 'final' #'final or nrt
		
		#the filename changes on the following days
		#start:n07, 19870821: f08, 1991219: f11 ,19950930: f13, 2008: f17

		

	def dayloop(self):
		'''downloads data'''
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			filenameformatted = 'X:/NSIDC_south/DataFiles/NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			if self.mode == 'nrt':
				filenameNRT = 'nt_{}{}{}_f18_nrt_s.bin'.format(self.year,self.stringmonth,self.stringday) # near realtime
				ftp.cwd('/pub/DATASETS/nsidc0081_nrt_nasateam_seaice/south/')              # near realtime
				ftp.retrbinary('RETR '+filenameNRT, open(filenameformatted, 'wb').write)
				
			if self.mode == 'final':
				filenamefinal = 'nt_{}{}{}_f08_v1.1_s.bin'.format(self.year,self.stringmonth,self.stringday) # final data
				ftp.cwd('/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/'+str(self.year))  # final gsfc
				ftp.retrbinary('RETR '+filenamefinal, open(filenameformatted, 'wb').write)
				
			
			try:
				self.formatfile(filenameformatted)
			except:
				print('cant format')
						
			self.day = self.day+1
			if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
				self.day=1
				self.month = self.month+1
			elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
				self.day=1
				self.month = self.month+1
			elif self.day==30 and self.month==2:
				self.day=1
				self.month = self.month+1
			elif  self.day==32 and self.month == 12:
				self.day = 1
				self.month = 1
				self.year = self.year+1
				
		print('Done')
		ftp.quit()
		
			
	def formatfile(self, newfilename):
		'''removes header'''
		with open(newfilename, 'rb') as fr:
			header = fr.read(300)
			ice = np.fromfile(fr, dtype=np.uint8)

		with open(newfilename, 'wb') as frr:
			frr.write(ice)

		print(self.year,self.month,self.day)

action = Downloader()
action.dayloop()

