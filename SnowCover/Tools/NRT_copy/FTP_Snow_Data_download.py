from ftplib import FTP
import datetime
from datetime import timedelta
import File_Manager
import Daily_NOAA_Snow_npz
import Daily_NOAA_Graphs


class Downloader:

	def __init__  (self):
		self.today = datetime.date.today()
		self.yesterday = self.today-timedelta(days=1)
		self.day_of_year = self.today.timetuple().tm_yday-1
		self.year = self.today.year
		self.month = self.today.month
		self.day = self.today.day
		self.dof = str(self.day_of_year).zfill(3)
# 		print(self.day_of_year)


	def mass_download(self):
		'''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		start = 320
		for count in range (start,321): #366
			try:
				filename = f"ims'{self.year}{count.zfill(3)}_00UTC_24km_v1.3.asc.gz" # final data
				filenameformatted = f'/home/nico/Cryoscripts/SnowCover/DataFiles/gzip_files/NOAA_{self.year}{count}_24km_v1.1.asc.gz'
				print(filename)
				ftp.cwd(f'/pub/DATASETS/NOAA/G02156/24km/{self.year}' )# final gsfc
				ftp.retrbinary('RETR '+filename, open(filenameformatted, 'wb').write)
				self.extract(filenameformatted[21:])
			except:
				print('Error: '+str(self.year)+str(count).zfill(3))
			
		print('Done')
		ftp.quit()
		
	def daily_download(self):
		'''downloads latest date'''
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		
		try:
			filename = f"ims{self.year}{self.dof}_00UTC_24km_v1.3.asc.gz" # final data
			filenameformatted = f'/home/nico/Cryoscripts/SnowCover/DataFiles/gzip_files/NOAA_{self.year}{self.dof}_24km_v1.3.asc.gz'
			print(filename)
			ftp.cwd('/pub/DATASETS/NOAA/G02156/24km/'+str(self.year))  # final gsfc
			ftp.retrbinary('RETR '+filename, open(filenameformatted, 'wb').write)
			ftp.quit()
		except:
			print(f'Error: {self.year}{self.dof}')

		self.process_data(filenameformatted[54:])
		
		print('Done')


			
	def process_data(self, filenameformatted):
		'''extracts file, calculates extent & creates map/graphs'''
		print(filenameformatted)
		File_Manager.dailyupdate(filenameformatted)
		Daily_NOAA_Snow_npz.action.automated(self.year,self.month,self.day,self.day_of_year)
#		Snow_Daily_AWP.action.automated(self.year,self.month,self.day,self.dof)
		Daily_NOAA_Graphs.action.automated(self.year,self.month,self.day,self.day_of_year)
#		Snow_Daily_AWP_Graphs.action.automated(self.year,self.month,self.day,self.dof)
		
	def manualdownload(self,year,date):
		self.day_of_year = date
		self.year = year
		self.dof = str(self.day_of_year).zfill(3)
		
		self.daily_download()
		filenameformatted = f'/home/nico/Cryoscripts/SnowCover/DataFiles/gzip_files/NOAA_{self.year}{self.dof}_24km_v1.3.asc.gz'
		File_Manager.dailyupdate(filenameformatted[54:])
		

action = Downloader()

#action.mass_download()
action.daily_download()
# action.manualdownload(2022,365)

'''

National Ice Center. 2008, updated daily. IMS Daily Northern Hemisphere Snow and Ice Analysis at 1 km, 4 km, and 24 km Resolutions, Version 1.1-1.3. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi: https://doi.org/10.7265/N52R3PMC.
'''