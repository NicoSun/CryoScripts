import pandas as pd
import numpy as np
import CryoIO



class Data_restructure:

    def __init__  (self):
        print('Data_restructure')
    
    
    def regionExcelbook_Daily_by_year (self):
        with pd.ExcelWriter('CSVexport/Melt_AWP_by_Year_regional_Daily.xlsx') as writer:
            for year in range(1979,2020):
                Climatedata = pd.read_csv('Melt_AWP/csv/_melt_AWP_regional_daily_{}.csv'.format(year))
                Climatedata.to_excel(writer, sheet_name=year,index=False)
                
                
    def regionExcelbook_by_region (self,region):
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
        
        if region =='Europe':
            names = ['North Europe','West Europe','Central Europe','Southern Europe','Eastern Europe'] # 5
            AWP_mean = ['A', 'B', 'C', 'D', 'E']
        elif region =='Asia':
            names = ['East Siberia','Central Siberia','West Siberia','Central Asia','Central Mountain Asia','Eastern Asia','Tibet','Western Asia','Persia'] #9
            AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        elif region =='NorthAmerica':
            names = ['Greenland','eastern Canada','Central Canada','Canadian Rockies','northern Canada','Alaska','US NE','US SE','US MidWest','US SW',
            'US Pacific','US Rockies'] # 12
            AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        inputfile = 'CSVexport/Region_raw_data/{}_Regional_extent_{}.csv'
        outputfile = f'CSVexport/Regional_data_{region}.xlsx'

        
        for year in range(1997,2023):
            Climatedata = pd.read_csv(inputfile.format(year,region), names=AWP_mean,header=0)
            Region1[year] = Climatedata.A
            Region2[year] = Climatedata.B
            Region3[year] = Climatedata.C
            Region4[year] = Climatedata.D
            Region5[year] = Climatedata.E
            if region == 'Asia' or region == 'NorthAmerica':
                Region6[year] = Climatedata.F
                Region7[year] = Climatedata.G
                Region8[year] = Climatedata.H
                Region9[year] = Climatedata.I
            if region == 'NorthAmerica':
                Region10[year] = Climatedata.J
                Region11[year] = Climatedata.K
                Region12[year] = Climatedata.L

            
#            print(Climatedata.B[0])
        with pd.ExcelWriter(outputfile) as writer:
            Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
            Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
            Region3.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
            Region4.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
            Region5.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)
            if region == 'Asia' or region == 'NorthAmerica':
                Region6.to_excel(writer, sheet_name='{}'.format(names[5]),index=False)
                Region7.to_excel(writer, sheet_name='{}'.format(names[6]),index=False)
                Region8.to_excel(writer, sheet_name='{}'.format(names[7]),index=False)
                Region9.to_excel(writer, sheet_name='{}'.format(names[8]),index=False)
            if region == 'NorthAmerica':
                Region10.to_excel(writer, sheet_name='{}'.format(names[9]),index=False)
                Region11.to_excel(writer, sheet_name='{}'.format(names[10]),index=False)
                Region12.to_excel(writer, sheet_name='{}'.format(names[11]),index=False)
        
    
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
    
    def regionExcelbook_by_region_decades (self,region):
        
        self.init_regions()
        
        if region =='Europe':
            names = ['North Europe','West Europe','Central Europe','Southern Europe','Eastern Europe'] # 5
            AWP_mean = ['A', 'B', 'C', 'D', 'E']
        elif region =='Asia':
            names = ['East Siberia','Central Siberia','West Siberia','Central Asia','Central Mountain Asia','Eastern Asia','Tibet','Western Asia','Persia'] #9
            AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        elif region =='NorthAmerica':
            names = ['Greenland','Eastern Canada','Central Canada','Canadian Rockies','Northern Canada','Alaska','US NE','US SE','US MidWest','US SW',
            'US Pacific','US Rockies'] # 12
            AWP_mean = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

        inputfile = 'CSVexport/Region_raw_data/{}_Regional_extent_{}.csv'
        outputfile = f'CSVexport/10_year_mean_{region}.xlsx'
        
        decade_names = ['1997-06','2005-14','2013-22']
        decades = [1997,2005,2013]
        years = 10
        
