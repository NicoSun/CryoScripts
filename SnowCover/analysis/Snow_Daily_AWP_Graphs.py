"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script creates the Volume and Thickness graphs
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt


class AWP_graphs:
	def __init__  (self):
		'''ADS object initializing'''
		
	
	def makeYeargraph(self):
		'''create full year graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Northern Hemisphere Land AWP', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.text(5, 25.2, r'Snow Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(5, 24.6, r'AWP model: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('AWP in MJ / 'r'$m^2$')
		major_ticks = np.arange(0, 50, 2.5)
		ax.set_yticks(major_ticks)   

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
   		
		ax.grid(True)
		
		x = np.arange(366)
		
		CanadaSDup = [x+2*y for x,y in zip(self.MCanada,self.SDCanada)]
		CanadaSDdown = [x-2*y for x,y in zip(self.MCanada,self.SDCanada)]
		
		USASDup = [x+2*y for x,y in zip(self.MUSA,self.SDUSA)]
		USASDdown = [x-2*y for x,y in zip(self.MUSA,self.SDUSA)]
		
		EuropeSDup = [x+2*y for x,y in zip(self.MEurope,self.SDEurope)]
		EuropeSDdown = [x-2*y for x,y in zip(self.MEurope,self.SDEurope)]
		
		AsiaSDup = [x+2*y for x,y in zip(self.MAsia,self.SDAsia)]
		AsiaSDdown = [x-2*y for x,y in zip(self.MAsia,self.SDAsia)]
		
		GreenSDup = [x+2*y for x,y in zip(self.MGreen,self.SDGreen)]
		GreenSDdown = [x-2*y for x,y in zip(self.MGreen,self.SDGreen)]
		
		plt.fill_between(x,CanadaSDup,CanadaSDdown,color='red', alpha=0.333)
		plt.fill_between(x,USASDup,USASDdown,color='blue', alpha=0.333)
		plt.fill_between(x,EuropeSDup,EuropeSDdown,color='green', alpha=0.333)
		plt.fill_between(x,AsiaSDup,AsiaSDdown,color='orange', alpha=0.333)
		plt.fill_between(x,GreenSDup,GreenSDdown,color='grey',label='2 standard deviations', alpha=0.333)
	
		plt.plot( self.NRT_Canada, color='red',label='Canada',lw=2)
		plt.plot( self.NRT_USA, color='blue',label='USA 48',lw=2)
		plt.plot( self.NRT_Europe, color='green',label='Europe',lw=2)
		plt.plot( self.NRT_Asia, color='orange',label='Siberia',lw=2)
		plt.plot( self.NRT_Green, color='black',label='Greenland',lw=2)

		
#		last_value =  int(self.V2018[-1])
#		ax.text(0.75, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^3$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 0
		ymax = 26
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=1, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/Land_AWP_graph.png')
#		plt.show()
		plt.close()

			
	def make_Anomaly_graph(self):
		'''create 3 month zoomed graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Northern Hemisphere Snow Extent', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.text(36, 26, r'Snow Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(36, 24, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Extent in 10^6 'r'$km^2$')
		major_ticks = np.arange(0, 50, 2.5)
		ax.set_yticks(major_ticks)

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/snow-cover',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
		
		ax.grid(True)
		
		x = np.arange(366)
		IceSDup = [x+2*y for x,y in zip(self.MSeaIce,self.SD_SeaIce)]
		IceSDdown = [x-2*y for x,y in zip(self.MSeaIce,self.SD_SeaIce)]
		
		AmericaSDup = [x+2*y for x,y in zip(self.MAmerica,self.SD_America)]
		AmericaSDdown = [x-2*y for x,y in zip(self.MAmerica,self.SD_America)]
		
		GreenlandSDup = [x+2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
		GreenlandSDdown = [x-2*y for x,y in zip(self.MGreenland,self.SD_Greenland)]
		
		EuropeSDup = [x+2*y for x,y in zip(self.MEurope,self.SD_Europe)]
		EuropeSDdown = [x-2*y for x,y in zip(self.MEurope,self.SD_Europe)]
		
		AsiaSDup = [x+2*y for x,y in zip(self.MAsia,self.SD_Asia)]
		AsiaSDdown = [x-2*y for x,y in zip(self.MAsia,self.SD_Asia)]
		
		
#		plt.fill_between(x,IceSDup,IceSDdown,color='orange', alpha=0.333)
		plt.fill_between(x,AmericaSDup,AmericaSDdown,color='red', alpha=0.333)
		plt.fill_between(x,GreenlandSDup,GreenlandSDdown,color='blue', alpha=0.333)
		plt.fill_between(x,EuropeSDup,EuropeSDdown,color='green', alpha=0.333)
		plt.fill_between(x,AsiaSDup,AsiaSDdown,color='grey',label='2 standard deviations', alpha=0.333)
	
#		plt.plot( self.NRT_SeaIce, color='orange',label='Sea Ice',lw=2)
# =============================================================================
# 		plt.plot( self.NRT_America, color='red',label='America',lw=2)
# 		plt.plot( self.NRT_Greenland, color='blue',label='Greenland',lw=2)
# 		plt.plot( self.NRT_Europe, color='green',label='Europe',lw=2)
# 		plt.plot( self.NRT_Asia, color='black',label='Asia',lw=2)
# =============================================================================
		
#		last_value =  self.T2018[-1]
#		ax.text(0.75, 0.01, 'Last value: {} cm'.format(last_value), fontsize=10,color='black',transform=ax.transAxes)
		
		xstart = self.dayofyear-30
		xend = self.dayofyear+60
		
		ymin = max(0,min(self.NRT_Greenland[-1]-1,self.NRT_Europe[-1]-1))
		ymax = max(self.NRT_Greenland[-1]+2,self.NRT_Asia[-1]+2)
		plt.axis([xstart,xend,ymin,ymax])
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/Snow_Cover_Data/NOAA_SnowCover_season.png')
#		plt.show()
		plt.close()

	
	def loadCSVdata (self):
		'''loads the graph data from csv files'''
		#Climate value Data
		Climatecolnames = ['Date','Greenland','Canada','USA','Europe','Asia','SD1','SD2','SD3','SD4','SD5']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Land_AWP_climate.csv', names=Climatecolnames,header=0)
		self.MGreen = Climatedata.Greenland.tolist()
		self.MCanada = Climatedata.Canada.tolist()
		self.MUSA = Climatedata.USA.tolist()
		self.MEurope = Climatedata.Europe.tolist()
		self.MAsia = Climatedata.Asia.tolist()
		
		
		self.SDGreen = Climatedata.SD1.tolist()
		self.SDCanada = Climatedata.SD2.tolist()
		self.SDUSA = Climatedata.SD3.tolist()
		self.SDEurope = Climatedata.SD4.tolist()
		self.SDAsia = Climatedata.SD5.tolist()
		

		Climatecolnames = ['Date','Greenland','Canada','USA','Europe','Asia']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Land_AWP_NRT.csv', names=Climatecolnames,header=0)
		self.NRT_Green = Climatedata.Greenland.tolist()
		self.NRT_Canada = Climatedata.Canada.tolist()
		self.NRT_USA = Climatedata.USA.tolist()
		self.NRT_Europe = Climatedata.Europe.tolist()
		self.NRT_Asia = Climatedata.Asia.tolist()
		


	def automated (self,day,month,year,dayofyear):
		'''function to automate parts of the monthly update procedure'''
		self.year = year
		self.month =str(month).zfill(2)
		self.day = str(day).zfill(2)
		self.dayofyear = dayofyear

		self.loadCSVdata()
		self.makeYeargraph()
#		self.makeSeasongraph()
#		self.makegif()
#		plt.show()


action = AWP_graphs()
if __name__ == "__main__":
	print('main')
	action.automated(31,12,2018,353) 
#	action.makeYeargraph()
#	action.makeSeasongraph()
#	action.makegif()

'''
Citation:

'''