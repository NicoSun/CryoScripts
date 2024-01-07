import numpy as np
import pandas
import CryoIO

def looop():
	'''iterates through a 366 day year'''
	Cdate = CryoIO.CryoDate()
	daycount = 366
	
	
	# options Max,Min,Mean,Stdv
	mode = 'Min'
	yearlist = [year for year in range(1979,2023)]

	Columns = ['hole']
	csvdata = pandas.read_csv('../Tools/2008_polehole.csv', names=Columns,dtype=int)
	icepole = csvdata.hole.tolist()
	 		
	Columns = ['edge']
	csvdata = pandas.read_csv('../Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
	icepoleedge = csvdata.edge.tolist()
	
	for count in range (0,daycount): #366
		month = Cdate.strMonth
		day = Cdate.strDay
		datestring = f'{month}{day}'
		
		data = []
		if mode == 'Mean':
			filename_out = f'../DataFiles/Mean_00_19/NSIDC_{mode}_{datestring}.npz'
		elif mode == 'Max':
			filename_out = f'../DataFiles/Max/NSIDC_{mode}_{datestring}.npz'
		elif mode == 'Min':
			filename_out = f'../DataFiles/Min/NSIDC_{mode}_{datestring}.npz'
		elif mode =='Stdv':
			filename_out = f'../DataFiles/Stdv/NSIDC_{mode}_{datestring}.npz'
		

		for year in yearlist:
			filename = f'../DataFiles/{year}/NSIDC_{year}{datestring}.npz'
			icef = CryoIO.readnumpy(filename)
			data.append(icef)

		if mode =='Min':
			ice_new = calcMinimum(data)
		elif mode =='Max':
			ice_new = calcMaximum(data)
		elif mode =='Mean':
			ice_new = calcMean(data)
		elif mode =='Stdv':
			ice_new = calcStdv(data)
		
		ice_new = polehole(ice_new,icepole,icepoleedge)
		export = export_data(mode,ice_new)	
		CryoIO.savenumpy(filename_out, export)
		
			
		print(mode,datestring)
		Cdate.datecalc()
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
		
def export_data(mode,ice_new):
	'''sets array data type'''
	if mode =='Stdv':
		export = np.array(ice_new, dtype=np.float16)
	else:
		export = np.array(ice_new, dtype=np.uint8)
		
	return export



looop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
