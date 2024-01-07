import CryoIO
import numpy as np
import os

class npz_converter:
	
	def __init__  (self):
		pass		

	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		hemi = ['DataFiles','DataFiles_s']
		for hem in hemi:
			filepath = f'{hem}/Mean_80_21/'
			for file in os.listdir(filepath):
				print(file)
				filename = file
				filename_npz = filename[:-3] + 'npz'

				icef = CryoIO.openfile(f'{filepath}{filename}', np.uint8)
				ice = np.array(icef,dtype=np.uint8)
				
				CryoIO.savenumpy(f'{filepath}{filename_npz}', ice)
				os.remove(f'{filepath}{filename}')
		
			
action = npz_converter()
action.dayloop()
# =============================================================================
# for year in range(1979,2022):
# 	action.dayloop(year)
# 	print(year)
# =============================================================================
