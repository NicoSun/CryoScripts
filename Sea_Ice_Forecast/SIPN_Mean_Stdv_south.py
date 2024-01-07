import numpy as np
import CryoIO

def looop():
        '''iterates through a 366 day year'''
        obs_filepath = '/media/prussian/Cryosphere/NSIDC_South'
#         obs_filepath = '/media/nico/REVIVA/HomeServer/Cryoscripts/NSIDC'
        yearlist = [year for year in range(1980,2022)]
        
        # options Max,Min,Mean,Stdv, SIPN, Forecast_Mean
        mode = 'Mean'
        forecast_month = '12' # 06,07,08,09,12
        if mode == 'SIPN' or mode == 'SIPN_S':
            yearlist = [1981,1983,1983,1983,1983,1984,1984,1985,1987,1987,1987,1989,1989,1989,1992,1995,1996,1996,1999,1999,2001,2001,2008,2014,2016,2016,2016,2018,2018,2019,2019,2020,2020,2020,2021,2021]

        month = 1
        daycount = 366
        day = 1
        
        if mode == 'SIPN':
            if forecast_month == '08':
                    month = 8
                    daycount = 62
            elif forecast_month == '09':
                    month = 9
                    daycount = 31
        
        for count in range (0,daycount,1): #366
            stringmonth = str(month).zfill(2)
            stringday = str(day).zfill(2)
            
            data = []
            if mode == 'SIPN':
                    filename_out = 'DataFiles_s/Forecast_{}/Forecast_Manual/NSIDC_{}_{}{}.npz'.format(forecast_month,'Mean',stringmonth,stringday)
                    filename_out2 = 'DataFiles_s/Forecast_{}/Forecast_Stdv/NSIDC_{}_{}{}.npz'.format(forecast_month,'Stdv',stringmonth,stringday)
            elif mode == 'Forecast_Mean' or mode == 'SIPN_S': 
                    filename_out = 'DataFiles_s/Forecast_Mean/NSIDC_{}_{}{}.npz'.format('Mean',stringmonth,stringday)
                    filename_out2 = 'DataFiles_s/Forecast_Stdv/NSIDC_{}_{}{}.npz'.format('Stdv',stringmonth,stringday)
            elif mode == 'Mean':
                    filename_out = 'DataFiles_s/Mean_80_21/NSIDC_{}_{}{}.npz'.format(mode,stringmonth,stringday)
            

            for year in yearlist:
                filename = f'{obs_filepath}/DataFiles/{year}/NSIDC_{year}{stringmonth}{stringday}_south.bin'
                icef = CryoIO.openfile(filename, np.uint8)
                data.append(icef)

            if mode =='Mean':
                ice_new = calcMean(data)
            elif mode =='Stdv':
                ice_new = calcStdv(data)
            elif mode =='SIPN' or mode == 'Forecast_Mean' or mode == 'SIPN_S':
                ice_new = calcMean(data)
                ice_new2 = calcStdv(data)
                
                export2 = export_data('Stdv',ice_new2)
                CryoIO.savenumpy(filename_out2,export2)
            
            export = export_data(mode,ice_new)        
            CryoIO.savenumpy(filename_out,export)
            
                    
            print(mode,month,day)
            
            day = day+1
            if day==32 and (month==1 or month==3 or month==5 or month==7 or month==8 or month==10):
                    day=1
                    month = month+1
            elif day==31 and (month==4 or month==6 or month==9 or month==11):
                    day=1
                    month = month+1
            elif day==30 and month==2:
                    day=1
                    month = month+1
            elif  day==32 and month == 12:
                day = 1
                month = 1
                year = year+1
        print('Done')
        return mode, forecast_month
        

def calcMean(data):
    '''calculates the minimum grid cell concentration'''
    result = np.asarray(data).mean(0)
    return result

def calcStdv(data):
    '''calculates the minimum grid cell concentration'''
    result = np.asarray(data).std(0)
    return result
                
def export_data(mode,ice_new):
    '''sets array data type'''
    if mode =='Stdv':
            export = np.array(ice_new, dtype=np.float16)
    else:
            export = np.array(ice_new, dtype=np.uint8)
            
    return export



mode, forecast_month = looop()

import SIPN_Daily_change
action = SIPN_Daily_change.NSIDC_Filler(mode,forecast_month)
action.dayloop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
