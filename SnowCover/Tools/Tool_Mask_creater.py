import numpy as np
import matplotlib.pyplot as plt
import os

def Landmask():
	day_of_year = 52

	for day_of_year in range (1,2): #366
		filename7 = 'DataFiles/NOAA_2007'+str(day_of_year).zfill(3)+'_24km.bin'

		
		with open(filename7, 'rb') as fr7:
			ice7 = np.fromfile(fr7, dtype=np.uint8)
		
		ice7f = np.array(ice7, dtype=float)

		#274500 
		for x in range (0,len(ice7f)):
			if ice7f[x] == 4:
				ice7f[x] = 2
			if ice7f[x] == 3:
				ice7f[x] = 1
		export = np.array(ice7f, dtype=np.uint8)
				
		try:
			with open('Masks/Landmask.msk', 'wb') as fwr:
				fwr.write(export)
			
		except:
			print('cant write')
	print('Done')
		
def latlon_mask_resize():
	filename = 'Masks/Landmask.msk'
	with open('Masks/imslon_24km.bin', 'rb') as fr:
		latmask = np.fromfile(fr, dtype='float32')
			
#	print(len(latmask))
	latmask = latmask.reshape(1024,1024)
	snowmap = np.flip(latmask,axis=1)
	snowmap = np.flip(snowmap,axis=0)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
	snowmap = np.array(snowmap,dtype='float32')
#	plt.imshow(latmask)
#	plt.show()
	with open(os.path.join('Masks/','Longitude_Mask.msk'), 'wb') as writer:
		writer.write(snowmap)
		
def pixel_area():
	import time
	start = time.time()
	with open('Masks/imslat_24km.bin', 'rb') as fr:
		latmask = np.fromfile(fr, dtype='float32')
			
	conversionlist = np.loadtxt('Masks/Pixel_area_vs_Latitude.csv',delimiter=',',skiprows=1)
#	print(conversionlist[:,0])
	pixelareamask = np.zeros(len(latmask))
	for x,y in enumerate(latmask):
		latitude = y
		listindex = []
		for xx in conversionlist[:,0]:
			listindex.append(abs(latitude-xx))
			
		index = listindex.index(min(listindex))
		try:
			pixelareamask[x] = conversionlist[index,1]
		except:
			pixelareamask[x] = 'nan'

	pixelareamask = pixelareamask.reshape(1024,1024)
	plt.imshow(pixelareamask)
	plt.show()
	pixelareamask = np.array(pixelareamask,dtype='float32')
	with open(os.path.join('Masks/','Pixel_area.msk'), 'wb') as writer:
		writer.write(pixelareamask)
		
def pixel_area_crop():
	with open('Masks/ims_pixel_area_24km.bin', 'rb') as fr:
		latmask = np.fromfile(fr, dtype='float32')
	
	latmask = latmask.reshape(1024,1024)
	snowmap = np.flip(latmask,axis=1)
	snowmap = np.flip(snowmap,axis=0)
	snowmap = snowmap[220:830,250:700]
	snowmap = np.rot90(snowmap,k=2)
	snowmap = np.array(snowmap,dtype='uint16')
#	latmask = latmask.reshape(1024,1024)
#	plt.imshow(latmask)
#	plt.show()
	with open(os.path.join('Masks','Pixel_area_crop.msk'), 'wb') as writer:
		writer.write(snowmap)
		
def region_creater():
	filename = 'Masks/Landmask.msk'
	with open(filename, 'rb') as fr:
		landmask = np.fromfile(fr, dtype='uint8')
	filename = 'Masks/Latitude_Mask.msk'
	with open(filename, 'rb') as fr:
		Latitude_Mask = np.fromfile(fr, dtype='float32')
	filename = 'Masks/Longitude_Mask.msk'
	with open(filename, 'rb') as fr:
		Longitude_Mask = np.fromfile(fr, dtype='float32')
		
	for cell in range(0,len(Latitude_Mask)):
		#North America
		if -168 < Longitude_Mask[cell] < -77 and landmask[cell]==2:
			landmask[cell]=3
		if -77 < Longitude_Mask[cell] < -58 and landmask[cell]==2 and Latitude_Mask[cell]<73:
			landmask[cell]=3
		if -60 < Longitude_Mask[cell] < -50 and landmask[cell]==2 and Latitude_Mask[cell]<58:
			landmask[cell]=3
		if -77 < Longitude_Mask[cell] < -69 and landmask[cell]==2 and Latitude_Mask[cell]>79:
			landmask[cell]=3
		if -69 < Longitude_Mask[cell] < -66 and landmask[cell]==2 and 80 < Latitude_Mask[cell]:
			landmask[cell]=3
			
		#Greenland
		if -60 < Longitude_Mask[cell] < -25 and landmask[cell]==2  and Latitude_Mask[cell]>58:
			landmask[cell]=4
		if -25 < Longitude_Mask[cell] < -5 and landmask[cell]==2  and Latitude_Mask[cell]>68:
			landmask[cell]=4
		if -74 < Longitude_Mask[cell] < -60 and landmask[cell]==2 and 75 < Latitude_Mask[cell] < 79:
			landmask[cell]=4
		if -66 < Longitude_Mask[cell] < -50 and landmask[cell]==2 and 75 < Latitude_Mask[cell] < 81:
			landmask[cell]=4
			
		#Europe
		if -11 < Longitude_Mask[cell] < 48 and landmask[cell]==2:
			landmask[cell]=5
		if -25 < Longitude_Mask[cell] < -10 and landmask[cell]==2 and 60 < Latitude_Mask[cell] < 68:
			landmask[cell]=5

			
		#Asia
		if 48 < Longitude_Mask[cell] < 180 and landmask[cell]==2:
			landmask[cell]=6
		if -180 < Longitude_Mask[cell] < -169 and landmask[cell]==2:
			landmask[cell]=6

			
			
	regionmask = landmask.reshape(610,450)
	for y in range (366,370):
		regionmask[y,191] = 3
	regionmask[349,196] = 3
	regionmask[349,197] = 3
	regionmask[350,197] = 3
	regionmask[350,198] = 3
	regionmask[351,197] = 3
	regionmask[352,197] = 3
	
	regionmask[350,200] = 4
	regionmask[351,200] = 4
	regionmask[352,200] = 4
	regionmask[352,199] = 4
	regionmask[353,200] = 4
	regionmask[353,201] = 4
	regionmask[354,200] = 4
	regionmask[354,201] = 4
	
	regionmask[358,197] = 4
	regionmask[358,198] = 4
	regionmask[359,197] = 4
	regionmask[359,198] = 4
	
	regionmask[363,199] = 4
	regionmask[364,199] = 4
	regionmask[364,198] = 4
	
	regionmask[355,198] = 1

	plt.imshow(regionmask)
	plt.tight_layout(pad=0)
	plt.show()
	exportmask = np.array(regionmask,dtype='uint8')
	with open('Masks/Region_Mask.msk', 'wb') as writer:
		writer.write(exportmask)

def Coastmarker():
	filename7 = 'Masks/Landmask.msk'
	with open(filename7, 'rb') as fr7:
		landmask = np.fromfile(fr7, dtype=np.uint8)
		
		landmask = landmask.reshape(610,450)
		
		for x in range (1,609):
			for y in range(1,449):
				if landmask[x,y]==2 and landmask[x+1,y]==1:
					landmask[x,y]=3
				if landmask[x,y]==2 and landmask[x-1,y]==1:
					landmask[x,y]=3
				if landmask[x,y]==2 and landmask[x,y+1]==1:
					landmask[x,y]=3
				if landmask[x,y]==2 and landmask[x,y-1]==1:
					landmask[x,y]=3
			
		export = np.array(landmask, dtype=np.uint8)

# =============================================================================
# 		plt.imshow(landmask)
# 		plt.tight_layout(pad=0)
# 		plt.show()
# =============================================================================
				
		try:
			with open('Masks/Coastmask.msk', 'wb') as fwr:
				fwr.write(export)
			
		except:
			print('cant write')
	print('Done')
	
def biome():
	import cv2
	filename = 'Biome_mask_filled.png'#+name
	img = cv2.imread(filename)
	BiomeMap = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
#	BiomeMap = np.rot90(BiomeMap,k=2)
	BiomeMap = BiomeMap[:,:,0]
	BiomeMap = BiomeMap.reshape(274500)
	
	filename7 = 'Masks/Landmask.msk'
	with open(filename7, 'rb') as fr7:
		landmask = np.fromfile(fr7, dtype=np.uint8)
		
	for x,y in enumerate(landmask):
		if y==1:
			BiomeMap[x] = 1
		else:
			if BiomeMap[x]==221:
				BiomeMap[x] = 10
			elif BiomeMap[x]==20:
				BiomeMap[x] = 20
			elif BiomeMap[x]==187:
				BiomeMap[x] = 30
			elif BiomeMap[x]==108:
				BiomeMap[x] = 40
			elif BiomeMap[x]==176:
				BiomeMap[x] = 50
			else:
				BiomeMap[x] = 0
			
	'''
	biome
	222: tundra
	20: forest
	177: cropland
	109: bare areas
	188: grassland
	'''

	export = np.array(BiomeMap,dtype='uint8')
	BiomeMap = BiomeMap.reshape(610,450)
	

	with open('Masks/Biome_mask.msk', 'wb') as fwr:
		fwr.write(export)
	plt.imshow(BiomeMap)
	plt.show()
	
def regionmask():
	import cv2
	filename = 'SubRegion_mask_filled.png'#+name
	img = cv2.imread(filename)
	RegionMap = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
#	RegionMap = np.rot90(RegionMap,k=2)
	RegionMap = RegionMap[:,:,0]
	RegionMap = RegionMap.reshape(274500)
	
	filename7 = 'Masks/Landmask.msk'
	with open(filename7, 'rb') as fr7:
		landmask = np.fromfile(fr7, dtype=np.uint8)
		
	for x,y in enumerate(landmask):
		if y==1:
			RegionMap[x] = 1
		else:
			#Canada
			if RegionMap[x]==200:
				RegionMap[x] = 10
			elif RegionMap[x]==100:
				RegionMap[x] = 12
			elif RegionMap[x]==120:
				RegionMap[x] = 16
			elif RegionMap[x]==129:
				RegionMap[x] = 18
			
			#USA
			elif RegionMap[x]==89:
				RegionMap[x] = 20
			elif RegionMap[x]==80:
				RegionMap[x] = 21
			elif RegionMap[x]==70:
				RegionMap[x] = 22
			elif RegionMap[x]==219:
				RegionMap[x] = 23
			elif RegionMap[x]==209:
				RegionMap[x] = 24
			elif RegionMap[x]==149:
				RegionMap[x] = 25
			elif RegionMap[x]==140:
				RegionMap[x] = 26
			
			#Asia
			elif RegionMap[x]==82:
				RegionMap[x] = 30
			elif RegionMap[x]==152:
				RegionMap[x] = 31
			elif RegionMap[x]==162:
				RegionMap[x] = 32
			elif RegionMap[x]==220:
				RegionMap[x] = 33
			elif RegionMap[x]==122:
				RegionMap[x] = 34
			elif RegionMap[x]==212:
				RegionMap[x] = 35
			elif RegionMap[x]==142:
				RegionMap[x] = 36
			elif RegionMap[x]==250:
				RegionMap[x] = 37
			elif RegionMap[x]==230:
				RegionMap[x] = 38
			
			#Europe
			elif RegionMap[x]==189:
				RegionMap[x] = 40
			elif RegionMap[x]==165:
				RegionMap[x] = 42
			elif RegionMap[x]==174:
				RegionMap[x] = 44
			elif RegionMap[x]==244:
				RegionMap[x] = 46
			elif RegionMap[x]==55:
				RegionMap[x] = 48
			
			#Greenland
			elif RegionMap[x]==255:
				RegionMap[x] = 50

			else:
				RegionMap[x] = 0
			
	'''
	biome
	subregions
	200: eastern Canada
	100: western Canada
	120: northern Canada
	121: Canadian Rockies
	90: Alaska
	80: North east
	70: South east
	220: Mid West
	210: South West
	150: Pacific
	140: US Rockies
	
	255: Greenland
	
	82: Eastern Siberia
	152: Central Siveria
	162: Western Siberia
	212: Eastern Asia
	222: Central Asia
	122: North Asia mountain
	142: Tibet
	250: West Asia
	230: Persia
	
	190: Scandinavia
	165: Western Europe
	175: Central Europe
	245: Southern Europe
	55: Eastern Europe
	
	'''

	export = np.array(RegionMap,dtype='uint8')
	RegionMap = RegionMap.reshape(610,450)
	

	with open('Masks/SubRegion_Mask.msk', 'wb') as fwr:
		fwr.write(export)
	plt.imshow(RegionMap)
	plt.show()
	
def Rutgers_regionmask():
	import cv2
	filename = 'ZZZ_rutgers.png'#+name
	img = cv2.imread(filename)
	RegionMap = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
#	RegionMap = np.rot90(RegionMap,k=2)
	RegionMap = RegionMap[:,:,0]
	RegionMap = RegionMap.reshape(7744)
	
		
	for index,value in enumerate(RegionMap):
		if value==0:
			RegionMap[index] = 0
		else:
			#Canada
			if RegionMap[index]==250:
				RegionMap[index] = 10
			elif RegionMap[index]==240:
				RegionMap[index] = 20
			elif RegionMap[index]==30:
				RegionMap[index] = 30
			elif RegionMap[index]==10:
				RegionMap[index] = 40
				
		'''
		250 North America
		240 Greenland
		30 Europe
		10 Asia
		0 Ocean
		'''

	export = np.array(RegionMap,dtype='uint8')
	RegionMap = RegionMap.reshape(88,88)
	

	with open('Masks/Rutgers_Region_Mask.msk', 'wb') as fwr:
		fwr.write(export)
	plt.imshow(RegionMap)
	plt.show()

def arrayasImage():
	from PIL import Image
	stringyearday = str(95).zfill(3)
	filename = 'X:/SnowCover/Datafiles/NOAA_{}{}_24km.bin'.format(2017,stringyearday)
	with open(filename, 'rb') as fr:
		snow = np.fromfile(fr, dtype='uint8')
	regionmask = snow.reshape(610,450)
	rescaled = (255.0 / regionmask.max() * (regionmask - regionmask.min())).astype(np.uint8)
	im = Image.fromarray(rescaled)
	im.save('ZZZ_{}.png'.format(stringyearday))


#Landmask()
#region_creater()
#latlon_mask_resize()
#Coastmarker()
#pixel_area_crop()
#biome()
regionmask()
#arrayasImage()
#plt.imshow(ice) 
#plt.colorbar()
#plt.show()

'''
Regionmask:
North America: 3
Greenland: 4
Europe: 5
Asia: 6
'''
