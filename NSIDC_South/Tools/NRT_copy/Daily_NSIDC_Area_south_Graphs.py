import pandas
import matplotlib.pyplot as plt
import numpy as np

class NSIDC_Graph:

    def __init__  (self):
        self.webpath = '/var/www/Cryoweb'
        self.year = 2023
        self.stringmonth = '00'
        self.stringday = '00'
        
        self.xAxis = [0,30,59,90,120,151,181,212,243,273,304,334,365] # month divder ines
        self.xlabel = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan']
        
            
    def makegraph(self):
        
        #del self.CSVArea[0]        
        fig = plt.figure(figsize=(8, 6))
        fig.suptitle('Antarctic Sea Ice Area', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
        ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.75, -0.08, 'cryospherecomputing.com',
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.grid(True)
        
        x = np.arange(len(self.Mean))
        IceSDup = [x+2*y for x,y in zip(self.Mean,self.CSD)]
        IceSDdown = [x-2*y for x,y in zip(self.Mean,self.CSD)]
        
        plt.plot( self.Mean, color=(0.2,0.2,0.2),label='2000-19',lw=2,ls='--')
        plt.fill_between(x,IceSDup,IceSDdown,color='grey',label='2 SD', alpha=0.3)
        
#        plt.plot( self.C1986, color='red',label='1986',lw=2)
        plt.plot( self.C2014, color='blue',label='2014',lw=2)
        plt.plot( self.C2016, color='green',label='2016',lw=2)
        plt.plot( self.C2017, color='brown',label='2017',lw=2)
        plt.plot( self.C2019, color='purple',label='2019',lw=2)
        plt.plot( self.C2021, color='orange',label='2021',lw=2)
        plt.plot( self.C2022, color='red',label='2022',lw=2)
        plt.plot( self.CSVArea, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVArea[-1]*1e6)
        prev_day = int(self.CSVArea[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = max(0,float(self.CSVArea[-1])-4)
        ymax = min(17,float(self.CSVArea[-1])+4)
        plt.axis([len(self.CSVArea)-44,len(self.CSVArea)+33,ymin,ymax])
        legend = plt.legend(loc=4, shadow=True, fontsize='medium')
        
        ax.text(0.5, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.5, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.08)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Antarctic_Graph.png')
        plt.close()


    def makegraph_full(self):
        #del self.CSVArea[0]
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Antarctic Sea Ice Area', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.text(5, 16.5, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax.text(5, 16.2, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
        major_ticks = np.arange(0, 17, 1)
        ax.set_yticks(major_ticks)     

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',
        transform=ax.transAxes,
        color='grey', fontsize=10)    
        ax.grid(True)
        
        
        x = np.arange(len(self.Mean))
        IceSDup = [x+2*y for x,y in zip(self.Mean,self.CSD)]
        IceSDdown = [x-2*y for x,y in zip(self.Mean,self.CSD)]
        
        plt.plot( self.Mean, color=(0.2,0.2,0.2),label='2000-19',lw=2,ls='--')
        plt.fill_between(x,IceSDup,IceSDdown,color='grey',label='2 SD', alpha=0.3)
        
        plt.plot( self.C2014, color='blue',label='2014',lw=2)
        plt.plot( self.C2016, color='green',label='2016',lw=2)
        plt.plot( self.C2017, color='brown',label='2017',lw=2)
        plt.plot( self.C2019, color='purple',label='2019',lw=2)
        plt.plot( self.C2021, color='orange',label='2021',lw=2)
        plt.plot( self.C2022, color='red',label='2022',lw=2)
        plt.plot( self.CSVArea, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVArea[-1]*1e6)
        prev_day = int(self.CSVArea[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.6, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = 0
        ymax = 17
        plt.axis([0,365,ymin,ymax])
        legend = plt.legend(loc=(0.835,0.01), shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.06)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Antarctic_Graph_full.png')
        plt.close()
    
    def makegraph_compaction(self):
        #del self.CSVCompaction[0]
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Antarctic Sea Ice Compaction (Area / Extent)', fontsize=14, fontweight='bold')
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
        
        x = np.arange(len(self.CompactionMean))
        IceSDup = [x+2*y for x,y in zip(self.CompactionMean,self.CompactionSD)]
        IceSDdown = [x-2*y for x,y in zip(self.CompactionMean,self.CompactionSD)]
        
        plt.plot( self.CompactionMean, color=(0.2,0.2,0.2),label='2000-19',lw=2,ls='--')
        plt.fill_between(x,IceSDup,IceSDdown,color='grey',label='2 SD', alpha=0.3)
        
        plt.plot( self.Compaction2014, color='blue',label='2014',lw=2)
        plt.plot( self.Compaction2016, color='green',label='2016',lw=2)
        plt.plot( self.Compaction2017, color='brown',label='2017',lw=2)
        plt.plot( self.Compaction2019, color='purple',label='2019',lw=2)
        plt.plot( self.Compaction2021, color='orange',label='2021',lw=2)
        plt.plot( self.Compaction2022, color='red',label='2022',lw=2)
        plt.plot( self.CSVCompaction, color='black',label=self.year,lw=2)
        
        last_value =  round(self.CSVCompaction[-1],2)
        ax.text(0.75, 0.01, 'Last value: '+str(last_value)+' %', fontsize=10,color='black',transform=ax.transAxes)
        
        yearday = len(self.CSVCompaction)
        ymin = max(49,float(self.CSVCompaction[-1])-7*self.CompactionSD[yearday])
        ymax = min(86,float(self.CSVCompaction[-1])+7*self.CompactionSD[yearday])
        plt.axis([len(self.CSVCompaction)-55,len(self.CSVCompaction)+44,ymin,ymax])
        
        
        legend = plt.legend(loc=4, shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.06)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Antarctic_Graph_Compaction.png')
        plt.close()
        
    def makeExtentgraph(self):
        fig = plt.figure(figsize=(8, 6))
        fig.suptitle('Antarctic Sea Ice Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('Sea Ice Extent in 'r'[$10^6$ $km^2$]')
        ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.75, -0.08, 'cryospherecomputing.com',
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.grid(True)
        
        x = np.arange(len(self.EMean))
        IceSDup = [x+2*y for x,y in zip(self.EMean,self.ESD)]
        IceSDdown = [x-2*y for x,y in zip(self.EMean,self.ESD)]
        
        plt.plot( self.EMean, color=(0.2,0.2,0.2),label='2000-19',lw=2,ls='--')
        plt.fill_between(x,IceSDup,IceSDdown,color='grey',label='2 SD', alpha=0.3)
        
        plt.plot( self.E2014, color='blue',label='2014',lw=2)
        plt.plot( self.E2016, color='green',label='2016',lw=2)
        plt.plot( self.E2017, color='brown',label='2017',lw=2)
        plt.plot( self.E2019, color='purple',label='2019',lw=2)
        plt.plot( self.E2021, color='orange',label='2021',lw=2)
        plt.plot( self.E2022, color='red',label='2022',lw=2)
        plt.plot( self.CSVExtent, color='black',label=self.year,lw=2)
        
        last_value =  int(self.CSVExtent[-1]*1e6)
        prev_day = int(self.CSVExtent[-2]*1e6)
        change = (last_value - prev_day)/1000
        change = "%+d" % (change)
        ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$ ({}k)'.format(change), fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = max(0,float(self.CSVExtent[-1])-5)
        ymax = min(20.5,float(self.CSVExtent[-1])+5)
        plt.axis([len(self.CSVExtent)-55,len(self.CSVExtent)+44,ymin,ymax])
        legend = plt.legend(loc=4, shadow=True, fontsize='medium')
        
        ax.text(0.5, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.5, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.subplots_adjust(bottom=0.08)
        fig.savefig(f'{self.webpath}/NSIDC_Area/charts/Antarctic_Graph_Extent.png')
        plt.close()

    def loadCSVdata (self):
    
        #NRT Data
        Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
        Yeardata = pandas.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_NSIDC_Area_NRT.csv', names=Yearcolnames,header=0)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVArea = Yeardata.Area.tolist()
        self.CSVExtent = Yeardata.Extent.tolist()
        self.CSVCompaction = Yeardata.Compaction.tolist()
        
        #Climate Data
        Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        Climatedata = pandas.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_climate.csv', names=Climatecolnames,header=0)
        self.Mean = Climatedata.B.tolist()
        self.CSD = Climatedata.C.tolist()
        self.C2014 = Climatedata.D.tolist()
        self.C2016 = Climatedata.E.tolist()
        self.C2017 = Climatedata.F.tolist()
        self.C2019 = Climatedata.G.tolist()
        self.C2021 = Climatedata.H.tolist()
        self.C2022 = Climatedata.I.tolist()
        
        #Climate Data
        Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        Climatedata = pandas.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_climate_Extent.csv', names=Climatecolnames,header=0)
        self.EMean = Climatedata.B.tolist()
        self.ESD = Climatedata.C.tolist()
        self.E2014 = Climatedata.D.tolist()
        self.E2016 = Climatedata.E.tolist()
        self.E2017 = Climatedata.F.tolist()
        self.E2019 = Climatedata.G.tolist()
        self.E2021 = Climatedata.H.tolist()
        self.E2022 = Climatedata.I.tolist()
        
        #Compaction Data
        Compactioncolnames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        Compactiondata = pandas.read_csv(f'{self.webpath}/NSIDC_Area/Data/Antarctic_climate_compaction.csv', names=Compactioncolnames,header=0)
        self.CompactionMean = Compactiondata.B.tolist()
        self.CompactionSD = Compactiondata.C.tolist()
        self.Compaction2014 = Compactiondata.D.tolist()
        self.Compaction2016 = Compactiondata.E.tolist()
        self.Compaction2017 = Compactiondata.F.tolist()
        self.Compaction2019 = Compactiondata.G.tolist()
        self.Compaction2021 = Compactiondata.H.tolist()
        self.Compaction2022 = Compactiondata.I.tolist()
    
    
    
    def automated (self,year,month,day):
        
        self.year = year
        self.stringmonth = month
        self.stringday = day
        
        self.loadCSVdata()
        self.makegraph()
        self.makegraph_full()
        self.makegraph_compaction()
        self.makeExtentgraph()
#        plt.show()

action = NSIDC_Graph()
if __name__ == "__main__":
    print('main')
    action.automated(2023,'0','0')
#     action.loadCSVdata()
    #action.makegraph()
    #action.makegraph_compaction()
#     action.makeExtentgraph()
