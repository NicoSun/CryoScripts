import pandas as pd
import numpy as np



class Data_restructure:

	def __init__  (self):
		print('Data_restructure')

	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
	
	def appendSuperRegionList(self,data):
		
		for x,y in enumerate(data[0]):
			self.datum.append (data[0][x])
			self.SoO.append(data[1][x])
			self.Bers.append(data[2][x])
			self.HB.append(data[3][x])
			self.BB.append(data[4][x])
			self.EG.append(data[5][x])
			self.BaS.append(data[6][x])
			self.KS.append(data[7][x])
			self.LS.append(data[8][x])
			self.ES.append(data[9][x])
			self.CS.append(data[10][x])
			self.BeaS.append(data[11][x])
			self.CA.append(data[12][x])
			self.AB.append(data[13][x])
		
	def final_region_value(self,data):
		
		self.SoO.append(data[0][-1])
		self.Bers.append(data[1][-1])
		self.HB.append(data[2][-1])
		self.BB.append(data[3][-1])
		self.EG.append(data[4][-1])
		self.BaS.append(data[5][-1])
		self.KS.append(data[6][-1])
		self.LS.append(data[7][-1])
		self.ES.append(data[8][-1])
		self.CS.append(data[9][-1])
		self.BeaS.append(data[10][-1])
		self.CA.append(data[11][-1])
		self.AB.append(data[12][-1])


	def appendSuperList(self,data):
		
		for x,y in enumerate(data[0]):
			self.datum.append(data[0][x])
			self.AWP_Daily_mean.append(data[1][x])
			self.AWP_Accu_mean.append(data[2][x])
			self.AWP_Daily_mean_centre.append(data[3][x])
			self.AWP_Accu_mean_centre.append(data[4][x])
			
	def createSuperlist (self):
		
		self.datum = []
		self.AWP_Daily_mean = []
		self.AWP_Accu_mean = []
		self.AWP_Daily_mean_centre = []
		self.AWP_Accu_mean_centre = []
		
		for year in range(1979,2023):
			AWP_mean = ['A', 'B', 'C', 'D', 'E']
			Climatedata = pd.read_csv('Melt_AWP/csv/_melt_AWP_{}.csv'.format(year), names=AWP_mean,header=0)
			column1 = Climatedata.A.tolist()
			column2 = Climatedata.B.tolist()
			column3 = Climatedata.C.tolist()
			column4 = Climatedata.D.tolist()
			column5 = Climatedata.E.tolist()
			data = [column1,column2,column3,column4,column5]
			self.appendSuperList(data)
			
		self.csvexport('Melt_AWP/Superlist_main.csv',[self.datum,self.AWP_Daily_mean,self.AWP_Accu_mean,
					self.AWP_Daily_mean_centre,self.AWP_Accu_mean_centre])
	
	def createSuperRegionList (self):
		
		self.SoO = ['Sea of Okhotsk']
		self.Bers = ['Bering Sea']
		self.HB = ['Hudson Bay']
		self.BB = ['Baffin Bay']
		self.EG = ['East Greenland Sea']
		self.BaS = ['Barents Sea']
		self.KS = ['Kara Sea']
		self.LS = ['Laptev Sea']
		self.ES = ['East Siberian Sea']
		self.CS = ['Chukchi Sea']
		self.BeaS = ['Beaufort Sea']
		self.CA = ['Canadian Archipelago']
		self.AB = ['Central Arctic']
		
		for year in range(1979,2023):
			AWP_mean = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
			Climatedata = pd.read_csv('Melt_AWP/csv/_melt_AWP_regional_{}.csv'.format(year), names=AWP_mean,header=0)
			column2 = Climatedata.B.tolist()
			column3 = Climatedata.C.tolist()
			column4 = Climatedata.D.tolist()
			column5 = Climatedata.E.tolist()
			column6 = Climatedata.F.tolist()
			column7 = Climatedata.G.tolist()
			column8 = Climatedata.H.tolist()
			column9 = Climatedata.I.tolist()
			column10 = Climatedata.J.tolist()
			column11 = Climatedata.K.tolist()
			column12 = Climatedata.L.tolist()
			column13 = Climatedata.M.tolist()
			column14 = Climatedata.N.tolist()
			data = [column2,column3,column4,column5,column6,column7,column8,column9,column10,column11,column12,column13,column14]
#			self.appendSuperRegionList(data)
			self.final_region_value(data)
			print(year)

		self.csvexport('Melt_AWP/Melt_AWP_region_Heatmap.csv',[self.SoO,self.Bers,self.HB,self.BB,self.EG,
					 self.BaS,self.KS,self.LS,self.ES,self.CS,self.BeaS,self.CA,self.AB])
	
	def regionExcelbook_whole_Arctic (self,mode):
		RegionA = pd.DataFrame()
		RegionB = pd.DataFrame()
		RegionC = pd.DataFrame()
		RegionD = pd.DataFrame()
			
		if mode == 'decade':
			sheetnames = ['Daily','Accu','Daily High','Accu High']
			inputfile = 'Melt_AWP/csv/_melt_AWP_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_new.xlsx'
			decade_names = ['1980s','1990s','2000s','2010s']
			decades = [1980,1990,2000,2010]
			years = 10

			for index,xxx in enumerate(decade_names):
				Region1 = pd.DataFrame()
				Region2 = pd.DataFrame()
				Region3 = pd.DataFrame()
				Region4 = pd.DataFrame()
				for year in range(decades[index],decades[index]+years):
					AWP_mean = ['A', 'B', 'C', 'D', 'E']
					Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
					Region1[str(year)] = Climatedata.B
					Region2[str(year)] = Climatedata.C
					Region3[str(year)] = Climatedata.D
					Region4[str(year)] = Climatedata.E
			
			
				RegionA[xxx] = Region1.mean(axis=1)
				RegionB[xxx] = Region2.mean(axis=1)
				RegionC[xxx] = Region3.mean(axis=1)
				RegionD[xxx] = Region4.mean(axis=1)
			
			outputfile = 'Melt_AWP/Melt_AWP_decades.xlsx'
			
			with pd.ExcelWriter(outputfile) as writer:
				RegionA.to_excel(writer, sheet_name='{}'.format(sheetnames[0]),index=False)
				RegionB.to_excel(writer, sheet_name='{}'.format(sheetnames[1]),index=False)
				RegionC.to_excel(writer, sheet_name='{}'.format(sheetnames[2]),index=False)
				RegionD.to_excel(writer, sheet_name='{}'.format(sheetnames[3]),index=False)
			
