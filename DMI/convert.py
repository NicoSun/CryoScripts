import csv
 
year = 2008

while year <2009:
	yeartemp = []
	with open('tempT799_clim_plus80_'+str(year)+'.txt', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			temp = row[2]
			yeartemp.append(temp)
		
		
	with open('temp_'+str(year)+'.csv','w', newline='') as f:
		writer = csv.writer(f)
		for writeing in range(0,len(yeartemp)):
			writer.writerow([yeartemp[writeing]])
	year = year+1