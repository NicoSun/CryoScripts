import matplotlib.pyplot as plt
import numpy as np
import copy

class AMSR2_maps:

    def __init__  (self):
        self.image_init()
        self.webpath = '/var/www/Cryoweb'
        
    def normalshow(self,icemap,hemi,datestring,icesum=0):
        '''displays sea ice data'''
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        cmap = copy.copy(plt.cm.get_cmap("jet"))
        cmap.set_bad('black',0.6)
        icemap = np.ma.masked_greater(icemap, 100)
        
        self.ax.clear()
#         self.ax.set_title(f'Date: {datestring}')
        self.ax.text(0.8, 0.98, f'Date: {datestring}',
        transform=self.ax.transAxes,color='white', fontsize=12,fontweight='bold')
#         self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
        cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
        
#         cbar = self.fig.colorbar(cax, ticks=[0,25,50,75,100],shrink=0.85).set_label('Sea Ice concentration in %')
        
        self.ax.axis('off')
        self.ax.text(6, 33, r'Data: AWI AMSR2', fontsize=11,color='white',fontweight='bold')
        self.ax.text(6, 66, r'Map: Nico Sun', fontsize=11,color='white',fontweight='bold')
        self.ax.text(0.01, 0.01, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='white', fontsize=12,fontweight='bold')
        self.fig.tight_layout()
#         self.fig.subplots_adjust(left=0.05)
        self.fig.savefig(f'{self.webpath}/AMSR/AMSR2_{hemi}-1.png',bbox_inches='tight')
        # plt.pause(0.01)
        # plt.show()
        
    
    def anomalyshow(self,icemap,hemi,datestring,icesum=0):
        '''creates separate figures for sea ice data'''
        icesum = round(icesum,3)
        icesum = '{0:.3f}'.format(icesum)
        
        icemap = np.ma.masked_greater(icemap,100)
        
        self.ax2.clear()
        self.ax2.text(0.75, 0.98, f'Date: {datestring}',
        transform=self.ax2.transAxes,color='white', fontsize=12,fontweight='bold')
        
        cmap2 = copy.copy(plt.cm.get_cmap("coolwarm_r"))
        cmap2.set_bad('black',0.6)
        
        # self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
        cax2 = self.ax2.imshow(icemap, interpolation='nearest', vmin=-75, vmax=75, cmap=cmap2)
        
        # cbar = self.fig2.colorbar(cax2, ticks=[-75,-50,-25,0,25,50,75],shrink=0.85).set_label('Sea Ice concentration anomaly in %')
        
        self.ax2.axis('off')
        self.ax2.text(6, 33, r'Data: AWI AMSR2', fontsize=10,color='black',fontweight='bold')
        self.ax2.text(6, 66, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
        # self.ax2.text(165, 346,r'Anomaly Base: 2012-2019', fontsize=8,color='black',fontweight='bold')
        self.ax2.text(0.01, 0.01, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='black', fontsize=12,fontweight='bold')
        self.fig2.tight_layout()
        # self.fig2.subplots_adjust(left=0.05)
        self.fig2.savefig(f'{self.webpath}/AMSR/AMSR2_{hemi}_anom-1.png',bbox_inches='tight')
        # plt.pause(0.01)
        # plt.show()
    
        
    def image_init(self):
        '''creates separate figures for sea ice data'''
        self.fig, self.ax = plt.subplots(figsize=(14, 14))
        self.fig2, self.ax2 = plt.subplots(figsize=(14, 14))




action = AMSR2_maps()
if __name__ == "__main__":
    print('main')
#     action.normalshow() #note substract xxx days from last available day

    

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

#Regionmask:
0: lakes
1: Ocean
2: Sea of Okothsk
3: Bering Sea
4: Hudson bay
5: St Lawrence
6: Baffin Bay
7: Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Achipelago
15: Central Arctic
20: Land
21: Coast
'''
