import math
import pandas as pd

year = 2021

def loadcsvfiles():
	distance_dict = {}
	
	
	for week in range(1,51):
		df = pd.read_csv('{}/icebergs_{}.csv'.format(year,'WK_'+str(week)),sep=",")
		df_old = pd.read_csv('{}/icebergs_{}.csv'.format(year,'WK_'+str(week-1)))
	

		names = df['Iceberg']
		Latitude = df['Latitude']
		Longitude = df['Longitude']
		
		names_old = df_old['Iceberg']
		Latitude_old = df_old['Latitude']
		Longitude_old = df_old['Longitude']
		
		dictionary = {}
		dictionary_old = {}
		
		for count,name in enumerate(names):
			dictionary[name] = [Latitude[count],Longitude[count]]
		for count,name in enumerate(names_old):
			dictionary_old[name] = [Latitude_old[count],Longitude_old[count]]
		
		for key in dictionary:
			if key in dictionary_old:
				distance = calctravel(dictionary[key][0],dictionary_old[key][0],dictionary[key][1],dictionary_old[key][1])
				if key in distance_dict:
					distance_dict[key] += distance/1000
				else:
					distance_dict[key] = distance/1000
				
# 		print(distance_dict)
	
	with open(f"{year}_distancedict.csv", "w", newline="") as f:
		for key in distance_dict.keys():
			f.write("%s,%s\n"%(key,distance_dict[key]))
	
	create_graph(distance_dict)

def create_graph(data):
	import matplotlib.pyplot as plt
	plt.style.use('dark_background')
	
	#remove grounded icebergs
	newdict = {}
	for key in data.keys():
		if data[key] > 250:
			newdict[key] = data[key]
	
# 	newdict = sorted(newdict)
	newlist = sorted(newdict.items(), key=lambda x: x[1], reverse=True)
	newdict = dict(newlist)
	print(newdict)
	
	fig = plt.figure(figsize=(12,6))
	
	ax = fig.add_subplot(111)
	
	plt.bar(range(len(newdict)), list(newdict.values()), align='center',color="darkred")
	plt.xticks(range(len(newdict)), list(newdict.keys()))

	plt.ylabel('km')	
# =============================================================================
# 	ax.text(0.52, 0.07, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
# 	ax.text(0.52, 0.04, r'Distance calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
# =============================================================================
	ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
        transform=ax.transAxes,color='grey', fontsize=10)
	ax.text(0.35, 1.02, f'{year} Iceberg movement',
        transform=ax.transAxes, fontsize=12,fontweight='bold')
	fig.tight_layout(pad=1)

	fig.savefig("{}_icebergs_movement.png".format(year))

	plt.show()
	


def convert_to_radian(*args):
	aaa = []
	for x in args:
		aaa.append(math.radians(x))
	return aaa
		

def calctravel(lat1,lat2,lon1,lon2):
	
	lat1,lat2,lon1,lon2 = convert_to_radian(lat1,lat2,lon1,lon2)
	
	distance = math.acos(min(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1),1 )) * 6371000
	
#	print(distance/1000)
	return distance


#calctravel(-72.52,-72.82,-172.31,-172.83)

if __name__ == '__main__':
	loadcsvfiles()



