import numpy as np
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import CryoIO

class NSIDC_Filler:

    def __init__  (self,mode,forecast_month):
        self.start = date(2015, 11, 30)
        self.daycount = 94 #366 year, 186summer
#        self.dailyorcumu()

        if mode == 'SIPN':
            self.filepath = f'DataFiles_s/Forecast_{forecast_month}/Forecast_Manual/'
            self.filepath_export = f'DataFiles_s/Forecast_{forecast_month}/Forecast_SIC_change/'
            
            if forecast_month == '08':
                self.start = date(2016, 8, 1)
                self.daycount = 61
            elif forecast_month == '09':
                self.start = date(2016, 9, 1)
                self.daycount = 30
        else:
            self.filepath = 'DataFiles_s/Mean_80_21/' #Mean_80_21, Forecast_Mean
            self.filepath_export = 'DataFiles_s/Mean_SIC_change/' # Mean_SIC_change, Forecast_SIC_change
        
        self.loopday    = self.start
        self.year = self.start.year
        self.month = self.start.month
        self.day = self.start.day
        self.stringmonth = str(self.month).zfill(2)
        self.stringday = str(self.day).zfill(2)
        
    def dayloop(self):
        
        for count in range (0,self.daycount,1): 
            
            filenameMean = 'NSIDC_Mean_{}{}.npz'.format(self.stringmonth,self.stringday)
            filenamePlus1 = 'NSIDC_Mean_{}.npz'.format(self.calcday(1))
            filenameChange = 'NSIDC_SIC_Change_{}{}.npz'.format(self.stringmonth,self.stringday)
            
            ice = CryoIO.readnumpy(f'{self.filepath}{filenameMean}')
            iceP1 = CryoIO.readnumpy(f'{self.filepath}{filenamePlus1}')
                

            icechange = np.subtract(iceP1 , ice)
            icechange_export = np.array(icechange, dtype=np.int8) 
#           self.dailyloop(icechange)
            CryoIO.savenumpy(f'{self.filepath_export}{filenameChange}',icechange_export)
            
                
            print('{}-{}'.format(self.stringmonth,self.stringday))
            self.advanceday(1)
#        plt.show()
            
    def dailyloop(self,icemap):        
        icemap = icemap.reshape(448, 304)
        
        cmap = plt.cm.jet
        cmap.set_bad('black',0.6)
        
        self.ax.clear()
        self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2),x=0.15)
        self.ax.set_xlabel('NSIDC Area: Ice concentration')
        self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=-25, vmax=25, cmap=cmap)
#        self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=250, cmap=cmap)
        #self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        plt.tight_layout(pad=2)
        plt.pause(0.4)
        
    def dailyorcumu(self):        
        self.icenull = np.zeros(136192, dtype=float)
        self.icenull = self.icenull.reshape(448, 304)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 10))
        self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=-25, vmax=25,cmap = plt.cm.jet)
#            self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
        self.cbar = self.fig.colorbar(self.cax, ticks=[-25,0,25]).set_label('Ice concentration in %')
        self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold',x=0.175)
            
    def advanceday(self,delta):    
        self.loopday = self.loopday+timedelta(days=delta)
        self.year = self.loopday.year
        self.month = self.loopday.month
        self.day = self.loopday.day
        self.stringmonth = str(self.month).zfill(2)
        self.stringday = str(self.day).zfill(2)
        
    def calcday(self,delta):    
        loopday = self.loopday+timedelta(days=delta)
        month = loopday.month
        day = loopday.day
        stringmonth = str(month).zfill(2)
        stringday = str(day).zfill(2)
        return '{}{}'.format(stringmonth,stringday)

        

if __name__ == "__main__":
    print('main')
    mode = 'Mean' # SIPN , Forecast_Mean
    forecast_month = '12'
    action = NSIDC_Filler(mode,forecast_month)
    action.dayloop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA