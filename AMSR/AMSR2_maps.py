import matplotlib.pyplot as plt
import numpy as np
import copy

class AMSR2_maps:

	def __init__  (self):
		self.image_init()
		
	def normalshow(self,icemap,hemi,datestring,icesum=0):
		'''displays sea ice data'''
		icesum = round(icesum,3)
		icesum = '{0:.3f}'.format(icesum)
		
		cmap = copy.copy(plt.cm.get_cmap("jet"))
		cmap.set_bad('black',0.6)
		icemap = np.ma.masked_greater(icemap, 100)
		
		self.ax.clear()
# 		self.ax.set_title(f'Date: {datestring}')
		self.ax.text(0.8, 0.98, f'Date: {datestring}',
        transform=self.ax.transAxes,color='white', fontsize=12,fontweight='bold')
# 		self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
		cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
		
# 		cbar = self.fig.colorbar(cax, ticks=[0,25,50,75,100],shrink=0.85).set_label('Sea Ice concentration in %')
		
		self.ax.axis('off')
		self.ax.text(6, 33, r'Data: AWI AMSR2', fontsize=11,color='white',fontweight='bold')
		self.ax.text(6, 66, r'Map: Nico Sun', fontsize=11,color='white',fontweight='bold')
		self.ax.text(0.01, 0.01, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='white', fontsize=12,fontweight='bold')
		self.fig.tight_layout()
# 		self.fig.subplots_adjust(left=0.05)
# 		self.fig.savefig(f'/home/nico/Cryoweb/AMSR/AMSR2_{hemi}-1.png',bbox_inches='tight')
		plt.pause(0.01)
		plt.show()
		
		fig, ax = plt.subplots(figsize=(14, 14))
	
	def anomalyshow(self,icemap,icesum):
		'''creates separate figures for sea ice data'''
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		icesum = round(icesum,3)
		icesum = '{0:.3f}'.format(icesum)
		
		self.ax2.clear()
		self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))		
		cmap2 = copy.copy(plt.cm.get_cmap("coolwarm_r"))
		cmap2.set_bad('black',0.6)
		
		self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
		cax = self.ax2.imshow(icemap*100, interpolation='nearest', vmin=-75, vmax=75, cmap=cmap2)
		
		cbar = self.fig2.colorbar(cax, ticks=[-75,-50,-25,0,25,50,75],shrink=0.85).set_label('Sea Ice concentration anomaly in %')
		
		self.ax2.axis('off')
		self.ax2.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 16, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(165, 346,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
		self.fig2.savefig('/home/nico/Cryoweb/NSIDC_Area/Arctic_anom-1.png')
		plt.pause(0.01)
	
		
	def image_init(self):
		'''creates separate figures for sea ice data'''
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
# 		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))




action = AMSR2_maps()
if __name__ == "__main__":
	print('main')
# 	action.normalshow() #note substract xxx days from last available day

	

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
