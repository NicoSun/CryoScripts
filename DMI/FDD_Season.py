"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun
The script calculates the Freezing Degree Days for the freezing season at 80N (Sep-May)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv


class degreefreezing:

	def __init__ (self):
		self.mode = 'man'
		self.currentjahr = [0]
		self.year = 2021
		self.month = 1
		self.day = 7
		
	def Currentyear(self):
		'''loads the current year data'''
		with open('ZZZ_80N_List.csv', newline='') as csvfile:
			tempreader = csv.reader(csvfile, delimiter=',')
			tempreader = list(tempreader)
		
		
		#January-May
		if 0 < self.month < 7:
			for row in range(0,len(tempreader)):
				temp = float(tempreader[row][2])
				freezingtemp = 273.15-temp
				self.currentjahr.append(float(self.currentjahr[-1])+freezingtemp)
		
		#September-December
		if self.month > 8:
			for row in range(244,len(tempreader)): # 244 is the real date in gapyear (date 0 exists)
				temp = float(tempreader[row][2])
				freezingtemp = 273.15-temp
				self.currentjahr.append(float(self.currentjahr[-1])+freezingtemp)
		#print(self.currentjahr)
		del self.currentjahr[0]
		
	
	def loaddata(self):
		'''loads all historic data'''
		Climatecolnames = ['A', 'B', 'C', 'D', 'E', 'F','G','H','I']
		Climatedata = pd.read_csv('X:/DMI/DMI_FDD_Season_climate.csv', names=Climatecolnames,header=0 )	
		self.ERA40 = Climatedata.A.tolist()
		self.C1960s = Climatedata.B.tolist()
		self.C1980s = Climatedata.C.tolist()
		self.C2000s = Climatedata.D.tolist()
		self.C2010s = Climatedata.E.tolist()
		
		self.C2015 = Climatedata.F.tolist()
		self.C2016 = Climatedata.G.tolist()
		self.C2017 = Climatedata.H.tolist()
		self.C2020 = Climatedata.I.tolist()
		
		
		self.labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar', 'Apr','May','Jun']
		self.xtick = [0,30,61,91,122,153,182,213,243,274]
		
		#reads the previous year since September
		if self.month < 6:
			self.currentjahr = self.C2020
			del (self.currentjahr[-153:]) # deletes NAN values
			print(self.currentjahr)
		
		
	
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
		ax.text(175, 280, 'Data: DMI meanT 80N ', fontsize=10,color='black',fontweight='bold')
		ax.text(175, 80, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')

		lastFDD = round(float(self.currentjahr[-1]))
		FDDthick = round(1.33*lastFDD**0.58)
		FDDthick_anom = round(1.33*self.currentjahr[-1]**0.58) - round(1.33*self.ERA40[len(self.currentjahr)]**0.58)
		
		ax.text(230, 2850, 'Last FDD: '+str(lastFDD)+'°C', fontsize=10,color='black')
		ax.text(230, 2700, 'Thickness: '+str(FDDthick)+' cm', fontsize=10,color='black')
		ax.text(212, 2550, 'Thickness anomaly: '+str(FDDthick_anom)+' cm', fontsize=10,color='black')
		
		
		ax.text(0.01, -0.07, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.07, 'cryospherecomputing.tk',transform=ax.transAxes,color='grey', fontsize=10)
		
		ax.text(5, 550, '50cm', fontsize=8,color='black')
		ax.axhline(y=511,xmin=0,xmax=275,color=(0.75,0.75,0.75),lw=1,ls='--')
		ax.text(5, 1700, '100cm', fontsize=8,color='black')
		ax.axhline(y=1686,xmin=0,xmax=275,color=(0.5,0.5,0.5),lw=1,ls='--')
		ax.text(5, 3400, '150cm', fontsize=8,color='black')
		ax.axhline(y=3387,xmin=0,xmax=275,color=(0.25,0.25,0.25),lw=1,ls='--')
		ax.text(5, 5600, 'The dashed lines represent estimated sea ice thickness, 200cm', fontsize=8,color='black')
		ax.axhline(y=5555,xmin=0,xmax=275,color=(0.1,0.1,0.1),lw=1,ls='--')
		
			
		plt.plot( self.C1960s, color=(0.75,0.75,0.75),label='1960s',lw=2,ls='--')
		plt.plot( self.C1980s, color=(0.5,0.5,0.5),label='1980s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( self.C2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
#		plt.plot( self.C2013, color='blue',label='2013/4',lw=2)
		plt.plot( self.C2015, color='orange',label='2015/6',lw=2)
		plt.plot( self.C2016, color='red',label='2016/7',lw=2)
		plt.plot( self.C2017, color='green',label='2017/8',lw=2)
#		plt.plot( self.C2018, color='purple',label='2018/9',lw=2)
		plt.plot( self.currentjahr, color='black',label='2020/21',lw=2)
		
		xmin = 0
		xmax = 275
		ymax = 6200
		plt.axis([xmin,xmax,0,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/DMI/DMI_FDD_Season.png')
#		plt.show()
			
			
	def makeanomgraph(self):
		'''creates the anomaly graph'''
		fig = plt.figure(figsize=(10, 7.5))
		#fig.suptitle('Degree Days Freezing based on DMI 80N+ data', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		plt.xticks(self.xtick,self.labels)

		ax.set_ylabel('FDD anomaly in °C')
		major_ticks = np.arange(500, -5000, -250)
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
#		C2018_anom = list(map(self.minus,self.C2018,self.ERA40))
#		C2019_anom = list(map(self.minus,self.C2019,self.ERA40))
		current_anom = list(map(self.minus,self.currentjahr,self.ERA40))
		
		plt.plot( C1960s_anom, color=(0.75,0.75,0.75),label='1960s',lw=2,ls='--')
		plt.plot( C1980s_anom, color=(0.5,0.5,0.5),label='1980s',lw=2,ls='--')
		plt.plot( C2000s_anom, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
#		plt.plot( C2012_anom, color='blue',label='2012/3',lw=2)
		plt.plot( C2015_anom, color='orange',label='2015/6',lw=2)
		plt.plot( C2016_anom, color='red',label='2016/7',lw=2)
		plt.plot( C2017_anom, color='green',label='2017/8',lw=2)
#		plt.plot( C2018_anom, color='purple',label='2018/9',lw=2)
		plt.plot( current_anom, color='black',label='{}/{}'.format(2021,21),lw=2)
		
		lastFDD_anom = round(float(current_anom[-1]))
		averageTemp_anom = round(lastFDD_anom/len(current_anom),2)
		
		
		ax.text(205, -140, 'Last FDD anomaly: '+str(lastFDD_anom)+'°C', fontsize=10,color='black')
		ax.text(205, -190, 'Mean Temp anomaly: '+'{0:+1.2f}'.format(averageTemp_anom*(-1))+' °C', fontsize=10,color='black')
		
		
		ax.text(45, C2016_anom[-1], 'Data: DMI meanT 80N ', fontsize=10,color='black',fontweight='bold')
		ax.text(45, C2016_anom[-1]*1.03, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		xmin = 0
		xmax = 275
		ymax = C2016_anom[-1]*1.05
		plt.axis([xmin,xmax,300,ymax])
		plt.gca().invert_yaxis()
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/DMI/DMI_FDD_Season_Anom.png')
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
	fddcalc.Currentyear()
	fddcalc.makegraph()
	fddcalc.makeanomgraph()
#	fddcalc.automated(2018)


'''
Thickness (cm) = 1.33 * FDD (°C)0.58
'''