import pandas as pd
import numpy as np



class Data_restructure:

	def __init__  (self):
		print('Data_restructure')

	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')	
	
	def regionExcelbook_whole_Arctic (self,mode):
		RegionA = pd.DataFrame()
		RegionB = pd.DataFrame()
		RegionC = pd.DataFrame()
			
		if mode == 'decade':
			sheetnames = ['Date','Area','Extent','High Arctic']
			inputfile = 'temp/regional/Pan_Arctic_{}.csv'
			outputfile = 'YYY_Regional_by_Metric_Decades.xlsx'
			decade_names = ['1980s','1990s','2000s','2010s']
			decades = [1980,1990,2000,2010]
			years = 10

			for index,xxx in enumerate(decade_names):
				Region1 = pd.DataFrame()
				Region2 = pd.DataFrame()
				Region3 = pd.DataFrame()
				for year in range(decades[index],decades[index]+years):
					AWP_mean = ['A', 'B', 'C', 'D']
					Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
					Region1[str(year)] = Climatedata.B
					Region2[str(year)] = Climatedata.C
					Region3[str(year)] = Climatedata.D
			
			
				RegionA[xxx] = Region1.mean(axis=1)
				RegionB[xxx] = Region2.mean(axis=1)
				RegionC[xxx] = Region3.mean(axis=1)
			
			with pd.ExcelWriter(outputfile) as writer:
				RegionA.to_excel(writer, sheet_name='{}'.format(sheetnames[0]),index=False)
				RegionB.to_excel(writer, sheet_name='{}'.format(sheetnames[1]),index=False)
				RegionC.to_excel(writer, sheet_name='{}'.format(sheetnames[2]),index=False)
			
#			outputfile = 'Melt_AWP/Melt_AWP_decades.csv'
#			self.csvexport(outputfile,[RegionA,RegionB,RegionC,RegionD])

		else:
			Region1 = pd.DataFrame()
			Region2 = pd.DataFrame()
			Region3 = pd.DataFrame()
			
			names = ['Date','Area','Extent','High Arctic']
			inputfile = 'temp/regional/Pan_Arctic_{}.csv'
			outputfile = 'YYY_Regional_by_Metric.xlsx'
	
			
			for year in range(1979,2021):
				AWP_mean = ['A', 'B', 'C', 'D']
				Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
				Region1[str(year)] = Climatedata.B
				Region2[str(year)] = Climatedata.C
				Region3[str(year)] = Climatedata.D
				
				
			with pd.ExcelWriter(outputfile) as writer:
				Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
				Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
				Region3.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)

	
	def regionExcelbook_by_year (self):
		with pd.ExcelWriter('YYY_Regional.xlsx') as writer:
			for year in range(1979,2021):
				Climatedata = pd.read_csv('temp/regional/Regional_{}.csv'.format(year))
				Climatedata.to_excel(writer, sheet_name=str(year),index=False)
				

				
	def regionExcelbook_by_region (self):
		Region1 = pd.DataFrame()
		Region2 = pd.DataFrame()
		Region3 = pd.DataFrame()
		Region4 = pd.DataFrame()
		Region5 = pd.DataFrame()
		Region6 = pd.DataFrame()
		Region7 = pd.DataFrame()
		Region8 = pd.DataFrame()
		Region9 = pd.DataFrame()
		Region10 = pd.DataFrame()
		Region11 = pd.DataFrame()
		Region12 = pd.DataFrame()
		Region13 = pd.DataFrame()
		
		names = ['Sea of Okhotsk','Bering Sea','Hudson Bay','Baffin Bay','East Greenland Sea','Barents Sea','Kara Sea','Laptev Sea','East Siberian Sea','Chukchi Sea','Beaufort Sea','Canadian Archipelago','Central Arctic']
#		
		inputfile = 'temp/regional/Regional_{}.csv'
		outputfile = 'YYY_Regional_by_Region.xlsx'

		
		for year in range(1979,2021):
			AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
			Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
			Region1[str(year)] = Climatedata.B
			Region2[str(year)] = Climatedata.C
			Region3[str(year)] = Climatedata.D
			Region4[str(year)] = Climatedata.E
			Region5[str(year)] = Climatedata.F
			Region6[str(year)] = Climatedata.G
			Region7[str(year)] = Climatedata.H
			Region8[str(year)] = Climatedata.I
			Region9[str(year)] = Climatedata.J
			Region10[str(year)] = Climatedata.K
			Region11[str(year)] = Climatedata.L
			Region12[str(year)] = Climatedata.M
			Region13[str(year)] = Climatedata.N
			
#			print(Climatedata.B[0])
		with pd.ExcelWriter(outputfile) as writer:
			Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
			Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
			Region3.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
			Region4.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
			Region5.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)
			Region6.to_excel(writer, sheet_name='{}'.format(names[5]),index=False)
			Region7.to_excel(writer, sheet_name='{}'.format(names[6]),index=False)
			Region8.to_excel(writer, sheet_name='{}'.format(names[7]),index=False)
			Region9.to_excel(writer, sheet_name='{}'.format(names[8]),index=False)
			Region10.to_excel(writer, sheet_name='{}'.format(names[9]),index=False)
			Region11.to_excel(writer, sheet_name='{}'.format(names[10]),index=False)
			Region12.to_excel(writer, sheet_name='{}'.format(names[11]),index=False)
			Region13.to_excel(writer, sheet_name='{}'.format(names[12]),index=False)
		
	
	def init_regions(self):
		self.RegionA = pd.DataFrame()
		self.RegionB = pd.DataFrame()
		self.RegionC = pd.DataFrame()
		self.RegionD = pd.DataFrame()
		self.RegionE = pd.DataFrame()
		self.RegionF = pd.DataFrame()
		self.RegionG = pd.DataFrame()
		self.RegionH = pd.DataFrame()
		self.RegionI = pd.DataFrame()
		self.RegionJ = pd.DataFrame()
		self.RegionK = pd.DataFrame()
		self.RegionL = pd.DataFrame()
		self.RegionM = pd.DataFrame()
		
	def init_regions2(self):
		self.Region1 = pd.DataFrame()
		self.Region2 = pd.DataFrame()
		self.Region3 = pd.DataFrame()
		self.Region4 = pd.DataFrame()
		self.Region5 = pd.DataFrame()
		self.Region6 = pd.DataFrame()
		self.Region7 = pd.DataFrame()
		self.Region8 = pd.DataFrame()
		self.Region9 = pd.DataFrame()
		self.Region10 = pd.DataFrame()
		self.Region11 = pd.DataFrame()
		self.Region12 = pd.DataFrame()
		self.Region13 = pd.DataFrame()
	
	def regionExcelbook_by_region_decades (self,mode):
		
		self.init_regions()
		
		names = ['Sea of Okhotsk','Bering Sea','Hudson Bay','Baffin Bay','East Greenland Sea','Barents Sea','Kara Sea','Laptev Sea','East Siberian Sea','Chukchi Sea','Beaufort Sea','Canadian Archipelago','Central Arctic']
#		
		if mode == 'normal':
			decade_names = ['1980s','1990s','2000s','2010s']
			decades = [1980,1990,2000,2010]
			years = 10
		
			inputfile = 'temp/regional/Regional_{}.csv'
			outputfile = 'YYY_Regional_by_Region_decade.xlsx'
		elif mode == 'decade':
			inputfile = 'temp/regional/Regional_{}.csv'
			outputfile = 'YYY_Regional_by_Region_decade_2000-19.csv'
			
			decade_names = ['2000-19']
			decades = [2000]
			years = 20
			
		
		for index,xxx in enumerate(decade_names):
			self.init_regions2()
			for year in range(decades[index],decades[index]+years):
				AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
				Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
				self.Region1[str(year)] = Climatedata.B
				self.Region2[str(year)] = Climatedata.C
				self.Region3[str(year)] = Climatedata.D
				self.Region4[str(year)] = Climatedata.E
				self.Region5[str(year)] = Climatedata.F
				self.Region6[str(year)] = Climatedata.G
				self.Region7[str(year)] = Climatedata.H
				self.Region8[str(year)] = Climatedata.I
				self.Region9[str(year)] = Climatedata.J
				self.Region10[str(year)] = Climatedata.K
				self.Region11[str(year)] = Climatedata.L
				self.Region12[str(year)] = Climatedata.M
				self.Region13[str(year)] = Climatedata.N
				
			self.RegionA[xxx] = self.Region1.mean(axis=1)/1e6
			self.RegionB[xxx] = self.Region2.mean(axis=1)/1e6
			self.RegionC[xxx] = self.Region3.mean(axis=1)/1e6
			self.RegionD[xxx] = self.Region4.mean(axis=1)/1e6
			self.RegionE[xxx] = self.Region5.mean(axis=1)/1e6
			self.RegionF[xxx] = self.Region6.mean(axis=1)/1e6
			self.RegionG[xxx] = self.Region7.mean(axis=1)/1e6
			self.RegionH[xxx] = self.Region8.mean(axis=1)/1e6
			self.RegionI[xxx] = self.Region9.mean(axis=1)/1e6
			self.RegionJ[xxx] = self.Region10.mean(axis=1)/1e6
			self.RegionK[xxx] = self.Region11.mean(axis=1)/1e6
			self.RegionL[xxx] = self.Region12.mean(axis=1)/1e6
			self.RegionM[xxx] = self.Region13.mean(axis=1)/1e6
			
#			print(Climatedata.B[0])
		if mode == 'normal':
			with pd.ExcelWriter(outputfile) as writer:
				self.RegionA.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
				self.RegionB.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
				self.RegionC.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
				self.RegionD.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
				self.RegionE.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)
				self.RegionF.to_excel(writer, sheet_name='{}'.format(names[5]),index=False)
				self.RegionG.to_excel(writer, sheet_name='{}'.format(names[6]),index=False)
				self.RegionH.to_excel(writer, sheet_name='{}'.format(names[7]),index=False)
				self.RegionI.to_excel(writer, sheet_name='{}'.format(names[8]),index=False)
				self.RegionJ.to_excel(writer, sheet_name='{}'.format(names[9]),index=False)
				self.RegionK.to_excel(writer, sheet_name='{}'.format(names[10]),index=False)
				self.RegionL.to_excel(writer, sheet_name='{}'.format(names[11]),index=False)
				self.RegionM.to_excel(writer, sheet_name='{}'.format(names[12]),index=False)
		
		elif mode == 'decade':
			self.csvexport(outputfile,[self.RegionA,self.RegionB,self.RegionC,self.RegionD,self.RegionE,self.RegionF,
								 self.RegionG,self.RegionH,self.RegionI,self.RegionJ,self.RegionK,self.RegionL,self.RegionM])
			

mode = 'normal' #normal, decade

action = Data_restructure()
if __name__ == "__main__":
 	action.regionExcelbook_whole_Arctic(mode)
 	# action.regionExcelbook_by_year()
 	# action.regionExcelbook_by_region()
 	action.regionExcelbook_by_region_decades(mode)
