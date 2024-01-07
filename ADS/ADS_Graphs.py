"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script creates the Volume and Thickness graphs
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt
from datetime import date
import ADS_netcdf

class ADS_data:
	def __init__  (self):
		'''ADS object initializing'''
		self.start = date(2012, 7, 3)
		self.year = self.start.year
		
	def makethickdistgraph(self,data):
		'''create volume graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Snow & Ice Volume', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = np.arange(0,500,100)
		x = [0,4,8,12,16,20] # 1st Jan is day zero
		plt.xticks(x,labels)

#		ax.text(5, 1000, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
#		ax.text(5, 400, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Area in 'r'$km^2$')
		ax.set_xlabel('thickness in cm')
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.com/SIT',transform=ax.transAxes,
        color='grey', fontsize=10)	
   		
		colourlist = [[0,0,0],[128,128,128],[200,200,200],[128,0,0],[250,0,0],[250,130,0],[128,128,0],[240,240,0],
				[0,128,0],[0,255,0],[0,128,128],[0,250,250],[0,0,128],[0,0,250],[128,0,128],[250,0,250]]
		
		ax.grid(True)
		

		plt.plot(data, color='orange',label=data[0],lw=1)

		ymin = 0
		ymax = max(data)*1.05
		plt.axis([0,16,ymin,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
#		fig.savefig('Upload/AMSR2_Sea_Ice_Volume.png')
		#plt.show()
		
		
	def monththickdistgraph(self,data,month):
		'''create volume graph'''
		plt.style.use('dark_background')
		labels = ['January', 'February', 'March', 'April','May','June','July','August','September','October','November','December']
		
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Thickness Distribution {}'.format(labels[month-1]), fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = np.arange(12.5,500,25)
		x = [0,5,10,15,20,25,30]
		x_lab = [0,5,10,15,20,25,30] # Day of month
		plt.xticks(x,x_lab)

#		ax.text(5, 1000, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
#		ax.text(5, 400, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Extent in $10^6$ $km^2$')
		ax.set_xlabel('Day of Month')
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.com/SIT',transform=ax.transAxes,
        color='grey', fontsize=10)	
   		
#		colourlist = [[0.5,0.5,0.5],[1,1,1],[0.5,0,0],[1,0,0],[1,0.5,0],[0.5,0.5,0],[1,1,0],
#				[0,0.5,0],[0,1,0],[0,0.5,0.5],[0,1,1],[0,0,0.5],[0,0,1],[0.5,0,0.5],[1,0,0.8],[1,0.5,1]]
		
		colourlist = [[0,0.25,0.25],[0,0.4,0],[0,0,1],[0,0.5,0.5],[0,1,1],[0,1,0],[0.5,0.5,0],[1,1,0],
				[1,0.5,0],[1,0,0],[0.5,0,0],[1,0,0.8],[0.5,0.1,0.6],[1,0.5,1],[1,1,1],[0.5,0.5,0.5]]
		
		
		ax.grid(True)
		
		j = 0
		for xxx in data:
			plt.plot(data[xxx]/1e4, color=colourlist[j], label=labels[j],lw=2) # /1e4 = convert to million km2
			j += 1

		plt.legend(loc='upper center', shadow=True, fontsize='medium')
		
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Upload/AMSR2_thickness_distribution.png')
		#plt.show()
		
	def makeVolumegraph(self):
		'''create volume graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Ice Volume', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,30,59,90,120,151,181,212,243,273,304,334] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.text(36, 800, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
		ax.text(36, 300, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Volume in 'r'$km^3$')
		major_ticks = np.arange(0, 30000, 2500)
		ax.set_yticks(major_ticks)   

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.com/SIT',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
   		
		ax.grid(True)
		
		plt.plot( self.VMean, color=(0.5,0.5,0.5),label='Mean',lw=2,ls='--')
		plt.plot( self.V2012, color='orange',label='2012',lw=1)
		plt.plot( self.V2013, color='purple',label='2013',lw=1)
		plt.plot( self.V2014, color='blue',label='2014',lw=1)
		plt.plot( self.V2016, color='grey',label='2016',lw=1)
		plt.plot( self.V2019, color='brown',label='2019',lw=1)
		plt.plot( self.V2020, color='green',label='2020',lw=1)
		plt.plot( self.V2021, color='red',label='2021',lw=1)
		plt.plot( self.Vcurrent, color='black',label=self.year,lw=2)
		
		last_value =  int(self.Vcurrent[-1])
		ax.text(0.75, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^3$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 0
		ymax = 23000
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Upload/AMSR2_Sea_Ice_Volume.png')
		#plt.show()

			
	def makeThicknessgraph(self):
		'''create thickness graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Ice Thickness', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,30,59,90,120,151,181,212,243,273,304,334] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.text(36, 56, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
		ax.text(36, 53, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Volume in 'r'$km^3$')
		major_ticks = np.arange(0, 30000, 2500)
		ax.set_yticks(major_ticks)   

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.com/SIT',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
		
		ax.set_ylabel('Sea Ice Thickness in centimetres')
		major_ticks = np.arange(0, 220, 10)
		ax.set_yticks(major_ticks)      		
		ax.grid(True)
		
		plt.plot( self.TMean, color=(0.5,0.5,0.5),label='Mean',lw=2,ls='--')
		plt.plot( self.T2012, color='orange',label='2012',lw=1)
		plt.plot( self.T2013, color='purple',label='2013',lw=1)
		plt.plot( self.T2014, color='blue',label='2014',lw=1)
		plt.plot( self.T2016, color='grey',label='2016',lw=1)
		plt.plot( self.T2019, color='brown',label='2019',lw=1)
		plt.plot( self.T2020, color='green',label='2020',lw=1)
		plt.plot( self.T2021, color='red',label='2021',lw=1)
		plt.plot( self.Tcurrent, color='black',label=self.year,lw=2)
		
		last_value =  round(self.Tcurrent[-1],2)
		ax.text(0.75, 0.01, 'Last value: {} cm'.format(last_value), fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 50
		ymax = 185
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Upload/AMSR2_Sea_Ice_Thickness.png')

	
	def loadCSVdata (self):
		'''loads the graph data from csv files'''
		#Volume Data
		Volumecolnames = ['Date','Mean','C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017', 'C2018', 'C2019', 'C2020','C2021','C2022']
		Volumedata = pandas.read_csv('Upload/AMSR2_SIT_Volume.csv', names=Volumecolnames,header=0)
		self.VMean = Volumedata.Mean.tolist()
		self.V2012 = Volumedata.C2012.tolist()
		self.V2013 = Volumedata.C2013.tolist()
		self.V2014 = Volumedata.C2014.tolist()
		self.V2015 = Volumedata.C2015.tolist()
		self.V2016 = Volumedata.C2016.tolist()
		self.V2017 = Volumedata.C2017.tolist()
		self.V2018 = Volumedata.C2018.tolist()
		self.V2019 = Volumedata.C2019.tolist()
		self.V2020 = Volumedata.C2020.tolist()
		self.V2021 = Volumedata.C2021.tolist()
		self.Vcurrent= Volumedata.C2022.dropna().tolist()
		
		#Thickness Data
		Thicknesscolnames = ['Date','Mean','C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017', 'C2018', 'C2019', 'C2020','C2021','C2022']
		Thicknessdata = pandas.read_csv('Upload/AMSR2_SIT_Thickness.csv', names=Thicknesscolnames,header=0)
		self.TMean = Thicknessdata.Mean.tolist()
		self.T2012 = Thicknessdata.C2012.tolist()
		self.T2013 = Thicknessdata.C2013.tolist()
		self.T2014 = Thicknessdata.C2014.tolist()
		self.T2015 = Thicknessdata.C2015.tolist()
		self.T2016 = Thicknessdata.C2016.tolist()
		self.T2017 = Thicknessdata.C2017.tolist()
		self.T2018 = Thicknessdata.C2018.tolist()
		self.T2019 = Thicknessdata.C2019.tolist()
		self.T2020 = Thicknessdata.C2020.tolist()
		self.T2021 = Thicknessdata.C2021.tolist()
		self.Tcurrent = Thicknessdata.C2022.dropna().tolist()
		
	def thickness_distribution(self,month):
		import CryoIO
		import os
		import pandas as pd
		monthlist = pd.DataFrame()
			
#		filename = 'Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
		filepath = 'Binary'
		for file in os.listdir(filepath):
			iceread = CryoIO.openfile(os.path.join(filepath,file),np.uint16)

			thicknesslist = np.ma.masked_greater(iceread,400)
			histogram = np.histogram(thicknesslist,bins=16,range=(20,400))
			
			monthlist[file[14:-4]] = histogram[0]
		monthlist_transposed = monthlist.T
		self.monththickdistgraph(monthlist_transposed,month)
#		print(monthlist_transposed)
		
		
#		plt.show()
		

	def automated (self,day,month,year):
		'''function to automate parts of the monthly update procedure'''
		self.year = year
		self.stringmonth =str(month).zfill(2)
		self.stringday = str(day).zfill(2)

		self.loadCSVdata()
		self.makeVolumegraph()
		self.makeThicknessgraph()
		self.thickness_distribution(month)
# 		self.makemovie()

	def makemovie(self):
		from moviepy.editor import ImageSequenceClip
		import os
		filepath = 'Images/SIT'
		filepath_anom = 'Images/Anomaly'
		image_list = []
		image_list_anom = []
		for filename in os.listdir(filepath):
			image_list.append(os.path.join(filepath,filename))
		for filename in os.listdir(filepath_anom):
			image_list_anom.append(os.path.join(filepath_anom,filename))
		clip = ImageSequenceClip(image_list, fps=5)
		clip_anom = ImageSequenceClip(image_list_anom, fps=5)
		clip.write_videofile("Upload/AMSR2_SIT_Last_month.webm",bitrate="5000000", audio=None,codec="libvpx")
		clip_anom.write_videofile("Upload/AMSR2_SIT_Last_month_anomaly.webm",bitrate="5000000", audio=None,codec="libvpx")
		clip.close()
		clip_anom.close()

year = 2022
month = 7
day = 31

action = ADS_data()
if __name__ == "__main__":
	print('main')
	action.automated(day,month,year) 
	#action.makemovie()
#	ADS_netcdf.action.automated(1,month,year,day)
#	action.thickness_distribution()


'''
Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''