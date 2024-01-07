import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import CryoIO
from netCDF4 import Dataset
from datetime import date
from datetime import timedelta

dataset = Dataset('DataFiles/Low_resolution/nhsce_v01r01_19661004_20230102.nc')
snow_arrays = dataset.variables['snow_cover_extent']
land = dataset.variables['land'][:]

print(len(snow_arrays))

def looop():
	#day_of_year = 50	
#	dataset = Dataset('DataFiles/Low_resolution/nhsce_v01r01_19661004_20200706.nc')
#	snow_arays = dataset.variables['snow_cover_extent']
#	land = dataset.variables['land'][:]
	
	snowdaycount = np.zeros(7744)
	start = date(1966, 10, 4)
	loopday	= start
	
	for x in snow_arrays:
		snownew = np.array(x,dtype='uint8').reshape(7744)
		aaa = np.vectorize(snowcount)
		snowdaycount = aaa(snowdaycount,snownew)
		
		loopday += timedelta(weeks=1)
		loopdate = f'{loopday.year}-{loopday.strftime("%V")}'
		
		if loopday.month == 12 and loopday.strftime("%V") == '52':
			print(loopdate)
			createmap(snowdaycount,land,loopday.year)
			export = np.array(snowdaycount, dtype=np.uint16)
			CryoIO.savebinaryfile('temp/low_res/Snow_cover_days_{}.bin'.format(loopday.year),export)
			snowdaycount = np.zeros(7744)


	print('Done')
		
def snowcount(snowdaycount,snownew):
	
	if snownew == 1:
		snowdaycount += 1
	return snowdaycount

def createmap(snowmap,land,year):
	'''displays snow cover data'''
	snowmap = snowmap.reshape(88,88)
	snowmap = np.ma.masked_greater(snowmap, 366)
	fig, ax = plt.subplots(figsize=(4.5, 6))
	
	land = np.ma.masked_equal(land,1)
	land = land[:80,20:75]
	snowmap = snowmap[:80,20:75]
		
	plt.rcParams["ytick.color"] = 'white'
	
	cmap = plt.cm.get_cmap("CMRmap").copy()
	cmap.set_bad([0.53,0,0.08],1)
	ax.clear()
	ax.text(0.5, 0.02, 'Map: Nico Sun', fontsize=10,color='white',transform=ax.transAxes)

	ax.set_title('NCDC/NOAA Snow cover (weeks) Year {}'.format(year),x=0.5)
	ax.set_ylabel('cryospherecomputing.com/snow-cover',y=0.26)
	ax.text(1.02, 0.24, 'Snow coverd weeks',
		transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
	axins1  = inset_axes(ax, width="5%", height="30%", loc=4)
	
	im1 = ax.imshow(snowmap, interpolation='nearest',vmin=0, vmax=52, cmap=cmap) # Water & Land
	im2 = ax.imshow(land, interpolation='nearest',vmin=0, vmax=1, cmap='jet') # Water & Land
	plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[0,10,20,30,40,50])#,color='white')
	axins1.yaxis.set_ticks_position("left")
	
#	ax.axis( 'off' )
	ax.axes.get_yaxis().set_ticks([])
	ax.axes.get_xaxis().set_ticks([])

	plt.tight_layout(pad=1)
	fig.savefig('img/NOAA_Snowmap_{}.png'.format(year))
	plt.close()
#	plt.pause(0.01)
	
def create_anolamy_map(snowmap,land,year):
	'''displays snow cover data'''
	snowmap = snowmap.reshape(88,88)
#	snowmap = np.ma.masked_greater(snowmap, 366)
	fig, ax = plt.subplots(figsize=(4.5, 6))
	
	land = np.ma.masked_equal(land,1)
	land = land[:80,20:75]
	snowmap = snowmap[:80,20:75]
	
	plt.rcParams["ytick.color"] = 'white'
	
	cmap_anom = plt.cm.get_cmap("RdBu").copy()
	cmap_anom.set_bad('black',0.8)
	ax.clear()
	ax.text(0.5, 0.02, 'Map: Nico Sun', fontsize=11,color='white',transform=ax.transAxes)

	ax.set_title('NCDC/NOAA Snow anomaly (weeks) Year {}'.format(year),x=0.5)
	ax.set_ylabel('cryospherecomputing.com/snow-cover',y=0.26)
	ax.text(1.02, 0.33, 'Snow coverd weeks anomaly',
		transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
	axins1  = inset_axes(ax, width="5%", height="30%", loc=4)
		
	im1 = ax.imshow(snowmap, interpolation='nearest',vmin=-15, vmax=15, cmap=cmap_anom) # Water & Land
	im2 = ax.imshow(land, interpolation='nearest',vmin=0, vmax=1, cmap='jet') # Water & Land
	plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[-15,-7,0,7,15])#,color='white')
	axins1.yaxis.set_ticks_position("left")
	
#	ax.axis( 'off' )
	ax.axes.get_yaxis().set_ticks([])
	ax.axes.get_xaxis().set_ticks([])

	plt.tight_layout(pad=1)
	fig.savefig('img/NOAA_Snowmap_anomaly_{}.png'.format(year))
	plt.close()
#	plt.pause(0.1)
	
	
def calc_mean():
	snowMean = np.zeros(7744)
	start = 1998
	end = 2023
	for year in range(start,end):
		filename = 'temp/low_res/Snow_cover_days_{}.bin'.format(year)
		snow = CryoIO.openfile(filename,'uint16')
		snowMean = snowMean+snow
	snowMean = snowMean / (end -start)
	
	
	createmap(snowMean,land,'Mean')
	export = np.array(snowMean, dtype=np.uint16)
	CryoIO.savebinaryfile('temp/low_res/Snow_cover_days_snowmean.bin',export)


	
def calc_anomaly():
	
	filename = 'temp/low_res/Snow_cover_days_snowmean.bin'
	snowMean = CryoIO.openfile(filename,'uint16')

	snowanomaly = np.zeros(88*88,dtype='float')
#	file = 'Snow_cover_days_snowmean.bin'
#	file = 'Snow_cover_days_2020.bin'
	for year in range(1967,2023):
		filename = 'temp/low_res/Snow_cover_days_{}.bin'.format(year)
		snow = CryoIO.openfile(filename,'uint16')
		snowanomaly = snow-snowMean

		create_anolamy_map(snowanomaly,land,year)
#		snowanomaly = np.array(snowanomaly, dtype='int16')
#		CryoIO.savebinaryfile('netcdf/anomaly/Snow_cover_days_anomaly_{}.bin'.format(year),snowanomaly)
		
		

# looop()
# calc_mean()
calc_anomaly()
#plt.show()

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
'''