import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import CryoIO



class Simpleviewer:


    def __init__  (self):
        self.Cdate = CryoIO.CryoDate(2022,12,1) # initilizes a 366 day year
        self.daycount = 6 #366 year,39 years
        
        # options Mean, Stdv, Change
        self.mode = 'Change'
        self.plotType() 
        
    def masksload(self):
    
        filename = f'{self.filepath}/Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)

        filename = f'{self.filepath}/Masks/psn25area_v3.dat'
        self.areamaskf = CryoIO.openfile(filename,np.uint32)/1000

        filename= f'{self.filepath}/Masks/psn25lats_v3.dat'
        self.latmaskf = CryoIO.openfile(filename,np.uint32)/100000
        
        filename = f'{self.filepath}/Masks/psn25lons_v3.dat'
        self.lonmaskf = CryoIO.openfile(filename,np.uint32)/100000

        '''
        self.icemask = 'Masks/SEAICEMASKS/NIC_valid_ice_mask.N25km.01.1972-2007.nc'
        print(len(self.icemask))
        with open(self.icemask, 'rb') as flmsk:
            self.mask4 = np.fromfile(flmsk, dtype=np.int32)
        
        self.icemaskf = np.array(self.mask4, dtype=float)
        #self.icemaskf = self.icemaskf /100000
        '''
        # self.maskview(self.regionmask)
        # plt.show()
        
    
    def viewloop(self):
    
        for count in range (0,self.daycount,1): 
            year = self.Cdate.year
            month = self.Cdate.strMonth
            day = self.Cdate.strDay
            if self.mode == 'Mean':
                filename = f'DataFiles_s/Forecast_Mean/NSIDC_Mean_{month}{day}.npz'
            elif self.mode == 'Stdv':
                filename = f'DataFiles_s/Forecast_SIC_change/NSIDC_SIC_Change_{month}{day}.npz'
            elif self.mode == 'Change':
                filename = f'DataFiles_s/Forecast_Stdv/NSIDC_Stdv_{month}{day}.npz'

            ice = CryoIO.readnumpy(filename)/250
            if self.mode =='Change':
                self.changeShow(ice)
            else:
                self.concentrationShow(ice)
            self.Cdate.datecalc()
            
        plt.show()
        
        
    def concentrationShow(self,icemap):
        icemap = ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(332, 316)
#        icemap = icemap[60:410,30:260]
        
        cmap = plt.cm.jet
        cmap.set_bad('black',0.8)
        
        self.ax.clear()
        self.ax.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
        self.ax.set_xlabel('NSIDC Area: Ice concentration'+self.mode)
#        self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=-25, vmax=25, cmap=cmap)
        self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
        self.ax.axes.get_yaxis().set_ticks([])
        self.ax.axes.get_xaxis().set_ticks([])
        plt.tight_layout(pad=1)
        self.fig.savefig(f'temp/{self.mode}_{self.Cdate.strMonth}{self.Cdate.strDay}.png')
        plt.pause(0.3)
        
    def changeShow(self,icemap):
        icemap = ma.masked_greater(icemap, 1)
        icemap = icemap.reshape(332, 316)
#        icemap = icemap[60:410,30:260]
        
        cmap = plt.colormaps["coolwarm_r"]
        
        self.ax3.clear()
        self.ax3.set_title('Date: {}-{}-{}'.format(self.Cdate.year,self.Cdate.strMonth,self.Cdate.strDay))
        self.ax3.set_xlabel('NSIDC Area: Ice concentration'+self.mode)
        self.cax3 = self.ax3.imshow(icemap, interpolation='nearest', vmin=-0.5, vmax=0.5, cmap=cmap)
        self.ax3.axes.get_yaxis().set_ticks([])
        self.ax3.axes.get_xaxis().set_ticks([])
        plt.tight_layout(pad=1)
        self.fig3.savefig(f'temp/{self.mode}_{self.Cdate.strMonth}{self.Cdate.strDay}.png')
        plt.pause(0.3)
        
    def maskview(self,icemap):        
        icemap = icemap.reshape(332, 316)
        self.fig, self.ax = plt.subplots(figsize=(8, 10))
        self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
        self.ax.clear()
        #self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
        #self.ax.set_xlabel(': '+str(icesum)+' Wh/m2')
        self.cax = self.ax.imshow(icemap, interpolation='nearest')
        #self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
        plt.pause(0.1)
        
        
    def plotType(self):        
        self.icenull = np.zeros(332*316, dtype=float)
        self.icenull = self.icenull.reshape(332, 316)
        
        if self.mode !='Change':
            self.fig, self.ax = plt.subplots(figsize=(8, 8))
            self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
            self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
            
            
        if self.mode =='Change':
            self.fig3, self.ax3 = plt.subplots(figsize=(8, 8))
            self.cax3 = self.ax3.imshow(self.icenull, interpolation='nearest', vmin=-0.5, vmax=0.5,cmap = plt.cm.coolwarm_r)
            self.cbar = self.fig3.colorbar(self.cax3, ticks=[-1,-.5,0,.5,1]).set_label('Sea Ice concentration in %')
            
        
        
forecast_month = '06'
action = Simpleviewer()
action.viewloop()
#action.masksload()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