#			outputfile = 'Melt_AWP/Melt_AWP_decades.csv'
#			self.csvexport(outputfile,[RegionA,RegionB,RegionC,RegionD])

		else:
			Region1 = pd.DataFrame()
			Region2 = pd.DataFrame()
			Region3 = pd.DataFrame()
			Region4 = pd.DataFrame()
			
			names = ['Daily','Accu','Daily High','Accu High']
			inputfile = 'Melt_AWP/csv/_melt_AWP_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_new.xlsx'
	
			
			for year in range(1979,2023):
				AWP_mean = ['A', 'B', 'C', 'D', 'E']
				Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
				Region1[str(year)] = Climatedata.B
				Region2[str(year)] = Climatedata.C
				Region3[str(year)] = Climatedata.D
				Region4[str(year)] = Climatedata.E
				
				
			with pd.ExcelWriter(outputfile) as writer:
				Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
				Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
				Region3.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
				Region4.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)

	
	
	
	def regionExcelbook_Daily_by_year (self):
		with pd.ExcelWriter('Melt_AWP/Melt_AWP_by_Year_regional_Daily.xlsx') as writer:
			for year in range(1979,2023):
				Climatedata = pd.read_csv('Melt_AWP/csv/_melt_AWP_regional_daily_{}.csv'.format(year))
				Climatedata.to_excel(writer, sheet_name=str(year),index=False)
				
	def regionExcelbook_Accu_by_year (self):
		with pd.ExcelWriter('Melt_AWP/Melt_AWP_by_Year_regional_Accu.xlsx') as writer:
			for year in range(1979,2023):
				Climatedata = pd.read_csv('Melt_AWP/csv/_melt_AWP_regional_{}.csv'.format(year))
				Climatedata.to_excel(writer, sheet_name=str(year),index=False)
				
	def regionExcelbook_by_region (self,mode):
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
		if mode == 'Accu':
			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_by_region.xlsx'
		elif mode == 'Daily':
			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_daily_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_by_region_Daily.xlsx'
		
		for year in range(1979,2023):
			AWP_mean = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
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
		decade_names = ['1980s','1990s','2000s','2010s']
		decades = [1980,1990,2000,2010]
		years = 10
		
		if mode == 'Accu':
			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_by_region_decades.xlsx'
		elif mode == 'Daily':
			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_daily_{}.csv'
			outputfile = 'Melt_AWP/Melt_AWP_by_region_Daily_decades.xlsx'
			
		elif mode == 'decade':
			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_{}.csv'
			outputfile = 'Melt_AWP/2020s_mean_Melt_AWP_by_region.csv'
			
#			inputfile = 'Melt_AWP/csv/_melt_AWP_regional_daily_{}.csv'
#			outputfile = 'Melt_AWP/2020mean_Melt_AWP_by_region_Daily.csv'
			decade_names = ['2000-19']
			decades = [2000]
			years = 20
			
		
		for index,xxx in enumerate(decade_names):
			self.init_regions2()
			for year in range(decades[index],decades[index]+years):
				AWP_mean = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
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
				
			self.RegionA[xxx] = self.Region1.mean(axis=1)
			self.RegionB[xxx] = self.Region2.mean(axis=1)
			self.RegionC[xxx] = self.Region3.mean(axis=1)
			self.RegionD[xxx] = self.Region4.mean(axis=1)
			self.RegionE[xxx] = self.Region5.mean(axis=1)
			self.RegionF[xxx] = self.Region6.mean(axis=1)
			self.RegionG[xxx] = self.Region7.mean(axis=1)
			self.RegionH[xxx] = self.Region8.mean(axis=1)
			self.RegionI[xxx] = self.Region9.mean(axis=1)
			self.RegionJ[xxx] = self.Region10.mean(axis=1)
			self.RegionK[xxx] = self.Region11.mean(axis=1)
			self.RegionL[xxx] = self.Region12.mean(axis=1)
			self.RegionM[xxx] = self.Region13.mean(axis=1)
			
#			print(Climatedata.B[0])
		if mode == 'Daily' or mode =='Accu':
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
			

mode = 'decade' #Daily, Accu, decade

action = Data_restructure()
if __name__ == "__main__":
# 	action.createSuperlist()
 	# action.createSuperRegionList()
# 	action.regionExcelbook_whole_Arctic(mode)
# 	action.regionExcelbook_Daily_by_year()
# 	action.regionExcelbook_Accu_by_year()
# 	action.regionExcelbook_by_region(mode)
	action.regionExcelbook_by_region_decades(mode)
