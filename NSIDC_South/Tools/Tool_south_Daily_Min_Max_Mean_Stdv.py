import numpy as np
import CryoIO

def looop():
	'''iterates through a 366 day year'''
	Cdate = CryoIO.CryoDate()
	daycount = 366
	
	# options Max,Min,Mean,Stdv
	mode = 'Max'
	yearlist = [year for year in range(1979,2023)]
	
	for count in range (0,daycount,1): #366
		data = []
		month = Cdate.strMonth
		day = Cdate.strDay
		datestring = f'{month}{day}'
		if mode == 'Mean': # Forecast_Mean , Forecast_Manual
			filename_out = f'../DataFiles/Forecast_Manual/NSIDC_{mode}_{datestring}_south.npz'
		elif mode == 'Stdv':
			filename_out = f'../DataFiles/Forecast_Stdv/NSIDC_{mode}_{datestring}_south.npz'
		elif mode == 'Max':
			filename_out = f'../DataFiles/Max/NSIDC_{mode}_{datestring}_south.npz'
		elif mode == 'Min':
			filename_out = f'../DataFiles/Min/NSIDC_{mode}_{datestring}_south.npz'
		
		for year in yearlist:
			filename = f'../DataFiles/{year}/NSIDC_{year}{datestring}_south.npz'
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
