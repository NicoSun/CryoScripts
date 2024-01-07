import pandas as pd
import matplotlib.pyplot as plt
#style.use('ggplot')


class Graph_Creater:

    def __init__  (self):
        self.year = 2016
        self.month = 1
        self.day = 1
            
        
            
    def make_mean_graph(self,df,sheet_name,regionnumber):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Snow Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        x = [0,30,59,90,120,151,181,212,243,273,304,334]
        plt.xticks(x,labels)

        ax.set_ylabel('Extent in 10^6 'r'$km^2$')
        ax.text(0.02, 0.05, r'Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.02, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.68, -0.06, 'cryospherecomputing.com/snow-regional',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0.1,0.1,0.1],[1,0,0],[1,0.5,0],[0.9,0.9,0],
                [0,0.8,0],[0,0.5,1],[0.5,0,0.5],[1,0,1]]
        
        ax.grid(True)
        df = df/1e6
        j =0
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2)
            j +=1
        
        ymin = 0
        ymax = max(df.max(0))*1.05
        plt.axis([0,365,ymin,ymax])
        plt.legend(loc="upper center", shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('temp/regional/Mean_extent_Region{}.png'.format(regionnumber))
        #plt.show()
        plt.close()
        
    def make_region_graph(self,df,sheet_name,region,regionnumber):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Snow Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        x = [0,30,59,90,120,151,181,212,243,273,304,334]
        plt.xticks(x,labels)

        ax.set_ylabel('Extent in 10^6 'r'$km^2$')
        ax.text(0.01, 0.05, r'Extent Data: NOAA / NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.01, 0.02, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.68, -0.06, 'cryospherecomputing.com/snow-regional',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0,0,1],[0.1,0.1,0.1],[0.9,0,0]]
        
        ax.grid(True)
        df = df/1e6
        j =0
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2,label=df[i].name)
            j +=1
        
        ymin = 0
        ymax = max(df.max(0))*1.05
        plt.axis([0,365,ymin,ymax])
        plt.legend(loc=4, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('temp/regional/{}_Region{}.png'.format(region,regionnumber))
        # plt.show()
        plt.close()
    
    def make_low_res_graph(self,df,sheet_name,region,regionnumber):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Weekly 200km Resolution Snow Extent', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        x = [0,4.4,8.8,13.2,17.6,22,26.4,30.8,35.2,39.6,44,48.4]
        plt.xticks(x,labels)

        ax.set_ylabel('Extent in 10^6 'r'$km^2$')
        ax.text(0.02, 0.05, r'Extent Data: NCDC / NOAA', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.02, r'Graph: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.68, -0.06, 'cryospherecomputing.com/snow',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0,0,1],[0.1,0.1,0.1],[0.9,0,0],[0,0.6,0],[0.9,0.5,0.2]]
        
        ax.grid(True)
        j =0
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2)
            j +=1
        
        ymin = 0
        ymax = max(df.max(0))*1.05
        plt.axis([0,52,ymin,ymax])
        plt.legend(loc=4, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('temp/regional/{}_Region{}.png'.format(region,regionnumber))
        plt.show()
        # plt.close()
    
    
    def mean_Regionaldata(self):
        
        excelfile = 'CSVexport/Mean_Snow_Extents.xlsx'

        for xxx in range(0,5):    #13 regional
            xls = pd.ExcelFile(excelfile)
            sheet_name = xls.sheet_names[xxx]
            df = pd.read_excel(xls,sheet_name=xxx)
            df.drop(columns=df.columns[0], inplace=True)
            
            self.make_mean_graph(df,sheet_name,xxx+1)

            
    def load_ten_year_mean(self,region):
        
        if region =='Europe':
            excelfile = f'CSVexport/10_year_mean_{region}.xlsx'
            sheets = 5
        elif region =='Asia':
            excelfile = f'CSVexport/10_year_mean_{region}.xlsx'
            sheets = 9
        elif region =='NorthAmerica':
            excelfile = f'CSVexport/10_year_mean_{region}.xlsx'
            sheets = 12
        
        for xxx in range(0,sheets):    #13 sheets
            xls = pd.ExcelFile(excelfile)
            sheet_name = xls.sheet_names[xxx]
            df = pd.read_excel(xls,sheet_name=xxx)
            self.make_region_graph(df,sheet_name,region,xxx+1)
            
    def low_res_ten_year_mean(self):
        excelfile = 'CSVexport/Low_Res_extent_decade.xlsx'
        
        sheets = 4

        for xxx in range(0,sheets):    #13 regional
            xls = pd.ExcelFile(excelfile)
            sheet_name = xls.sheet_names[xxx]
            df = pd.read_excel(xls,sheet_name=xxx)
            df.drop(['Date'], 1, inplace=True)
            
            
            self.make_low_res_graph(df,sheet_name,'Low_res',xxx+1)

            
#
mode = 'Europe' #Asia, Europe, NorthAmerica

action = Graph_Creater()
if __name__ == "__main__":
    print('main')
#    action.mean_Regionaldata()
    action.load_ten_year_mean(mode)
    # action.low_res_ten_year_mean()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA