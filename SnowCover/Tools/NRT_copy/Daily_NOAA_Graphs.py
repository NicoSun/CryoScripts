"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script creates the Volume and Thickness graphs
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt


class ADS_data:
    def __init__  (self):
        '''ADS object initializing'''
        self.year = 2022
        self.month =str(12).zfill(2)
        self.day = str(31).zfill(2)
        self.webpath = '/var/www/Cryoweb'
        
    
    def makeYeargraph(self):
        '''create full year graph'''
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Northern Hemisphere Snow Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        x = [0,30,59,90,120,151,181,212,243,273,304,334]
        plt.xticks(x,labels)

        ax.text(5, 27.2, r'Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold')
        ax.text(5, 26.6, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.set_ylabel('Extent in 10^6 'r'$km^2$')
        major_ticks = np.arange(0, 50, 2.5)
        ax.set_yticks(major_ticks)   

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',transform=ax.transAxes,color='grey', fontsize=10)    
           
        ax.grid(True)
        
        x = np.arange(366)
        
        AmericaSDup = [x+2*y for x,y in zip(self.MAmerica,self.SD_America)]
        AmericaSDdown = [x-2*y for x,y in zip(self.MAmerica,self.SD_America)]
        
        GreenlandSDup = [x+2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
        GreenlandSDdown = [x-2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
        
        EuropeSDup = [x+2*y for x,y in zip(self.MEurope,self.SD_Europe)]
        EuropeSDdown = [x-2*y for x,y in zip(self.MEurope,self.SD_Europe)]
        
        AsiaSDup = [x+2*y for x,y in zip(self.MAsia,self.SD_Asia)]
        AsiaSDdown = [x-2*y for x,y in zip(self.MAsia,self.SD_Asia)]
        
        
#        plt.fill_between(x,IceSDup,IceSDdown,color='orange', alpha=0.333)
        plt.fill_between(x,AmericaSDup,AmericaSDdown,color='red', alpha=0.333)
        plt.fill_between(x,GreenlandSDup,GreenlandSDdown,color='blue', alpha=0.333)
        plt.fill_between(x,EuropeSDup,EuropeSDdown,color='green', alpha=0.333)
        plt.fill_between(x,AsiaSDup,AsiaSDdown,color='grey',label='2 standard deviations', alpha=0.333)
    
#        plt.plot( self.NRT_SeaIce, color='orange',label='Sea Ice',lw=2)
        plt.plot( self.NRT_America, color='red',label='America',lw=2)
        plt.plot( self.NRT_Greenland, color='blue',label='Greenland',lw=2)
        plt.plot( self.NRT_Europe, color='green',label='Europe',lw=2)
        plt.plot( self.NRT_Asia, color='black',label='Asia',lw=2)
        
        plt.plot( self.MAmerica, color='red',lw=1,linestyle='--')
        plt.plot( self.MGreenland, color='blue',lw=1,linestyle='--')
        plt.plot( self.MEurope, color='green',lw=1,linestyle='--')
        plt.plot( self.MAsia, color='black',label='{}'.format('Mean'),lw=1,linestyle='--')
        
        America_anom = int((self.NRT_America[self.dayofyear] - self.MAmerica[self.dayofyear])*1e6)
        Europe_anom = int((self.NRT_Europe[self.dayofyear] - self.MEurope[self.dayofyear])*1e6)
        Asia_anom = int((self.NRT_Asia[self.dayofyear] - self.MAsia[self.dayofyear])*1e6)
        
        
        ax.text(0.6, 0.95, 'America anomaly: '+'{:,}'.format(America_anom)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
        ax.text(0.6, 0.93, 'Europe anomaly: '+'{:,}'.format(Europe_anom)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
        ax.text(0.6, 0.91, 'Asia anomaly: '+'{:,}'.format(Asia_anom)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = 0
        ymax = 28
        plt.axis([0,365,ymin,ymax])
        plt.legend(loc=9, shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
        fig.savefig(f'{self.webpath}/Snow_Cover_Data/NOAA_SnowCover.png')
        
#        plt.show()
        plt.close()

            
    def makemultiyeargraph(self):
        '''create 3 month zoomed graph'''
        fig = plt.figure(figsize=(12, 8))
        fig.suptitle('Northern Hemisphere Snow Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        x = [0,30,59,90,120,151,181,212,243,273,304,334]
        plt.xticks(x,labels)

        ax.text(36, 56, r'Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold')
        ax.text(36, 53, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.set_ylabel('Extent in 10^6 'r'$km^2$')
        major_ticks = np.arange(0, 50, 2.5)
        ax.set_yticks(major_ticks)

        ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
        ax.text(0.85, -0.06, 'cryospherecomputing.com',transform=ax.transAxes,color='grey', fontsize=10)    
        
        ax.grid(True)
        
        x = np.arange(366)
# =============================================================================
#         IceSDup = [x+2*y for x,y in zip(self.MSeaIce,self.SD_SeaIce)]
#         IceSDdown = [x-2*y for x,y in zip(self.MSeaIce,self.SD_SeaIce)]
# =============================================================================
        
        AmericaSDup = [x+2*y for x,y in zip(self.MAmerica,self.SD_America)]
        AmericaSDdown = [x-2*y for x,y in zip(self.MAmerica,self.SD_America)]
        
        GreenlandSDup = [x+2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
        GreenlandSDdown = [x-2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
        
        EuropeSDup = [x+2*y for x,y in zip(self.MEurope,self.SD_Europe)]
        EuropeSDdown = [x-2*y for x,y in zip(self.MEurope,self.SD_Europe)]
        
        AsiaSDup = [x+2*y for x,y in zip(self.MAsia,self.SD_Asia)]
        AsiaSDdown = [x-2*y for x,y in zip(self.MAsia,self.SD_Asia)]
        
        plt.fill_between(x,AmericaSDup,AmericaSDdown,color='red',label='America', alpha=0.333)
        plt.fill_between(x,GreenlandSDup,GreenlandSDdown,color='blue',label='Greenland', alpha=0.333)
        plt.fill_between(x,EuropeSDup,EuropeSDdown,color='green',label='Europe', alpha=0.333)
        plt.fill_between(x,AsiaSDup,AsiaSDdown,color='grey',label='Asia', alpha=0.333)
        
        plt.plot( self.NRT_SeaIce, color='orange',label='Sea Ice',lw=2)
        plt.plot( self.NRT_America, color='red',lw=2)
        plt.plot( self.NRT_Greenland, color='blue',lw=2)
        plt.plot( self.NRT_Europe, color='green',lw=2)
        plt.plot( self.NRT_Asia, color='black',label='{}'.format(self.year),lw=2)
        
        plt.plot( self.NRT_SeaIce1, color='orange',lw=2)
        plt.plot( self.NRT_America1, color='red',lw=1)
        plt.plot( self.NRT_Greenland1, color='blue',lw=1)
        plt.plot( self.NRT_Europe1, color='green',lw=1)
        plt.plot( self.NRT_Asia1, color='black',label='{}'.format(self.preyear),lw=1)
        
        
#        last_value =  int(self.V2018[-1])
#        ax.text(0.75, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^3$', fontsize=10,color='black',transform=ax.transAxes)
        
        ymin = 0
        ymax = 28
        plt.axis([0,365,ymin,ymax])
        plt.legend(loc=3, shadow=True, fontsize='medium')
        fig.tight_layout(pad=2)
        fig.subplots_adjust(top=0.95)
#        fig.savefig(f'{self.webpath}/Snow_Cover_Data/NOAA_SnowCover_multiyear.png')
#        plt.show()
        plt.close()

    
    def loadCSVdata (self):
        '''loads the graph data from csv files'''
        #Mean value Data
        Meancolnames = ['Date','SeaIce', 'NorthAmerica', 'Greenland', 'Europe', 'Asia']
        Meandata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/Mean_extents.csv', names=Meancolnames,header=0)
        self.MSeaIce = Meandata.SeaIce.tolist()
        self.MAmerica = Meandata.NorthAmerica.tolist()
        self.MGreenland = Meandata.Greenland.tolist()
        self.MEurope = Meandata.Europe.tolist()
        self.MAsia = Meandata.Asia.tolist()

        
        #Standard Deviation Data
        Sdeviationcolnames = ['Date','SeaIce', 'NorthAmerica', 'Greenland', 'Europe', 'Asia']
        SDdata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/Standard_Deviations.csv', names=Sdeviationcolnames,header=0)
        self.SD_SeaIce = SDdata.SeaIce.tolist()
        self.SD_America = SDdata.NorthAmerica.tolist()
        self.SD_Greenland = SDdata.Greenland.tolist()
        self.SD_Europe = SDdata.Europe.tolist()
        self.SD_Asia = SDdata.Asia.tolist()
        
        #NRT Data
        NRTcolnames = ['Date','SeaIce', 'NorthAmerica', 'Greenland', 'Europe', 'Asia']
        NRTdata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/NRT_extent_data.csv', names=NRTcolnames,header=0)
        self.NRT_SeaIce = NRTdata.SeaIce.tolist()
        self.NRT_America = NRTdata.NorthAmerica.tolist()
        self.NRT_Greenland = NRTdata.Greenland.tolist()
        self.NRT_Europe = NRTdata.Europe.tolist()
        self.NRT_Asia = NRTdata.Asia.tolist()
                
# =============================================================================
#         self.preyear = 2012
#         
#         #NRT Data last year
#         NRTcolnames = ['Date','SeaIce', 'NorthAmerica', 'Greenland', 'Europe', 'Asia']
#         NRTdata = pandas.read_csv(f'{self.webpath}/Snow_Cover_Data/NRT_extent_data_{}.csv'.format(self.preyear), names=NRTcolnames,header=0)
#         self.Pre_SeaIce = NRTdata.SeaIce.tolist()
#         self.Pre_America = NRTdata.NorthAmerica.tolist()
#         self.Pre_Greenland = NRTdata.Greenland.tolist()
#         self.Pre_Europe = NRTdata.Europe.tolist()
#         self.Pre_Asia = NRTdata.Asia.tolist()
# =============================================================================
        
        
        #for incomplete data
#        self.T2018 = Thicknessdata.C2018.dropna().tolist()


    def automated (self,year,month,day,dayofyear):
        '''function to automate parts of the monthly update procedure'''
        self.year = year
        self.month =str(month).zfill(2)
        self.day = str(day).zfill(2)
        self.dayofyear = dayofyear-1 # removes table header 

            
        self.loadCSVdata()
        self.makeYeargraph()
#        self.makemultiyeargraph()
        self.makemovie()
        
    def makemovie(self):
        from moviepy.editor import ImageSequenceClip
        import os
        filepath = f'{self.webpath}/Snow_Cover_Data/Images/Extent'
        filepath_anom = f'{self.webpath}/Snow_Cover_Data/Images/Anomaly'

            
        clip = ImageSequenceClip(filepath,fps=2)
        clip_anom = ImageSequenceClip(filepath_anom,fps=2)
        
        clip.write_videofile(f'{self.webpath}/Snow_Cover_Data//Snow_map_10days.webm',bitrate="5000000", audio=None,codec="libvpx")
        clip_anom.write_videofile(f'{self.webpath}/Snow_Cover_Data/Snow_map_anomaly_10days.webm',bitrate="5000000", audio=None,codec="libvpx")
        
        clip.close()
        clip_anom.close()
        
        try:
            os.remove('{}/Snow_Cover_Data/Images/Extent/NOAA_Snowmap_normal_{}.png'.format(self.webpath,str(self.dayofyear-10).zfill(3)))
            os.remove('{}/Snow_Cover_Data/Images/Anomaly/NOAA_Snowmap_anomaly_{}.png'.format(self.webpath,str(self.dayofyear-10).zfill(3)))
        except:
            print('cant remove day')



action = ADS_data()
if __name__ == "__main__":
    print('main')
    action.automated(2023,9,99,270)
#    action.makeYeargraph()
#    action.loadCSVdata()
#    action.makeYeargraph()
#    action.makemultiyeargraph()
#     action.makemovie()
