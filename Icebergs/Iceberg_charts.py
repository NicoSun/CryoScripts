import csv
import matplotlib.pyplot as plt
plt.style.use('dark_background')

class Iceberg_charts:
    
    def __init__  (self):
        self.run = True
        
    def load_list(self):
        listname = 'temp/iceberg_combined_area.csv'
        
        dictaa = {}
        with open(listname, newline='') as csvfile:
            tempreader = csv.reader(csvfile, delimiter=',')
            templist = list(tempreader)
        for xxx in templist:
            dictaa[xxx[0]] = float(xxx[1])
        # self.create_graph_distance(dictaa)
        # self.create_graph_age(dictaa)
        # self.create_calving_size(dictaa)
        # self.create_iceberg_size(dictaa)
        self.create_combined_iceberg_area(dictaa)
    
    
    def create_graph_distance(self,data):
        
        #remove grounded icebergs
        min_distance = 2500
        newdict = {}
        for key in data.keys():
            if data[key] > min_distance:
                newdict[key] = float(data[key])
        
        newlist = sorted(newdict.items(), key=lambda x: x[1], reverse=True)
        newdict = dict(newlist)
        print(newdict)
        
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(range(len(newdict)), list(newdict.values()), align='center',color="darkred")
    
        plt.ylabel('km')    

        ax.text(0.72, 0.95, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
        ax.text(0.72, 0.92, r'Distance calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)

        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.0, -0.08, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, f'Iceberg travel distance (over {min_distance} km)',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("images/Icebergs_distance.png")
    
        plt.show()
        
    def create_graph_age(self,data):

        min_age = 365
        newdict = {}
        for key in data.keys():
            if data[key] > min_age:
                newdict[key] = float(data[key])/365
        
        newlist = sorted(newdict.items(), key=lambda x: x[1], reverse=True)
        newdict = dict(newlist)
        print(newdict)
        
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(range(len(newdict)), list(newdict.values()), align='center',color="darkred")
#         plt.xticks(range(len(newdict)), list(newdict.keys()))
    
        plt.ylabel('years')    
        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.0, -0.08, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, 'Iceberg survival time (min 1 year)',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("images/Icebergs_age.png")
    
        plt.show()
        
    def create_calving_size(self,data):
        #remove uneven years
        xlabels = []
        
        for year in range(1978,2024):
            if year % 2 == 0:
                xlabels.append(year)
            else:
                xlabels.append('  ')
            
        print(data)
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(list(data.keys()), list(data.values()), align='center',color="darkred")
        plt.xticks(range(len(xlabels)), list(xlabels))
    
        plt.ylabel('size in km2')    

        ax.text(0.72, 0.95, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
        ax.text(0.72, 0.92, r'Size calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)

        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.0, -0.08, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, 'Total calving area per year',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("images/Iceberg_calving.png")
    
        plt.show()
        
    def create_combined_iceberg_area(self,data):
        #remove uneven years
        xlabels = []
        
        for year in range(1980,2024):
            if year % 2 == 0:
                xlabels.append(year)
            else:
                for y in range(7):
                    xlabels.append('  ')
            
        print(data)
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(list(data.keys()), list(data.values()), align='center',color="darkred")
        plt.xticks(range(len(xlabels)), list(xlabels))
    
        plt.ylabel('size in km2')    

        ax.text(0.8, 0.95, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
        ax.text(0.8, 0.92, r'Size calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)

        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.0, -0.08, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.25, 1.02, 'Combined iceberg area (some years seem to have no data)',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("images/Iceberg_combined_area.png")
    
        plt.show()
        
    def create_iceberg_size(self,data):
        
        #remove small icebergs
        min_size = 500
        newdict = {}
        for key in data.keys():
            if data[key] > min_size:
                newdict[key] = float(data[key])
        
        newlist = sorted(newdict.items(), key=lambda x: x[1], reverse=True)
        newdict = dict(newlist)
        print(newdict)
        
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(range(len(newdict)), list(newdict.values()), align='center',color="darkred")
    
        plt.ylabel('size in sq km')    

        ax.text(0.72, 0.95, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
        ax.text(0.72, 0.92, r'Size calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)

        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.0, -0.08, '1978-2023.08',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, f'Iceberg size distribution (min {min_size} sq km)',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
        fig.savefig("images/Iceberg_size.png")
        plt.show()


if __name__ == '__main__':
    action = Iceberg_charts()
    action.load_list()
    
    
    



