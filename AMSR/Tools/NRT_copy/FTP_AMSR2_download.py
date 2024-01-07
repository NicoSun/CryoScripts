from ftplib import FTP
from datetime import date
from datetime import timedelta
import io
import File_Manager

class AMSR2_Downloader:

    def __init__  (self):
        self.today = date.today()
        self.yesterday = self.today-timedelta(days=1)
        self.year = self.yesterday.year
        self.todaymonth = str(self.today.month).zfill(2)
        self.todayday = str(self.today.day).zfill(2)
        self.stringmonth = str(self.yesterday.month).zfill(2)
        self.stringday = str(self.yesterday.day).zfill(2)
        print(self.yesterday)
        

    def test_download(self):
        '''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
        ftp = FTP('ftp.awi.de')     # connect to host, default port
        ftp.login()                     # user anonymous, passwd anonymous@
        
        datestring = f'{self.year}-{self.stringmonth}-{self.stringday}'
        hemi = 'nh'
        # filename = f"{hemi}_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
        filename = f"{hemi}_SIC_LEAD_{self.year}{self.stringmonth}2412_092500.nc.gz"
        if(hemi == 'nh'):
            filenameformatted = f'DataFiles/AMSR2_nh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
        else:
            filenameformatted = f'DataFiles/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
        print(filename)
        ftp.cwd(f'/sea_ice/product/amsr2/v110/{hemi}/{self.year}/{self.stringmonth}')

        download = io.BytesIO()
        ftp.retrbinary('RETR '+filename, download.write)
        File_Manager.action.dailyupdate(download,filenameformatted,hemi,datestring)
            
        print('Done')
        ftp.quit()


    def mass_download(self):
        import logging
        logging.basicConfig(filename='logs/FTP_download.log', level=logging.INFO)
        '''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
        
        self.ftp = FTP('ftp.awi.de')     # connect to host, default port
        self.ftp.login()                     # user anonymous, passwd anonymous@
        self.start = date(2023, 10, 18) #first data date(2012, 7, 4)
        self.end = date(2023,10,19) # 10,17
        
        self.daycount = (self.end - self.start).days
        print(self.daycount)
        self.year = self.start.year
        self.stringmonth = str(self.start.month).zfill(2)
        self.stringday = str(self.start.day).zfill(2)
        
        self.tomorrow = self.start+timedelta(days=1)
        self.tomorrowmonth = str(self.tomorrow.month).zfill(2)
        self.tomorrowday = str(self.tomorrow.day).zfill(2)
        loopday    = self.start
        
        for count in range (0,self.daycount): #366
            datedict = {'year':self.year,'month':self.stringmonth,'day':self.stringday}
            filenameFormatted = f'/home/nico/Cryoscripts/AMSR/DataFiles/nh/{self.year}/AMSR2_nh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
            filenameFormatted_sh = f'/home/nico/Cryoscripts/AMSR/DataFiles/sh/{self.year}/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
            
            print(datedict.values())
            try:
                filename = f"nh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
                filename_sh = f"sh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
                nh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/nh/{self.year}/{self.stringmonth}',filename)
                sh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/sh/{self.year}/{self.stringmonth}',filename_sh)
                File_Manager.action.dailyupdate(nh_file,filenameFormatted,'nh',datedict)
                File_Manager.action.dailyupdate(sh_file,filenameFormatted_sh,'sh',datedict)
            except:
                #trys afternoon (pm) data
                filename = f"nh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}12_{self.tomorrowmonth}{self.tomorrowday}00.nc.gz" # final data
                filename_sh = f"sh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}12_{self.tomorrowmonth}{self.tomorrowday}00.nc.gz" # final data
                print(filename)
                print(filename_sh)
                nh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/nh/{self.year}/{self.stringmonth}',filename)
                sh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/sh/{self.year}/{self.stringmonth}',filename_sh)
                
                File_Manager.action.dailyupdate(nh_file,filenameFormatted,'nh',datedict)
                File_Manager.action.dailyupdate(sh_file,filenameFormatted_sh,'sh',datedict)
            
            loopday += timedelta(days=1)
            self.year = loopday.year
            self.stringmonth = str(loopday.month).zfill(2)
            self.stringday = str(loopday.day).zfill(2)
        self.ftp.quit()
        
    def ftp_retrieve(self,directory,filename):
        download = io.BytesIO()
        self.ftp.cwd(directory)
        self.ftp.retrbinary('RETR '+filename, download.write)
        return download
        
    def daily_download(self):
        '''downloads latest date'''
        
        self.ftp = FTP('ftp.awi.de')     # connect to host, default port
        self.ftp.login()                     # user anonymous, passwd anonymous@
        datedict = {'year':self.year,'month':self.stringmonth,'day':self.stringday}
        filenameFormatted = f'/home/nico/Cryoscripts/AMSR/DataFiles/nh/{self.year}/AMSR2_nh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
        filenameFormatted_sh = f'/home/nico/Cryoscripts/AMSR/DataFiles/sh/{self.year}/AMSR2_sh_v110_{self.year}{self.stringmonth}{self.stringday}.npz'
        
        print(f'AMSR2 {datedict.values()}')
        try:
            filename = f"nh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
            filename_sh = f"sh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}00_{self.stringmonth}{self.stringday}12.nc.gz" # final data
            nh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/nh/{self.year}/{self.stringmonth}',filename)
            sh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/sh/{self.year}/{self.stringmonth}',filename_sh)
        except:
            #trys afternoon (pm) data
            filename = f"nh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}12_{self.todaymonth}{self.todayday}00.nc.gz" # final data
            filename_sh = f"sh_SIC_LEAD_{self.year}{self.stringmonth}{self.stringday}12_{self.todaymonth}{self.todayday}00.nc.gz" # final data
            print(filename)
            print(filename_sh)
            nh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/nh/{self.year}/{self.stringmonth}',filename)
            sh_file = self.ftp_retrieve(f'/sea_ice/product/amsr2/v110/sh/{self.year}/{self.stringmonth}',filename_sh)
            
        File_Manager.action.dailyupdate(nh_file,filenameFormatted,'nh',datedict)
        File_Manager.action.dailyupdate(sh_file,filenameFormatted_sh,'sh',datedict)
        
        self.ftp.quit()
        

action = AMSR2_Downloader()

# action.test_download()
# action.mass_download()
action.daily_download()
#action.manualdownload(2020,200)

'''

'''