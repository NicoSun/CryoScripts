from datetime import date
from datetime import timedelta
import io
import CryoIO
import numpy as np
import logging

class AMSR2_Downloader:

	def __init__  (self):
		self.active = 1
		
	def error_retry(self):
		from ftplib import FTP
		logging.basicConfig(filename='logs/error_retry2.log', level=logging.INFO)
		import File_Manager
		
		daylist = []
		with open('logs/error_retry1.log','r') as f:
			data = f.read().splitlines()
# 		
		for xxx in data:
			daystring = xxx[22:-4] # [21:-4] [30:-15]
			daylist.append(daystring)
# 			print(daystring)
			
		ftp = FTP('ftp.awi.de')     # connect to host, default port
		ftp.login()  # user anonymous, passwd anonymous@
			
		hemi = 'nh'
		for xxx in daylist:
			print(xxx)
			year = xxx[0:4]
			month = xxx[4:6]
			daystring = xxx[6:8]
# 			filename = f"{hemi}_SIC_LEAD_{xxx}00_{month}{daystring}12.nc.gz" 
			
			day = int(xxx[6:8])
			dayplus = str(day+1).zfill(2)
			dayminus = str(day-1).zfill(2)
# 			filename = f"{hemi}_SIC_LEAD_{xxx}12_{month}{dayplus}00.nc.gz" #following 12h
			filename = f"{hemi}_SIC_LEAD_{year}{month}{dayminus}12_{month}{daystring}00.nc.gz" # previous 12h
			
			
			if hemi == 'nh':
				filenameformatted = f'DataFiles/north/{year}/AMSR2_v110_{xxx}.npz'
			else:
				filenameformatted = f'DataFiles/south/{year}/AMSR2_sh_v110_{xxx}.npz'
				
			ftp.cwd(f'/sea_ice/product/amsr2/v110/{hemi}/{year}/{month}')
			download = io.BytesIO()
			try:
				ftp.retrbinary('RETR '+filename, download.write)
				File_Manager.dailyupdate(download,filenameformatted,hemi)
			except:
				logging.info(filenameformatted[21:-4])

		ftp.quit()
		
	def longgap(self,start,end,year,count):

		filepath = f'DataFiles/north/{year}/'
		
		filenamePlus1 = f'AMSR2_v110_{end}.npz'
		filenameMinus1 = f'AMSR2_v110_{start}.npz'
				
		iceP1 = CryoIO.readnumpy(f'{filepath}{filenamePlus1}')
		iceM1 = CryoIO.readnumpy(f'{filepath}{filenameMinus1}')
		
		iceP1 = np.array(iceP1.flatten())
		iceM1 = np.array(iceM1.flatten())
		
		ice = np.zeros(len(iceP1))
		for x in range (0,len(iceP1)):
			ice[x] = iceM1[x]
			if ice[x] < 101:
				ice[x] += (iceP1[x]-iceM1[x])/(self.daycount/(count+1))

		ice = ice.reshape(3300,2100)
		ice = np.array(ice,dtype=np.uint8)
		return ice
	
	def create_missing_data(self):
		
		self.start = date(2022, 11, 11) #first data date(2012, 7, 4)
		self.end = date(2022,11,13)
		self.daycount = (self.end - self.start).days
		loopday	= self.start
		
		start = self.start.strftime('%Y%m%d')
		end = self.end.strftime('%Y%m%d')
		filepath = f'DataFiles/north/{loopday.year}/'
		
		for xxx in range(0,self.daycount-1):
			loopday += timedelta(days=1)
			day = loopday.strftime('%Y%m%d')
			filename = f'AMSR2_v110_{day}.npz'
			print(filename)
			icemap = self.longgap(start,end,loopday.year,xxx)
			CryoIO.savenumpy(f'{filepath}{filename}',icemap)
		
		
action = AMSR2_Downloader()

# action.error_retry()
action.create_missing_data()


'''

'''