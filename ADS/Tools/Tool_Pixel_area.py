"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the ADS polehole location, polehole edge and exports the data into csv format
"""

import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
import pandas


class ADS_data:

	def __init__  (self):
		self.year = 2017
		self.month = 6
		self.day = 1
		self.daycount = 1 #366year, 186summer, total length: 2008 
		
		self.CSVDatum = ['Date']
		self.CSVVolume =['Volume']
		self.CSVThickness =['Thickness']

		self.masksload()
		
		
	def masksload(self):
	
		
		latlonmaskfile = 'X:/ADS/Masks/latlon_low.map'
		with open(latlonmaskfile, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint16)
		self.latmaskf = np.array(self.mask2, dtype=float)
		self.latmaskf = 0.01*self.mask2[:810000] 
		self.lonmaskf = 0.01*self.mask2[810000:]
		
# =============================================================================
# 		self.latmaskf = self.latmaskf.reshape(900, 900)
# 		verti = []
# 		hori = []
# 		for x in range(0,900):
# 			verti.append(self.latmaskf[450,x])
# 			hori.append(self.latmaskf[x,450])
# 		
# 		
# 		plt.imshow(self.latmaskf, interpolation='nearest',vmin=40, vmax=90, cmap=plt.cm.jet)
# 		with open('Latitude_list.csv', "w") as output: 
# 			writer = csv.writer(output, lineterminator='\n') #str(self.year)
# 			for writeing in range(0,len(verti)):
# 				writer.writerow([hori[writeing],verti[writeing]])
# 		plt.show()
# =============================================================================
		
	def showhole(self):
	
		
		Columns = ['hole','edge']
		csvdata = pandas.read_csv('polehole+edge.csv', names=Columns)
		hole = self.polehole #csvdata.hole.tolist()
		edge = self.newedge#csvdata.edge.tolist()
		#print(hole)

		icenull = np.zeros(810000, dtype=float)
		for x in range (0,810000):
			if x in hole:
				icenull[x] = 1
			if x in edge:	
				icenull[x] = 2
		
		fig = plt.figure(figsize=(10, 10))
		ax = fig.add_subplot(111)
		icemap = icenull.reshape(900, 900)
		ax.clear()
		ax.imshow(icemap, interpolation='nearest',vmin=0, vmax=3, cmap=plt.cm.jet)
		fig.tight_layout(pad=1)
		plt.show()

	def normalshow(self):	
		from matplotlib.colors import LinearSegmentedColormap
		filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2))
		with open(filename, 'rb') as frr:
			ice = np.fromfile(frr, dtype=np.uint16)
		icemap = ice/10

		
		
		#icemap = icemap.reshape(900, 900)
		#icemap = np.rot90(icemap,k=2)
		#icemap = icemap[80:750,:700]
		
		self.polehole = []		
		poleholeEdge = []		
		for x in range (0,810000):
			if  5500 < icemap[x] < 5600 and self.latmaskf[x] > 85:
				self.polehole.append (x+1)
				self.polehole.append (x-1)
				self.polehole.append (x+900)
				self.polehole.append (x-900)
				poleholeEdge.append (x-5)
				poleholeEdge.append (x+5)
				for z in range (1,6):
					poleholeEdge.append (x-(z*900))
					poleholeEdge.append (x+(z*900))
			
		self.clearing(poleholeEdge)
		
			
		#map1 = ma.masked_outside(icemap,0,500) # SIT
		#map2 = self.lonmaskf.reshape(900, 900)
		map2 = icemap.reshape(900, 900)
		
		colors = [(0.1, 0., 0.1), (0.6, 0.1, 0.1), (0.4, 0.4, 0.4)]  # NoData -> Land -> Water
		cmap_name = 'my_list'
		
		cm4 = LinearSegmentedColormap.from_list(
		cmap_name, colors, N=3)
		cmap = plt.cm.jet
		
		fig = plt.figure(figsize=(10, 9))
		ax = fig.add_subplot(111)
		
		ax.clear()
		ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		
		cax2 = ax.imshow(map2, interpolation='nearest',vmin=0, vmax=500, cmap=plt.cm.jet)
		#cax = ax.imshow(map1, interpolation='nearest',vmin=0, vmax=500, cmap=cmap)
		
		cbb = plt.colorbar(cax2,shrink=0.9)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		fig.tight_layout(pad=1)
		#fig.savefig('C:/Users/Nico/Desktop/EarthObservation/ADS/SIT.png')
		plt.pause(0.01)
		#plt.show()
		
	def remove_duplicates(self,values):
		output = []
		seen = set(self.polehole)
		for value in values:
			# If value has not been encountered yet,
			# ... add it to both list and set.
			if value not in seen:
				output.append(value)
				seen.add(value)
		return output

		
	def clearing(self,poleholeEdge):

		self.newedge = self.remove_duplicates(poleholeEdge)
		#print(newedge)
		self.showhole()
		
		with open('polehole.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.polehole)):
				writer.writerow([self.polehole[writeing]])
		
		with open('poleholeEdge.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.newedge)):
				writer.writerow([self.newedge[writeing]])
				
		

action = ADS_data()
if __name__ == "__main__":
	print('main')
#	action.normalshow()
	#action.showhole()





'''
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''