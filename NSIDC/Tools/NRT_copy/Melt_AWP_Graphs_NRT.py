import numpy as np
import pandas
import matplotlib.pyplot as plt



class AWP_graphs:

    def __init__  (self):
        self.labelfont = {'fontname':'Arial'}
        self.year = 2020
        self.stringmonth = '20'
        self.stringday = '20'
        self.webpath = '/var/www/Cryoweb'
        
        self.xAxis = [-20,10,40,71,101,132,163] # month divder lines
        self.xlabel = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
        
        import copy
        self.cmap = copy.copy(plt.colormaps["coolwarm"])
        self.cmap.set_bad('black',0.75)
        
    def minus(self,a,b):
        '''calculates the FDD anomaly'''
        a = float(a)
        b = float(b)
        c = a-b
        return c
    
    def IceMelt_NRT(self,icemap,icesum,date):
        '''displays melt AWP data'''
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        
        icemap = np.ma.masked_equal(icemap, -1)

        icesum = int(icesum)
        
        fig2, ax2 = plt.subplots(figsize=(7.2, 9))
        ax2.clear()
        ax2.set_title('Ice Melt AWP',loc='left')
        ax2.set_title('Date: '+str(date),loc='right')
        
        maxvalue = np.amax(icemap)*0.9

#        "{:,}".format(value)
        ax2.set_xlabel('Arctic Sum: {:,} [EJ]'.format(icesum),**self.labelfont)
        cax = ax2.imshow(icemap, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=self.cmap)
        fig2.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,0.5*maxvalue,maxvalue]).set_label('ice melt AWP in EJ',**self.labelfont)
        
        ax2.axes.get_yaxis().set_ticks([])
        ax2.axes.get_xaxis().set_ticks([])
        ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax2.set_ylabel('cryospherecomputing.com/melt-awp',y=0.15)
        fig2.tight_layout(pad=1)
        fig2.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Map1.png')
#        plt.pause(0.1)
#        plt.show()
        plt.close()
    
    def IceMelt_NRT_accu(self,icemap,icesum,date):
        '''displays melt AWP data'''
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        
        icemap = np.ma.masked_equal(icemap, -1)

        icesum = int(icesum)
        
        fig2, ax2 = plt.subplots(figsize=(7.2, 9))
        ax2.clear()
        ax2.set_title('Ice Melt AWP',loc='left')
        ax2.set_title('Date: '+str(date),loc='right')
        
        maxvalue = min(5e5,np.amax(icemap)*0.75)

#        "{:,}".format(value)
        ax2.set_xlabel('Arctic Sum: {:,} [EJ]'.format(icesum),**self.labelfont)
        cax = ax2.imshow(icemap, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=self.cmap)
        fig2.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,0.5*maxvalue,maxvalue]).set_label('ice melt AWP in EJ',**self.labelfont)
        
        ax2.axes.get_yaxis().set_ticks([])
        ax2.axes.get_xaxis().set_ticks([])
        ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax2.set_ylabel('cryospherecomputing.com/melt-awp',y=0.15)
        fig2.tight_layout(pad=1)
        fig2.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Map2.png')
