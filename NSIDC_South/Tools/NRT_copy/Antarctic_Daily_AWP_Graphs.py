import numpy as np
import pandas
import matplotlib.pyplot as plt



class AWP_graphs_south:

    def __init__  (self):
        self.webpath = '/var/www/Cryoweb'
        self.year = 2023
        self.stringmonth = '11'
        self.stringday = '11'
        
        self.xAxis = [-22,8,39,69,100,131,160] # month divder ines
        self.xlabel = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
        
    def minus(self,a,b):
        '''calculates the FDD anomaly'''
        a = float(a)
        b = float(b)
        c = a-b
        return c
        

    def daily_graph(self):
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Daily Pan Antarctic Albedo-Warming Potential', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(1,1,1)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption in [MJ / 'r'$m^2$]')
        major_ticks = np.arange(0,40,2.5)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south',transform=ax.transAxes,color='grey', fontsize=10)
        
        ax.grid(True)
        plt.plot( self.Icefree_daily, color=(0.1,0.1,0.7),label='IceFree',lw=2,ls='--')
        plt.plot( self.Mean_daily, color=(0.22,0.22,0.22),label='Mean',lw=2,ls='--')
        plt.plot( self.SDminus_daily, color=(0.6,0.6,0.6),label='-2SD',lw=2,ls='--')
        plt.plot( self.SDplus_daily, color=(0.66,0.66,0.66),label='+2SD',lw=2,ls='--')
#        plt.plot( self.C2012_daily, color='orange',label='2012',lw=1)
        plt.plot( self.C20134_daily, color='green',label='2013-4',lw=1)
        plt.plot( self.C2023_daily, color='red',label='2022-3',lw=1)
        plt.plot( self.CSVDaily, color='black',label='2023-24',lw=2)
        
        ymin = 0
        ymax = 31
        plt.axis([0,181,ymin,ymax])
        
        last_value =  round(self.CSVDaily[-1],3)
        ax.text(0.01, 0.01, 'Last value: '+'{} {}'.format(last_value,'[MJ / 'r'$m^2$]'), fontsize=10,color='black',transform=ax.transAxes)
        
        ax.text(0.02, 0.96, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.93, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper right')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph1.png',bbox_extra_artists=(lgd,))
        plt.close()
#        plt.show()
        
    def accu_graph(self):
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Accumulated Pan Antarctic Albedo-Warming Potential', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(1,1,1)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption in [MJ / 'r'$m^2$]')
        major_ticks = np.arange(0,5000,500)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south',transform=ax.transAxes,color='grey', fontsize=10)
        
        ax.grid(True)
        plt.plot( self.Icefree, color=(0.1,0.1,0.7),label='IceFree',lw=2,ls='--')
        plt.plot( self.Mean, color=(0.22,0.22,0.22),label='Mean',lw=2,ls='--')
        plt.plot( self.SDminus, color=(0.6,0.6,0.6),label='-2SD',lw=2,ls='--')
        plt.plot( self.SDplus, color=(0.66,0.66,0.66),label='+2SD',lw=2,ls='--')
#        plt.plot( self.C2012, color='orange',label='2012',lw=1)
        plt.plot( self.C20134, color='green',label='2013-4',lw=1)
        plt.plot( self.C2023, color='red',label='2022-3',lw=1)
        plt.plot( self.CSVCumu, color='black',label='2023-24',lw=2)
        
        ymin = 0
        ymax = 4000
        plt.axis([0,181,ymin,ymax])
        
        last_value =  int(self.CSVCumu[-1])
        ax.text(0.66, 0.01, 'Last value: '+'{} {}'.format(last_value,'[MJ / 'r'$m^2$]'), fontsize=10,color='black',transform=ax.transAxes)
        
        ax.text(0.02, 0.96, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.93, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='lower right')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph2.png',bbox_extra_artists=(lgd,))
        plt.close()
#        plt.show()

    def daily_anomaly(self):
        
        anom_20112 = list(map(self.minus,self.C20112_daily,self.AWP_Daily_mean))
        anom_20134 = list(map(self.minus,self.C20134_daily,self.AWP_Daily_mean))
        anom_20145 = list(map(self.minus,self.C20145_daily,self.AWP_Daily_mean))
        anom_20167 = list(map(self.minus,self.C20167_daily,self.AWP_Daily_mean))
        anom_2020 = list(map(self.minus,self.C2020_daily,self.AWP_Daily_mean))
        anom_2022 = list(map(self.minus,self.C2022_daily,self.AWP_Daily_mean))
        anom_2023 = list(map(self.minus,self.C2023_daily,self.AWP_Daily_mean))
        current_anom = list(map(self.minus,self.CSVDaily,self.AWP_Daily_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Daily Pan Antarctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        major_ticks = np.arange(-10,10,0.25)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south',transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( anom_20112, color='grey',label='2011-2',lw=1)
        plt.plot( anom_20134, color='green',label='2013-4',lw=1)
        plt.plot( anom_20145, color='purple',label='2014-5',lw=1)
        plt.plot( anom_20167, color='orange',label='2016-7',lw=1)
        plt.plot( anom_2020, color='brown',label='2019-20',lw=1)
        plt.plot( anom_2022, color='blue',label='2021-22',lw=1)
        plt.plot( anom_2023, color='red',label='2022-23',lw=1)
        plt.plot( current_anom, color='black',label='2023-24',lw=2)
        
        ymin = -2
        ymax = 2.75
        plt.axis([0,181,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper right')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph3.png',bbox_extra_artists=(lgd,))
        plt.close()

    
    def accumu_anomaly(self):
        
        anom_20112 = list(map(self.minus,self.C20112,self.AWP_Accu_mean))
        anom_20134 = list(map(self.minus,self.C20134,self.AWP_Accu_mean))
        anom_20145 = list(map(self.minus,self.C20145,self.AWP_Accu_mean))
        anom_20167 = list(map(self.minus,self.C20167,self.AWP_Accu_mean))
        anom_2020 = list(map(self.minus,self.C2020,self.AWP_Accu_mean))
        anom_2022 = list(map(self.minus,self.C2022,self.AWP_Accu_mean))
        anom_2023 = list(map(self.minus,self.C2023,self.AWP_Accu_mean))
        current_anom = list(map(self.minus,self.CSVCumu,self.AWP_Accu_mean))
    
        
        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle('Accumulated Pan Antarctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        major_ticks = np.arange(-500,500,25)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south', transform=ax.transAxes, color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        plt.plot( anom_20112, color='grey',label='2011-2',lw=1)
        plt.plot( anom_20134, color='green',label='2013-4',lw=1)
        plt.plot( anom_20145, color='purple',label='2014-5',lw=1)
        plt.plot( anom_20167, color='orange',label='2016-7',lw=1)
        plt.plot( anom_2020, color='brown',label='2019-20',lw=1)
        plt.plot( anom_2022, color='blue',label='2021-22',lw=1)
        plt.plot( anom_2023, color='red',label='2022-23',lw=1)
        plt.plot( current_anom, color='black',label='2023-24',lw=2)
        
        ymin = -150
        ymax = 200
        plt.axis([0,181,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph4.png',bbox_extra_artists=(lgd,))
        plt.close()
            
    def regiongraph(self):
        
        Climatecolnames = ['Date','B','C','D','E','F']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_mean_regional.csv', names=Climatecolnames,header=0)
        Wed_mean = Climatedata.B.tolist()
        Ind_mean = Climatedata.C.tolist()
        Pac_mean = Climatedata.D.tolist()
        Ross_mean = Climatedata.E.tolist()
        Bell_mean = Climatedata.F.tolist()
                
        Region1 = list(map(self.minus,self.Wed,Wed_mean))
        Region2 = list(map(self.minus,self.Ind,Ind_mean))
        Region3 = list(map(self.minus,self.Pac,Pac_mean))
        Region4 = list(map(self.minus,self.Ross,Ross_mean))
        Region5 = list(map(self.minus,self.Bell,Bell_mean))

        
        data = [Region1,Region2,Region3,Region4,Region5]

        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle(str(self.year)+' Accumulated Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south', transform=ax.transAxes, color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        
        plt.plot( Region1, color=(0.1,0.7,0.1),label='Weddel Sea',lw=2)
        plt.plot( Region2, color=(0.9,0.1,0.1),label='Indian Ocean',lw=2)
        plt.plot( Region3, color=(1,0.6,0.2),label='Pacific Ocean',lw=2)
        plt.plot( Region4, color=(0,0,0.6),label='Ross Sea',lw=2)
        plt.plot( Region5, color=(0,0,0),label='Bell-Amun Sea',lw=2)
        
        ymin = 0
        ymax = 0
        
        for x in data:
            value = x[-1]
            if value > ymax:
                ymax = value
            if value < ymin:
                ymin = value

        step = 25
        if max(ymax,abs(ymin)) > 210:
            step = 50
        
        ymin = -50
        major_ticks = np.arange(-600,600,step)
        ax.set_yticks(major_ticks)
        plt.axis([0,181,min(-40,ymin-15),ymax+15])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        #fig.subplots_adjust(bottom=0.1)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph_Region1.png')
        plt.close()

            
    def regiongraph_daily(self):
        
        Climatecolnames = ['Date','B','C','D','E','F']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_mean_regional_daily.csv', names=Climatecolnames,header=0)
        Wed_mean = Climatedata.B.tolist()
        Ind_mean = Climatedata.C.tolist()
        Pac_mean = Climatedata.D.tolist()
        Ross_mean = Climatedata.E.tolist()
        Bell_mean = Climatedata.F.tolist()
                
        Region1 = list(map(self.minus,self.Wed_daily,Wed_mean))
        Region2 = list(map(self.minus,self.Ind_daily,Ind_mean))
        Region3 = list(map(self.minus,self.Pac_daily,Pac_mean))
        Region4 = list(map(self.minus,self.Ross_daily,Ross_mean))
        Region5 = list(map(self.minus,self.Bell_daily,Bell_mean))
        
        data = [Region1,Region2,Region3,Region4,Region5]

        fig = plt.figure(figsize=(10,6.5))
        fig.suptitle(str(self.year)+' Daily Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        plt.xticks(self.xAxis,self.xlabel)

        ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        major_ticks = np.arange(-20,20,0.5)
        ax.set_yticks(major_ticks)
        
        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.7, -0.06, 'cryospherecomputing.com/awp-south', transform=ax.transAxes, color='grey', fontsize=10)
        ax.text(0.75, 0.02, 'Anomaly Base: 2000-2019', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
        
        ax.grid(True)
        
        plt.plot( Region1, color=(0.1,0.7,0.1),label='Weddel Sea',lw=2)
        plt.plot( Region2, color=(0.9,0.1,0.1),label='Indian Ocean',lw=2)
        plt.plot( Region3, color=(1,0.6,0.2),label='Pacific Ocean',lw=2)
        plt.plot( Region4, color=(0,0,0.6),label='Ross Sea',lw=2)
        plt.plot( Region5, color=(0,0,0),label='Bell-Amun Sea',lw=2)
        
        ymin = -3
        ymax = 4
                    
        plt.axis([0,181,ymin,ymax])
        
        ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.03, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        lgd = ax.legend(loc='upper left')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/AWP/South_AWP_Graph_Region2.png')
        plt.close()

    
    def loadCSVdata (self):
        Yearcolnames = ['Date','B','C']
        Yeardata = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT.csv', names=Yearcolnames,header=0)
        self.CSVDatum = Yeardata.Date.tolist()
        self.CSVDaily = Yeardata.B.tolist()
        self.CSVCumu = Yeardata.C.tolist()

        
        AWP_mean = ['A','B','C']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_mean.csv', names=AWP_mean,header=0)
        self.AWP_Daily_mean = Climatedata.B.tolist()
        self.AWP_Accu_mean = Climatedata.C.tolist()
        
        
        AWP_daily = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','K','L']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_pan_Daily.csv', names=AWP_daily,header=0)
#        Date = Climatedata.A.tolist()
        self.Icefree_daily = Climatedata.B.tolist()
        self.Mean_daily = Climatedata.C.tolist()
        self.SDminus_daily = Climatedata.D.tolist()
        self.SDplus_daily = Climatedata.E.tolist()
        self.C20112_daily = Climatedata.F.tolist()
        self.C20134_daily = Climatedata.G.tolist()
        self.C20145_daily = Climatedata.H.tolist()
        self.C20167_daily = Climatedata.I.tolist()
        self.C2020_daily = Climatedata.J.tolist()
        self.C2022_daily = Climatedata.K.tolist()
        self.C2023_daily = Climatedata.L.tolist()
        
        AWP_accu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J','K','L']
        Climatedata = pandas.read_csv(f'{self.webpath}/AWP_data/Climatology/South_AWP_pan_Accumulated.csv', names=AWP_accu,header=0)
#        Date = Climatedata.A.tolist()
        self.Icefree = Climatedata.B.tolist()
        self.Mean = Climatedata.C.tolist()
        self.SDminus = Climatedata.D.tolist()
        self.SDplus = Climatedata.E.tolist()
        self.C20112 = Climatedata.F.tolist()
        self.C20134 = Climatedata.G.tolist()
        self.C20145 = Climatedata.H.tolist()
        self.C20167 = Climatedata.I.tolist()
        self.C2020 = Climatedata.J.tolist()
        self.C2022 = Climatedata.K.tolist()
        self.C2023 = Climatedata.L.tolist()
    
    
    def loadCSVRegiondata (self):
        Yearcolnames = ['A', 'B', 'C', 'D', 'E', 'F']
        Yeardata = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT_regional.csv', names=Yearcolnames,header=0)
        self.Wed = Yeardata.B.tolist()
        self.Ind = Yeardata.C.tolist()
        self.Pac = Yeardata.D.tolist()
        self.Ross = Yeardata.E.tolist()
        self.Bell = Yeardata.F.tolist()
        
        Yearcolnames_daily = ['A', 'B', 'C', 'D', 'E', 'F']
        Yeardata = pandas.read_csv(f'{self.webpath}/AWP_data/South_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily,header=0)
        self.Wed_daily = Yeardata.B.tolist()
        self.Ind_daily = Yeardata.C.tolist()
        self.Pac_daily = Yeardata.D.tolist()
        self.Ross_daily = Yeardata.E.tolist()
        self.Bell_daily = Yeardata.F.tolist()
    
    
    
    def automated (self,year,month,day):
        
        self.year = year
        self.stringmonth = month
        self.stringday = day
        
        self.loadCSVdata()
        self.loadCSVRegiondata()

        self.daily_graph()
        self.accu_graph()

        self.daily_anomaly()
        self.accumu_anomaly()
        self.regiongraph()
        self.regiongraph_daily()
#        plt.show()
        

action = AWP_graphs_south()
if __name__ == "__main__":
    print('main')
    action.automated(2023,'09','99')
#    action.loadCSVdata()
#    action.daily_graph()
#    action.accu_graph()
    

