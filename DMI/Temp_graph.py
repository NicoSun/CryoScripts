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
		self.mode = 'man'
		self.year = 2021
		self.month = 1
		self.day = 1
		
	def Currentyear(self):
		'''loads the current year data'''
		self.currentyear = []
		with open('ZZZ_80N_List.csv', newline='') as csvfile:
			tempreader = csv.reader(csvfile, delimiter=',')
			templist = list(tempreader)
			for row in range(0,len(templist)):
				temp = float(templist[row][2])
				self.currentyear.append(temp-273.15)
#			print(self.currentyear)
	
	def loaddata(self):
		'''loads all historic data'''
		Climatecolnames = ['A', 'B', 'C', 'D', 'E']
		Climatedata = pandas.read_csv('X:/DMI/DMI_80N_Climate.csv', names=Climatecolnames,header=0)
		self.Date = Climatedata.A.tolist()
		self.C1960s = Climatedata.B.tolist()
		self.C1980s = Climatedata.C.tolist()
		self.C2000s = Climatedata.D.tolist()
		self.C2010s = Climatedata.E.tolist()
		
		#del self.ERA40[0],self.C2011[0],self.C2012[0],self.C2013[0],self.C2014[0],self.C2015[0],self.C2016[0]
		self.labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		self.xtick = [0,30,59,90,120,151,181,212,243,273,304,334]

		
	
	def makegraph(self):
		'''creates the normal graph'''
		fig = plt.figure(figsize=(10, 7))
		#fig.suptitle('Degree Days Freezing based on DMI 80N+ data', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		#ax.axes.get_xaxis().set_ticks([])
		
		plt.xticks(self.xtick,self.labels)

		ax.set_ylabel('Temperature in °C')
		major_ticks = np.arange(-50, 20, 5)
		ax.set_yticks(major_ticks)
		ax.grid(True)
		ax.set_title('DMI 80°N 2m Temperature ', fontsize=12, fontweight='bold')
		ax.text(2, 4, 'Data: DMI meanT 80N ', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 3, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		
		ax.text(0.01, -0.07, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.07, 'cryospherecomputing.tk',transform=ax.transAxes,color='grey', fontsize=10)
				
		plt.plot( self.C1960s, color=(0.2,0.2,0.85),label='1960s',lw=2,ls='--')
		plt.plot( self.C1980s, color=(0.2,0.8,0.7),label='1980s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.3,0.7,0),label='2000s',lw=2,ls='-.')
		plt.plot( self.C2010s, color=(1,0.2,0.1),label='2010s',lw=2,ls=':')
		plt.plot( self.currentyear, color='black',label=str(self.year),lw=2)
		
		lastTemp = round((self.currentyear[-1]),1)
		averageTemp = round((np.mean(self.currentyear[-14:])),2)
		
		ax.text(210, -32, 'Current Temp: '+str(lastTemp)+'°C', fontsize=10,color='black')
		ax.text(210, -33, 'Last 14 days: '+str(averageTemp)+' °C', fontsize=10,color='black')
		
		xmin = 0
		xmax = 366
		ymin = -35
		ymax = 5
		plt.axis([xmin,xmax,ymin,ymax])
		plt.legend(loc=8, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(bottom=0.08)

		fig.savefig('X:/Upload/DMI/DMI_Temp_graph.png')
#		plt.show()

			

		
	def automated(self,impyear,impmonth,impday):
		'''only used for daily updates'''
		self.mode = 'auto'
		self.year = impyear
		self.month = impmonth
		self.day = impday
		
		self.loaddata()
		self.Currentyear()
		self.makegraph()

		
tempcalc = degreefreezing()
if __name__ == "__main__":
	tempcalc.loaddata()
	tempcalc.Currentyear()
	tempcalc.makegraph()
#	tempcalc.makeanomgraph()
	#tempcalc.automated(2017)

