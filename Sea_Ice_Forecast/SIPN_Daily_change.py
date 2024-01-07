import numpy as np
import CryoIO

class NSIDC_Filler:

    def __init__  (self,mode,forecast_month):
        self.Cdate = CryoIO.CryoDate(2016, 6, 1)
        self.daycount = 124 #366 year, 186summer
#        self.dailyorcumu()

        if mode == 'SIPN':
            self.filepath = f'DataFiles/Forecast_{forecast_month}/Forecast_Manual/'
            self.filepath_export = f'DataFiles/Forecast_{forecast_month}/Forecast_SIC_change/'
            
            if forecast_month == '08':
                self.Cdate = CryoIO.CryoDate(2016, 8, 1)
                self.daycount = 61
            elif forecast_month == '09':
                self.Cdate = CryoIO.CryoDate(2016, 9, 1)
                self.daycount = 30
        else:
            self.filepath = 'DataFiles/Forecast_Mean/' #Mean_90_99, Forecast_Mean
            self.filepath_export = 'DataFiles/Forecast_SIC_change/'
        
    def dayloop(self):
        plusDay = CryoIO.CryoDate(self.Cdate.year,self.Cdate.month,self.Cdate.day)
        plusDay.datecalc()
        
        for count in range (0,self.daycount,1): 
            
            filenameMean = 'NSIDC_Mean_{}{}.npz'.format(self.Cdate.strMonth, self.Cdate.strDay)
            filenamePlus1 = 'NSIDC_Mean_{}{}.npz'.format(plusDay.strMonth, plusDay.strDay)
            filenameChange = 'NSIDC_SIC_Change_{}{}.npz'.format(self.Cdate.strMonth,self.Cdate.strDay)

            ice = CryoIO.readnumpy(f'{self.filepath}{filenameMean}')
            iceP1 = CryoIO.readnumpy(f'{self.filepath}{filenamePlus1}')
           
            icechange = np.subtract(iceP1 , ice)
            icechange_export = np.array(icechange, dtype=np.int8) 
            CryoIO.savenumpy(f'{self.filepath_export}{filenameChange}',icechange_export)
            
                
            print('{}-{}'.format(self.Cdate.strMonth,self.Cdate.strDay))
            self.Cdate.datecalc()
            plusDay.datecalc()
            

if __name__ == "__main__":
    print('main')
    mode = 'SIPN' # SIPN , Forecast_Mean
    forecast_month = '06'
    action = NSIDC_Filler(mode,forecast_month)
    action.dayloop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA