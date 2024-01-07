import numpy as np
import pandas
import CryoIO

def looop():
	'''iterates through a 366 day year'''
	month = 7
	day = 3
	daycount = 200
	
	# options Max,Min,Mean,Stdv
	mode = 'Mean'
	
	#Poleholelist
	Columns = ['hole']
	csvdata = pandas.read_csv('Tools/zzz_polehole.csv', names=Columns,dtype=int)
	icepole = csvdata.hole.tolist()
	
	Columns = ['edge']
	csvdata = pandas.read_csv('Tools/zzz_poleholeEdge.csv', names=Columns,dtype=int)
	icepoleedge = csvdata.edge.tolist()
		
	for count in range (0,daycount,1): #366
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		
		data = []		
		for year in range(2013,2021):
			filename = 'DataFiles/ADS_SIT_{}{}{}.dat'.format(year,stringmonth,stringday)
			filename_out = 'DataFiles/Mean/ADS_Mean_{}{}.dat'.format(stringmonth,stringday)
			ice = CryoIO.openfile(filename,np.uint16)
			data.append(ice)

		if mode =='Min':
			ice_new = calcMinimum(data)
		if mode =='Max':
			ice_new = calcMaximum(data)
		if mode =='Mean':
			ice_new = calcMean(data)
		if mode =='Stdv':
			ice_new = calcStdv(data)
		
		ice_new = polehole(ice_new,icepole,icepoleedge)
		
		if mode =='Stdv':
			export = np.array(ice_new, dtype=np.float16)
		else:
			export = np.array(ice_new, dtype=np.uint16)
		
		CryoIO.savebinaryfile(filename_out, export)
			
		print(month,day)
		
		day = day+1
		if day==32 and (month==1 or 3 or 5 or 7 or 8 or 10 or 12):
			day=1
			month = month+1
		elif day==31 and (month==4 or month==6 or month==9 or month==11):
			day=1
			month = month+1
		elif day==30 and month==2:
			day=1
			month = month+1
	print('Done')
	
def calcMinimum(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).min(0)
	return result

def calcMaximum(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).max(0)
	return result

def calcMean(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).mean(0)
	return result

def calcStdv(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).std(0)
	return result
	
def polehole(ice,icepole,icepoleedge):
	'''calculates the pole hole'''
	
	icepolecon = []
	for val in icepoleedge:
		icepolecon.append (ice[val])
		
	icepolecon = np.mean(icepolecon)
	
	for val2 in icepole:
		ice[val2] = icepolecon
	
	return ice


looop()

'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5664.8
water: 5775.9
unknown: 654X/655X

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''