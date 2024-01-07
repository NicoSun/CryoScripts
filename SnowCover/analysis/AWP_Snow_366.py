import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.pyplot as plt

from datetime import date
import time

class AWP_model:

	def __init__  (self):
		self.start = date(2019,1,1) #1997-02-05 first day
		self.loopday	= self.start
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
		
		self.daycount = 29 #366year,
		self.masksload()
		self.init_regionlists()
		self.CSVDatum = ['Date']
		
		
		self.starttime = time.time()
# =============================================================================
# 		self.fig, self.ax = plt.subplots(figsize=(8, 10))
# 		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
# =============================================================================
		
		# (1-albedo)
		self.land_absorb = (1 - 0.25)
		self.ice_absorb = (1 - 0.6)
		self.snow_absorb = (1 - 0.8)
		
		self.tundra_absorb = (1 - 0.3)
		self.tundra_snow_absorb = (1 - 0.8)
		self.forest_absorb = (1 - 0.15)
		self.forest_snow_absorb = (1 - 0.6)
		self.grass_absorb = (1 - 0.25)
		self.grass_snow_absorb = (1 - 0.75)
		self.bareland_absorb = (1 - 0.3)
		self.bareland_snow_absorb = (1 - 0.8)
		
	def init_regionlists(self):
		self.Ocean = ['Ice-Ocean']
		self.NorthAmerica = [['Canada','USA','eastern Canada','Central Canada','Canadian Rockies','northern Canada',
					'Alaska','US NE','US MidWest','US Pacific','US Rockies']]
		self.Greenland = ['Greenland AWP']
		self.Europe = [['Europe','Scandinavia','West Europe','Central Europe','Southern Europe','Eastern Europe']]
		self.Asia = [['Siberia','East Siberia','Central Siberial','West Siberia','Central Asia',
				'Central Mountain Asia','Eastern Asia','Tibet']]
		
		self.Ocean_anom = ['Ice-Ocean anomaly']
		self.NorthAmerica_anom = [['Canada','USA','eastern Canada','Central Canada','Canadian Rockies','northern Canada',
					'Alaska','US NE','US MidWest','US Pacific','US Rockies']]
		self.Greenland_anom = ['Greenland']
		self.Europe_anom = [['Europe','Scandinavia','West Europe','Central Europe','Southern Europe','Eastern Europe']]
		self.Asia_anom = [['Siberia','East Siberia','Central Siberial','West Siberia','Central Asia','Mountain Asia','Eastern Asia','Tibet']]
		
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		'''
		filename = 'X:/SnowCover/Masks/Biome_mask.msk'
		with open(filename, 'rb') as fr:
			self.Biomemask = np.fromfile(fr, dtype='uint8')
		filename = 'X:/SnowCover/Masks/Pixel_area_crop.msk'
		with open(filename, 'rb') as fr:
			self.pixelarea = np.fromfile(fr, dtype='uint16')
		filename = 'X:/SnowCover/Masks/Latitude_Mask.msk'
		with open(filename, 'rb') as fr:
			self.Latitude_Mask = np.fromfile(fr, dtype='float32')
			
		filename = 'X:/SnowCover/Masks/Max_SnowCover.msk'
		with open(filename, 'rb') as fr:
			self.Snow_Mask = np.fromfile(fr, dtype='uint8')
		filename = 'X:/SnowCover/Masks/SubRegion_Mask.msk'
		with open(filename, 'rb') as fr:
			self.SubRegion_Mask = np.fromfile(fr, dtype='uint8')
			
			
		
			
# =============================================================================
# 		Mask = self.SubRegion_Mask.reshape(610,450)
# 		plt.imshow(Mask)
# 		plt.tight_layout(pad=0)
# 		plt.show()
# =============================================================================
	
		
		#latitudes [20 to 90, step = 0.2]
		self.energy_lat_list = np.loadtxt('Masks/Lattable_MJ_all_year.csv', delimiter=',')
		self.energy_lat_list_water = np.loadtxt('Masks/Lattable_MJ_all_year_water.csv', delimiter=',')
		
	def listclear(self):
		'''define lists for regional calculation'''
			
		#AWP lists
		self.Ocean_calc = []
			
		self.Eastern_Canada_calc = []
		self.Central_Canada_calc = []
		self.Rockies_Canada_calc = []
		self.Northern_Canada_calc = []
		self.Alaska_calc = []
		self.US_NE_calc = []
		self.US_SE_calc = []
		self.US_MW_calc = []
		self.US_SW_calc = []
		self.US_Pacific_calc = []
		self.US_Rocki_calc = []
			
		self.Greenland_calc = []
			
		self.Scandinavia_calc = []
		self.West_Europe_calc = []
		self.Cent_Europe_calc = []
		self.South_Europe_calc = []
		self.East_Europe_calc = []
			
		self.East_sib_calc = []
		self.Cent_sib_calc = []
		self.West_sib_calc = []
		self.Cent_Asia_calc = []
		self.Mount_Asia_calc = []
		self.East_Asia_calc = []
		self.Tibet_calc = []
		
		# AWP anomaly lists
		self.Ocean_calc_anom = []

		self.Eastern_Canada_calc_anom = []
		self.Central_Canada_calc_anom = []
		self.Rockies_Canada_calc_anom = []
		self.Northern_Canada_calc_anom = []
		self.Alaska_calc_anom = []
		self.US_NE_calc_anom = []
		self.US_SE_calc_anom = []
		self.US_MW_calc_anom = []
		self.US_SW_calc_anom = []
		self.US_Pacific_calc_anom = []
		self.US_Rocki_calc_anom = []
		
		self.Greenland_calc_anom = []
		
		self.Scandinavia_calc_anom = []
		self.West_Europe_calc_anom = []
		self.Cent_Europe_calc_anom = []
		self.South_Europe_calc_anom = []
		self.East_Europe_calc_anom = []
		
		self.East_sib_calc_anom = []
		self.Cent_sib_calc_anom = []
		self.West_sib_calc_anom = []
		self.Cent_Asia_calc_anom = []
		self.Mount_Asia_calc_anom = []
		self.East_Asia_calc_anom = []
		self.Tibet_calc_anom = []
		
		#AWP area lists
		self.Ocean_area = []
		
		self.Eastern_Canada_area = []
		self.Central_Canada_area = []
		self.Rockies_Canada_area = []
		self.Northern_Canada_area = []
		self.Alaska_area = []
		self.US_NE_area = []
		self.US_SE_area = []
		self.US_MW_area = []
		self.US_SW_area = []
		self.US_Pacific_area = []
		self.US_Rocki_area = []
			
		self.Greenland_area = []
			
		self.Scandinavia_area = []
		self.West_Europe_area = []
		self.Cent_Europe_area = []
		self.South_Europe_area = []
		self.East_Europe_area = []
			
		self.East_sib_area = []
		self.Cent_sib_area = []
		self.West_sib_area = []
		self.Cent_Asia_area = []
		self.Mount_Asia_area = []
		self.East_Asia_area = []
		self.Tibet_area = []
		
	def listsappend(self):
		'''adds area corrected AWP to main lists'''
		self.Ocean.append (round((np.sum(self.Ocean_calc)/np.sum(self.Ocean_area)),3))
		self.Greenland.append (round((np.sum(self.Greenland_calc)/np.sum(self.Greenland_area)),3))
		self.Ocean_anom.append (round((np.sum(self.Ocean_calc_anom)/np.sum(self.Ocean_area)),3))
		self.Greenland_anom.append (round((np.sum(self.Greenland_calc_anom)/np.sum(self.Greenland_area)),3))
		
		#AWP lists
		calclist = [self.Eastern_Canada_calc,self.Central_Canada_calc,self.Rockies_Canada_calc,self.Northern_Canada_calc]
		arealist = [self.Eastern_Canada_area,self.Central_Canada_area,self.Rockies_Canada_area,self.Northern_Canada_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Canada = round(calclist_sum/arealist_sum,3)
		
		calclist = [self.US_NE_calc,self.US_MW_calc,self.US_Pacific_calc,self.US_Rocki_calc,self.US_SE_calc,self.US_SW_calc]
		arealist = [self.US_NE_area,self.US_MW_area,self.US_Pacific_area,self.US_Rocki_area,self.US_SE_area,self.US_SW_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		USA = round(calclist_sum/arealist_sum,3)
		
		Eastern_Canada = round((np.sum(self.Eastern_Canada_calc)/np.sum(self.Eastern_Canada_area)),3)
		Central_Canada = round((np.sum(self.Central_Canada_calc)/np.sum(self.Central_Canada_area)),3)
		Rockies_Canada = round((np.sum(self.Rockies_Canada_calc)/np.sum(self.Rockies_Canada_area)),3)
		Northern_Canada_area = round((np.sum(self.Northern_Canada_calc)/np.sum(self.Northern_Canada_area)),3)
		Alaska = round((np.sum(self.Alaska_calc)/np.sum(self.Alaska_area)),3)
		US_NE = round((np.sum(self.US_NE_calc)/np.sum(self.US_NE_area)),3)
		US_MW = round((np.sum(self.US_MW_calc)/np.sum(self.US_MW_area)),3)
		US_Pacific = round((np.sum(self.US_Pacific_calc)/np.sum(self.US_Pacific_area)),3)
		Rocki = round((np.sum(self.US_Rocki_calc)/np.sum(self.US_Rocki_area)),3)
		self.NorthAmerica.append([Canada,USA,Eastern_Canada,Central_Canada,Rockies_Canada,Northern_Canada_area,Alaska,US_NE,US_MW,US_Pacific,Rocki])

		calclist = [self.Scandinavia_calc,self.West_Europe_calc,self.Cent_Europe_calc,self.South_Europe_calc,self.East_Europe_calc]
		arealist = [self.Scandinavia_area,self.West_Europe_area,self.Cent_Europe_area,self.South_Europe_area,self.East_Europe_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Europe = round(calclist_sum/arealist_sum,3)
		
		Scandinavia = round((np.sum(self.Scandinavia_calc)/np.sum(self.Scandinavia_area)),3)
		West_Europe = round((np.sum(self.West_Europe_calc)/np.sum(self.West_Europe_area)),3)
		Cent_Europe = round((np.sum(self.Cent_Europe_calc)/np.sum(self.Cent_Europe_area)),3)
		South_Europe = round((np.sum(self.South_Europe_calc)/np.sum(self.South_Europe_area)),3)
		East_Europe = round((np.sum(self.East_Europe_calc)/np.sum(self.East_Europe_area)),3)
		self.Europe.append ([Europe,Scandinavia,West_Europe,Cent_Europe,South_Europe,East_Europe])
		
		
		calclist = [self.East_sib_calc,self.Cent_sib_calc,self.West_sib_calc]
		arealist = [self.East_sib_area,self.Cent_sib_area,self.West_sib_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Siberia = round(calclist_sum/arealist_sum,3)
		
		calclist = [self.Cent_Asia_calc,self.Mount_Asia_calc,self.East_Asia_calc,self.Tibet_calc]
		arealist = [self.Cent_Asia_area,self.Mount_Asia_area,self.East_Asia_area,self.Tibet_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Asia = round(calclist_sum/arealist_sum,3)
		
		East_sib = round((np.sum(self.East_sib_calc)/np.sum(self.East_sib_area)),3)
		Cent_sib = round((np.sum(self.Cent_sib_calc)/np.sum(self.Cent_sib_area)),3)
		West_sib = round((np.sum(self.West_sib_calc)/np.sum(self.West_sib_area)),3)
		Cent_Asia = round((np.sum(self.Cent_Asia_calc)/np.sum(self.Cent_Asia_area)),3)
		Mount_Asia = round((np.sum(self.Mount_Asia_calc)/np.sum(self.Mount_Asia_area)),3)
		East_Asia = round((np.sum(self.East_Asia_calc)/np.sum(self.East_Asia_area)),3)
		Tibet = round((np.sum(self.Tibet_calc)/np.sum(self.Tibet_area)),3)
		self.Asia.append ([Siberia,East_sib,Cent_sib,West_sib,Cent_Asia,Mount_Asia,East_Asia,Tibet])
		
		
		# Anomaly anomaly lists
		calclist = [self.Eastern_Canada_calc_anom,self.Central_Canada_calc_anom,self.Rockies_Canada_calc_anom,self.Northern_Canada_calc_anom]
		arealist = [self.Eastern_Canada_area,self.Central_Canada_area,self.Rockies_Canada_area,self.Northern_Canada_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Canada = round(calclist_sum/arealist_sum,3)
		
		calclist = [self.US_NE_calc_anom,self.US_MW_calc_anom,self.US_Pacific_calc_anom,self.US_Rocki_calc_anom,self.US_SE_calc_anom,self.US_SW_calc_anom]
		arealist = [self.US_NE_area,self.US_MW_area,self.US_Pacific_area,self.US_Rocki_area,self.US_SE_area,self.US_SW_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		USA = round(calclist_sum/arealist_sum,3)
		
		Eastern_Canada = round((np.sum(self.Eastern_Canada_calc_anom)/np.sum(self.Eastern_Canada_area)),3)
		Central_Canada = round((np.sum(self.Central_Canada_calc_anom)/np.sum(self.Central_Canada_area)),3)
		Rockies_Canada = round((np.sum(self.Rockies_Canada_calc_anom)/np.sum(self.Rockies_Canada_area)),3)
		Northern_Canada_area = round((np.sum(self.Northern_Canada_calc_anom)/np.sum(self.Northern_Canada_area)),3)
		Alaska = round((np.sum(self.Alaska_calc_anom)/np.sum(self.Alaska_area)),3)
		US_NE = round((np.sum(self.US_NE_calc_anom)/np.sum(self.US_NE_area)),3)
		US_MW = round((np.sum(self.US_MW_calc_anom)/np.sum(self.US_MW_area)),3)
		US_Pacific = round((np.sum(self.US_Pacific_calc_anom)/np.sum(self.US_Pacific_area)),3)
		Rocki = round((np.sum(self.US_Rocki_calc_anom)/np.sum(self.US_Rocki_area)),3)
		self.NorthAmerica_anom.append([Canada,USA,Eastern_Canada,Central_Canada,Rockies_Canada,Northern_Canada_area,Alaska,US_NE,US_MW,US_Pacific,Rocki])

		calclist = [self.Scandinavia_calc_anom,self.West_Europe_calc_anom,self.Cent_Europe_calc_anom,self.South_Europe_calc_anom,self.East_Europe_calc_anom]
		arealist = [self.Scandinavia_area,self.West_Europe_area,self.Cent_Europe_area,self.South_Europe_area,self.East_Europe_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Europe = round(calclist_sum/arealist_sum,3)

		Scandinavia = round((np.sum(self.Scandinavia_calc_anom)/np.sum(self.Scandinavia_area)),3)
		West_Europe = round((np.sum(self.West_Europe_calc_anom)/np.sum(self.West_Europe_area)),3)
		Cent_Europe = round((np.sum(self.Cent_Europe_calc_anom)/np.sum(self.Cent_Europe_area)),3)
		South_Europe = round((np.sum(self.South_Europe_calc_anom)/np.sum(self.South_Europe_area)),3)
		East_Europe = round((np.sum(self.East_Europe_calc_anom)/np.sum(self.East_Europe_area)),3)
		self.Europe_anom.append ([Europe,Scandinavia,West_Europe,Cent_Europe,South_Europe,East_Europe])
		
		calclist = [self.East_sib_calc_anom,self.Cent_sib_calc_anom,self.West_sib_calc_anom]
		arealist = [self.East_sib_area,self.Cent_sib_area,self.West_sib_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Siberia = round(calclist_sum/arealist_sum,3)
		
		calclist = [self.Cent_Asia_calc_anom,self.Mount_Asia_calc_anom,self.East_Asia_calc_anom,self.Tibet_calc_anom]
		arealist = [self.Cent_Asia_area,self.Mount_Asia_area,self.East_Asia_area,self.Tibet_area]
		calclist_sum = sum([sum(b) for b in calclist])
		arealist_sum = sum([sum(b) for b in arealist])
		Asia = round(calclist_sum/arealist_sum,3)
		
		East_sib = round((np.sum(self.East_sib_calc_anom)/np.sum(self.East_sib_area)),3)
		Cent_sib = round((np.sum(self.Cent_sib_calc_anom)/np.sum(self.Cent_sib_area)),3)
		West_sib = round((np.sum(self.West_sib_calc_anom)/np.sum(self.West_sib_area)),3)
		Cent_Asia = round((np.sum(self.Cent_Asia_calc_anom)/np.sum(self.Cent_Asia_area)),3)
		Mount_Asia = round((np.sum(self.Mount_Asia_calc_anom)/np.sum(self.Mount_Asia_area)),3)
		East_Asia = round((np.sum(self.East_Asia_calc_anom)/np.sum(self.East_Asia_area)),3)
		Tibet = round((np.sum(self.Tibet_calc_anom)/np.sum(self.Tibet_area)),3)
		self.Asia_anom.append ([Siberia,East_sib,Cent_sib,West_sib,Cent_Asia,Mount_Asia,East_Asia,Tibet])
		
	
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		AWPdaily = np.zeros(104912, dtype=float)
		AWP_anomaly = np.zeros(104912, dtype=float)
		
		for x in range (0,self.daycount): #366
			self.stringyearday = str(self.yearday).zfill(3)
#			self.stringstringyearday2 = str(self.yearday-1).zfill(3)
			filenameMean = 'X:/SnowCover/DataFiles/Mean/NOAA_Mean_{}_24km.bin'.format(self.stringyearday)
			filename = 'X:/SnowCover/Datafiles/NOAA_{}{}_24km.bin'.format(self.year,self.stringyearday)
#			filenameyesterday = 'X:/SnowCover/Datafiles/NOAA_{}{}_24km.bin'.format(self.year,self.stringstringyearday2)

			
			# loads the mean data file
			with open(filenameMean, 'rb') as fr:
				snowMean = np.fromfile(fr, dtype=np.float16)
			try:
				with open(filename, 'rb') as fr:
					snow = np.fromfile(fr, dtype='uint8')
			except:
				print('no 366 day')
			snowMean = np.array(snowMean,dtype=np.float)
			
			self.snow = snow
			
			self.listclear()
			#calculate the map
			aaa = np.vectorize(self.energycalc)
			AWPdaily,AWP_anomaly = aaa(self.snow,snowMean,self.Biomemask,self.Latitude_Mask)
			
			self.CSVDatum.append('{}-{}'.format(self.year,self.stringyearday))

			#calculate the map
			bbb = np.vectorize(self.regional_AWP)
			bbb(AWPdaily,AWP_anomaly,self.SubRegion_Mask,self.pixelarea,self.Snow_Mask)
			
			#append regional lists
			self.listsappend()

			print(self.year ,self.stringyearday)
			self.advanceday(1)
		end = time.time()
		print(end-self.starttime)
#		self.writetofile()
		self.end = 'true'
# =============================================================================
# 		with open('CSVexport/AWP_anomaly_'+str(self.year-1)+'-'+str(self.year)+'_s.bin', 'wb') as writecumu:
# 			icewr = writecumu.write(AWPcumulative)
# =============================================================================
#		self.fig2.savefig('CSVexport/Final_'+str(self.year-1)+'-'+str(self.year)+'.png')
		plt.show()
		
	def advanceday(self,delta):	
		if self.yearday < 366:
			self.yearday += 1
		else:
			self.yearday = 1
			self.year += 1
			
	
	def energycalc(self,snow,snowMean,Biomemask,latmask):
		'''AWP energy calculation & Regional breakdown'''
# =============================================================================
# 		AWPdaily_areaweighted = np.nan
# 		AWPdaily_oceanarea = np.nan
# 		AWPcumulative_areaweighted = np.nan
# 		AWPcumulative_oceanarea = np.nan
# =============================================================================
		snowanomaly = (snow-snowMean/10)*(-1)
		pixlat = max(20,latmask)
		indexx = int(round((pixlat-20)*(5)))
		MJ = self.energy_lat_list[indexx][self.yearday]
		MJ_w = self.energy_lat_list_water[indexx][self.yearday]
		
		if snow==1:
			AWPdaily = MJ_w
			AWP_anomaly = snowanomaly * (MJ_w - MJ * self.ice_absorb)
		elif snow==2:
			snowanomaly = ((snow+1)-snowMean/10) *(-1)
			if Biomemask == 10:
				AWPdaily =  MJ * self.tundra_absorb
				AWP_anomaly = snowanomaly * MJ * (self.tundra_absorb - self.tundra_snow_absorb)
			elif Biomemask == 20:
				AWPdaily =  MJ * self.forest_absorb
				AWP_anomaly = snowanomaly * MJ * (self.forest_absorb - self.forest_snow_absorb)
			elif Biomemask == 30:
				AWPdaily =  MJ * self.grass_absorb
				AWP_anomaly = snowanomaly * MJ * (self.grass_absorb - self.grass_snow_absorb)
			elif Biomemask == 40:
				AWPdaily =  MJ * self.bareland_absorb
				AWP_anomaly = snowanomaly * MJ * (self.bareland_absorb - self.bareland_snow_absorb)
			elif Biomemask == 50:
				AWPdaily =  MJ * self.grass_absorb
				AWP_anomaly = snowanomaly * MJ * (self.grass_absorb - self.grass_snow_absorb)
			else:
				AWPdaily =  MJ * self.land_absorb
				AWP_anomaly = snowanomaly * MJ * (self.land_absorb - self.snow_absorb)
			

		elif snow==3:
			snowanomaly = ((snow-1)-snowMean/10) *(-1)
			AWPdaily =  MJ * self.ice_absorb
			AWP_anomaly =snowanomaly * (MJ_w - MJ * self.ice_absorb)
		elif snow==4:
			if Biomemask == 10:
				AWPdaily =  MJ * self.tundra_snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.tundra_absorb - self.tundra_snow_absorb)
			elif Biomemask == 20:
				AWPdaily =  MJ * self.forest_snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.forest_absorb - self.forest_snow_absorb)
			elif Biomemask == 30:
				AWPdaily =  MJ * self.grass_snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.grass_absorb - self.grass_snow_absorb)
			elif Biomemask == 40:
				AWPdaily =  MJ * self.bareland_snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.bareland_absorb - self.bareland_snow_absorb)
			elif Biomemask == 50:
				AWPdaily =  MJ * self.grass_snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.grass_absorb - self.grass_snow_absorb)
			else:
				AWPdaily =  MJ * self.snow_absorb
				AWP_anomaly = snowanomaly * MJ * (self.land_absorb - self.snow_absorb)
			
		return AWPdaily,AWP_anomaly
	
	def regional_AWP(self,AWPdaily,AWP_anomaly,subregmask,areamask,Snowmask):
		if Snowmask==5:
			if subregmask == 1:
				self.Ocean_calc.append(AWPdaily*areamask)
				self.Ocean_calc_anom.append(AWP_anomaly*areamask)
				self.Ocean_area.append(areamask)
			elif subregmask == 50:
				self.Greenland_calc.append(AWPdaily*areamask)
				self.Greenland_calc_anom.append(AWP_anomaly*areamask)
				self.Greenland_area.append(areamask)
			#Canada Regions
			if subregmask == 10:
				self.Eastern_Canada_calc.append(AWPdaily*areamask)
				self.Eastern_Canada_calc_anom.append(AWP_anomaly*areamask)
				self.Eastern_Canada_area.append(areamask)
			elif subregmask == 12:
				self.Central_Canada_calc.append(AWPdaily*areamask)
				self.Central_Canada_calc_anom.append(AWP_anomaly*areamask)
				self.Central_Canada_area.append(areamask)
			elif subregmask == 16:
				self.Northern_Canada_calc.append(AWPdaily*areamask)
				self.Northern_Canada_calc_anom.append(AWP_anomaly*areamask)
				self.Northern_Canada_area.append(areamask)
			elif subregmask == 18:
				self.Rockies_Canada_calc.append(AWPdaily*areamask)
				self.Rockies_Canada_calc_anom.append(AWP_anomaly*areamask)
				self.Rockies_Canada_area.append(areamask)
			#USA Regions
			elif subregmask == 20:
				self.Alaska_calc.append(AWPdaily*areamask)
				self.Alaska_calc_anom.append(AWP_anomaly*areamask)
				self.Alaska_area.append(areamask)
			elif subregmask == 21:
				self.US_NE_calc.append(AWPdaily*areamask)
				self.US_NE_calc_anom.append(AWP_anomaly*areamask)
				self.US_NE_area.append(areamask)
			elif subregmask == 22:
				self.US_SE_calc.append(AWPdaily*areamask)
				self.US_SE_calc_anom.append(AWP_anomaly*areamask)
				self.US_SE_area.append(areamask)
			elif subregmask == 23:
				self.US_MW_calc.append(AWPdaily*areamask)
				self.US_MW_calc_anom.append(AWP_anomaly*areamask)
				self.US_MW_area.append(areamask)
			elif subregmask == 24:
				self.US_SW_calc.append(AWPdaily*areamask)
				self.US_SW_calc_anom.append(AWP_anomaly*areamask)
				self.US_SW_area.append(areamask)
			elif subregmask == 25:
				self.US_Pacific_calc.append(AWPdaily*areamask)
				self.US_Pacific_calc_anom.append(AWP_anomaly*areamask)
				self.US_Pacific_area.append(areamask)
			elif subregmask == 26:
				self.US_Rocki_calc.append(AWPdaily*areamask)
				self.US_Rocki_calc_anom.append(AWP_anomaly*areamask)
				self.US_Rocki_area.append(areamask)
			#Asia regions
			elif subregmask == 30:
				self.East_sib_calc.append(AWPdaily*areamask)
				self.East_sib_calc_anom.append(AWP_anomaly*areamask)
				self.East_sib_area.append(areamask)
			elif subregmask == 31:
				self.Cent_sib_calc.append(AWPdaily*areamask)
				self.Cent_sib_calc_anom.append(AWP_anomaly*areamask)
				self.Cent_sib_area.append(areamask)
			elif subregmask == 32:
				self.West_sib_calc.append(AWPdaily*areamask)
				self.West_sib_calc_anom.append(AWP_anomaly*areamask)
				self.West_sib_area.append(areamask)
			elif subregmask == 33:
				self.Cent_Asia_calc.append(AWPdaily*areamask)
				self.Cent_Asia_calc_anom.append(AWP_anomaly*areamask)
				self.Cent_Asia_area.append(areamask)
			elif subregmask == 34:
				self.Mount_Asia_calc.append(AWPdaily*areamask)
				self.Mount_Asia_calc_anom.append(AWP_anomaly*areamask)
				self.Mount_Asia_area.append(areamask)
			elif subregmask == 35:
				self.East_Asia_calc.append(AWPdaily*areamask)
				self.East_Asia_calc_anom.append(AWP_anomaly*areamask)
				self.East_Asia_area.append(areamask)
			elif subregmask == 36:
				self.Tibet_calc.append(AWPdaily*areamask)
				self.Tibet_calc_anom.append(AWP_anomaly*areamask)
				self.Tibet_area.append(areamask)
			#European regions
			elif subregmask == 40:
				self.Scandinavia_calc.append(AWPdaily*areamask)
				self.Scandinavia_calc_anom.append(AWP_anomaly*areamask)
				self.Scandinavia_area.append(areamask)
			elif subregmask == 42:
				self.West_Europe_calc.append(AWPdaily*areamask)
				self.West_Europe_calc_anom.append(AWP_anomaly*areamask)
				self.West_Europe_area.append(areamask)
			elif subregmask == 44:
				self.Cent_Europe_calc.append(AWPdaily*areamask)
				self.Cent_Europe_calc_anom.append(AWP_anomaly*areamask)
				self.Cent_Europe_area.append(areamask)
			elif subregmask == 46:
				self.South_Europe_calc.append(AWPdaily*areamask)
				self.South_Europe_calc_anom.append(AWP_anomaly*areamask)
				self.South_Europe_area.append(areamask)
			elif subregmask == 48:
				self.East_Europe_calc.append(AWPdaily*areamask)
				self.East_Europe_calc_anom.append(AWP_anomaly*areamask)
				self.East_Europe_area.append(areamask)


	def createmap(self,snowmap,snowextent,iceextent):
		'''displays snow cover data'''
		snowmap = snowmap.reshape(610,450)
		snowmap = np.ma.masked_greater(snowmap, 49)
		fig, ax = plt.subplots(figsize=(8, 10))
		cmap = plt.cm.ocean_r
		cmap2 = plt.cm.Greys
		cmap3 = plt.cm.RdBu_r
		cmap3.set_bad('black',0.9)
		
		ax.clear()
		ax.text(0.6, 0.01, 'AWP model: Nico Sun', fontsize=11,color='black',transform=ax.transAxes)
# =============================================================================
# 		ax.text(0.66, 0.03, 'Ice extent: '+'{:,}'.format(iceextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
# 		ax.text(0.66, 0.01, 'Snow extent: '+'{:,}'.format(snowextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
# =============================================================================
		
# =============================================================================
# 		ax.text(0.62, -0.02, 'Snow cover gain', fontsize=10,color='blue',transform=ax.transAxes)
# 		ax.text(0.82, -0.02, 'Snow cover loss', fontsize=10,color='red',transform=ax.transAxes)
# =============================================================================
		
		ax.set_title('Albedo Warming Potential (AWP)  {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),x=0.5)
		ax.set_xlabel('Snow Extent Data Source: https://nsidc.org/data/g02156',x=0.3)
		ax.set_ylabel('https://sites.google.com/site/cryospherecomputing/snow-cover',y=0.25)
		ax.text(1.02, 0.18, 'AMP in MJ / m2',
			transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
		axins1  = inset_axes(ax, width="5%", height="25%", loc=4)
		
		im1 = ax.imshow(snowmap, interpolation='nearest',vmin=0, vmax=30, cmap=cmap3) # Water & Land
		plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[0,5,10,15,20,25,30])
		axins1.yaxis.set_ticks_position("left")
		
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
		fig.savefig('CSVexport/Snow_Cover_AWP_map.png')
		plt.pause(0.01)
		
	def create_anolamy_map(self,snowmap):
		'''displays snow cover anomaly data'''
#		snowmap = ma.masked_greater(snowmap, 2)
		snowmap = snowmap.reshape(610,450)
		snowmap = np.ma.masked_greater(snowmap, 49)
		
		fig, ax = plt.subplots(figsize=(8, 10))
		cmap_anom = plt.cm.RdBu_r
		cmap_anom.set_bad('black',0.9)
		ax.clear()
		
		ax.text(0.6, 0.01, 'AWP model: Nico Sun', fontsize=11,color='black',transform=ax.transAxes)
		
		ax.set_title('Albedo Warming Potential (AWP) Anomaly  {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),x=0.5)
		ax.set_xlabel('Snow Extent Data Source: https://nsidc.org/data/g02156',x=0.3)
		ax.set_ylabel('https://sites.google.com/site/cryospherecomputing/snow-cover',y=0.25)
		ax.text(1.02, 0.2, 'AMP anomaly in MJ / m2',
			transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
		axins1  = inset_axes(ax, width="5%", height="25%", loc=4)
		im1 = ax.imshow(snowmap,vmin=-15, vmax=15, interpolation='nearest', cmap=cmap_anom)
		
		
		plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[-15,0,+15])
		axins1.yaxis.set_ticks_position("left")
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
		
		fig.savefig('CSVexport/Snow_Cover_AWP_anomaly.png')
		plt.pause(0.01)

		
	def writetofile(self):
		import csv
		'''writes data to a csv files'''
		
		with open('CSVexport/AWP_NorthAmerica.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Greenland[x],self.NorthAmerica[x][0],self.NorthAmerica[x][1],self.NorthAmerica[x][2],
				 self.NorthAmerica[x][3],self.NorthAmerica[x][4],self.NorthAmerica[x][5],self.NorthAmerica[x][6],
				 self.NorthAmerica[x][7],self.NorthAmerica[x][8],self.NorthAmerica[x][9],self.NorthAmerica[x][10]])
		with open('CSVexport/AWP_NorthAmerica_anomaly.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Greenland_anom[x],self.NorthAmerica_anom[x][0],self.NorthAmerica_anom[x][1],self.NorthAmerica_anom[x][2],
				 self.NorthAmerica_anom[x][3],self.NorthAmerica_anom[x][4],self.NorthAmerica_anom[x][5],self.NorthAmerica_anom[x][6],
				 self.NorthAmerica_anom[x][7],self.NorthAmerica_anom[x][8],self.NorthAmerica_anom[x][9],self.NorthAmerica[x][10]])
			
		with open('CSVexport/AWP_Europe.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Europe[x][0],self.Europe[x][1],self.Europe[x][2],
				 self.Europe[x][3],self.Europe[x][4],self.Europe[x][5]])
		with open('CSVexport/AWP_Europe_anom.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Europe_anom[x][0],self.Europe_anom[x][1],self.Europe_anom[x][2],
				 self.Europe_anom[x][3],self.Europe_anom[x][4],self.Europe_anom[x][5]])
			
		with open('CSVexport/AWP_Asia.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Asia[x][0],self.Asia[x][1],self.Asia[x][2],
				 self.Asia[x][3],self.Asia[x][4],self.Asia[x][5],self.Asia[x][6],self.Asia[x][7]])
		with open('CSVexport/AWP_Asia_anom.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Asia_anom[x][0],self.Asia_anom[x][1],self.Asia_anom[x][2],
				 self.Asia_anom[x][3],self.Asia_anom[x][4],self.Asia_anom[x][5],self.Asia[x][6],self.Asia[x][7]])
			
		with open('CSVexport/AWP_Ocean+anomaly.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDatum))):
				writer.writerow([self.CSVDatum[x],self.Ocean[x],self.Ocean_anom[x]])
			



action = AWP_model()
action.dayloop()
action.writetofile()
# =============================================================================
# for year in range(1979,1999):
# 	action.dayloop(year,9,22)
# action.writetofile()
# =============================================================================

'''
region_coding
1: Ocean
3: North America
4: Greenland
5: Europe
6: Asia
'''

'''
snowmap encoding
1: Ocean
2: Land
3: Ice
4: Snow

biome
0: undefined
10: tundra
20: forest
30: grassland
40: bare areas
50: cropland

subregions
10: eastern Canada
12: Central Canada
16: northern Canada
18: Canadian Rockies

20: Alaska
21: North east
22: South east
23: Mid West
24: South West
25: Pacific
26: US Rockies

30: Eastern Siberia
31: Central Siveria
32: Western Siberia
33: Central Asia
34: Central Mountain Asia
35: Eastern Asia
36: Tibet


40: Scandinavia
42: Western Europe
44: Central Europe
46: Southern Europe
48: Eastern Europe

50: Greenland
'''
