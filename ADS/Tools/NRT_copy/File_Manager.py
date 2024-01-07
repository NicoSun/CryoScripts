"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script decompresses and renames the sea ice thickness ADS files from
https://ads.nipr.ac.jp/portal/kiwa/Summary.action?owner_site=ADS&selectFile=A20170123-003&version=1.00&scr=list_home

"""

import os
import re
import gzip
import ADS_SIT
import CryoIO


def deletion(year,month,pattern):
	'''this function deletes ascencion node files and SIT files with 00 version numbers'''
	filepath = 'DataFiles/compressed/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):
		if re.search(pattern,file):
			print(os.path.join(filepath,file))
			os.remove(os.path.join(filepath,file))
			
def clearfolder():
	'''this function deletes last months images (for gif)'''
	filepath = 'Binary'
	filepath_2 = 'Images/Anomaly'
	filepath_3 = 'Images/SIT'
	for file in os.listdir(filepath):
		os.remove(os.path.join(filepath,file))
	for file in os.listdir(filepath_2):
		os.remove(os.path.join(filepath_2,file))
	for file in os.listdir(filepath_3):
		os.remove(os.path.join(filepath_3,file))
		
		
def rename2(year,month):
	'''this function renames all files to the format ADS_SIT_YYYYMMDD'''
	filepath = 'DataFiles/compressed/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):		
			os.rename(os.path.join(filepath,file),os.path.join(filepath,file[0:-7]+'.gz'))
	
def rename(year,month):
	'''this function renames all files to the format ADS_SIT_YYYYMMDD'''
	filepath = 'DataFiles/compressed/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):		
		pattern = r'{}{}..D'.format(str(year),str(month).zfill(2))
		match = re.search(pattern,file)
		if match:
			#print(match.group(0)[0:8])
			os.rename(os.path.join(filepath,file),os.path.join(filepath,'ADS_SIT_'+match.group(0)[0:8]+'.gz'))
			#print(os.path.join(filepath,'ADS_SIT_'+match.group(0)[0:8]))
		
def decompress(year,month):
	'''this function decompresses all renamed files'''
	month = str(month).zfill(2)
	filepath = f'DataFiles/compressed/{year}{month}'
	filepath_2 = f'DataFiles/{year}'
	for file in os.listdir(filepath):
		pattern = r'ADS' 
		match = re.search(pattern,file)
		if match:
			with gzip.open(os.path.join(filepath,file), mode='rb') as fr:
				file_content = fr.read()
			print(file[0:16]+'.dat')
# 			with open(os.path.join(filepath_2,file[0:16]+'.dat'), 'wb') as fw:
# 				fw.write(file_content)
			CryoIO.savenumpy(os.path.join(filepath_2,file[0:16]+'.npz'), file_content)
				
def move_files(year):
	'''this function moves data into a year folder'''
	filepath = 'DataFiles/'
	filepath_2 = f'DataFiles/{year}/'
	for file in os.listdir(filepath):		
		pattern = r'SIT_{}'.format(str(year))
		match = re.search(pattern,file)
		if match:
			os.rename(os.path.join(filepath,file),os.path.join(filepath_2,file))


year = 2023
month = 4
day = 1
daycount = 30

# =============================================================================
# for year in range (2013,2023):
# 	move_files(year)
# =============================================================================

#patterns: r'A_' Ascending nodes ; r'D_00' old versions;
clearfolder()
deletion(year,month,r'A_')
deletion(year,month,r'D_00')
rename(year,month)

# ADS_SIT.action.automated(year,month,day,daycount)
