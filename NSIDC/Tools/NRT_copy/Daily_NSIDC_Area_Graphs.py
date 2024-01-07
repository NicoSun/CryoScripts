import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class NSIDC_Graph:

    def __init__  (self):
        self.year = 2023
        self.stringmonth = '00'
        self.stringday = '00'
        self.xAxis = [0,30,59,90,120,151,181,212,243,273,304,334,365] # month divder lines
        self.xlabel = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']
        self.webpath = '/var/www/Cryoweb'
        
        
    def makegraph(self):
        '''creates a smaller seasonal sea ice area graph'''
        fig = plt.figure(figsize=(8, 6))
        fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
        
        ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.75, -0.08, 'cryospherecomputing.com',
        transform=ax.transAxes,color='grey', fontsize=10)
        
        ax.grid(True)
        
        plt.plot( self.C1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
        plt.plot( self.C1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
        plt.plot( self.C2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
        plt.plot( self.C2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
        plt.plot( self.C2012, color='orange',label='2012',lw=1)
        plt.plot( self.C2016, color='green',label='2016',lw=1)
        plt.plot( self.C2017, color='brown',label='2017',lw=1)
        plt.plot( self.C2019, color='purple',label='2019',lw=1)
        plt.plot( self.C2020, color='red',label='2020',lw=1)
        plt.plot( self.CSVArea, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVArea[-1]*1e6)
        prev_day = int(self.CSVArea[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = max(0,float(self.CSVArea[-1])-4)
        ymax = min(14.5,float(self.CSVArea[-1])+4)
        plt.axis([len(self.CSVArea)-44,len(self.CSVArea)+33,ymin,ymax])
        plt.legend(loc=4, shadow=True, fontsize='medium')
        
        ax.text(0.52, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.52, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.08)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Arctic_Graph.png')
        plt.close()

            
    def makegraph_full(self):
        '''creates the full year sea ice area graph'''
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.text(5, 0.5, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax.text(5, 0.2, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
        major_ticks = np.arange(0, 15, 1)
        ax.set_yticks(major_ticks)  

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',
        transform=ax.transAxes,
        color='grey', fontsize=10)    
        
        ax.grid(True)
        plt.plot( self.C1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
        plt.plot( self.C1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
        plt.plot( self.C2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
        plt.plot( self.C2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
        plt.plot( self.C2012, color='orange',label='2012',lw=1)
        plt.plot( self.C2016, color='green',label='2016',lw=1)
        plt.plot( self.C2017, color='brown',label='2017',lw=1)
        plt.plot( self.C2019, color='purple',label='2019',lw=1)
        plt.plot( self.C2020, color='red',label='2020',lw=1)
        plt.plot( self.CSVArea, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVArea[-1]*1e6)
        prev_day = int(self.CSVArea[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.66, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = 0
        ymax = 14.5
        plt.axis([0,365,ymin,ymax])
        plt.legend(loc=4, shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.06)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Arctic_Graph_full.png')
        plt.close()

            
    def makegraph_compaction(self):
        '''creates the sea ice compaction graph (area/extent)'''
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Arctic Sea Ice Compaction (Area / Extent)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)
        
        ax.text(0.01, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.01, 0.03, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.set_ylabel('Compaction in %')
        major_ticks = np.arange(0, 100, 5)
        ax.set_yticks(major_ticks)     

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',
        transform=ax.transAxes,
        color='grey', fontsize=10)
        
        ax.grid(True)
        
        plt.plot( self.Compaction1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
        plt.plot( self.Compaction1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
        plt.plot( self.Compaction2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
        plt.plot( self.Compaction2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
        plt.plot( self.Compaction2012, color='orange',label='2012',lw=1)
        plt.plot( self.Compaction2016, color='green',label='2016',lw=1)
        plt.plot( self.Compaction2017, color='brown',label='2017',lw=1)
        plt.plot( self.Compaction2019, color='purple',label='2019',lw=1)
        plt.plot( self.Compaction2020, color='red',label='2020',lw=1)
        plt.plot( self.CSVCompaction, color='black',label=self.year,lw=2)
        
        last_value =  round(self.CSVCompaction[-1],2)
        ax.text(0.75, 0.01, 'Last value: '+str(last_value)+' %', fontsize=10,color='black',transform=ax.transAxes)
        
        yearday = len(self.CSVCompaction)
        variance = [self.Compaction1980s[yearday],self.Compaction1990s[yearday],self.Compaction2000s[yearday],self.Compaction2010s[yearday]]
        variance_new = np.asarray(variance).astype(np.float32)
        deviation = np.std(variance_new)+1
        ymin = max(49,float(self.CSVCompaction[-1])-8*deviation)
        ymax = min(96,float(self.CSVCompaction[-1])+6*deviation)
        plt.axis([len(self.CSVCompaction)-55,len(self.CSVCompaction)+44,ymin,ymax])
        
        
        plt.legend(loc=4, shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.06)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Arctic_Graph_Compaction.png')
        plt.close()
        
    def Globalgraph(self):
        '''creates the Global Sea Ice Area Graph'''
        #NRT Data Antarctic
        Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
        Yeardata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv', names=Yearcolnames,header=0)
        CSVArea_ant = Yeardata.Area.tolist()
        CSVExtent_ant = Yeardata.Extent.tolist()
        
        #Climate Data
        Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        Climatedata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Global_climate.csv', names=Climatecolnames,header=0)
        Mean = Climatedata.B.tolist()
        SD = Climatedata.C.tolist()
        C2013 = Climatedata.D.tolist()
        C2014 = Climatedata.E.tolist()
        C2016 = Climatedata.F.tolist()
        C2017 = Climatedata.G.tolist()
        C2019 = Climatedata.H.tolist()
        C2020 = Climatedata.I.tolist()
        
        CSVArea = [x + y for x, y in zip(self.CSVArea, CSVArea_ant)]
        #del self.CSVArea[0]
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Global Sea Ice Area', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.text(5, 23.7, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax.text(5, 23.44, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
        major_ticks = np.arange(0, 30, 1)
        ax.set_yticks(major_ticks)     

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',
        transform=ax.transAxes,
        color='grey', fontsize=10)    
        ax.grid(True)
        
        
        x = np.arange(len(Mean))
        IceSDup = [x+2*y for x,y in zip(Mean,SD)]
        IceSDdown = [x-2*y for x,y in zip(Mean,SD)]
        
        plt.plot( Mean, color=(0.2,0.2,0.2),label='2000-19',lw=2,ls='--')
        plt.fill_between(x,IceSDup,IceSDdown,color='grey',label='2 SD', alpha=0.3)
        

        plt.plot( C2013, color='purple',label='2013',lw=2)
        plt.plot( C2014, color='blue',label='2014',lw=2)
        plt.plot( C2016, color='green',label='2016',lw=2)
        plt.plot( C2017, color='brown',label='2017',lw=2)
        plt.plot( C2019, color='orange',label='2019',lw=2)
        plt.plot( C2020, color='red',label='2020',lw=2)
        plt.plot( CSVArea, color='black',label=self.year,lw=3)
        
        last_value =  int(CSVArea[-1]*1e6)
        ax.text(0.55, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = 13
        ymax = 24
        plt.axis([0,365,ymin,ymax])
        legend = plt.legend(loc=(0.75,0.01), shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.06)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Global_Graph_full.png')
        plt.close()
#        plt.show()
        
    def makeExtentgraph(self):
        '''creates a smaller seasonal sea ice area graph'''
        fig = plt.figure(figsize=(8, 6))
        fig.suptitle('Arctic Sea Ice Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('Sea Ice Extent in 'r'[$10^6$ $km^2$]')
        
        ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.75, -0.08, 'cryospherecomputing.com',
        transform=ax.transAxes,color='grey', fontsize=10)
        
        ax.grid(True)
        
        plt.plot( self.E1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
        plt.plot( self.E1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
        plt.plot( self.E2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
        plt.plot( self.E2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
        plt.plot( self.E2012, color='orange',label='2012',lw=1)
        plt.plot( self.E2016, color='green',label='2016',lw=1)
        plt.plot( self.E2017, color='brown',label='2017',lw=1)
        plt.plot( self.E2019, color='purple',label='2019',lw=1)
        plt.plot( self.E2020, color='red',label='2020',lw=1)
        plt.plot( self.CSVExtent, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVExtent[-1]*1e6)
        prev_day = int(self.CSVExtent[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = max(0,float(self.CSVExtent[-1])-5)
        ymax = min(16,float(self.CSVExtent[-1])+5)
        plt.axis([len(self.CSVExtent)-55,len(self.CSVExtent)+44,ymin,ymax])
        plt.legend(loc=4, shadow=True, fontsize='medium')
        
        ax.text(0.52, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.52, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.08)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Arctic_Graph_Extent.png')
        plt.close()

    def loadCSVdata (self):
        '''Loads NRT & Climate data'''
        #NRT Data
        Yearcolnames = ['Date','B','C','D']
        Yeardata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Arctic_NSIDC_Area_NRT.csv', names=Yearcolnames,header=0)
        self.CSVArea = Yeardata.B.tolist()
        self.CSVExtent = Yeardata.C.tolist()
        self.CSVCompaction = Yeardata.D.tolist()
# =============================================================================
#         self.CSVArea_High = Yeardata.E.tolist()
#         self.CSVExtent_High = Yeardata.F.tolist()
# =============================================================================
        
        
        #Climate Data
        Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        Climatedata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Arctic_climate.csv', names=Climatecolnames,header=0)
        self.C1980s = Climatedata.B.tolist()
        self.C1990s = Climatedata.C.tolist()
        self.C2000s = Climatedata.D.tolist()
        self.C2010s = Climatedata.E.tolist()
        self.C2012 = Climatedata.F.tolist()
        self.C2016 = Climatedata.G.tolist()
        self.C2017 = Climatedata.H.tolist()
        self.C2019 = Climatedata.I.tolist()
        self.C2020 = Climatedata.J.tolist()
        
        #Climate Data
        Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        Climatedata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Arctic_climate_Extent.csv', names=Climatecolnames,header=0)
        self.E1980s = Climatedata.B.tolist()
        self.E1990s = Climatedata.C.tolist()
        self.E2000s = Climatedata.D.tolist()
        self.E2010s = Climatedata.E.tolist()
        self.E2012 = Climatedata.F.tolist()
        self.E2016 = Climatedata.G.tolist()
        self.E2017 = Climatedata.H.tolist()
        self.E2019 = Climatedata.I.tolist()
        self.E2020 = Climatedata.J.tolist()
    
        #Compaction Data
        Compactioncolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        Compactiondata = pd.read_csv(f'{self.webpath}/NSIDC_Area/Data/Arctic_climate_compaction.csv', names=Compactioncolnames,header=0)
        self.Compaction1980s = Compactiondata.B.tolist()
        self.Compaction1990s = Compactiondata.C.tolist()
        self.Compaction2000s = Compactiondata.D.tolist()
        self.Compaction2010s = Compactiondata.E.tolist()
        self.Compaction2012 = Compactiondata.F.tolist()
        self.Compaction2016 = Compactiondata.G.tolist()
        self.Compaction2017 = Compactiondata.H.tolist()
        self.Compaction2019 = Compactiondata.I.tolist()
        self.Compaction2020 = Compactiondata.J.tolist()
    
    
    def automated (self,year,month,day):
        
        self.year = year
        self.stringmonth = month
        self.stringday = day
        
        self.loadCSVdata()
        self.makegraph()
        self.makegraph_full()
        self.makegraph_compaction()
        self.Globalgraph()
        self.makeExtentgraph()
#        plt.show()

action = NSIDC_Graph()
if __name__ == "__main__":
    print('main')
    action.automated(2023,'0','0')
#     action.loadCSVdata()
#    action.Globalgraph()
#     action.makeExtentgraph()
