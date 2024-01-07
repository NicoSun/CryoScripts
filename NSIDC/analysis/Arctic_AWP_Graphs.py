import numpy as np
import matplotlib.pyplot as plt
import CryoIO


class AWP_analysis:

    def __init__ (self):
        self.icenull = np.zeros(136192, dtype=float)
        
        
        final_value_list = [1698,1713,1751,1672,1694,1735,1738,1732,1716,1762,1761,1849,1776,1738,1828,1765,1875,1758,1834,1838,1810,1846,
                      1829,1855,1882,1862,1918,1951,2003,1936,1894,1983,2010,2021,1925,1944,1984,2047,1989,1980,2055,2054,2000,1964]
        final_year_list = [year for year in range(1979,2023)]
        self.final_value_dict = {key:value for (key,value) in zip(final_year_list,final_value_list)}
        self.final_value_dict['icefree'] = 3259
        self.final_value_dict['00_19'] = 1946
        
        # print(self.final_value_dict[1980])
        self.masksload()
        
    def masksload(self):
        
        filename = '../Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)
        
        filename = '../Masks/Max_AWP_extent.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        
    def AWP_final(self,icemap,icesum,year):
        '''displays cumulative AWP data'''
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        icemap = np.ma.masked_greater(icemap, 9000)
        cmap2 = plt.cm.coolwarm
        cmap2.set_bad('black',0.8)
        
        fig2, ax2 = plt.subplots(figsize=(7.5, 9))
        ax2.clear()
        ax2.set_title('Albedo-Warming Potential',loc='left')
        ax2.set_title('Astronomical Summer '+str(year),loc='right')
#        ax2.set_title('Astronomical Summer without ice',loc='right')
        
        ax2.set_xlabel('Arctic Mean: '+str(icesum)+' [MJ / 'r'$m^2$]',)
        cax = ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=5000, cmap=cmap2)
        fig2.colorbar(cax, ticks=[0,1000,2000,3000,4000,5000]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]',)
        
        ax2.axes.get_yaxis().set_ticks([])
        ax2.axes.get_xaxis().set_ticks([])
        ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax2.set_ylabel('cryospherecomputing.com/awp',y=0.133)
        fig2.tight_layout(pad=0.5)
        fig2.savefig('AWP/img/pan_Arctic/Final_{}.png'.format(year))
        plt.close()
    
    def AWP_final_anomaly(self,icemap,year,icesum):
        '''displays anomaly AWP data'''
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.66)
        
        for x,y in enumerate(self.regmaskf):
            if y > 15:
                icemap[x] = 9999
        
        icemap = np.ma.masked_outside(icemap,-5000,5000) 
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        fig = plt.figure(figsize=(7, 9))
        ax = fig.add_subplot(111)

        cax = ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[-1000,-500,0,500,1000]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        
        ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.set_xlabel('Pan Arctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]',)
        ax.set_ylabel('cryospherecomputing.com/awp',y=0.133)
        ax.set_title('Albedo-Warming Potential Anomaly: {}'.format(year),x=0.5)
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.text(155, 375,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
        fig.tight_layout(pad=0.5)
        fig.savefig('AWP/img/pan_Arctic/AWP_anom_{}.png'.format(year))
        plt.close()
        
    def AWP_percentshow(self,icemap,year,icesum):
        '''displays anomaly AWP data'''
        cmap = plt.cm.Blues
        cmap.set_bad('black',0.66)
        
        for x,y in enumerate(self.regmaskf):
            if y > 15:
                icemap[x] = 9999
        
        icemap = icemap*100
        icemap = np.ma.masked_outside(icemap,-5000,5000) 
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        fig = plt.figure(figsize=(7, 9))
        ax = fig.add_subplot(111)

        cax = ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[0,25,50,75,100]).set_label('percent of permanent icefree conditions')
        
        ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.set_xlabel('Pan Arctic Mean: '+str(icesum)+' %',)
        ax.set_ylabel('cryospherecomputing.com/awp',y=0.133)
        ax.set_title('Albedo-Warming Potential (percent of max): {}'.format(year),x=0.5)
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        fig.tight_layout(pad=0.5)

        fig.savefig('AWP/img/pan_Arctic/AWP_percent_{}.png'.format(year))
        plt.close()
        
        
    def AWP_final_show(self):
        yearlist = [year for year in range(1979,1982)]
        
        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}.npz'
            file = CryoIO.readnumpy(filename)
            self.AWP_final(file,self.final_value_dict[value],value)
    
    
    def load_mean_AWP(self):
        filename_mean = f'AWP/final_data/AWP_energy_Mean.npz'
        try:
            file = CryoIO.readnumpy(filename_mean)
            return file
        except:
            icemean = self.icenull
            for year in range(2000,2020):
                filename = f'AWP/final_data/AWP_energy_{year}.npz'
                file = CryoIO.readnumpy(filename)
                icemean += file/20
                
            CryoIO.savenumpy(filename_mean, icemean)
            return icemean
    
    def calcanomaly(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icemean = self.load_mean_AWP()

        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}.npz'
            file = CryoIO.readnumpy(filename)
            iceanomaly = file - icemean
            anom_value = self.final_value_dict[value] - self.final_value_dict['00_19']
            
            self.AWP_final_anomaly(iceanomaly,value,anom_value)
#        plt.show()
            
    def AWP_calpercentage(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icelist = []
        
        noIcemap = CryoIO.readnumpy('AWP/final_data/AWP_energy_icefree.npz')
        
        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}.npz'
            file = CryoIO.readnumpy(filename)
            icelist.append(file)
                
        year = startyar
        for icemap in icelist:
            Mean_percent = []
            icepercent = icemap / noIcemap
            for x,y in enumerate(self.Icemask):
                if y ==1:
                    Mean_percent.append(icepercent[x])
            
            self.AWP_percentshow(icepercent,year,round(np.mean(Mean_percent)*100,1))
            year +=1
#        plt.show()
            

action = AWP_analysis()

if __name__ == '__main__':
    action.AWP_final_show()
    # action.calcanomaly(1979,2023)
    # action.AWP_calpercentage(1979,2023)
#    plt.show()
