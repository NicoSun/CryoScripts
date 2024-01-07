import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import os




class NSIDC_area:

	def __init__  (self):
		self.year = 2017
		self.month = 11
		self.day = 6
		self.daycount = 1 #366year, 186summer
		self.index = 0
		self.ccpath = 'D:/CryoComputing/CC_upload/'
		
				
		self.mode = 'man' #man, on
		self.masksload()
		
		
	def masksload(self):
	
		self.regionmask = 'D:/CryoComputing/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				self.mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		self.areamask = 'D:/CryoComputing/NSIDC/Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		
	def dayloop(self):		
		filepath = 'D:/CryoComputing/NSIDC/DataFiles/'	
		countmax = self.index+self.daycount
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			#filename5 = 'DataFiles/NSIDC_2005'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			filename6 = 'NSIDC_2006{}{}.bin'.format(self.stringmonth,self.stringday)
			filename7 = 'NSIDC_2007{}{}.bin'.format(self.stringmonth,self.stringday)
			filename8 = 'NSIDC_2008{}{}.bin'.format(self.stringmonth,self.stringday)
			filename9 = 'NSIDC_2009{}{}.bin'.format(self.stringmonth,self.stringday)
			filename10 = 'NSIDC_2010{}{}.bin'.format(self.stringmonth,self.stringday)
			filename11 = 'NSIDC_2011{}{}.bin'.format(self.stringmonth,self.stringday)
			filename12 = 'NSIDC_2012{}{}.bin'.format(self.stringmonth,self.stringday)
			filename13 = 'NSIDC_2013{}{}.bin'.format(self.stringmonth,self.stringday)
			filename14 = 'NSIDC_2014{}{}.bin'.format(self.stringmonth,self.stringday)
			filename15 = 'NSIDC_2015{}{}.bin'.format(self.stringmonth,self.stringday)
			filename16 = 'NSIDC_2016{}{}.bin'.format(self.stringmonth,self.stringday)
			
			iceminyear = np.zeros(136192, dtype=float)
			icemaxyear = np.zeros(136192, dtype=float)
			icefreeyear = np.zeros(136192, dtype=float)
			
			with open(os.path.join(filepath,filename6), 'rb') as fr6:
				ice6 = np.fromfile(fr6, dtype=np.uint8)
			with open(os.path.join(filepath,filename7), 'rb') as fr7:
				ice7 = np.fromfile(fr7, dtype=np.uint8)
			with open(os.path.join(filepath,filename8), 'rb') as fr8:
				ice8 = np.fromfile(fr8, dtype=np.uint8)
			with open(os.path.join(filepath,filename9), 'rb') as fr9:
				ice9 = np.fromfile(fr9, dtype=np.uint8)
			with open(os.path.join(filepath,filename10), 'rb') as fr10:
				ice10 = np.fromfile(fr10, dtype=np.uint8)
			with open(os.path.join(filepath,filename11), 'rb') as fr11:
				ice11 = np.fromfile(fr11, dtype=np.uint8)	
			with open(os.path.join(filepath,filename12), 'rb') as fr12:
				ice12 = np.fromfile(fr12, dtype=np.uint8)
			with open(os.path.join(filepath,filename13), 'rb') as fr13:
				ice13 = np.fromfile(fr13, dtype=np.uint8)
			with open(os.path.join(filepath,filename14), 'rb') as fr14:
				ice14 = np.fromfile(fr14, dtype=np.uint8)	
			with open(os.path.join(filepath,filename15), 'rb') as fr15:
				ice15 = np.fromfile(fr15, dtype=np.uint8)
			with open(os.path.join(filepath,filename16), 'rb') as fr16:
				ice16 = np.fromfile(fr16, dtype=np.uint8)
				
				
			for x in range (0,136192):
				if  1 < self.regmaskf[x] < 16:
					list = [ice6[x],ice7[x],ice8[x],ice9[x],ice10[x],ice11[x],ice12[x],ice13[x],ice14[x],ice15[x],ice16[x]]
					
					icemin = min(list)
					icemax = max(list)
					icefree = icemin
					countmin = 0
					countmax = 0
					countfree = 0
					
					for y in list:
						if y == icemin:
							countmin = countmin +1
							countfree = countmin
						if y == icemax:
							countmax = countmax +1 
					
					#min sea ice concentration
						
					if  ice6[x] == icemin:
						iceminyear[x] = 2006
					elif  ice7[x] == icemin:
						iceminyear[x] = 2007
					elif  ice8[x] == icemin:
						iceminyear[x] = 2008
					elif  ice9[x] == icemin:
						iceminyear[x] = 2009
					elif  ice10[x] == icemin:
						iceminyear[x] = 2010	
					elif  ice11[x] == icemin:
						iceminyear[x] = 2011
					elif  ice12[x] == icemin:
						iceminyear[x] = 2012
					elif  ice13[x] == icemin:
						iceminyear[x] = 2013
					elif  ice14[x] == icemin:
						iceminyear[x] = 2014
					elif  ice15[x] == icemin:
						iceminyear[x] = 2015
					elif  ice16[x] == icemin:
						iceminyear[x] = 2016
					if  countmin > 1:			
						iceminyear[x] = 0
					if  icemin > 225:
						iceminyear[x] = -2
						
					#max sea ice concentration
					
					if  ice6[x] == icemax:
						icemaxyear[x] = 2006
					elif  ice7[x] == icemax:
						icemaxyear[x] = 2007
					elif  ice8[x] == icemax:
						icemaxyear[x] = 2008
					elif  ice9[x] == icemax:
						icemaxyear[x] = 2009
					elif  ice10[x] == icemax:
						icemaxyear[x] = 2010
					elif  ice11[x] == icemax:
						icemaxyear[x] = 2011
					elif  ice12[x] == icemax:
						icemaxyear[x] = 2012
					elif  ice13[x] == icemax:
						icemaxyear[x] = 2013
					elif  ice14[x] == icemax:
						icemaxyear[x] = 2014
					elif  ice15[x] == icemax:
						icemaxyear[x] = 2015
					elif  ice16[x] == icemax:
						icemaxyear[x] = 2016
					if  countmax > 1:			
						icemaxyear[x] = -2
					if  icemax == 0:			
						icemaxyear[x] = 0	
					
					#ice free year
									
					elif  ice6[x] < 38:	
						icefreeyear[x] = 2006	
					elif  ice7[x] < 38:	
						icefreeyear[x] = 2007
					elif  ice8[x] < 38:	
						icefreeyear[x] = 2008
					elif  ice9[x] < 38:	
						icefreeyear[x] = 2009
					elif  ice10[x] < 38:	
						icefreeyear[x] = 2010
					elif  ice11[x] < 38:	
						icefreeyear[x] = 2011
					elif  ice12[x] < 38:	
						icefreeyear[x] = 2012
					elif  ice13[x] < 38:	
						icefreeyear[x] = 2013
					elif  ice14[x] < 38:	
						icefreeyear[x] = 2014
					elif  ice15[x] < 38:	
						icefreeyear[x] = 2015
					elif  ice16[x] < 38:	
						icefreeyear[x] = 2016						
					if  countfree > 9:			
						icefreeyear[x] = 0
					if  icefree > 37:
						icefreeyear[x] = -2		
									
					
						
				elif  self.regmaskf[x] > 16 or iceminyear[x] > 250:
					iceminyear[x] = 3333
					icemaxyear[x] = 3333
					icefreeyear[x] = 3333

			iceminyear = ma.masked_greater(iceminyear, 3000)
			icemaxyear = ma.masked_greater(icemaxyear, 3000)
			icefreeyear = ma.masked_greater(icefreeyear, 3000)
			
			self.normalshow(iceminyear,icemaxyear,icefreeyear)
				

			count = count+1			
			if count < countmax:
				self.day = self.day+1
				if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
					self.day=1
					self.month = self.month+1
				elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
					self.day=1
					self.month = self.month+1
				elif self.day==30 and self.month==2:
					self.day=1
					self.month = self.month+1
				elif  self.day==32 and self.month == 12:
					self.day = 1
					self.month = 1
					self.year = self.year+1
		plt.show()
		

	def normalshow(self,a,b,c):		
		iceminyear = a.reshape(448, 304)
		icemaxyear = b.reshape(448, 304)
		icefreeyear = c.reshape(448, 304)

		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = ma.masked_outside(iceminyear,2006,2016) 
		map2 = ma.masked_outside(icemaxyear,2006,2016) 
		map3 = ma.masked_outside(icefreeyear,2006,2016) 
		map11 = ma.masked_outside(iceminyear,-3,+2) 
		map22 = ma.masked_outside(icemaxyear,-3,+2) 
		map33 = ma.masked_outside(icefreeyear,-3,+2) 
		
		fig = plt.figure(figsize=(17, 8))
		fig.suptitle('Date: {}-{}'.format(self.stringmonth,self.stringday) , fontsize=14, fontweight='bold')
		
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)
		
		ax1.set_title('Lowest SIC by Year') 
		ax1.imshow(map1, interpolation='nearest', vmin=2006, vmax=2016, cmap=cmap)
		ax1.imshow(map11, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax2.set_title('Highest SIC by Year')
		ax2.imshow(map2, interpolation='nearest', vmin=2006, vmax=2016, cmap=cmap)
		ax2.imshow(map22, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax3.set_title('Icefree Year')
		cax = ax3.imshow(map3, interpolation='nearest', vmin=2006, vmax=2016, cmap=cmap)
		ax3.imshow(map33, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		cbar = fig.colorbar(cax, ticks=[2006,2008,2010,2012,2014,2016,]).set_label('Year')
		
		
		ax1.set_xlabel('white = Min SIC > 90%', fontsize=14)
		ax2.set_xlabel('white = Max SIC for multiple years', fontsize=14)
		ax3.set_xlabel('white = Min SIC > 15%', fontsize=14)
		
		ax1.axes.get_yaxis().set_ticks([])
		ax2.axes.get_yaxis().set_ticks([])
		ax3.axes.get_yaxis().set_ticks([])
		ax1.axes.get_xaxis().set_ticks([])
		ax2.axes.get_xaxis().set_ticks([])
		ax3.axes.get_xaxis().set_ticks([])
		
		fig.text(0.02, 0.95, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.02, 0.93, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.66, 0.03, 'https://sites.google.com/site/cryospherecomputing/YearlyData',)
		
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.88)
		fig.subplots_adjust(bottom=0.1)
		fig.savefig(os.path.join(self.ccpath,'Fun_concentration_map.png'))
			
		
	def automated (self,day,month):
		self.month = month
		self.day = day
		self.daycount = 1
		self.dayloop()
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	#action.dayloop()
	action.automated(1,10)
	
	
	
	#action.writetofile()
	#action.automated(1,2,2017) #note substract 3 days from last available day
	#action.makegraph()
	#action.makegraph_compaction()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA