import pandas as pd
import matplotlib.pyplot as plt
#style.use('ggplot')


class Graph_Creater:

    def __init__  (self):
        self.year = 2016
        self.month = 1
        self.day = 1
            
        
            
    def makegraph_daily(self,df,sheet_name,xxx):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Albedo-Warming Potential', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
        x = [-20,11,42,72,103,134,163]
        plt.xticks(x,labels)

        ax.set_ylabel('clear sky energy absorption in  [MJ / 'r'$m^2$]')
        ax.text(0.02, 0.94, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.92, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.75, -0.06, 'cryospherecomputing.com/awp',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0.1,0.1,1],[0.1,0.1,0.1],[0.2,0.8,0.1],[0.95,0.5,0.1],[0.6,0.15,0.9]]
        
        minimum = 0
        maximum = 31
        
        ax.grid(True)
        plt.plot(df['Icefree'],color=colourlist[0],lw=2,ls='--')
        df.drop(columns=df.columns[0], inplace=True)
        
        j =1
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2,label=df[i].name)
            j +=1
        
        
        plt.axis([0,186,minimum,maximum])
        plt.legend(loc=1, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('AWP/img/regional/North_AWP_RegionD{}.png'.format(xxx))
        plt.close()
        #plt.show()
    
    def makegraph_accu(self,df,sheet_name,xxx):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Accumulated Albedo-Warming Potential', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
        x = [-20,11,42,72,103,134,163]
        plt.xticks(x,labels)

        ax.set_ylabel('clear sky energy absorption in  [MJ / 'r'$m^2$]')
        ax.text(0.72, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.72, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.75, -0.06, 'cryospherecomputing.com/awp',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0.1,0.1,1],[0.1,0.1,0.1],[0.2,0.8,0.1],[0.95,0.5,0.1],[0.6,0.15,0.9]]
        
        minimum = 0
        maximum = 4500
        ax.grid(True)
        plt.plot(df['Icefree'],color=colourlist[0],lw=2,ls='--')
        df.drop(columns=df.columns[0], inplace=True)
        
        j =1
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2,label=df[i].name)
            j +=1
        
        
        plt.axis([0,186,minimum,maximum])
        plt.legend(loc=2, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('AWP/img/regional/North_AWP_RegionA{}.png'.format(xxx))
        #plt.show()
        plt.close()
    
    def loadRegionaldata(self):
        
        excelfile = 'AWP/AWP_regional_by_region_daily_decades.xlsx'
        excelfile2 = 'AWP/AWP_regional_by_region_decades.xlsx'
        for xxx in range(0,13):    #13 regional
            xls = pd.ExcelFile(excelfile)
            sheet_name = xls.sheet_names[xxx]
            df = pd.read_excel(xls,sheet_name=xxx)
            df2 = pd.read_excel(excelfile2,sheet_name=xxx)
            
            self.makegraph_daily(df,sheet_name,xxx+1)
            self.makegraph_accu(df2,sheet_name,xxx+1)
            
#


action = Graph_Creater()
if __name__ == "__main__":
    print('main')
    action.loadRegionaldata()



#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA