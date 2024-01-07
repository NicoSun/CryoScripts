import numpy as np
import matplotlib.pyplot as plt
import CryoIO


def createMask():
	'''reads a png file and creates a mask in binary'''
	import cv2
	
	landmaskfile = 'Masks/landmask_low.map'
	landmask = CryoIO.openfile(landmaskfile,np.uint8)
	
	filename = 'ZZZ_ADS_mask_40.png' #name
	img = cv2.imread(filename)
	RegionMap = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
#	RegionMap = np.rot90(RegionMap,k=2)
	RegionMap = RegionMap[:,:,0]
	RegionMap = RegionMap.reshape(900*900)
	
		
	for index,value in enumerate(landmask):
		if value < 40:
			if RegionMap[index]==100:
				RegionMap[index] = 20
			elif RegionMap[index]==110:
				RegionMap[index] = 22
			elif RegionMap[index]==120:
				RegionMap[index] = 24
			elif RegionMap[index]==130:
				RegionMap[index] = 26
			elif RegionMap[index]==140:
				RegionMap[index] = 28
			elif RegionMap[index]==150:
				RegionMap[index] = 30
			elif RegionMap[index]==160:
				RegionMap[index] = 32
			elif RegionMap[index]==90:
				RegionMap[index] = 34
			elif RegionMap[index]==80:
				RegionMap[index] = 36
			elif RegionMap[index]==60:
				RegionMap[index] = 40
			elif RegionMap[index]==40:
				RegionMap[index] = 42
			elif RegionMap[index]==180:
				RegionMap[index] = 44
			elif RegionMap[index]==250:
				RegionMap[index] = 46
				
			elif RegionMap[index]==200:
				RegionMap[index] = 52
			elif RegionMap[index]==210:
				RegionMap[index] = 54
			else:
				 RegionMap[index] = 0
		else:
			RegionMap[index] = 250
		'''
		100 Sea of Okost
		110 Bering Sea
		120 Hudson Bay
		130 Baffin Bay
		140 Greenland Sea
		150 Barents Sea
		160 Kara Sea
		90 Laptev Sea
		80 East Siberian Sea
		60 Chuckchi Sea
		40 Beafout Sea
		180 Canadian Archipelago
		250 Central Arctic
		
		200 Baltic Sea
		210 St lawrence Sea
		
		'''

	export = np.array(RegionMap,dtype='uint8')
	RegionMap = export.reshape(900,900)
	
	filename = 'Masks/Regionmask.map'
	#CryoIO.savebinaryfile(filename, export)

	plt.imshow(RegionMap)
	plt.show()

def arrayasImage():
	'''saves a binary file and png (RGB)'''
	from PIL import Image
	landmaskfile = 'Masks/landmask_low.map'
	#landmaskfile = 'Masks/Regionmask.msk'
	snow = CryoIO.openfile(landmaskfile,np.uint8)
	
	for index,value in enumerate(snow):
		if value < 40:
			snow[index] = 0
		else:
			snow[index] = 100
	
	regionmask = snow.reshape(900,900)
	rescaled = (255.0 / regionmask.max() * (regionmask - regionmask.min())).astype(np.uint8)
	im = Image.fromarray(rescaled)
	im.save('ZZZ_ADS_mask_40.png')


createMask()
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
