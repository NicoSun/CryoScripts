import numpy as np
import matplotlib.pyplot as plt
import CryoIO


class AWP_analysis_south:

    def __init__ (self):
        self.icenull = np.zeros(104912, dtype=float)
        
        
        final_value_list = [2773,2812,2825,2887,2870,2862,2820,2907,2841,2682,2851,2871,2666,2917,2776,2744,2819,2920,2756,2988,2968,
                            2756,2977,2525,2739,2844,2821,2846,2601,2744,2770,2985,2667,2695,2611,2611,2698,2988,3015,2957,2865,2841,3004]
        final_year_list = [year for year in range(1980,2023)]
        self.final_value_dict = {key:value for (key,value) in zip(final_year_list,final_value_list)}
        self.final_value_dict['icefree'] = 3852
        self.final_value_dict['00_19'] = 2790
        
        # print(self.final_value_dict[1980])
        self.masksload()
        
    def masksload(self):
        
        filename = '../Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)
        
        filename = '../Masks/Max_AWP_extent_south.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        
    def AWP_final(self,icemap,icesum,year):
        '''displays final AWP data'''
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        icemap = np.ma.masked_greater(icemap, 9000)
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.8)
        
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.clear()
        
        ax.set_title('Albedo-Warming Potential',loc='left')
        ax.set_title('Astronomical Summer: {}-{}'.format(year-1,year),loc='right')
        
        ax.set_xlabel('Antarctic Mean: '+str(icesum)+' [MJ / 'r'$m^2$]')
        cax = ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=5000, cmap=cmap)
        fig.colorbar(cax, ticks=[0,1000,2000,3000,4000,5000],shrink=0.95).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]')
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=11,color='black',fontweight='bold')
        ax.text(2, 16, r'AWP Model: Nico Sun', fontsize=11,color='black',fontweight='bold')
        ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.22)
        fig.tight_layout(pad=0.5)
        fig.savefig('AWP/img/pan_Antarctic/Final_{}_south.png'.format(year))
        plt.close()
    
    def AWP_final_anomaly(self,icemap,year,icesum):
        '''displays anomaly AWP data'''

        for x,y in enumerate(self.regmaskf):
            if y > 7:
                icemap[x] = 9999
        
        icemap = np.ma.masked_outside(icemap,-6000,6000) 
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.8)
        
        fig,ax = plt.subplots(figsize=(8, 7))
        ax.clear()
        
        ax.set_title('Albedo-Warming Potential Anomaly',loc='left')
        ax.set_title('Astronomical Summer: {}-{}'.format(year-1,year),loc='right')
        ax.set_xlabel('Pan Antarctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]')
        ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.22)

        cax = ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[-1000,-500,0,500,1000]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
        
        ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=11,color='black',fontweight='bold')
        ax.text(2, 16, r'AWP Model: Nico Sun', fontsize=11,color='black',fontweight='bold')
        ax.text(190, 285,'Anomaly Base: 2000-2019', fontsize=9,color='black',fontweight='bold')
        fig.tight_layout(pad=0.5)
        fig.savefig('AWP/img/pan_Antarctic/AWP_anom_{}_south.png'.format(year))
        plt.close()
        
    def AWP_percentshow(self,icemap,year,icesum):
        '''displays AWP data'''
        for x,y in enumerate(self.regmaskf):
            if y > 7:
                icemap[x] = 9999
        
        icemap = np.ma.masked_outside(icemap,-6000,6000) 
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        cmap = plt.cm.Blues
        cmap.set_bad('black',0.8)
        
        icemap = icemap*100
        
        fig,ax = plt.subplots(figsize=(8, 7))
        ax.clear()
        
        
        ax.set_title('Albedo-Warming Potential (percent of max): {}-{}'.format(year-1,year),x=0.5)
        ax.set_xlabel('Pan Antarctic Mean: '+str(icesum)+' %',)
        ax.set_ylabel('cryospherecomputing.com/awp-south',y=0.22)
        
        cax = ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[0,25,50,75,100]).set_label('percent of permanent icefree conditions')
        
        ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
        fig.tight_layout(pad=0.5)

        fig.savefig('AWP/img/pan_Antarctic/AWP_percent_{}_south.png'.format(year))
        plt.close()
        
        
    def AWP_final_show(self):
        yearlist = [year for year in range(1980,2023)]
        
        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}_south.npz'
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
                filename = f'AWP/final_data/AWP_energy_{year}_south.npz'
                file = CryoIO.readnumpy(filename)
                icemean += file/20
                
            CryoIO.savenumpy(filename_mean, icemean)
            return icemean
    
    def calcanomaly(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icemean = self.load_mean_AWP()

        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}_south.npz'
            file = CryoIO.readnumpy(filename)
            iceanomaly = file - icemean
            anom_value = self.final_value_dict[value] - self.final_value_dict['00_19']
            
            self.AWP_final_anomaly(iceanomaly,value,anom_value)
#        plt.show()
            
    def AWP_calpercentage(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icelist = []
        
        noIcemap = CryoIO.readnumpy('AWP/final_data/AWP_energy_icefree_south.npz')
        
        for value in (yearlist):
            filename = f'AWP/final_data/AWP_energy_{value}_south.npz'
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
            

action = AWP_analysis_south()

if __name__ == '__main__':
    # action.AWP_final_show()
    # action.calcanomaly(1980,2023)
    action.AWP_calpercentage(1980,2023)
    # plt.show()
