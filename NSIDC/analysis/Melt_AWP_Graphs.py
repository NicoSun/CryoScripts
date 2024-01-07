import numpy as np
import matplotlib.pyplot as plt
import CryoIO


class AWP_analysis:

    def __init__ (self):
        
        self.icenull = np.zeros(136192, dtype=float)
        
        
        final_value_list = [-803.8,-645.8,-279.4,-884.8,-557.0,-547.6,-319.9,-715.0,-461.8,-432.2,-574.6,-33.2,-235.1,-372.0,195.2,
                            -135.1,71.1,-495.3,-92.1,386.6,369.5,460.0,178.6,184.7,518.9,59.5,319.9,465.6,1103.3,857.8,487.0,955.2,
                            911.1,1418.2,789.0,586.7,1026.4,1176.1,717.9,701.2,1105.2,1156.9,1088.5,1119.4]
        final_year_list = [year for year in range(1979,2023)]
        self.final_value_dict = {key:value for (key,value) in zip(final_year_list,final_value_list)}
        self.final_value_dict['00_19'] = 701
        
        # print(self.final_value_dict[1980])
        self.masksload()
        
    def masksload(self):
        
        filename = '../Masks/Arctic_region_mask.bin'
        self.regmaskf = CryoIO.openfile(filename,np.uint32)
        
            
    def IceMelt_final(self,icemap,icesum,year):
        '''displays melt AWP data'''
        
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        oceanmap = np.ma.masked_not_equal(icemap,0)
        
        icemap = np.ma.masked_equal(icemap, -1)
        cmap2 = plt.cm.coolwarm
        cmap2.set_bad('black',0.8)

        
        fig2, ax2 = plt.subplots(figsize=(7.2, 9))
        ax2.clear()
        ax2.set_title('Ice Melt AWP',loc='left')
        ax2.set_title('Astronomical Summer '+str(year),loc='right')
        
        maxvalue = 500

#        "{:,}".format(value)
        ax2.set_xlabel('Arctic Sum: {:,} [EJ]'.format(icesum))
        cax = ax2.imshow(icemap/1000, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=cmap2)
        ax2.imshow(oceanmap, interpolation='nearest', vmin=-1, vmax=2, cmap='Greys')
        fig2.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,0.5*maxvalue,maxvalue]).set_label('Ice Melt AWP in ZJ')
        
        ax2.axes.get_yaxis().set_ticks([])
        ax2.axes.get_xaxis().set_ticks([])
        ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
        ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax2.set_ylabel('cryospherecomputing.com/melt-awp',y=0.15)
        fig2.tight_layout(pad=0.5)
        fig2.savefig('Melt_AWP/img/pan_Arctic/AWP_melt_{}.png'.format(year))
        plt.close()
        
    def IceMelt_final_anomaly(self,icemap,year,icesum):
        '''displays anomaly AWP data'''
        cmap = plt.cm.coolwarm
        cmap.set_bad('black',0.66)
        
        for x,y in enumerate(self.regmaskf):
            if y > 15:
                icemap[x] = -1
        
        icemap = np.ma.masked_equal(icemap,-1) 
        icemap = icemap.reshape(448, 304)
        icemap = icemap[50:430,20:260]
        fig = plt.figure(figsize=(7, 9))
        ax = fig.add_subplot(111)
        
        maxvalue = 333
        ax.set_title('Ice Melt AWP (Anomaly): {}'.format(year),x=0.5)

        cax = ax.imshow(icemap/1000, interpolation='nearest', vmin=-maxvalue, vmax=maxvalue, cmap=cmap)
        cbar = fig.colorbar(cax, ticks=[-maxvalue,-maxvalue*0.5,0,maxvalue*0.5,maxvalue]).set_label('Ice Melt AWP (Anomaly) in ZJ')
        
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])
        ax.set_xlabel('Pan Arctic Anomaly: {} EJ'.format(icesum))
        ax.set_ylabel('cryospherecomputing.com/melt-awp',y=0.15)
        ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        ax.text(155, 375,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
        fig.tight_layout(pad=0.5)
        fig.savefig('Melt_AWP/img/pan_Arctic/AWP_anom_{}.png'.format(year))
        plt.close()
        
        
    def final_Ice_melt(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        for value in yearlist:
            filename = f'Melt_AWP/final_data/Melt_AWP_energy_{value}.npz'
            file = CryoIO.readnumpy(filename)
            self.IceMelt_final(file,self.final_value_dict[value],value)
            
    def load_mean_AWP(self):
        filename_mean = f'Melt_AWP/final_data/Melt_AWP_energy_Mean.npz'
        try:
            file = CryoIO.readnumpy(filename_mean)
            return file
        except:
            icemean = self.icenull
            for year in range(2000,2020):
                filename = f'Melt_AWP/final_data/Melt_AWP_energy_{year}.npz'
                file = CryoIO.readnumpy(filename)
                icemean += file/20
                
            CryoIO.savenumpy(filename_mean, icemean)
            return icemean

            
    def final_Ice_melt_anomaly(self,startyar,endyear):
        yearlist = [year for year in range(startyar,endyear)]
        icemean = self.load_mean_AWP()

        for value in (yearlist):
            filename = f'Melt_AWP/final_data/Melt_AWP_energy_{value}.npz'
            file = CryoIO.readnumpy(filename)
            iceanomaly = file - icemean
            anom_value = self.final_value_dict[value] - self.final_value_dict['00_19']
            
            self.IceMelt_final_anomaly(iceanomaly,value,anom_value)


action = AWP_analysis()

if __name__ == '__main__':
    # action.final_Ice_melt(1979,2023)
    action.final_Ice_melt_anomaly(1979,2023)
    # plt.show()
