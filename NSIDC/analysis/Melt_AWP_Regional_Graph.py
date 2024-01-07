import pandas as pd
import matplotlib.pyplot as plt
#style.use('ggplot')


class Graph_Creater:

    def __init__  (self):
        self.year = 2016
        self.month = 1
        self.day = 1
            
        
    
    def make_melt_awp_graph(self,df,sheet_name,xxx):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Ice Melt AWP', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
        x = [-20,11,42,72,103,134,163]
        plt.xticks(x,labels)

        ax.set_ylabel('clear sky energy balance in EJ (over ice)')
        ax.text(0.02, 0.94, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.02, 0.92, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.7, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0.1,0.1,1],[0.1,0.1,0.1],[0.2,0.8,0.1],[0.95,0.5,0.1],[0.6,0.15,0.9]]
        
        minimum = -18
        maximum = 8
        ax.grid(True)
        
        j =0
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2,label=df[i].name)
            j +=1
        
        
        plt.axis([0,186,minimum,maximum])
        plt.legend(loc=1, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('Melt_AWP/img/regional/Melt_AWP_Daily_Region{}.png'.format(xxx))
        #plt.show()
        plt.close()

    
    def make_melt_awp_graph_accu(self,df,sheet_name,xxx):
        fig = plt.figure(figsize=(10, 6.5))
        fig.suptitle(str(sheet_name)+' - Accumulated Ice Melt AWP', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
        x = [-20,11,42,72,103,134,163]
        plt.xticks(x,labels)

        ax.set_ylabel('clear sky energy balance in  EJ (over ice)')
        ax.text(0.72, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        ax.text(0.72, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
        
        ax.text(0.7, -0.06, 'cryospherecomputing.com/melt-awp',transform=ax.transAxes,color='grey', fontsize=10)
        
        colourlist = [[0.1,0.1,1],[0.1,0.1,0.1],[0.2,0.8,0.1],[0.95,0.5,0.1],[0.6,0.15,0.9]]
        
        minimum = -1400
        maximum = 500
        ax.grid(True)

        j =0
        for i in df:
            plt.plot(df[i],color=colourlist[j],lw=2,label=df[i].name)
            j +=1
        
        
        plt.axis([0,186,minimum,maximum])
        plt.legend(loc=2, shadow=True, fontsize='medium')
        fig.tight_layout(pad=1)
        fig.subplots_adjust(top=0.95)
        fig.savefig('Melt_AWP/img/regional/Melt_AWP_Accu_Region{}.png'.format(xxx))
        #plt.show()
        plt.close()


            
    def loadMelt_AWP_data(self):
        
        excelfile = 'Melt_AWP/Melt_AWP_by_region_Daily_decades.xlsx'
        excelfile2 = 'Melt_AWP/Melt_AWP_by_region_decades.xlsx'
        for xxx in range(0,13):    #13 regional
            xls = pd.ExcelFile(excelfile)
            sheet_name = xls.sheet_names[xxx]
            df = pd.read_excel(xls,sheet_name=xxx)
            df2 = pd.read_excel(excelfile2,sheet_name=xxx)
            
            self.make_melt_awp_graph(df,sheet_name,xxx+1)
            self.make_melt_awp_graph_accu(df2,sheet_name,xxx+1)
#


action = Graph_Creater()
if __name__ == "__main__":
    print('main')
    action.loadMelt_AWP_data()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA