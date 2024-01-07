'''
This initilization script should be run after the correlation script. It automatically selects the best years for a good mean SIC

@author: Nico Sun

'''

import numpy as np
import pandas
import CryoIO


def loadfile(filename):
    # Yearcolnames = ['year','SIC_Dec','SIE_Dec']
    Yearcolnames = ['year','SIC_June','SIE_June','SIC_July','SIE_July','SIC_August','SIE_August','SIC_September','SIE_September']
    Yeardata = pandas.read_csv(filename, names=Yearcolnames)
    return Yeardata
    

def calcMean(data):
    '''calculates the minimum grid cell concentration'''
    result = np.asarray(data).mean(0)
    return result

def calcStdv(data):
    '''calculates the minimum grid cell concentration'''
    result = np.asarray(data).std(0)
    return result

def yearweighting(yearlist, stdv, year):
    '''adds good years multiple times'''
    yyy = 0
    while yyy < stdv:
        yearlist.append(year)
        yyy += 1
    return yearlist

def single_month(year,month):
    filename = f'correlation_data/{mode}_{year}_overview.csv'
    df = loadfile(filename)
#     print(df['SIE_June'])
    if month =='06':
        sic = np.array(df['SIC_June'])
        sie = np.array(df['SIE_June'])
        month2 = '06'
    elif month =='07':
        sic = np.array(df['SIC_July'])
        sie = np.array(df['SIE_July'])
        month2 = '07'
    elif month =='08':
        sic = np.array(df['SIC_August'])
        sie = np.array(df['SIE_August'])
        month2 = '08'
    elif month =='09':
        sic = np.array(df['SIC_September'])
        sie = np.array(df['SIE_September'])
        month2 = '09'
    elif month =='12':
        sic = np.array(df['SIC_December'])
        sie = np.array(df['SIE_December'])
        month2 = '12'
        
    sic2 = sic[1:]
    sie2 = sie[1:]
    # convert to lambda function
    for x in range (0,len(sic2)):
        sic2[x] = int(sic2[x])
        sie2[x] = int(sie2[x])


    sic_mean = calcMean(sic2)
    sic_stdv = calcStdv(sic2)
    sie_mean = calcMean(sie2)
    sie_stdv = calcStdv(sie2)
    
    #calculates 
#     sic_mean = sic_mean
    stdv_sic = []
    stdv_sie = []
    factor = []
    for x in range(1,len(sic)):
        aaa = (sic[x]-sic_mean)/sic_stdv
        bbb = (sie[x]-sie_mean)/sie_stdv
        stdv_sic.append(aaa)
        stdv_sie.append(bbb)
        
        factor.append(round((aaa+bbb)/2/0.5))

# =============================================================================
#     print(stdv_sic)    
#     print(stdv_sie)    
# =============================================================================
    yearlist = []
    
    for x in range(0,len(factor)):
        if factor[x] < 0.2:
            year2 = df['year'][x+1]
            yearlist = yearweighting(yearlist,abs(factor[x]),year2)
                
            
    print(yearlist)
    CryoIO.csv_columnexport(f'mean_sic_yearlists/{year}_{month2}_yearlist.txt',yearlist)

mode = 'summer' #summer winter

if __name__ == '__main__':
    for year in range(2023,2024):
        for month in range(6,8):
            stringmonth = str(month).zfill(2)
            single_month(year,stringmonth)
