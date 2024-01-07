import numpy as np
import pandas
import CryoIO
import os

def looop():
    '''iterates through a 366 day year'''
    obs_filepath = os.path.abspath('../NSIDC')
    yearlist = [year for year in range(2007,2022)]
    
    # options Max,Min,Mean,Stdv, SIPN, Forecast_Mean
    mode = 'SIPN'
    forecast_month = '07' # 06,07,08,09
    if mode == 'SIPN':
        yearlist = [2007,2008,2010,2010,2012,2012,2015,2016,2016,2021,2022,2022,2022]


    Columns = ['hole']
    csvdata = pandas.read_csv(f'{obs_filepath}/Tools/2008_polehole.csv', names=Columns,dtype=int)
    icepole = csvdata.hole.tolist()
             
    Columns = ['edge']
    csvdata = pandas.read_csv(f'{obs_filepath}/Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
    icepoleedge = csvdata.edge.tolist()
    
    if mode == 'SIPN':
        Cdate = CryoIO.CryoDate(2000,6,1)
        daycount = 125
        if forecast_month == '08':
            Cdate = CryoIO.CryoDate(2000,8,1)
            daycount = 62
        elif forecast_month == '09':
            Cdate = CryoIO.CryoDate(2000,9,1)
            daycount = 31
    
    for count in range (0,daycount,1): #366
        
        data = []
        if mode == 'SIPN':
            filename_out = 'DataFiles/Forecast_{}/Forecast_Manual/NSIDC_{}_{}{}.npz'.format(forecast_month,'Mean',Cdate.strMonth,Cdate.strDay)
            filename_out2 = 'DataFiles/Forecast_{}/Forecast_Stdv/NSIDC_{}_{}{}.npz'.format(forecast_month,'Stdv',Cdate.strMonth,Cdate.strDay)
        elif mode == 'Forecast_Mean': 
            filename_out = 'DataFiles/Forecast_Mean/NSIDC_{}_{}{}.npz'.format('Mean',Cdate.strMonth,Cdate.strDay)
            filename_out2 = 'DataFiles/Forecast_Stdv/NSIDC_{}_{}{}.npz'.format('Stdv',Cdate.strMonth,Cdate.strDay)
        elif mode == 'Mean':
            filename_out = 'DataFiles/Mean_00_19/NSIDC_{}_{}{}.npz'.format(mode,Cdate.strMonth,Cdate.strDay)
        

        for year in yearlist:
            filename = f'{obs_filepath}/DataFiles/{year}/NSIDC_{year}{Cdate.strMonth}{Cdate.strDay}.npz'
            icef = CryoIO.readnumpy(filename)
            data.append(icef)

        if mode =='Mean':
            ice_new = calcMean(data)
        elif mode =='Stdv':
            ice_new = calcStdv(data)
        elif mode =='SIPN' or mode == 'Forecast_Mean':
            ice_new = calcMean(data)
            ice_new2 = calcStdv(data)
            
            ice_new2 = polehole(ice_new2,icepole,icepoleedge)
            export2 = export_data('Stdv',ice_new2)
            CryoIO.savenumpy(filename_out2,export2)
        
        ice_new = polehole(ice_new,icepole,icepoleedge)
        export = export_data(mode,ice_new)    
        CryoIO.savenumpy(filename_out,export)
        
            
        print(mode,Cdate.strMonth,Cdate.strDay)
        
        Cdate.datecalc()
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
    
def polehole(ice,icepole,icepoleedge):
    '''calculates the pole hole'''
    
    icepolecon = []
    for val in icepoleedge:
        icepolecon.append (ice[val])
        
    icepolecon = np.mean(icepolecon)
    
    for val2 in icepole:
        ice[val2] = icepolecon
    
    return ice
        
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