# =============================================================================
#         outputfile = f'CSVexport/20_year_mean_{region}.xlsx'
#         decade_names = ['2000-19']
#         decades = [2000]
#         years = 10
# =============================================================================

        for index,xxx in enumerate(decade_names):
            self.init_regions2()
            for year in range(decades[index],decades[index]+years):
                Climatedata = pd.read_csv(inputfile.format(year,region), names=AWP_mean,header=0)
                self.Region1[year] = Climatedata.A
                self.Region2[year] = Climatedata.B
                self.Region3[year] = Climatedata.C
                self.Region4[year] = Climatedata.D
                self.Region5[year] = Climatedata.E
                if region == 'Asia' or region == 'NorthAmerica':
                    self.Region6[year] = Climatedata.F
                    self.Region7[year] = Climatedata.G
                    self.Region8[year] = Climatedata.H
                    self.Region9[year] = Climatedata.I
                if region == 'NorthAmerica':
                    self.Region10[year] = Climatedata.J
                    self.Region11[year] = Climatedata.K
                    self.Region12[year] = Climatedata.L

                
            self.RegionA[xxx] = self.Region1.mean(axis=1).astype(int)
            self.RegionB[xxx] = self.Region2.mean(axis=1).astype(int)
            self.RegionC[xxx] = self.Region3.mean(axis=1).astype(int)
            self.RegionD[xxx] = self.Region4.mean(axis=1).astype(int)
            self.RegionE[xxx] = self.Region5.mean(axis=1).astype(int)
            if region == 'Asia' or region == 'NorthAmerica':
                self.RegionF[xxx] = self.Region6.mean(axis=1).astype(int)
                self.RegionG[xxx] = self.Region7.mean(axis=1).astype(int)
                self.RegionH[xxx] = self.Region8.mean(axis=1).astype(int)
                self.RegionI[xxx] = self.Region9.mean(axis=1).astype(int)
            if region == 'NorthAmerica':
                self.RegionJ[xxx] = self.Region10.mean(axis=1).astype(int)
                self.RegionK[xxx] = self.Region11.mean(axis=1).astype(int)
                self.RegionL[xxx] = self.Region12.mean(axis=1).astype(int)

            

        with pd.ExcelWriter(outputfile) as writer:
            self.RegionA.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
            self.RegionB.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
            self.RegionC.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
            self.RegionD.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
            self.RegionE.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)
            if region == 'Asia' or region == 'NorthAmerica':
                self.RegionF.to_excel(writer, sheet_name='{}'.format(names[5]),index=False)
                self.RegionG.to_excel(writer, sheet_name='{}'.format(names[6]),index=False)
                self.RegionH.to_excel(writer, sheet_name='{}'.format(names[7]),index=False)
                self.RegionI.to_excel(writer, sheet_name='{}'.format(names[8]),index=False)
            if region == 'NorthAmerica':
                self.RegionJ.to_excel(writer, sheet_name='{}'.format(names[9]),index=False)
                self.RegionK.to_excel(writer, sheet_name='{}'.format(names[10]),index=False)
                self.RegionL.to_excel(writer, sheet_name='{}'.format(names[11]),index=False)
# =============================================================================
#         if region == 'Europe':
#             regionarray = [self.RegionA,self.RegionB,self.RegionC,self.RegionD,self.RegionE]
#         if region == 'Asia':
#             regionarray = [self.RegionA,self.RegionB,self.RegionC,self.RegionD,self.RegionE,self.RegionF,
#                               self.RegionG,self.RegionH,self.RegionI]
#         if region == 'NorthAmerica':
#             regionarray = [self.RegionA,self.RegionB,self.RegionC,self.RegionD,self.RegionE,self.RegionF,
#                               self.RegionG,self.RegionH,self.RegionI,self.RegionJ,self.RegionK,self.RegionL]
# =============================================================================
        
        # CryoIO.csv_columnexport(f'CSVexport/{years}_year_mean_{region}.csv',regionarray)
                
    def low_res_ldata(self):
        
        decades = [1970,1980,1990,2000,2010]
        years = 10
        allregions = pd.DataFrame()
        excelfile = 'CSVexport/Low_Res_extent.xlsx'
        
        for sheetnumber in range(0,4):    #5 regional
            df = pd.read_excel(excelfile,sheet_name=sheetnumber)
            xls = pd.ExcelFile(excelfile)
            sheet_name2 = xls.sheet_names[sheetnumber]
            region = pd.DataFrame()
            for index,xxx in enumerate(decades):
                decade_mean = pd.DataFrame()
                for year in range(decades[index],decades[index]+years):
                    decade_mean[year] = df[year]
                region[decades[index]] = decade_mean.mean(axis=1) 
        
#        print(allregions)
        
            outputfile = '{}.xlsx'.format(sheet_name2)
            with pd.ExcelWriter(outputfile) as writer:
                region.to_excel(writer, sheet_name='{}'.format(sheet_name2),index=False)
    # =============================================================================
    #             self.RegionB.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
    #             self.RegionC.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
    #             self.RegionD.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
    # =============================================================================


mode = 'Europe' #Europe, Asia, NorthAmerica, decades

action = Data_restructure()
if __name__ == "__main__":
#    action.regionExcelbook_whole_Arctic(mode)
#    action.regionExcelbook_Daily_by_year()
    # action.regionExcelbook_by_region(mode)
    action.regionExcelbook_by_region_decades(mode)
#     action.low_res_ldata()

    
