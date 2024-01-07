import numpy as np
import matplotlib.pyplot as plt
import CryoIO


class AWP_analysis_south:

    def __init__ (self):
        self.icenull = np.zeros(104912, dtype=float)
        
        
        final_value_list = [2013,2570,2708,2117,2853,2389,2654,2405,3574,2343,2171,2362,2420,3496,2255,2269,
                            3054,2614,2330,3010,3214,2030,3412,2227,3043,2869,2983,3000,2893,3588,2884,3702,
                            3292,2537,2928,3522,3209,2966,3091,3108,2679,3692,3885]
        final_year_list = [year for year in range(1980,2023)]
        self.final_value_dict = {key:value for (key,value) in zip(final_year_list,final_value_list)}
        self.final_value_dict['00_19'] = 3025
        
        # print(self.final_value_dict[1980])
        self.masksload()
        
    def masksload(self):
        
        filename = '../Masks/region_s_pure.msk'
        self.regmaskf = CryoIO.openfile(filename,np.uint8)
        
        filename = '../Masks/Max_AWP_extent_south.bin'
        self.Icemask = CryoIO.openfile(filename,np.uint8)
        
        
    def AWP_final(self,icemap,icesum,year):
        '''displays final AWP data'''
        
        for x,y in enumerate(self.regmaskf):
            if y > 7:
                icemap[x] = 999999
        
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        oceanmap = np.ma.masked_not_equal(icemap,0)
        icemap = np.ma.masked_greater(icemap/1000, 900)
        
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.clear()
        
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.8)
        
        ax.set_title('Ice Melt AWP',loc='left')
        ax.set_title('Astronomical Summer: {}-{}'.format(year-1,year),loc='right')
        
        maxvalue = 500
        
        ax.set_xlabel('Antarctic Sum: '+str(icesum)+' YJ')
        cax = ax.imshow(icemap, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=cmap)
        ax.imshow(oceanmap, interpolation='nearest', vmin=-1, vmax=2, cmap='Greys')
        fig.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,0.5*maxvalue,maxvalue]).set_label('Ice Melt AWP in ZJ')
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=11,color='black',fontweight='bold')
        ax.text(2, 16, r'AWP Model: Nico Sun', fontsize=11,color='black',fontweight='bold')
        ax.set_ylabel('cryospherecomputing.com/melt-awp-south',y=0.25)
        fig.tight_layout(pad=0.5)
        fig.savefig('Melt_AWP/img/pan_Antarctic/Melt_Final_{}_south.png'.format(year))
        plt.close()
    
    def AWP_final_anomaly(self,icemap,year,icesum):
        '''displays anomaly AWP data'''

        for x,y in enumerate(self.regmaskf):
            if y > 7:
                icemap[x] = -1
        
        icemap = np.ma.masked_equal(icemap,-1) 
        icemap = icemap.reshape(332, 316)
        icemap = icemap[10:300,30:310]
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.8)
        
        fig,ax = plt.subplots(figsize=(8, 7))
        ax.clear()
        
        ax.set_title('Ice Melt AWP (Anomaly): {}-{}'.format(year-1,year),x=0.5)
        ax.set_xlabel('Pan Antarctic Anomaly: {} EJ'.format(icesum))
        ax.set_ylabel('cryospherecomputing.com/melt-awp-south',y=0.25)

        maxvalue = 500
        

        cax = ax.imshow(icemap/1000, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,maxvalue*0.5,maxvalue]).set_label('Ice Melt AWP (Anomaly) in ZJ')
        
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=11,color='black',fontweight='bold')
        ax.text(2, 16, r'AWP Model: Nico Sun', fontsize=11,color='black',fontweight='bold')
        ax.text(190, 285,'Anomaly Base: 2000-2019', fontsize=9,color='black',fontweight='bold')
        fig.tight_layout(pad=0.5)
        fig.savefig('Melt_AWP/img/pan_Antarctic/Melt_anom_{}_south.png'.format(year))
        plt.close()
        
        
        
    def AWP_final_show(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        
        for value in (yearlist):
            filename = f'Melt_AWP/final_data/Melt_AWP_energy_{value}_south.npz'
            file = CryoIO.readnumpy(filename)
            self.AWP_final(file,self.final_value_dict[value],value)
    
    
    def load_mean_AWP(self):
        filename_mean = f'Melt_AWP/final_data/Melt_AWP_energy_Mean_south.npz'
        try:
            file = CryoIO.readnumpy(filename_mean)
            return file
        except:
            icemean = self.icenull
            for year in range(2000,2020):
                filename = f'Melt_AWP/final_data/Melt_AWP_energy_{year}_south.npz'
                file = CryoIO.readnumpy(filename)
                icemean += file/20
                
            CryoIO.savenumpy(filename_mean, icemean)
            return icemean
    
    def calcanomaly(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icemean = self.load_mean_AWP()

        for value in (yearlist):
            filename = f'Melt_AWP/final_data/Melt_AWP_energy_{value}_south.npz'
            file = CryoIO.readnumpy(filename)
            iceanomaly = file - icemean
            anom_value = self.final_value_dict[value] - self.final_value_dict['00_19']
            
            self.AWP_final_anomaly(iceanomaly,value,anom_value)
#        plt.show()


action = AWP_analysis_south()

if __name__ == '__main__':
    # action.AWP_final_show(1980,2023)
    action.calcanomaly(2022,2023)
    # plt.show()
