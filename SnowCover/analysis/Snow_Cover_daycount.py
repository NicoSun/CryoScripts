import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import CryoIO

filename = 'Masks/Coastmask.msk'
coastmask = CryoIO.openfile(filename,'uint8')


def looop():
	#day_of_year = 50
	
	filename = 'Masks/Landmask.msk'
	Landmask = CryoIO.openfile(filename,'uint8')

	for year in range(2021,2022):
		snowdaycount = np.zeros(len(coastmask))
		for day_of_year in range (1,366): #366
			stringday = str(day_of_year).zfill(3)
			
			filename = 'DataFiles/{}/NOAA_{}{}_24km.npz'.format(year,year,stringday)
			snownew = CryoIO.readnumpy(filename)

			aaa = np.vectorize(snowcount)
			snowdaycount = aaa(snowdaycount,snownew)
			print(year,day_of_year)
			
		for x,y in enumerate(coastmask):
			if coastmask[x] == 3:
				snowdaycount[x] = 400
		createmap(snowdaycount,year)
		export = np.array(snowdaycount, dtype=np.uint16)
		CryoIO.savebinaryfile('netcdf/Snow_cover_days_{}.bin'.format(year),export)


# 	print('Done')
		
def snowcount(snowdaycount,snownew):
	
	if snownew ==3 or snownew==4:
		snowdaycount += 1
	return snowdaycount

def createmap(snowmap,year):
	'''displays snow cover data'''
	snowmap = snowmap.reshape(610,450)
	snowmap = np.ma.masked_greater(snowmap, 366)
	fig, ax = plt.subplots(figsize=(8, 10))
	
#	plt.rcParams["text.color"] = 'white'
#	plt.rcParams["axes.labelcolor"] = 'white'
#	plt.rcParams["xtick.color"] =  'white'
	plt.rcParams["ytick.color"] = 'white'
	
	cmap = plt.cm.get_cmap("CMRmap").copy()
	cmap.set_bad([0.53,0,0.08],1)
	ax.clear()
	ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='white',transform=ax.transAxes)

	ax.set_title('NOAA / NSIDC IMS Snow & Ice covered days  Year {}'.format(year),x=0.5)
	ax.set_xlabel('Data source: https://nsidc.org/data/g02156',x=0.22)
	ax.set_ylabel('cryospherecomputing.com/snow-cover',y=0.15)
	ax.text(1.02, 0.09, 'Snow coverd days',
		transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
	axins1  = inset_axes(ax, width="5%", height="30%", loc=4)
		
	im1 = ax.imshow(snowmap, interpolation='nearest',vmin=0, vmax=365, cmap=cmap) # Water & Land
	plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[0,90,180,270,365])#,color='white')
	axins1.yaxis.set_ticks_position("left")
	
#	ax.axis( 'off' )
	ax.axes.get_yaxis().set_ticks([])
	ax.axes.get_xaxis().set_ticks([])

	plt.tight_layout(pad=1)
	fig.savefig('CSVexport/NOAA_Snowmap_{}.png'.format(year))
# 	plt.pause(0.01)
	
def create_anolamy_map(snowmap,year):
	'''displays snow cover data'''
	snowmap = snowmap.reshape(610,450)
#	snowmap = np.ma.masked_greater(snowmap, 366)
	fig, ax = plt.subplots(figsize=(8, 10))
	
	cmap_anom = plt.cm.get_cmap("RdBu").copy()
	cmap_anom.set_bad('black',0.8)
	ax.clear()
	ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='black',transform=ax.transAxes)

	ax.set_title('NOAA / NSIDC IMS Snow & Ice covered days anomaly  Year {}'.format(year),x=0.5)
	ax.set_xlabel('Data source: https://nsidc.org/data/g02156',x=0.22)
	ax.set_ylabel('cryospherecomputing.com/snow-cover',y=0.15)
	ax.text(1.02, 0.075, 'Snow coverd days anomaly',
		transform=ax.transAxes,rotation='vertical',color='black', fontsize=9)
	axins1  = inset_axes(ax, width="5%", height="30%", loc=4)
		
	im1 = ax.imshow(snowmap, interpolation='nearest',vmin=-100, vmax=100, cmap=cmap_anom) # Water & Land
	plt.colorbar(im1, cax=axins1, orientation='vertical',ticks=[-100,-50,0,50,100])#,color='white')
	axins1.yaxis.set_ticks_position("left")
	
#	ax.axis( 'off' )
	ax.axes.get_yaxis().set_ticks([])
	ax.axes.get_xaxis().set_ticks([])

	plt.tight_layout(pad=1)
	fig.savefig('CSVexport/NOAA_Snowmap_anomaly_{}.png'.format(year))
#	plt.pause(0.1)
	
	
def calc_mean():
	snowMean = np.zeros(len(coastmask))
	start = 1998
	end = 2023
	for year in range(start,end):
		filename = 'netcdf/Snow_cover_days_{}.bin'.format(year)
		snow = CryoIO.openfile(filename,'uint16')
		snowMean = snowMean+snow
	snowMean = snowMean / (end -start)
	
	createmap(snowMean,'Mean')
	export = np.array(snowMean, dtype=np.uint16)
	CryoIO.savebinaryfile('netcdf/Snow_cover_days_snowmean.bin',export)


	
def calc_anomaly():
	
	filename = 'netcdf/Snow_cover_days_snowmean.bin'
	snowMean = CryoIO.openfile(filename,'uint16')

	snowanomaly = np.zeros(610*450,dtype='float')

	for year in range(1997,2023):
		filename = 'netcdf/Snow_cover_days_{}.bin'.format(year)
		snow = CryoIO.openfile(filename,'uint16')
		snowanomaly = snow-snowMean


		for x,y in enumerate(coastmask):
			if y == 3:
				snowanomaly[x] = 400

		create_anolamy_map(snowanomaly,year)
		snowanomaly = np.array(snowanomaly, dtype='int16')
		CryoIO.savebinaryfile('netcdf/anomaly/Snow_cover_days_anomaly_{}.bin'.format(year),snowanomaly)
		
		

# looop()
calc_mean()
# calc_anomaly()
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