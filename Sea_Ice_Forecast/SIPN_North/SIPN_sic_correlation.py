'''
This correlation script compares the SIC of one year to other ones. (including later ones)
This is different from the re-forecast correlation script

@author: Nico Sun

'''
from multiprocessing import Pool
from functools import partial
import numpy as np
import CryoIO
import os

class NSIDC_analysis:

    def __init__  (self):

        self.sic_error = ['SIC error']
        self.extent_error = ['extent error']
        self.CSVDatum = ['Date']
        
        self.filepath = os.path.abspath('../../NSIDC')
        self.filepath_SIPN = os.path.abspath('..')
        
        self.masksload()
        
        
    def masksload(self):
    
        filename = f'{self.filepath}/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = f'{self.filepath}/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000

        filename= f'{self.filepath}/Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = f'{self.filepath}/Masks/psn25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000
        

    def calc_extent_error(self,icepredict,iceobserve,regionmask):
        extent_over = 0
        extent_under = 0
        sicerror = 0
        error_map = iceobserve
        
        #only considers high arctic
        if 5 < regionmask < 16:
            error_map = iceobserve-icepredict
            sicerror = abs(error_map)*100
            if iceobserve > 0.15 and icepredict < 0.15:
                extent_under = 1
            elif iceobserve < 0.15 and icepredict > 0.15:
                extent_over = 1

        return error_map,extent_over,extent_under,sicerror
    

    
    def compute_error(self):
        '''loads data for computation of SIC error and extent error of a single day'''
        
        if self.Cdate.year == 'mean_80':
            filename_pre = f'{self.filepath_SIPN }/DataFiles/Mean_80_99/NSIDC_Mean_{self.Cdate.strMonth}{self.Cdate.strDay}.npz'
        elif self.Cdate.year == 'mean_90':
            filename_pre = f'{self.filepath_SIPN }/DataFiles/Mean_90_99/NSIDC_Mean_{self.Cdate.strMonth}{self.Cdate.strDay}.npz'
        elif self.Cdate.year == 'Forecast_Mean':
            filename_pre = f'{self.filepath_SIPN }/DataFiles/Forecast_Mean/NSIDC_Mean_{self.Cdate.strMonth}{self.Cdate.strDay}.npz'
        else:
            filename_pre = f'{self.filepath }/DataFiles/{self.Cdate.year}/NSIDC_{self.Cdate.datestring}.npz'
        
        
        filename_obs = f'{self.filepath }/DataFiles/{self.yearref}/NSIDC_{self.datestringref}.npz'
        
        icerefyear = CryoIO.readnumpy(filename_obs)/250
        icepreyear = CryoIO.readnumpy(filename_pre)/250
        
#--------------------------

        #extent error        
        aaa = np.vectorize(self.calc_extent_error)
        error_map,extent_over,extent_under,sicerror = aaa(icepreyear,icerefyear,self.regmaskf)
        
        extent_over = np.sum(extent_over)
        extent_under = np.sum(extent_under)
        extent_total = extent_over + extent_under
        sicerrorr = np.sum(sicerror)
        self.extent_list_over.append(extent_over)
        self.extent_list_under.append(extent_under)
        self.extent_list_total.append(extent_total)
        self.sicerrorr.append(sicerrorr)
        self.CSVDatum.append(self.Cdate.datestring)
        

    def dateloop(self,refyear,year,month,day):
        if year == 'Forecast_Manual' or year == 'mean_80' or year == 'mean_90':
            self.Cdate = CryoIO.CryoDate(2015, month, day)
        else:
            self.Cdate = CryoIO.CryoDate(year, month, day)
        
        self.yearref = refyear
        self.datestringref = '{}{}{}'.format(refyear,self.Cdate.strMonth,self.Cdate.strDay)
        
        self.extent_list_over = [year]
        self.extent_list_under = [year]
        self.extent_list_total = [year]
        self.sicerrorr = [year]
        self.overview = [year]
        
        
        
        countmax = 30+10 #123 June - September
        for count in range (0,countmax,1):
            #calc with multiprocess
            self.compute_error()

            self.Cdate.datecalc()
            self.datestringref = '{}{}{}'.format(self.yearref,self.Cdate.strMonth,self.Cdate.strDay)
            print(self.Cdate.datestring)
            
#         fill = '---'
        #June 1-31
        #July 31-62
        #August 62-93
        #September (whole month) ; 93-123
        
        juneEnd = 12
        juneStart = juneEnd - 5
            
        julyEnd = 30+11
        julyStart = julyEnd - 5
        
        augustEnd = 30+31+11
        augustStart = augustEnd -5
        
        septemberEnd = 30+31+31+7
        septemberStart = septemberEnd -5
#         print(self.sicerrorr)
        
        #June
        self.overview.append(int(sum(self.sicerrorr[juneStart:juneEnd])/100))
        self.overview.append(sum(self.extent_list_over[juneStart:juneEnd])+sum(self.extent_list_under[juneStart:juneEnd]))
        #July
        self.overview.append(int(sum(self.sicerrorr[julyStart:julyEnd])/100))
        self.overview.append(sum(self.extent_list_over[julyStart:julyEnd])+sum(self.extent_list_under[julyStart:julyEnd]))
        #August
        self.overview.append(int(sum(self.sicerrorr[augustStart:augustEnd])/100))
        self.overview.append(sum(self.extent_list_over[augustStart:augustEnd])+sum(self.extent_list_under[augustStart:augustEnd]))
        #September
        self.overview.append(int(sum(self.sicerrorr[septemberStart:septemberEnd])/100))
        self.overview.append(sum(self.extent_list_over[septemberStart:septemberEnd])+sum(self.extent_list_under[septemberStart:septemberEnd]))

        return self.overview
            

# yearcalc = 2005

def spawnprocess(datalist,yearcalc):
    action = NSIDC_analysis()
    overview = action.dateloop(yearcalc,datalist,6,1)
    return overview

def yearloop(yearStart,yearEnd):
    for i in range(yearStart,yearEnd):
        datalist = [] # 'Forecast_Manual','Forecast_Mean', 'mean_80','mean_90'
        for year in range(2007,2023):
            if year == i:
                print(year)
            else:
                datalist.append(year)
        
        spawnyear = partial(spawnprocess, yearcalc=i)
        p = Pool(processes=24)
        data = p.map(spawnyear, datalist)
        print(len(data))
        p.close()
        overview = [['year','SIC_June','SIE_June','SIC_July','SIE_July','SIC_August','SIE_August','SIC_September','SIE_September']]
        for x in data:
            overview.append(x)

        CryoIO.csv_rowexport(f'correlation_data/{i}_overview.csv',overview)
#         CryoIO.csv_columnexport(f'temp/{i}_overview.csv',overview)
        
    
if __name__ == '__main__':
    # for compute error
    yearloop(2023,2024)
    


'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''