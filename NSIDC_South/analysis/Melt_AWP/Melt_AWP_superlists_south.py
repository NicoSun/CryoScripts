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

        
    def final_region_value(self,data):
        
        self.region1.append(data[0][-1])
        self.region2.append(data[1][-1])
        self.region3.append(data[2][-1])
        self.region4.append(data[3][-1])
        self.region5.append(data[4][-1])


    
    def createSuperRegionList (self):
        
        self.region1 = ['Weddel_Sea']
        self.region2 = ['Indian_Ocean']
        self.region3 = ['Pacific_Ocean']
        self.region4 = ['Ross_Sea']
        self.region5 = ['Bell_Amun_Sea']
        
        for year in range(1980,2023):
            AWP_mean = ['A', 'B', 'C', 'D', 'E']
            Climatedata = pd.read_csv(f'Melt_AWP/csv/Melt_AWP_regional_{year}_south.csv', names=AWP_mean,header=0)
            column1 = Climatedata.A.tolist()
            column2 = Climatedata.B.tolist()
            column3 = Climatedata.C.tolist()
            column4 = Climatedata.D.tolist()
            column5 = Climatedata.E.tolist()
            data = [column1,column2,column3,column4,column5]
#            self.appendSuperRegionList(data)
            self.final_region_value(data)
            print(year)

        self.csvexport('Melt_AWP/Melt_AWP_region_Heatmap_south.csv',[self.region1,self.region2,self.region3,self.region4,self.region5])
    
    def regionExcelbook_whole_Antarctic (self):
        Region1 = pd.DataFrame()
        Region2 = pd.DataFrame()

        
        names = ['Daily','Accu']
        inputfile = 'Melt_AWP/csv/Melt_AWP_{}_south.csv'
        outputfile = 'Melt_AWP/Melt_AWP_new.xlsx'

        
        for year in range(1980,2023):
            AWP_mean = ['A', 'B', 'C']
            Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
            Region1[str(year)] = Climatedata.B
            Region2[str(year)] = Climatedata.C

            
#            print(Climatedata.B[0])
        with pd.ExcelWriter(outputfile) as writer:
            Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
            Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)

    
    
    def regionExcelbook_Daily_by_year (self):
        with pd.ExcelWriter('Melt_AWP/Melt_AWP_by_Year_regional_Daily.xlsx') as writer:
            for year in range(1980,2023):
                Climatedata = pd.read_csv('Melt_AWP/csv/Melt_AWP_regional_daily_{}_south.csv'.format(year))
                Climatedata.to_excel(writer, sheet_name=str(year),index=False)
                
    def regionExcelbook_Accu_by_year (self):
        with pd.ExcelWriter('Melt_AWP/Melt_AWP_by_Year_regional_Accu.xlsx') as writer:
            for year in range(1980,2023):
                Climatedata = pd.read_csv('Melt_AWP/csv/Melt_AWP_regional_{}_south.csv'.format(year))
                Climatedata.to_excel(writer, sheet_name=str(year),index=False)
                
    def regionExcelbook_by_region (self,mode):
        Region1 = pd.DataFrame()
        Region2 = pd.DataFrame()
        Region3 = pd.DataFrame()
        Region4 = pd.DataFrame()
        Region5 = pd.DataFrame()

        
        names = ['Weddel_Sea','Indian_Ocean','Pacific_Ocean','Ross_Sea','Bell_Amun_Sea']
#        
        if mode == 'Accu':
            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_{}_south.csv'
            outputfile = 'Melt_AWP/Melt_AWP_by_region.xlsx'
        elif mode == 'Daily':
            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_daily_{}_south.csv'
            outputfile = 'Melt_AWP/Melt_AWP_by_region_Daily.xlsx'
        
        for year in range(1980,2023):
            AWP_mean = ['B', 'C', 'D', 'E', 'F']
            Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
            Region1[str(year)] = Climatedata.B
            Region2[str(year)] = Climatedata.C
            Region3[str(year)] = Climatedata.D
            Region4[str(year)] = Climatedata.E
            Region5[str(year)] = Climatedata.F

            
