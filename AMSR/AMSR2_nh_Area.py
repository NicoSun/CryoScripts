import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import copy
import CryoIO


class NSIDC_area:

	def __init__  (self):
		self.year = 2021
		self.month = 1
		self.day = 1
		
		self.daycount = 1 #366year, 186summer
		
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		self.CSVCompaction = ['Compaction']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.SoO_area = ['Sea of Okhotsk']
		self.Bers_area = ['Bering Sea']
		self.HB_area = ['Hudson Bay']
		self.BB_area = ['Baffin Bay']
		self.EG_area = ['East Greenland Sea']
		self.BaS_area = ['Barents Sea']
		self.KS_area = ['Kara Sea']
		self.LS_area = ['Laptev Sea']
		self.ES_area = ['East Siberian Sea']
		self.CS_area = ['Chukchi Sea']
		self.BeaS_area = ['Beaufort Sea']
		self.CA_area = ['Canadian Archipelago']
		self.AB_area = ['Central Arctic']
		self.CSVArea_High = ['High Arctic Area']
		
		self.SoO_extent = ['Sea of Okhotsk']
		self.Bers_extent = ['Bering Sea']
		self.HB_extent = ['Hudson Bay']
		self.BB_extent = ['Baffin Bay']
		self.EG_extent = ['East Greenland Sea']
		self.BaS_extent = ['Barents Sea']
		self.KS_extent = ['Kara Sea']
		self.LS_extent = ['Laptev Sea']
		self.ES_extent = ['East Siberian Sea']
		self.CS_extent = ['Chukchi Sea']
		self.BeaS_extent = ['Beaufort Sea']
		self.CA_extent = ['Canadian Archipelago']
		self.AB_extent = ['Central Arctic']
		self.CSVExtent_High = ['High Arctic Extent']
		
		self.plottype = 'both' #normal, anomaly, both
		self.masksload()
		self.initRegions()
		self.normalandanomaly()
		
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		filename = '/home/nico/cryodata/AMSR/Masks/AMSR2_land_nh.dat'
		self.landmask = CryoIO.openfile(filename,np.uint8)
		
		filename = '/home/nico/cryodata/AMSR/Masks/AMSR2_latitude_nh.dat'
		self.latmask = CryoIO.openfile(filename,np.uint8)
		
		filename = '/home/nico/cryodata/AMSR/Masks/AMSR2_longitude_nh.dat'
		self.lonmask = CryoIO.openfile(filename,np.int8)

		self.maskview(self.lonmask)
		plt.show()

	def initRegions(self):		
		self.SoO = []
		self.Bers = [] 
		self.HB = []
		self.BB = []
		self.EG = []
		self.BaS = []
		self.KS = []
		self.LS = []
		self.ES = []
		self.CS = []
		self.BeaS = []
		self.CA = []
		self.AB = []
		
		self.SoO_ext = []
		self.Bers_ext = [] 
		self.HB_ext = []
		self.BB_ext = []
		self.EG_ext = []
		self.BaS_ext = []
		self.KS_ext = []
		self.LS_ext = []
		self.ES_ext = []
		self.CS_ext = []
		self.BeaS_ext = []
		self.CA_ext = []
		self.AB_ext = []
		
	def appendregion(self):
		self.SoO_area.append(int(np.sum(self.SoO))/1e6)
		self.Bers_area.append(int(np.sum(self.Bers))/1e6)
		self.HB_area.append(int(np.sum(self.HB))/1e6)
		self.BB_area.append(int(np.sum(self.BB))/1e6)
		self.EG_area.append(int(np.sum(self.EG))/1e6)
		self.BaS_area.append(int(np.sum(self.BaS))/1e6)
		self.KS_area.append(int(np.sum(self.KS))/1e6)
		self.LS_area.append(int(np.sum(self.LS))/1e6)
		self.ES_area.append(int(np.sum(self.ES))/1e6)
		self.CS_area.append(int(np.sum(self.CS))/1e6)
		self.BeaS_area.append(int(np.sum(self.BeaS))/1e6)
		self.CA_area.append(int(np.sum(self.CA))/1e6)
		self.AB_area.append(int(np.sum(self.AB))/1e6)
		
		High_Arctic = self.AB_area[-1]+self.CA_area[-1]+self.BeaS_area[-1]+self.CS_area[-1]+ self.ES_area[-1]+self.LS_area[-1]+self.KS_area[-1]
		self.CSVArea_High.append(round(High_Arctic,3))
		
		self.SoO_extent.append(int(np.sum(self.SoO_ext))/1e6)
		self.Bers_extent.append(int(np.sum(self.Bers_ext))/1e6)
		self.HB_extent.append(int(np.sum(self.HB_ext))/1e6)
		self.BB_extent.append(int(np.sum(self.BB_ext))/1e6)
		self.EG_extent.append(int(np.sum(self.EG_ext))/1e6)
		self.BaS_extent.append(int(np.sum(self.BaS_ext))/1e6)
		self.KS_extent.append(int(np.sum(self.KS_ext))/1e6)
		self.LS_extent.append(int(np.sum(self.LS_ext))/1e6)
		self.ES_extent.append(int(np.sum(self.ES_ext))/1e6)
		self.CS_extent.append(int(np.sum(self.CS_ext))/1e6)
		self.BeaS_extent.append(int(np.sum(self.BeaS_ext))/1e6)
		self.CA_extent.append(int(np.sum(self.CA_ext))/1e6)
		self.AB_extent.append(int(np.sum(self.AB_ext))/1e6)
		
		High_Arctic_extent = self.AB_extent[-1]+self.CA_extent[-1]+self.BeaS_extent[-1]+self.CS_extent[-1]+ self.ES_extent[-1]+self.LS_extent[-1]+self.KS_extent[-1]
		self.CSVExtent_High.append(round(High_Arctic_extent,3))
		self.initRegions()
		
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		filepath = '/home/nico/Cryoscripts/NSIDC/DataFiles/'
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'Mean_00_19/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)	
			print(filename)
			
			#loads data file
			ice = CryoIO.openfile(os.path.join(filepath,filename),np.uint8)/250
				
			# loads the mean data file
			iceaveragef = CryoIO.openfile(os.path.join(filepath,filenameMean),np.uint8)/250
		
			#area & extent calculation
			aaa = np.vectorize(self.calculateAreaExtent)
			icemap_new,icemapanomaly,area,extent,areaanomaly = aaa(ice,iceaveragef,self.areamaskf,self.regmaskf)
			
			compaction = (np.sum(area)/np.sum(extent))*100
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			self.CSVArea.append((np.sum(area))/1e6)
			self.CSVExtent.append (np.sum(extent)/1e6)
			self.CSVCompaction.append(round(compaction,3))
			
			self.appendregion()
			
			area_anom = np.sum(areaanomaly)/1e6

			if count == (self.daycount-1):
				self.normalshow(icemap_new,self.CSVArea[-1])
				self.anomalyshow(icemapanomaly,area_anom)
