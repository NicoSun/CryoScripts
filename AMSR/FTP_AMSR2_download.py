from ftplib import FTP
from datetime import date
from datetime import timedelta
import logging
import io

logging.basicConfig(filename='logs/FTP_download.log', level=logging.INFO)
import File_Manager

class AMSR2_Downloader:

	def __init__  (self):
		self.today = date.today()
		self.yesterday = self.today-timedelta(days=1)
		self.year = self.yesterday.year
		self.stringmonth = str(self.yesterday.month).zfill(2)
		self.stringday = str(self.yesterday.day).zfill(2)
		

	def test_download(self):
		'''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
		ftp = FTP('ftp.awi.de')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@

		hemi = 'sh'
		filename = f"{hemi}_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
		
		if(hemi == 'nh'):
			filenameformatted = f'DataFiles/AMSR2_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
		else:
			filenameformatted = f'DataFiles/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
		print(filename)
		ftp.cwd(f'/sea_ice/product/amsr2/v110/{hemi}/{self.year}/{self.stringmonth}')
# =============================================================================
# 		ftp.retrbinary('RETR '+filename, open(f'DataFiles/{filename}', 'wb').write) #old version
# 		File_Manager.dailyupdate_old(f'DataFiles/{filename}',filenameformatted,hemi) #old version
# =============================================================================

		download = io.BytesIO()
		ftp.retrbinary('RETR '+filename, download.write)
		File_Manager.dailyupdate(download,filenameformatted,hemi)
			
		print('Done')
		ftp.quit()


	def mass_download(self):
		'''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
		
		ftp = FTP('ftp.awi.de')     # connect to host, default port
		ftp.login()  # user anonymous, passwd anonymous@
		self.start = date(2023, 3, 9) #first data date(2012, 7, 4)
		self.end = date(2023,4,15)
		
		self.daycount = (self.end - self.start).days
		print(self.daycount)
		self.stringmonth = str(self.start.month).zfill(2)
		self.stringday = str(self.start.day).zfill(2)
		loopday	= self.start
		
		hemi = 'sh'
		for count in range (0,self.daycount): #366
			try:
				filename = f"{hemi}_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
				
				if hemi == 'nh':
					filenameformatted = f'DataFiles/north/{self.year}/AMSR2_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
				else:
					filenameformatted = f'DataFiles/south/{self.year}/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
				print(loopday)
				ftp.cwd(f'/sea_ice/product/amsr2/v110/{hemi}/{self.year}/{self.stringmonth}') 
# =============================================================================
# 				ftp.retrbinary('RETR '+filename, open(f'DataFiles/{filename}', 'wb').write)  #old version
# 				File_Manager.dailyupdate_old(f'DataFiles/{filename}',filenameformatted,hemi) #old version
# =============================================================================
				
				download = io.BytesIO()
				ftp.retrbinary('RETR '+filename, download.write)
				File_Manager.dailyupdate(download,filenameformatted,hemi)
				
			except:
				logging.error(f'Error: {filename}')

				
			loopday += timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
			
		print('Done')
		ftp.quit()
		
	def daily_download(self):
		'''downloads latest date'''
		
		ftp = FTP('ftp.awi.de')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@

		filename = f"nh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
		filename_sh = f"sh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
		filenameFormatted = f'/home/nico/Cryoscripts/AMSR/DataFiles/north/{self.year}/AMSR2_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
		filenameFormatted_sh = f'/home/nico/Cryoscripts/AMSR/DataFiles/south/{self.year}/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
		
		# print(filename)
		download = io.BytesIO()
		download_sh = io.BytesIO()
		ftp.cwd(f'/sea_ice/product/amsr2/v110/nh/{self.year}/{self.stringmonth}')
		ftp.retrbinary('RETR '+filename, download.write)
		File_Manager.dailyupdate(download,filenameformatted,'nh')
		logging.info(filename)
		
		download = io.BytesIO()
		
		ftp.cwd(f'/sea_ice/product/amsr2/v110/sh/{self.year}/{self.stringmonth}')
		ftp.retrbinary('RETR '+filename_sh, download_sh.write)
		File_Manager.dailyupdate(download,filenameFormatted_sh,'sh')
		
		ftp.quit()
		print('Done')
		

action = AMSR2_Downloader()

# action.test_download()
# action.mass_download()
action.daily_download()
#action.manualdownload(2020,200)

'''

'''