#            print(Climatedata.B[0])
        with pd.ExcelWriter(outputfile) as writer:
            Region1.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
            Region2.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
            Region3.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
            Region4.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
            Region5.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)

        
    
    def init_regions(self):
        self.RegionA = pd.DataFrame()
        self.RegionB = pd.DataFrame()
        self.RegionC = pd.DataFrame()
        self.RegionD = pd.DataFrame()
        self.RegionE = pd.DataFrame()

        
    def init_regions2(self):
        self.Region1 = pd.DataFrame()
        self.Region2 = pd.DataFrame()
        self.Region3 = pd.DataFrame()
        self.Region4 = pd.DataFrame()
        self.Region5 = pd.DataFrame()

    
    def regionExcelbook_by_region_decades (self,mode):
        
        self.init_regions()
        
        names = ['Weddel_Sea','Indian_Ocean','Pacific_Ocean','Ross_Sea','Bell_Amun_Sea']
        
        if mode == 'Accu':
            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_{}_south.csv'
            outputfile = 'Melt_AWP/Melt_AWP_by_region_decades.xlsx'
        elif mode == 'Daily':
            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_daily_{}_south.csv'
            outputfile = 'Melt_AWP/Melt_AWP_by_region_daily_decades.xlsx'

        decade_names = ['1980s','1990s','2000s','2010s']
        decades = [1980,1990,2000,2010]
        years = 10
        
        if mode == 'decades':
            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_{}_south.csv'
            outputfile = 'Melt_AWP/Melt_AWP_2020s_mean_by_region.xlsx'
            
#            inputfile = 'Melt_AWP/csv/Melt_AWP_regional_daily_{}.csv'
#            outputfile = 'Melt_AWP/2020mean_AWP_by_region_Daily.csv'
            decade_names = ['2000-19']
            decades = [2000]
            years = 20
            
        
        for index,xxx in enumerate(decade_names):
            self.init_regions2()
            for year in range(decades[index],decades[index]+years):
                AWP_mean = ['B', 'C', 'D', 'E', 'F']
                Climatedata = pd.read_csv(inputfile.format(year), names=AWP_mean,header=0)
                self.Region1[str(year)] = Climatedata.B
                self.Region2[str(year)] = Climatedata.C
                self.Region3[str(year)] = Climatedata.D
                self.Region4[str(year)] = Climatedata.E
                self.Region5[str(year)] = Climatedata.F

                
            self.RegionA[xxx] = self.Region1.mean(axis=1)
            self.RegionB[xxx] = self.Region2.mean(axis=1)
            self.RegionC[xxx] = self.Region3.mean(axis=1)
            self.RegionD[xxx] = self.Region4.mean(axis=1)
            self.RegionE[xxx] = self.Region5.mean(axis=1)

            
#            print(Climatedata.B[0])
        if mode == 'Daily' or 'Accu':
            with pd.ExcelWriter(outputfile) as writer:
                self.RegionA.to_excel(writer, sheet_name='{}'.format(names[0]),index=False)
                self.RegionB.to_excel(writer, sheet_name='{}'.format(names[1]),index=False)
                self.RegionC.to_excel(writer, sheet_name='{}'.format(names[2]),index=False)
                self.RegionD.to_excel(writer, sheet_name='{}'.format(names[3]),index=False)
                self.RegionE.to_excel(writer, sheet_name='{}'.format(names[4]),index=False)

        
        if mode == 'decades':
            self.csvexport(outputfile,[self.RegionA,self.RegionB,self.RegionC,self.RegionD,self.RegionE])
            
    def all_lists(self):
        self.createSuperRegionList()
        self.regionExcelbook_whole_Antarctic()
        self.regionExcelbook_Daily_by_year()
        self.regionExcelbook_Accu_by_year()
        self.regionExcelbook_by_region_decades('decades')
        
        mode = 'Accu'
        self.regionExcelbook_by_region(mode)
        self.regionExcelbook_by_region_decades(mode)
        mode = 'Daily'
        self.regionExcelbook_by_region(mode)
        self.regionExcelbook_by_region_decades(mode)
        
            

mode = 'all' #Daily, Accu, decades, all

action = Data_restructure()
if __name__ == "__main__":
    if mode == 'all':
        action.all_lists()
        
    elif mode == 'Accu':
        action.regionExcelbook_by_region(mode)
        action.regionExcelbook_by_region_decades(mode)
    elif mode == 'Daily':
        action.regionExcelbook_by_region(mode)
        action.regionExcelbook_by_region_decades(mode)