# =============================================================================
# 					plt.close()
# 					plt.close()
# =============================================================================
			
			count += 1
			if count < self.daycount:
				self.datecalc()
				
				
	def datecalc(self):
		''' calculates the day-month for a 366 day year'''
		self.day += 1
		if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
			self.day=1
			self.month += 1
		elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
			self.day=1
			self.month = self.month+1
		elif self.day==30 and self.month==2:
			self.day=1
			self.month += 1
		elif  self.day==32 and self.month == 12:
			self.day = 1
			self.month = 1
			self.year = self.year+1
					
	def calculateAreaExtent(self,icemap,iceMean,areamask,regionmask):
		'''area & extent calculation & remove lake ice'''
		area = 0
		extent = 0
		icemap_new = icemap
		icemapanomaly = icemap - iceMean
		areaanomaly = 0
		
		if regionmask < 2:
			icemap_new = 0.0
			icemapanomaly = 0.0
		if 1 < regionmask < 16:
			if icemap == 1.02: #value for missing data
				icemap = iceMean
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
				if regionmask == 2:
					self.SoO.append (area)
					self.SoO_ext.append (areamask)
				elif regionmask == 3:
					self.Bers.append (area)
					self.Bers_ext.append (areamask)
				elif regionmask == 4:
					self.HB.append (area)
					self.HB_ext.append (areamask)
				elif regionmask == 6:
					self.BB.append (area)
					self.BB_ext.append (areamask)
				elif regionmask == 7:
					self.EG.append (area)
					self.EG_ext.append (areamask)
				elif regionmask == 8:
					self.BaS.append (area)
					self.BaS_ext.append (areamask)
				elif regionmask == 9:
					self.KS.append (area)
					self.KS_ext.append (areamask)
				elif regionmask == 10:
					self.LS.append (area)
					self.LS_ext.append (areamask)
				elif regionmask == 11:
					self.ES.append (area)
					self.ES_ext.append (areamask)
				elif regionmask == 12:
					self.CS.append (area)
					self.CS_ext.append (areamask)
				elif regionmask == 13:
					self.BeaS.append (area)
					self.BeaS_ext.append (areamask)
				elif regionmask == 14:
					self.CA.append (area)
					self.CA_ext.append (areamask)
				elif regionmask == 15:
					self.AB.append (area)
					self.AB_ext.append (areamask)
		if regionmask > 16: #Land mask
			icemapanomaly = 5
		if icemap <=1 and icemapanomaly <=1: #cheap anomaly calculation
				areaanomaly = icemapanomaly*areamask
				
		return icemap_new,icemapanomaly,area,extent,areaanomaly
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(3300, 2100)
		plt.imshow(icemap, interpolation='nearest', vmin=-180, vmax=180, cmap=plt.cm.jet)


	def normalshow(self,icemap,icesum):
		'''displays sea ice data'''
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		icesum = round(icesum,3)
		icesum = '{0:.3f}'.format(icesum)
		
		cmap = copy.copy(plt.cm.get_cmap("jet"))
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Minimum of Minima')
		self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
		cax = self.ax.imshow(icemap*100, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
		
		cbar = self.fig.colorbar(cax, ticks=[0,25,50,75,100],shrink=0.85).set_label('Sea Ice concentration in %')
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 16, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		self.fig.savefig('/home/nico/Cryoweb/NSIDC_Area/Arctic-1.png')
		plt.pause(0.01)
	
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
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 16, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(165, 346,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.03, 'cryospherecomputing.com',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
		self.fig2.savefig('/home/nico/Cryoweb/NSIDC_Area/Arctic_anom-1.png')
		plt.pause(0.01)
	
		
	def normalandanomaly(self):
		'''creates separate figures for sea ice data'''
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))

	def loadCSVdata (self,deletion):
		#NRT Data
		Yearcolnames = ['Date', 'B', 'C','D','E','F']
		Yeardata = pd.read_csv('/home/nico/Cryoweb/NSIDC_Area/Data/Arctic_NSIDC_Area_NRT.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()[:-deletion]
		self.CSVArea = Yeardata.B.tolist()[:-deletion]
		self.CSVExtent = Yeardata.C.tolist()[:-deletion]
		self.CSVCompaction = Yeardata.D.tolist()[:-deletion]
		self.CSVArea_High = Yeardata.E.tolist()[:-deletion]
		self.CSVExtent_High = Yeardata.F.tolist()[:-deletion]
		
	def loadCSVRegiondata (self,deletion):
		Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata = pd.read_csv('/home/nico/Cryoweb/NSIDC_Area/Data/Regional_NRT.csv', names=Yearcolnames)
		self.SoO_area = Yeardata.Sea_of_Okhotsk.tolist()[:-deletion]
		self.Bers_area = Yeardata.Bering_Sea.tolist()[:-deletion]
		self.HB_area = Yeardata.Hudson_Bay.tolist()[:-deletion]
		self.BB_area = Yeardata.Baffin_Bay.tolist()[:-deletion]
		self.EG_area = Yeardata.East_Greenland_Sea.tolist()[:-deletion]
		self.BaS_area = Yeardata.Barents_Sea.tolist()[:-deletion]
		self.KS_area = Yeardata.Kara_Sea.tolist()[:-deletion]
		self.LS_area = Yeardata.Laptev_Sea.tolist()[:-deletion]
		self.ES_area = Yeardata.East_Siberian_Sea.tolist()[:-deletion]
		self.CS_area = Yeardata.Chukchi_Sea.tolist()[:-deletion]
		self.BeaS_area = Yeardata.Beaufort_Sea.tolist()[:-deletion]
		self.CA_area = Yeardata.Canadian_Archipelago.tolist()[:-deletion]
		self.AB_area = Yeardata.Central_Arctic.tolist()[:-deletion]
		
		Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata_ext = pd.read_csv('/home/nico/Cryoweb/NSIDC_Area/Data/Regional_NRT_extent.csv', names=Yearcolnames)
		self.SoO_extent = Yeardata_ext.Sea_of_Okhotsk.tolist()[:-deletion]
		self.Bers_extent = Yeardata_ext.Bering_Sea.tolist()[:-deletion]
		self.HB_extent = Yeardata_ext.Hudson_Bay.tolist()[:-deletion]
		self.BB_extent = Yeardata_ext.Baffin_Bay.tolist()[:-deletion]
		self.EG_extent = Yeardata_ext.East_Greenland_Sea.tolist()[:-deletion]
		self.BaS_extent = Yeardata_ext.Barents_Sea.tolist()[:-deletion]
		self.KS_extent = Yeardata_ext.Kara_Sea.tolist()[:-deletion]
		self.LS_extent = Yeardata_ext.Laptev_Sea.tolist()[:-deletion]
		self.ES_extent = Yeardata_ext.East_Siberian_Sea.tolist()[:-deletion]
		self.CS_extent = Yeardata_ext.Chukchi_Sea.tolist()[:-deletion]
		self.BeaS_extent = Yeardata_ext.Beaufort_Sea.tolist()[:-deletion]
		self.CA_extent = Yeardata_ext.Canadian_Archipelago.tolist()[:-deletion]
		self.AB_extent = Yeardata_ext.Central_Arctic.tolist()[:-deletion]
		
	def exportdata(self):
		CryoIO.csv_columnexport('/home/nico/Cryoweb/NSIDC_Area/Data/Arctic_NSIDC_Area_NRT.csv',
			[self.CSVDatum,self.CSVArea,self.CSVExtent,self.CSVCompaction,self.CSVArea_High,self.CSVExtent_High])
		CryoIO.csv_columnexport('/home/nico/Cryoweb/NSIDC_Area/Data/Regional_NRT.csv',
				[self.CSVDatum,self.SoO_area,self.Bers_area,self.HB_area,self.BB_area,self.EG_area,self.BaS_area,
				self.KS_area,self.LS_area,self.ES_area,self.CS_area,self.BeaS_area,self.CA_area,self.AB_area])
		CryoIO.csv_columnexport('/home/nico/Cryoweb/NSIDC_Area/Data/Regional_NRT_extent.csv',
				[self.CSVDatum,self.SoO_extent,self.Bers_extent,self.HB_extent,self.BB_extent,self.EG_extent,self.BaS_extent,
				self.KS_extent,self.LS_extent,self.ES_extent,self.CS_extent,self.BeaS_extent,self.CA_extent,self.AB_extent])
	
	def maintanance(self):
		xxx = 6
		while xxx > 0:
			try:
				file1 = f'/home/nico/Cryoweb/NSIDC_Area/Arctic-{xxx}.png'
				file2 = f'/home/nico/Cryoweb/NSIDC_Area/Arctic-{xxx+1}.png'
				file3 = f"/home/nico/Cryoweb/NSIDC_Area/Arctic_anom-{xxx}.png"
				file4 = f"/home/nico/Cryoweb/NSIDC_Area/Arctic_anom-{xxx+1}.png"
				
				self.rename_image(file1, file2)
				self.rename_image(file3, file4)
			except:
				print(f'no day {xxx}')
			xxx -= 1
				
			
	def rename_image(self,file1,file2):
		os.rename(file1,file2)

	
	def automated (self,day,month,year,daycount):
		self.year = year
		self.month = month
		self.day = day
		self.daycount = daycount
		self.maintanance()
		
		self.loadCSVdata(self.daycount-1)
		self.loadCSVRegiondata(self.daycount-1)
		self.dayloop()
		self.exportdata()



action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
# 	action.dayloop()
# 	action.exportdata()
# 	action.automated(30,12,2021,3) #note substract xxx days from last available day

	

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
