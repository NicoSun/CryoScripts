import requests
import gzip
from io import BytesIO
import datetime
from datetime import timedelta
import numpy as np
import CryoIO

class Downloader:

    def __init__  (self):
        self.today = datetime.date.today()
        self.yesterday = self.today-timedelta(days=1)
        self.day_of_year = self.yesterday.timetuple().tm_yday
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
        self.dof = str(self.day_of_year).zfill(3)
        
        self.session = requests.Session()
        
    def open_gzip_data_in_bytesio(self,data_bytesio):
        try:
            with gzip.GzipFile(fileobj=data_bytesio, mode='rb') as gzip_file:
                decompressed_data = gzip_file.read()
            return decompressed_data
        except Exception as e:
            print(f"Error opening or decompressing gzip data: {e}")
            return None
        
    def numpy_conversion(self,asc_file):
        snow = np.genfromtxt(asc_file,skip_header =30,delimiter=1)
        snowmap = np.flip(snow,axis=1)
        snowmap = snowmap[220:830,250:700]
        snowmap = np.rot90(snowmap,k=2)
        snowbinary = np.array(snowmap).reshape(-1)
        return snowbinary

        
    def daily_download(self):
        folder =f"https://noaadata.apps.nsidc.org/NOAA/G02156/24km/{self.year}/"
        filename = f"ims{self.year}{self.dof}_00UTC_24km_v1.3.asc.gz" # final data
        '''downloads latest date'''

        filenameformatted = f'NOAA_{self.year}{self.dof}_24km_v1.1.npz'
        print(folder,filename)
        url_24km = folder + filename
        # print(url_24km)
        resp = self.session.get(url_24km, stream=True)

        gz_file = BytesIO(resp.content)

        self.process_data(gz_file,filenameformatted)
        # self.process_data_legacy(filenameformatted)
        print('Done')

    def process_data(self,gz_file,filenameformatted):
        '''extracts file, calculates extent & creates map/graphs'''

        data_unzipped = self.open_gzip_data_in_bytesio(gz_file)
        text_file = BytesIO(data_unzipped)
        
        snowbinary = self.numpy_conversion(text_file)
        filename = filenameformatted[0:17]
        file_convert = f'/home/nico/Cryoscripts/SnowCover/DataFiles/npz/{filename}.npz'
        CryoIO.savenumpy(file_convert,snowbinary)

    def process_data_legacy(self,filenameformatted):
        '''extracts file, calculates extent & creates map/graphs'''
        import os
        filename = filenameformatted[0:17]
        with gzip.open(os.path.join('/home/nico/Cryoscripts/SnowCover/DataFiles',filenameformatted), mode='rb') as fr:
            file_content = fr.read()
                    
        text_file = BytesIO(file_content)
        snowbinary = self.numpy_conversion(text_file)
        file_convert = f'/home/nico/Cryoscripts/SnowCover/DataFiles/{filename}.npz'
        CryoIO.savenumpy(file_convert,snowbinary)
        self.daily_compute()
        
    def daily_compute(self):
        import Daily_NOAA_Snow_npz
        import Daily_NOAA_Graphs
        print(self.day,self.month,self.year,self.day_of_year)
        
        Daily_NOAA_Snow_npz.action.automated(self.year,self.month,self.day,self.day_of_year)
        Daily_NOAA_Graphs.action.automated(self.year,self.month,self.day,self.day_of_year)
        # Snow_Daily_AWP_Graphs.action.automated(self.year,self.month,self.day,self.dof)


action = Downloader()

#action.mass_download()
action.daily_download()
action.daily_compute()

'''

National Ice Center. 2008, updated daily. IMS Daily Northern Hemisphere Snow and Ice Analysis at 1 km, 4 km, and 24 km Resolutions, Version 1.1-1.3. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi: https://doi.org/10.7265/N52R3PMC.
'''