#        plt.pause(0.1)
#        plt.show()
        plt.close()
        
    def daily_anomaly(self):
                
        C2000s_anom = list(map(self.minus,self.C2000s_daily,self.AWP_Daily_mean))
        C2010s_anom = list(map(self.minus,self.C2010s_daily,self.AWP_Daily_mean))
        C2007_anom = list(map(self.minus,self.C2007_daily,self.AWP_Daily_mean))
        C2012_anom = list(map(self.minus,self.C2012_daily,self.AWP_Daily_mean))
        C2014_anom = list(map(self.minus,self.C2014_daily,self.AWP_Daily_mean))
        C2016_anom = list(map(self.minus,self.C2016_daily,self.AWP_Daily_mean))
        C2019_anom = list(map(self.minus,self.C2019_daily,self.AWP_Daily_mean))
        current_anom = list(map(self.minus,self.CSVDaily,self.AWP_Daily_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Daily Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-20,20,2.5)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( C2000s_anom, color=(0.75,0.75,0.75),label='2000s',lw=2,ls='--')
        plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
        plt.plot( C2007_anom, color='brown',label='2007',lw=1)
        plt.plot( C2012_anom, color='orange',label='2012',lw=1)
        plt.plot( C2014_anom, color='blue',label='2014',lw=1)
        plt.plot( C2016_anom, color='green',label='2016',lw=1)
        plt.plot( C2019_anom, color='red',label='2019',lw=1)
        plt.plot( current_anom, color='black',label=self.year,lw=2)
        
        ymin = -11
        ymax = 16
        plt.axis([0,186,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph1.png',bbox_extra_artists=(lgd,))
        plt.close()
#        plt.show()

    
    def accumulated_anomaly(self):
        
        C2000s_anom = list(map(self.minus,self.C2000s,self.AWP_Accu_mean))
        C2010s_anom = list(map(self.minus,self.C2010s,self.AWP_Accu_mean))
        C2007_anom = list(map(self.minus,self.C2007,self.AWP_Accu_mean))
        C2012_anom = list(map(self.minus,self.C2012,self.AWP_Accu_mean))
        C2014_anom = list(map(self.minus,self.C2014,self.AWP_Accu_mean))
        C2016_anom = list(map(self.minus,self.C2016,self.AWP_Accu_mean))
        C2019_anom = list(map(self.minus,self.C2019,self.AWP_Accu_mean))
        current_anom = list(map(self.minus,self.CSVCumu,self.AWP_Accu_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Accumulated Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-1000,1000,100)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( C2000s_anom, color=(0.75,0.75,0.75),label='2000s',lw=2,ls='--')
        plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
        plt.plot( C2007_anom, color='brown',label='2007',lw=1)
        plt.plot( C2012_anom, color='orange',label='2012',lw=1)
        plt.plot( C2014_anom, color='blue',label='2014',lw=1)
        plt.plot( C2016_anom, color='green',label='2016',lw=1)
        plt.plot( C2019_anom, color='red',label='2019',lw=1)
        plt.plot( current_anom, color='black',label=self.year,lw=2)
        
        ymin = -200
        ymax = 800
        plt.axis([0,186,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph2.png',bbox_extra_artists=(lgd,))
        plt.close()
#        plt.show()
        
    def centredailygraph(self):
        
        Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_centre_Daily.csv', names=Climatecolnames,header=0)
        
        C2000s = Climatedata.A.tolist()
        C2010s = Climatedata.B.tolist()
        C2007 = Climatedata.C.tolist()
        C2012 = Climatedata.D.tolist()
        C2014 = Climatedata.E.tolist()
        C2016 = Climatedata.F.tolist()
        C2019 = Climatedata.G.tolist()
        
        C2000s_anom = list(map(self.minus,C2000s,self.AWP_centre_Daily_mean))
        C2010s_anom = list(map(self.minus,C2010s,self.AWP_centre_Daily_mean))
        C2007_anom = list(map(self.minus,C2007,self.AWP_centre_Daily_mean))
        C2012_anom = list(map(self.minus,C2012,self.AWP_centre_Daily_mean))
        C2014_anom = list(map(self.minus,C2014,self.AWP_centre_Daily_mean))
        C2016_anom = list(map(self.minus,C2016,self.AWP_centre_Daily_mean))
        C2019_anom = list(map(self.minus,C2019,self.AWP_centre_Daily_mean))
        current_anom = list(map(self.minus,self.CSVDaily_central,self.AWP_centre_Daily_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Daily High Arctic Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-50,50,1)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( C2000s_anom, color=(0.75,0.75,0.75),label='2000s',lw=2,ls='--')
        plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
        plt.plot( C2007_anom, color='brown',label='2007',lw=1)
        plt.plot( C2012_anom, color='orange',label='2012',lw=1)
        plt.plot( C2014_anom, color='blue',label='2014',lw=1)
        plt.plot( C2016_anom, color='green',label='2016',lw=1)
        plt.plot( C2019_anom, color='red',label='2019',lw=1)
        plt.plot( current_anom, color='black',label=self.year,lw=2)
        
        ymin = -9
        ymax = 13
        plt.axis([0,186,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph3.png',bbox_extra_artists=(lgd,))
        plt.close()

    
    def centreaccumulatedgraph(self):
        
        Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_centre_Accumulated.csv', names=Climatecolnames,header=0)
        
        C2000s = Climatedata.A.tolist()
        C2010s = Climatedata.B.tolist()
        C2007 = Climatedata.C.tolist()
        C2012 = Climatedata.D.tolist()
        C2014 = Climatedata.E.tolist()
        C2016 = Climatedata.F.tolist()
        C2019 = Climatedata.G.tolist()
        
        C2000s_anom = list(map(self.minus,C2000s,self.AWP_centre_Accu_mean))
        C2010s_anom = list(map(self.minus,C2010s,self.AWP_centre_Accu_mean))
        C2007_anom = list(map(self.minus,C2007,self.AWP_centre_Accu_mean))
        C2012_anom = list(map(self.minus,C2012,self.AWP_centre_Accu_mean))
        C2014_anom = list(map(self.minus,C2014,self.AWP_centre_Accu_mean))
        C2016_anom = list(map(self.minus,C2016,self.AWP_centre_Accu_mean))
        C2019_anom = list(map(self.minus,C2019,self.AWP_centre_Accu_mean))
        current_anom = list(map(self.minus,self.CSVAccu_central,self.AWP_centre_Accu_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Accumulated High Arctic Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-1000,1000,50)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( C2000s_anom, color=(0.75,0.75,0.75),label='2000s',lw=2,ls='--')
        plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
        plt.plot( C2007_anom, color='brown',label='2007',lw=1)
        plt.plot( C2012_anom, color='orange',label='2012',lw=1)
        plt.plot( C2014_anom, color='blue',label='2014',lw=1)
        plt.plot( C2016_anom, color='green',label='2016',lw=1)
        plt.plot( C2019_anom, color='red',label='2019',lw=1)
        plt.plot( current_anom, color='black',label=self.year,lw=2)
        
        ymin = -300
        ymax = 750
        plt.axis([0,186,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph4.png',bbox_extra_artists=(lgd,))
        plt.close()

            
    def regiongraph(self):
        
        Climatecolnames = ['Date','B','C','D','E','F','G','H','I','J','K','L','M','N']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_mean_regional.csv', names=Climatecolnames,header=0)
        
        SoO_mean = Climatedata.B.tolist()
        Bers_mean = Climatedata.C.tolist()
        HB_mean = Climatedata.D.tolist()
        BB_mean = Climatedata.E.tolist()
        EG_mean = Climatedata.F.tolist()
        BaS_mean = Climatedata.G.tolist()
        KS_mean = Climatedata.H.tolist()
        LS_mean = Climatedata.I.tolist()
        ES_mean = Climatedata.J.tolist()
        CS_mean = Climatedata.K.tolist()
        BeaS_mean = Climatedata.L.tolist()
        CA_mean = Climatedata.M.tolist()
        AB_mean = Climatedata.N.tolist()
                
        Region1 = list(map(self.minus,self.SoO,SoO_mean))
        Region2 = list(map(self.minus,self.Bers,Bers_mean))
        Region3 = list(map(self.minus,self.HB,HB_mean))
        Region4 = list(map(self.minus,self.BB,BB_mean))
        Region5 = list(map(self.minus,self.EG,EG_mean))
        Region6 = list(map(self.minus,self.BaS,BaS_mean))
        Region7 = list(map(self.minus,self.KS,KS_mean))
        Region8 = list(map(self.minus,self.LS,LS_mean))
        Region9 = list(map(self.minus,self.ES,ES_mean))
        Region10 = list(map(self.minus,self.CS,CS_mean))
        Region11 = list(map(self.minus,self.BeaS,BeaS_mean))
        Region12 = list(map(self.minus,self.CA,CA_mean))
        Region13 = list(map(self.minus,self.AB,AB_mean))
        
        data = [Region1,Region2,Region3,Region4,Region5,Region6,Region7,Region8,Region9,Region10,Region11,Region12,Region13]

        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle(str(self.year)+' Accumulated Regional Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-500,500,25)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/awp', transform=ax.transAxes, color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        
        plt.plot( Region1, color=(0,0.4,0),label='Sea of Okhotsk',lw=2)
        plt.plot( Region2, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
        plt.plot( Region3, color=(0.2,0.8,0.2),label='Hudson Bay',lw=2)
        plt.plot( Region4, color=(0.68,0,0.33),label='Baffin Bay',lw=2)
        plt.plot( Region5, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
        plt.plot( Region6, color=(0.9,0.9,0),label='Barents Sea',lw=2)
        plt.plot( Region7, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
        plt.plot( Region8, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
        plt.plot( Region9, color=(0,0,0.6),label='East. Siberian',lw=2)
        plt.plot( Region10, color=(0.5,0.25,0),label='Chukchi',lw=2)
        plt.plot( Region11, color=(1,0.5,0),label='Beaufort Sea',lw=2)
        plt.plot( Region12, color=(1,0.26,1),label='Can. Archipelago',lw=2)
        plt.plot( Region13, color='black',label='Central Arctic',lw=2)
        
        ymin = 0
        ymax = 0
        
        for x in data:
            value = x[-1]
            if value > ymax:
                ymax = value
            if value < ymin:
                ymin = value
                
        ymax = max(ymax, 100)
        plt.axis([0,len(Region1),min(-40,ymin-15),ymax+15])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        #fig.subplots_adjust(bottom=0.1)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph_Region1.png')
        plt.close()

            
    def regiongraph_daily(self):
        
        Climatecolnames = ['Date','B','C','D','E','F','G','H','I','J','K','L','M','N']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_mean_regional_daily.csv', names=Climatecolnames,header=0)
        
        SoO_mean = Climatedata.B.tolist()
        Bers_mean = Climatedata.C.tolist()
        HB_mean = Climatedata.D.tolist()
        BB_mean = Climatedata.E.tolist()
        EG_mean = Climatedata.F.tolist()
        BaS_mean = Climatedata.G.tolist()
        KS_mean = Climatedata.H.tolist()
        LS_mean = Climatedata.I.tolist()
        ES_mean = Climatedata.J.tolist()
        CS_mean = Climatedata.K.tolist()
        BeaS_mean = Climatedata.L.tolist()
        CA_mean = Climatedata.M.tolist()
        AB_mean = Climatedata.N.tolist()
                
        Region1 = list(map(self.minus,self.SoO_daily,SoO_mean))
        Region2 = list(map(self.minus,self.Bers_daily,Bers_mean))
        Region3 = list(map(self.minus,self.HB_daily,HB_mean))
        Region4 = list(map(self.minus,self.BB_daily,BB_mean))
        Region5 = list(map(self.minus,self.EG_daily,EG_mean))
        Region6 = list(map(self.minus,self.BaS_daily,BaS_mean))
        Region7 = list(map(self.minus,self.KS_daily,KS_mean))
        Region8 = list(map(self.minus,self.LS_daily,LS_mean))
        Region9 = list(map(self.minus,self.ES_daily,ES_mean))
        Region10 = list(map(self.minus,self.CS_daily,CS_mean))
        Region11 = list(map(self.minus,self.BeaS_daily,BeaS_mean))
        Region12 = list(map(self.minus,self.CA_daily,CA_mean))
        Region13 = list(map(self.minus,self.AB_daily,AB_mean))
        
        data = [Region1,Region2,Region3,Region4,Region5,Region6,Region7,Region8,Region9,Region10,Region11,Region12,Region13]

        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle(str(self.year)+' Daily Regional Ice Melt Energy (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('AWP Ice Melt Energy in EJ (anomaly)',**self.labelfont)
        major_ticks = np.arange(-50,50,1)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}'.format(self.datestring),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.72, -0.06, 'cryospherecomputing.com/awp', transform=ax.transAxes, color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        
        plt.plot( Region1, color=(0,0.4,0),label='Sea of Okhotsk',lw=2)
        plt.plot( Region2, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
        plt.plot( Region3, color=(0.2,0.8,0.2),label='Hudson Bay',lw=2)
        plt.plot( Region4, color=(0.68,0,0.33),label='Baffin Bay',lw=2)
        plt.plot( Region5, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
        plt.plot( Region6, color=(0.9,0.9,0),label='Barents Sea',lw=2)
        plt.plot( Region7, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
        plt.plot( Region8, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
        plt.plot( Region9, color=(0,0,0.6),label='East. Siberian',lw=2)
        plt.plot( Region10, color=(0.5,0.25,0),label='Chukchi',lw=2)
        plt.plot( Region11, color=(1,0.5,0),label='Beaufort Sea',lw=2)
        plt.plot( Region12, color=(1,0.26,1),label='Can. Archipelago',lw=2)
        plt.plot( Region13, color='black',label='Central Arctic',lw=2)
        
        ymin = -4 #-4
        ymax = 7 #7
                    
        plt.axis([0,len(Region1),ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Melt_AWP/North_IceMelt_Graph_Region2.png')
        plt.close()

    
    def loadCSVdata (self):
        Yearcolnames = ['Date','B','C','D','E']
        Yeardata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT.csv', names=Yearcolnames,header=0)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVDaily = Yeardata.B.tolist()
        self.CSVCumu = Yeardata.C.tolist()
        self.CSVDaily_central = Yeardata.D.tolist()
        self.CSVAccu_central = Yeardata.E.tolist()
        
        AWP_mean = ['A','B','C','D']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_mean.csv', names=AWP_mean,header=0)
        self.AWP_Daily_mean = Climatedata.A.tolist()
        self.AWP_Accu_mean = Climatedata.B.tolist()
        self.AWP_centre_Daily_mean = Climatedata.C.tolist()
        self.AWP_centre_Accu_mean = Climatedata.D.tolist()
        
        
        AWP_daily = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_pan_Daily.csv', names=AWP_daily,header=0)
#        Date = Climatedata.A.tolist()
        self.C2000s_daily = Climatedata.B.tolist()
        self.C2010s_daily = Climatedata.C.tolist()
        self.C2007_daily = Climatedata.D.tolist()
        self.C2012_daily = Climatedata.E.tolist()
        self.C2014_daily = Climatedata.F.tolist()
        self.C2016_daily = Climatedata.G.tolist()
        self.C2019_daily = Climatedata.H.tolist()
        
        AWP_accu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        Climatedata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Climatology/Arctic_AWP_pan_Accumulated.csv', names=AWP_accu,header=0)
#        Date = Climatedata.A.tolist()
        self.C2000s = Climatedata.B.tolist()
        self.C2010s = Climatedata.C.tolist()
        self.C2007 = Climatedata.D.tolist()
        self.C2012 = Climatedata.E.tolist()
        self.C2014 = Climatedata.F.tolist()
        self.C2016 = Climatedata.G.tolist()
        self.C2019 = Climatedata.H.tolist()
    
    
    def loadCSVRegiondata (self):
        Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional.csv', names=Yearcolnames,header=0)
        self.SoO = Yeardata.Sea_of_Okhotsk.tolist()
        self.Bers = Yeardata.Bering_Sea.tolist()
        self.HB = Yeardata.Hudson_Bay.tolist()
        self.BB = Yeardata.Baffin_Bay.tolist()
        self.EG = Yeardata.East_Greenland_Sea.tolist()
        self.BaS = Yeardata.Barents_Sea.tolist()
        self.KS = Yeardata.Kara_Sea.tolist()
        self.LS = Yeardata.Laptev_Sea.tolist()
        self.ES = Yeardata.East_Siberian_Sea.tolist()
        self.CS = Yeardata.Chukchi_Sea.tolist()
        self.BeaS = Yeardata.Beaufort_Sea.tolist()
        self.CA = Yeardata.Canadian_Archipelago.tolist()
        self.AB = Yeardata.Central_Arctic.tolist()
        
        Yearcolnames_daily = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
        Yeardata_daily = pandas.read_csv(f'{self.webpath}/Melt_AWP/Arctic_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily,header=0)
        self.SoO_daily = Yeardata_daily.Sea_of_Okhotsk.tolist()
        self.Bers_daily = Yeardata_daily.Bering_Sea.tolist()
        self.HB_daily = Yeardata_daily.Hudson_Bay.tolist()
        self.BB_daily = Yeardata_daily.Baffin_Bay.tolist()
        self.EG_daily = Yeardata_daily.East_Greenland_Sea.tolist()
        self.BaS_daily = Yeardata_daily.Barents_Sea.tolist()
        self.KS_daily = Yeardata_daily.Kara_Sea.tolist()
        self.LS_daily = Yeardata_daily.Laptev_Sea.tolist()
        self.ES_daily = Yeardata_daily.East_Siberian_Sea.tolist()
        self.CS_daily = Yeardata_daily.Chukchi_Sea.tolist()
        self.BeaS_daily = Yeardata_daily.Beaufort_Sea.tolist()
        self.CA_daily = Yeardata_daily.Canadian_Archipelago.tolist()
        self.AB_daily = Yeardata_daily.Central_Arctic.tolist()
    
    
    
    def automated (self,year,datestring):
        
        self.year = year
        self.datestring = datestring
        
        self.loadCSVdata()
        self.loadCSVRegiondata()

        self.daily_anomaly()
        self.accumulated_anomaly()
        self.centredailygraph()
        self.centreaccumulatedgraph()
        self.regiongraph()
        self.regiongraph_daily()
#        plt.show()
        

action = AWP_graphs()
if __name__ == "__main__":
    print('main')
    action.automated(2023,'2023-09-22')
#    action.loadCSVdata()
#    action.loadCSVRegiondata()
#    action.daily_graph()
#    action.daily_anomaly()
#    action.accumulated_anomaly()
#    action.regiongraph_daily()
#    action.regiongraph()
#    action.centredailygraph()
#    action.centreaccumulatedgraph()
    
    

