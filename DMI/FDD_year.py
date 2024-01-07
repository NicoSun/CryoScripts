"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun
The script calculates the Freezing Degree Days for a whole year
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas
import csv
 


class degreefreezing:

	def __init__ (self):
		self.currentjahr = [0]
		self.year = 2021
		self.month = 1
		self.day = 7
		
	def Currentyear(self,year):
		'''loads the current year data'''
		with open('ZZZ_80N_List.csv', newline='') as csvfile:
			tempreader = csv.reader(csvfile, delimiter=',')
			tempreader = list(tempreader)
		for row in range(0,len(tempreader)):
			temp = float(tempreader[row][2])
			freezingtemp = 273.15-temp
			self.currentjahr.append(self.currentjahr[-1]+freezingtemp)
		del self.currentjahr[0]
		#print(self.currentjahr)
		
	
	def loaddata(self):
		'''loads all historic data'''
		Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F','G','H','I']
		Climatedata = pandas.read_csv('X:/DMI/DMI_FDD_Year_climate.csv', names=Climatecolnames,header=0)
		self.ERA40 = Climatedata.A.tolist()
		self.C1960s = Climatedata.B.tolist()
		self.C1980s = Climatedata.C.tolist()
		self.C2000s = Climatedata.D.tolist()
		self.C2010s = Climatedata.E.tolist()
		
		self.C2015 = Climatedata.F.tolist()
		self.C2016 = Climatedata.G.tolist()
		self.C2017 = Climatedata.H.tolist()
		self.C2018 = Climatedata.I.tolist()
		
		#del self.ERA40[0],self.C2011[0],self.C2012[0],self.C2013[0],self.C2014[0],self.C2015[0],self.C2016[0]
		self.labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		self.xtick = [0,30,59,90,120,151,181,212,243,273,304,334]
		
	
	def makegraph(self):
		'''creates the normal graph'''
		fig = plt.figure(figsize=(10, 7.5))
		#fig.suptitle('Degree Days Freezing based on DMI 80N+ data', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		#ax.axes.get_xaxis().set_ticks([])
		
		plt.xticks(self.xtick,self.labels)

		ax.set_ylabel('FDD in °C')
		major_ticks = np.arange(0, 8000, 500)
		ax.set_yticks(major_ticks)
		ax.grid(True)
		ax.set_title('DMI 2m temperature for north of 80°N: Freezing Degree Days (FDD)', fontsize=12, fontweight='bold')
		ax.text(235, 280, 'Data: DMI meanT 80N ', fontsize=10,color='black',fontweight='bold')
		ax.text(235, 80, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		
		ax.text(0.01, -0.07, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.07, 'cryospherecomputing.tk',transform=ax.transAxes,color='grey', fontsize=10)
				
		plt.plot( self.C1960s, color=(0.75,0.75,0.75),label='1960s',lw=2,ls='--')
		plt.plot( self.C1980s, color=(0.5,0.5,0.5),label='1980s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( self.C2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
#		plt.plot( self.C2013, color='blue',label='2013',lw=2)
		plt.plot( self.C2015, color='orange',label='2015',lw=2)
		plt.plot( self.C2016, color='red',label='2016',lw=2)
		plt.plot( self.C2017, color='green',label='2017',lw=2)
		plt.plot( self.C2018, color='purple',label='2018',lw=2)
		plt.plot( self.currentjahr, color='black',label=str(self.year),lw=2)
		
		lastFDD = round(float(self.currentjahr[-1]))
		averageTemp = round(lastFDD/(len(self.currentjahr)),2)
		
		ax.text(240, 1300, 'Last FDD: '+str(lastFDD)+'°C', fontsize=10,color='black')
		ax.text(240, 1100, 'Mean Temp: '+str(averageTemp*(-1))+' °C', fontsize=10,color='black')
		
		xmin = 0
		xmax = 366
		ymax = 6200
		plt.axis([xmin,xmax,0,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/DMI/DMI_FDD_Year.png')

			
			
	def makeanomgraph(self):
		'''creates the anomaly graph'''
		fig = plt.figure(figsize=(10, 7.5))
		#fig.suptitle('Degree Days Freezing based on DMI 80N+ data', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		plt.xticks(self.xtick,self.labels)

		ax.set_ylabel('FDD anomaly in °C')
		major_ticks = np.arange(1000, -5000, -250)
		ax.set_yticks(major_ticks)
		ax.grid(True)
		ax.set_title('DMI 2m temperature for north of 80°N: Freezing Degree Days (FDD) Anomaly', fontsize=12, fontweight='bold')
		ax.text(0.01, -0.07, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.07, 'cryospherecomputing.tk',transform=ax.transAxes,color='grey', fontsize=10)
		
		C1960s_anom = list(map(self.minus,self.C1960s,self.ERA40))
		C1980s_anom = list(map(self.minus,self.C1980s,self.ERA40))
		C2000s_anom = list(map(self.minus,self.C2000s,self.ERA40))
		C2010s_anom = list(map(self.minus,self.C2010s,self.ERA40))
		C2015_anom = list(map(self.minus,self.C2015,self.ERA40))
		C2016_anom = list(map(self.minus,self.C2016,self.ERA40))
		C2017_anom = list(map(self.minus,self.C2017,self.ERA40))
		C2018_anom = list(map(self.minus,self.C2018,self.ERA40))
		current_anom = list(map(self.minus,self.currentjahr,self.ERA40))
		
		plt.plot( C1960s_anom, color=(0.75,0.75,0.75),label='1960s',lw=2,ls='--')
		plt.plot( C1980s_anom, color=(0.5,0.5,0.5),label='1980s',lw=2,ls='--')
		plt.plot( C2000s_anom, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
#		plt.plot( C2013_anom, color='blue',label='2013',lw=2)
		plt.plot( C2015_anom, color='orange',label='2015',lw=2)
		plt.plot( C2016_anom, color='red',label='2016',lw=2)
		plt.plot( C2017_anom, color='green',label='2017',lw=2)
		plt.plot( C2018_anom, color='purple',label='2018',lw=2)
		plt.plot( current_anom, color='black',label=str(self.year),lw=2)
		
		lastFDD_anom = round(float(current_anom[-1]))
		averageTemp_anom = round(lastFDD_anom/(len(current_anom)),2)
		
		ax.text(180, -1690, 'Last FDD anomaly: '+str(lastFDD_anom)+'°C', fontsize=10,color='black')
		ax.text(180, -1740, 'Mean Temp anomaly: '+'{0:+1.2f}'.format(averageTemp_anom*(-1))+' °C', fontsize=10,color='black')
		
		ax.text(62, C2016_anom[-1], 'Data: DMI meanT 80N ', fontsize=10,color='black',fontweight='bold')
		ax.text(62, C2016_anom[-1]*1.03, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		xmin = 0
		xmax = 366
		ymax = C2016_anom[-1]*1.05
		plt.axis([xmin,xmax,300,ymax])
		plt.gca().invert_yaxis()
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/DMI/DMI_FDD_Year_Anom.png')
		
	def automated(self,impyear,impmonth,impday):
		'''only used for daily updates'''
		self.mode = 'auto'
		self.year = impyear
		self.month = impmonth
		self.day = impday
		
		self.loaddata()
		self.Currentyear(self.year)
		self.makegraph()
		self.makeanomgraph()
		
	
	def minus(self,a,b):
		'''calculates the FDD anomaly'''
		a = float(a)
		b = float(b)
		c = a-b
		return c
		
fddcalc = degreefreezing()
if __name__ == "__main__":
	fddcalc.loaddata()
	fddcalc.Currentyear(2021)
	fddcalc.makegraph()
	fddcalc.makeanomgraph()
	#fddcalc.automated(2017)

