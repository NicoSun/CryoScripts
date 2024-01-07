import pandas as pd
import csv



class NSIDC_area:

	def __init__  (self):
		
		self.forecasttype = '001' # Low: 001 Mean: 002 High: 003
		self.columnA = []
		self.columnB = []
		self.columnC = []
		self.columnD = []

	def makeSuperList(self,data):
		
		for x,y in enumerate(data[0]):
			self.columnA.append(data[0][x])
			self.columnB.append(data[1][x])
			self.columnC.append(data[2][x])
			self.columnD.append(data[3][x])
		
	def writetofile(self):
		with open('Super_List_{}.csv'.format(self.forecasttype), "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.columnA))):
				writer.writerow([self.columnA[x],self.columnB[x],self.columnC[x],self.columnD[x]])
	
	def loadyearcsvdata (self):
		for yearload in range(2007,2019):
			AWP_mean = ['A', 'B', 'C', 'D']
			Climatedata = pd.read_csv('_SIPN_forecast_{}_{}.csv'.format(self.forecasttype,yearload), names=AWP_mean,header=0)
			column1 = Climatedata.A.tolist()
			column2 = Climatedata.B.tolist()
			column3 = Climatedata.C.tolist()
			column4 = Climatedata.D.tolist()
			data = [column1,column2,column3,column4]
			self.makeSuperList(data)
			
		self.writetofile()
		

		


action = NSIDC_area()
if __name__ == "__main__":
	print('main')
#	action.loadYeardata()
	action.loadyearcsvdata()
