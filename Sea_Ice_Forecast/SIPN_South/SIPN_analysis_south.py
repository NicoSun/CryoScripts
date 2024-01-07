'''
This analytical script should be run after the _tuning script. It has basically three functions:
1. calculate the error of every single year
2. calculate a mean error map of all years
3. create a bias correction map

Each step depends on the previous one. The order can not be reversed.
It is advisable to look at the mean error map and mean error values before creating the bias correction map.

@author: Nico Sun

'''
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt
import CryoIO

from datetime import date
from datetime import timedelta


class NSIDC_analysis:

	def __init__  (self):
		self.filepath = '/media/prussian/Cryosphere/NSIDC_South'
		self.filepath_SIPN = '/media/prussian/Cryosphere/Sea_Ice_Forecast'

		self.masksload()
		
		self.icenull = np.zeros(332*316, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		self.CSVDatum = ['Date']
		
	def masksload(self):
		''' Loads NSIDC masks and Daily Solar Energy Data'''
		
		filename = f'{self.filepath}/Masks/region_s_pure.msk'
		self.regmaskf = CryoIO.openfile(filename, np.uint8)
		
		filename = f'{self.filepath}/Masks/pss25area_v3.dat'
		self.areamaskf = CryoIO.openfile(filename, np.int32)/1000
		
		filename = f'{self.filepath}/Masks/pss25lats_v3.dat'
		self.latmaskf = CryoIO.openfile(filename, np.int32)/100000
		
		filename = f'{self.filepath}/Masks/pss25lons_v3.dat'
		self.lonmaskf = CryoIO.openfile(filename, np.int32)/100000
		
	
	def thickmap_create(self):
		''' creates a base matplotlib image for thickness'''
		self.fig, self.ax = plt.subplots(figsize=(8, 8))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,0.5,1,1.5,2,2.5,3]).set_label('Sea Ice Thickness in m')
		
	def conmap_create(self):
		''' creates a base matplotlib image for concentration'''
		self.fig2, self.ax2 = plt.subplots(figsize=(8, 8))
		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
		self.cbar = self.fig2.colorbar(self.cax2, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
		
	def errormap_create(self):
		''' creates a base matplotlib image for the correction map'''
		self.fig3, self.ax3 = plt.subplots(figsize=(8, 8))
		self.cax3 = self.ax3.imshow(self.icenull, interpolation='nearest', vmin=-1, vmax=1,cmap = plt.cm.coolwarm_r)
		self.cbar = self.fig3.colorbar(self.cax3, ticks=[-1,-.5,0,.5,1]).set_label('Sea Ice concentration in %')
	

	def thicknessshow(self,icemap,Volumevalue,extentvalue,outlooktype,datestring):
		''' creates the proper matplotlib image for thickness'''
		icemap = np.ma.masked_greater(icemap, 5)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Volumevalue = '{:,}'.format(Volumevalue)+' 'r'$km^3$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.get_cmap("jet").copy()
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('{}_Forecast , Date: {}'.format(outlooktype,datestring))
		#self.ax.set_title('Average Forecast')
		self.ax.set_xlabel('Volume: {} / Extent: {}'.format(Volumevalue,extentvalue), fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=3, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		plt.pause(0.1)
		
		
	def concentrationshow(self,icemap,Areavalue,extentvalue,outlooktype,datestring):
		''' creates the proper matplotlib image for concentration'''
		icemap = icemap/250
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Areavalue = '{:,}'.format(Areavalue)+' 'r'$km^2$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.get_cmap("jet").copy()
		cmap.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('{}_Forecast , Date: {}'.format(outlooktype,datestring))
		#self.ax.set_title('Average Forecast')
		self.ax2.set_xlabel('Area: {} / Extent: {}'.format(Areavalue,extentvalue), fontsize=14)
		self.cax2 = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
		plt.savefig('Images/{}'.format(datestring))
#		plt.pause(0.1)
		
	def errorshow(self,icemap,extent,calc_date,title):
		''' creates the proper matplotlib image for correction map'''
		icemap =np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(332, 316)
		
		cmap = plt.cm.get_cmap("coolwarm_r").copy()
		cmap.set_bad('black',0.6)
		
		self.ax3.clear()
		self.ax3.set_title('{}, Date: {}-{}-{}'.format(title,calc_date[1],calc_date[2],calc_date[3]))

		self.ax3.set_xlabel('Extent_Error: {}'.format(extent), fontsize=14)
		self.cax3 = self.ax3.imshow(icemap, interpolation='nearest', vmin=-1, vmax=1, cmap=cmap)
		
		self.ax3.axes.get_yaxis().set_ticks([])
		self.ax3.axes.get_xaxis().set_ticks([])
		self.ax3.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax3.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig3.tight_layout(pad=1)
		self.fig3.subplots_adjust(left=0.05)
# 		plt.pause(0.05)
		
	def calc_extent_error(self,icepredict,iceobserve,regionmask):
		''' calculates an extent error for a single day'''
		extent_over = 0
		extent_under = 0
		error_map = iceobserve
		
		if regionmask < 11:
			if iceobserve > 0.15 and icepredict < 0.15:
				extent_under = 1
				error_map = -1
			elif iceobserve < 0.15 and icepredict > 0.15:
				extent_over = 1
				error_map = 1
			else:
				error_map = 0

		if regionmask > 10:
			error_map = 0
		
		return error_map,extent_over,extent_under
	
	def show_mean_error(self,errormap,regionmask):
		''' calculates SIC error for a single day of the mean error map'''
		extent = 0
		if regionmask < 10:
			if abs(errormap) > 0.33:
				extent = 1
		if regionmask > 10:
			errormap = 5
		
		return errormap,extent
	
	def calc_difference(self,icepredict,iceobserve,filename_error):
		'''calculates the SIC error for a single day'''
		
		error_map = icepredict - iceobserve
		
		for x,y in enumerate(error_map):
			if self.regmaskf[x] > 10:
				error_map[x] = 0
		
		error_map = np.array(error_map*100,dtype=np.float16)
		CryoIO.savenumpy(filename_error,error_map)
		return
	
	def calcMean(self,data):
		'''calculates the mean grid cell value'''
		result = np.asarray(data).mean(0)
		return result
	
	def compute_error(self):
		'''loads data for computation of SIC error and extent error of a single day'''
		filename_obs = f'{self.filepath}/DataFiles/{self.year}/NSIDC_{self.datestring}_south.bin'
		filename_pre = f'analysis/predict/SIPN2_{self.datestring}.npz'
		
		if mode == 'base':
			filename_error = f'analysis/forecast/SIPN2_error_{self.datestring}.npz'
			filename_extent_error = f'analysis/forecast_extent/SIPN2_error_{self.datestring}.npz'
		elif mode == 'corrected':
			filename_error = f'analysis/drifterror_new/SIPN2_error_{self.datestring}.npz'
			filename_extent_error = f'analysis/extent_error_new/SIPN2_error_{self.datestring}.npz'
		
		
		iceobserve = CryoIO.openfile(filename_obs,np.uint8)/250
		iceforecast = CryoIO.readnumpy(filename_pre)/250
		
		#SIC error
		self.calc_difference(iceforecast,iceobserve,filename_error)
		
		#---------------------------
		#extent error
		aaa = np.vectorize(self.calc_extent_error)
		error_map,extent_over,extent_under = aaa(iceforecast,iceobserve,self.regmaskf)
		export = np.array(error_map*100, dtype=np.int8)
		CryoIO.savenumpy(filename_extent_error,export)
		
		extent_over = sum(extent_over)
		extent_under = sum(extent_under)
		extent_total = extent_over + extent_under
		self.extent_list_over.append(extent_over)
		self.extent_list_under.append(extent_under)
		self.extent_list_total.append(extent_total)
		self.CSVDatum.append(self.datestring)
		
	def mix_errormaps(self,sic_error,extent_error):
		''' creates the bias correction map '''
		errormap = extent_error
		
				
		'''SIPN North model'''
		for x in range(0,len(self.regmaskf)):
			if self.regmaskf[x] < 11 and self.latmaskf[x] < -54:
				errormap[x] = (sic_error[x] + extent_error[x]/1.5)
			elif self.regmaskf[x] > 10:
				errormap[x] = 5
					
		return errormap
	
	def create_correction_maps(self,calc_date):
		''' loads data to create the bias correction map '''
		yesterday = calc_date[0]-timedelta(days=2)
		stringmonth = str(yesterday.month).zfill(2)
		stringday = str(yesterday.day).zfill(2)
		
		
		if mode == 'base':
			# to create base error maps
			filename_mean_error = 'analysis/mean_drifterror/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
			filename_mean_error_extent = 'analysis/mean_drifterror_extent/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
		elif mode == 'corrected':
			#to create error maps with drift correction
			filename_mean_error = 'analysis/mean_drifterror_new/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
			filename_mean_error_extent = 'analysis/mean_drifterror_extent_new/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
		
		mixmap_name = 'analysis/icedrift_correction/SIPN2_error_{}{}.npz'.format(stringmonth,stringday)
		
		error_map = CryoIO.readnumpy(filename_mean_error)/100
		error_map2 = CryoIO.readnumpy(filename_mean_error_extent)/100
		
		mix_map = self.mix_errormaps(error_map,error_map2)
		
		if mode == 'base':
			export = np.array(mix_map*100,dtype=np.float16)
			CryoIO.savenumpy(mixmap_name,export)
		
		self.errorshow(mix_map,5,calc_date,'Correction Map')
		self.fig3.savefig('Images/Correction/Correction_Map_{}{}{}'.format(calc_date[1],calc_date[2],calc_date[3]))
	
	
	def calc_error_of_mean_grid(self,calc_date):
		'''calculates the error of the mean error maps'''
		if mode == 'base':
			# to create base error maps
			SIC_map = 'analysis/mean_drifterror/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
			extent_map = 'analysis/mean_drifterror_extent/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
		elif mode == 'corrected':
			#to create error maps with drift correction
			SIC_map = 'analysis/mean_drifterror_new/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
			extent_map = 'analysis/mean_drifterror_extent_new/SIPN2_error_{}{}.npz'.format(calc_date[2],calc_date[3])
		
		#---------------------------
		#show mean error
		error_map1 = CryoIO.readnumpy(SIC_map)/100
		aaa = np.vectorize(self.show_mean_error)
		error_map1,extent1 = aaa(error_map1,self.regmaskf)
		
		error_map2 = CryoIO.readnumpy(extent_map)/100
		aaa = np.vectorize(self.show_mean_error)
		error_map2,extent2 = aaa(error_map2,self.regmaskf)
		#---------------------------
		
		extent1 = sum(extent1)
		extent2 = sum(extent2)
		
		if mode == 'base':
			self.errorshow(error_map1,extent1,calc_date,'SIC Error Base')
			self.fig3.savefig('Images/SIC_base/SIC_{}{}'.format(calc_date[2],calc_date[3]))
			self.errorshow(error_map2,extent2,calc_date,'Extent Error Base')
			self.fig3.savefig('Images/SIE_base/SIE_{}{}'.format(calc_date[2],calc_date[3]))
		elif mode == 'corrected':
			self.errorshow(error_map1,extent1,calc_date,'SIC Error New')
			self.fig3.savefig('Images/SIC_new/SIC_{}{}'.format(calc_date[2],calc_date[3]))
			self.errorshow(error_map2,extent2,calc_date,'Extent Error New')
			self.fig3.savefig('Images/SIE_new/SIE_{}{}'.format(calc_date[2],calc_date[3]))
		
		return '{}/{}/{}'.format(calc_date[1],calc_date[2],calc_date[3]), extent1, extent2

	def create_mean_error_grid(self):
		''''calculates a mean error map for the entire dataset'''
		
		self.start = date(2012, 11, 30)
		self.loopday	= self.start
		self.index = self.loopday.timetuple().tm_yday
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
		countmax = self.index + period -1 #91 to 28th February
		for count in range (self.index,countmax,1):
			
			data = []
			data_extent = []
		
			if mode == 'base':
				# to create base error maps
				filename_out = 'analysis/mean_drifterror/SIPN2_error_{}{}.npz'.format(self.stringmonth,self.stringday)
				filename_out_extent = 'analysis/mean_drifterror_extent/SIPN2_error_{}{}.npz'.format(self.stringmonth,self.stringday)
			elif mode == 'corrected':
				#to create error maps with drift correction
				filename_out = 'analysis/mean_drifterror_new/SIPN2_error_{}{}.npz'.format(self.stringmonth,self.stringday)
				filename_out_extent = 'analysis/mean_drifterror_extent_new/SIPN2_error_{}{}.npz'.format(self.stringmonth,self.stringday)
	
			for year in range(startyear,endyear):
				year2 = year
				if self.loopday.month < 11:
					year2 = year + 1
					
				if mode == 'base':
					filename_error = 'analysis/forecast/SIPN2_error_{}{}{}.npz'.format(year2,self.stringmonth,self.stringday)
					filename_error_extent = 'analysis/forecast_extent/SIPN2_error_{}{}{}.npz'.format(year2,self.stringmonth,self.stringday)
				elif mode == 'corrected':
					filename_error = 'analysis/drifterror_new/SIPN2_error_{}{}{}.npz'.format(year2,self.stringmonth,self.stringday)
					filename_error_extent = 'analysis/extent_error_new/SIPN2_error_{}{}{}.npz'.format(year2,self.stringmonth,self.stringday)
				
				ice = CryoIO.readnumpy(filename_error) #int8
				ice_extent = CryoIO.readnumpy(filename_error_extent) #float16
				
				data.append(ice)
				data_extent.append(ice_extent)
				
			self.advanceday(1)
			print(self.datestring)
		
			ice = self.calcMean(data)
			ice_extent = self.calcMean(data_extent)
			export = np.array(ice, dtype=np.float16)
			export_extent = np.array(ice_extent, dtype=np.float16)
			CryoIO.savenumpy(filename_out,export)
			CryoIO.savenumpy(filename_out_extent,export_extent)

	
	def advanceday(self,delta):
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
	def dateloop(self,year,month,day):
		''' Starts the day loop'''
		self.start = date(year, month, day)
		self.loopday	= self.start
		self.index = self.loopday.timetuple().tm_yday
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.datestring = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
		self.extent_list_over = [f'Over_{year}']
		self.extent_list_under = [f'Under_{year}']
		self.extent_list_total = [f'total_{year}']
		
		countmax = self.index + period #91 to 28th February
		for count in range (self.index,countmax,1):
			self.compute_error()
			self.advanceday(1)
			print(self.datestring)
			
		return self.extent_list_under,self.extent_list_over,self.extent_list_total
			


def spawnprocess(year):
	action = NSIDC_analysis()
	extent1,extent2,extent3 = action.dateloop(year,start[0],start[1])
	return extent1,extent2,extent3

def spawnprocess_mean_calc(date):
	action = NSIDC_analysis()
	action.errormap_create()
	value1,value2, value3 = action.calc_error_of_mean_grid(date)
	return value1,value2, value3

def spawnprocess_correction_map(date):
	action = NSIDC_analysis()
	action.errormap_create()
	action.create_correction_maps(date)
	return

def dateloop():
	datelist = []
	startdate = date(2012,start[0],start[1])
	loopday	= startdate
	
	for count in range (0,period - 1): #91
		year = str(loopday.year)
		stringmonth = str(loopday.month).zfill(2)
		stringday = str(loopday.day).zfill(2)
		datelist.append([loopday,year,stringmonth,stringday])
		loopday = loopday+timedelta(days=1)
	return datelist

def calcMeanerrorgrid():
	'''calculation for mean error grid'''
	print('Mean Error Calc')
	action = NSIDC_analysis()
	action.create_mean_error_grid()
	datelist = dateloop()
	p = Pool(processes=24)
	data = p.map(spawnprocess_mean_calc, datelist)
	print(len(data))
	p.close()
	CryoIO.csv_columnexport(f'analysis/mean_error_{mode}.csv',[data])
	
def calcCorrectiongrid():
	'''calculation for mean error grid'''
	datelist = dateloop()
	p = Pool(processes=24)
	data = p.map(spawnprocess_correction_map, datelist)
	p.close()
	
def calcsingleyearerror():
	'''calculation for single year error grids'''
	datalist = []
	for year in range(startyear,endyear):
		datalist.append(year)
	
	p = Pool(processes=24)
	data = p.map(spawnprocess, datalist)
	print(len(data))
	p.close()
	
	extent_under = []
	extent_over = []
	extent_total = []
	for x in data:
		extent_under.append(x[0])
		extent_over.append(x[1])
		extent_total.append(x[2])
		
# 	action = NSIDC_analysis()
	CryoIO.csv_columnexport('analysis/extent_under.csv',extent_under)
	CryoIO.csv_columnexport('analysis/extent_over.csv',extent_over)
# 	CryoIO.csv_columnexport('analysis/extent_total.csv',extent_total)
	
mode = 'corrected' # base, corrected
period = 92 # 91 summer , 122 winter
start = [11,30] # [11,30] summer , [6,1] winter

startyear = 1980
endyear = 2022

if __name__ == '__main__':
	calcsingleyearerror()
	calcMeanerrorgrid()
# 	calcCorrectiongrid()


'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''