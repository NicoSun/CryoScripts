import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
from matplotlib import cm



class Warming:

	def __init__  (self):
		self.year = 2008
		self.month = 1
		self.day = 1

		self.plottype = 'daily'
		
		
		
	def dayloop(self):		
				
		for count in range (0,1,1): #366year, 186summer
			filename = 'DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			
			with open(filename ,'rb') as frr:
				ice = np.fromfile(frr, dtype=np.uint8)
				
			icef = np.array(ice, dtype=float)
		
			
			self.polehole=[]
			self.poleholeedge=[]
			
			'''
			for x in range (0,136192):
				if  icef[x]==251:
					self.polehole.append (x)
				if  icef[x]==251 and icef[x-304]<251:
					self.poleholeedge.append (x-304)
					self.poleholeedge.append (x-608)
				if  icef[x]==251 and icef[x+304]<251:
					self.poleholeedge.append (x+304)
					self.poleholeedge.append (x+608)
				if  icef[x]==251 and icef[x-1]<251:
					self.poleholeedge.append (x-1)
					self.poleholeedge.append (x-2)
				if  icef[x]==251 and icef[x+1]<251:
					self.poleholeedge.append (x+1)
					self.poleholeedge.append (x+2)
			'''		
			for x in range (0,136192):
				if  icef[x]==251:
					self.polehole.append (x)
					self.poleholeedge.append (x+3)
					self.poleholeedge.append (x-3)
					for z in range (1,4):
						self.poleholeedge.append (x-(z*304))
						self.poleholeedge.append (x+(z*304))
					
			
		self.writetofile()

		
		
	def writetofile(self):
		
		
		with open(str(self.year)+'_hole.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,len(self.polehole)):
				writer.writerow([self.polehole[writeing]])
                
		with open(str(self.year)+'_edge.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,len(self.poleholeedge)):
				writer.writerow([self.poleholeedge[writeing]])
				


action = Warming()
action.dayloop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA