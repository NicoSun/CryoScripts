import math
import pandas as pd
import os

year = 2020

class Iceberg_calculator:

    def __init__  (self):
        self.iceberg_dict = {}
        self.iceberg_dict_start = {}
        self.speed_list = []

    def load_csvfiles(self):
        
        
        filepath = year
        for week in range(1,52):
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
                    self.speed_list.append(self.calc_speed(key,dictionary,dictionary_old))
        # print(self.speed_list)
        
# =============================================================================
#         for item in speed_dict:
#             self.speed_list.append(item)
# =============================================================================

        with open(f"temp/{year}_all.csv", "w", newline="") as f:
#             for key in self.iceberg_dict.keys():
#                 f.write("%s,%s\n"%(key,self.iceberg_dict[key]))
#                 f.write("%s,%s,%s\n"%(key,self.iceberg_dict[key][0],self.iceberg_dict[key][1]))
            for item in self.speed_list:
                f.write("%s,%s,%s,%s\n"%(item[0],item[1],item[2],item[3]))

#         self.calving_graph(self.iceberg_dict)
        

    def calc_speed(self,key,dictionary,dictionary_old):
        try:
            distance = self.calctravel(dictionary[key][0],dictionary_old[key][0],dictionary[key][1],dictionary_old[key][1])
            distance = int(distance)/1000 # convert to km
                    
            if dictionary[key][0] != 0 and dictionary_old[key][0] != 0:
                londiff = dictionary[key][1] - dictionary_old[key][1]
    
                if (abs(londiff) < 300):
                    mean_lat = (dictionary[key][0] + dictionary_old[key][0] ) /  2
                    mean_lon = (dictionary[key][1] + dictionary_old[key][1] ) /  2
    
            return [key,mean_lat,mean_lon,distance]
        except:
            return [0,0,0,0]
        
    
    def calc_distance(self,df):
        
        dates = df['date']
        sensor = ['nic_','ascat_','sass_','ers_','nscat_','oscat_','qscat_']
        
        totaldistance = 0
        for xxx in range(0,len(dates)-1):
            for yyy in sensor:
                try:
                    Latitude = df[f'{yyy}1'][xxx]
                    Longitude = df[f'{yyy}2'][xxx]
                    
                    Latitude2 = df[f'{yyy}1'][xxx+1]
                    Longitude2 = df[f'{yyy}2'][xxx+1]
                    if Latitude != 0:
#                         print('break')
                        break #no need to check other sensors once one is found
                except:
                    continue
#                     print(f'sensor {yyy}')
            
            
            if Latitude != 0 and Latitude2 != 0:
                distance = self.calctravel(Latitude,Latitude2,Longitude,Longitude2)
                totaldistance += distance/1000
    
                
        print(totaldistance)
        return totaldistance
        
        
        
    #     create_graph(distance_dict)
    
    def calc_age(self,iceberg_name,iceberg_name_2,df):
        
        year1, day1, lifespan = self.calc_lifespan(df)
        
        self.iceberg_dict_start[iceberg_name] = year1, day1
        
        if iceberg_name_2 not in self.iceberg_dict:
            self.iceberg_dict[iceberg_name_2] = lifespan
        elif iceberg_name_2 in self.iceberg_dict:
            lifespan = self.calc_lifespan2(df,self.iceberg_dict_start[iceberg_name])
            if lifespan > self.iceberg_dict[iceberg_name_2]:
                self.iceberg_dict[iceberg_name_2] = lifespan
        
        
    
    def calc_lifespan(self,df):
        # 189,000 km2 all bergs together
        dates = df['date']
        xxx = dates.tolist()
        
        year1 = int(f'{xxx[0]}'[0:4])
        day1 = int(f'{xxx[0]}'[4:7])
        
        year2 = int(f'{xxx[-1]}'[0:4])
        day2 = int(f'{xxx[-1]}'[4:7])
        
        lifespan = (year2-year1)*365 + day2 - day1
        
        return year1, day1, lifespan
    
    def calc_lifespan2(self,df,year_day):
        dates = df['date']
        xxx = dates.tolist()
        
        year2 = int(f'{xxx[-1]}'[0:4])
        day2 = int(f'{xxx[-1]}'[4:7])
        
        lifespan = (year2-year_day[0])*365 + day2 - year_day[1]
        
        return lifespan
    
    def calc_size(self,df):
        area = 0
        try:
            size1 = df['size_1']
            size2 = df['size_2']
            xxx = size1.tolist()
            yyy = size2.tolist()
            
            xxx = max(xxx) * 1.852 # convert nautical miles to km
            yyy = max(yyy) * 1.852
            
            area = xxx * yyy
        except KeyError:
            print('no size')
        
        return area
    
    
    def create_graph(self,data):
        import matplotlib.pyplot as plt
        plt.style.use('dark_background')
        
        #remove grounded icebergs
        newdict = {}
        for key in data.keys():
            if data[key] > 2000:
                newdict[key] = float(data[key])
        
        newlist = sorted(newdict.items(), key=lambda x: x[1], reverse=True)
        newdict = dict(newlist)
        print(newdict)
        
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(range(len(newdict)), list(newdict.values()), align='center',color="darkred")
#         plt.xticks(range(len(newdict)), list(newdict.keys()))
    
        plt.ylabel('distance in km')    
    # =============================================================================
    #     ax.text(0.52, 0.07, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
    #     ax.text(0.52, 0.04, r'Distance calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
    # =============================================================================
        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, 'Iceberg travel distance',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("temp/Icebergs_distance.png".format(year))
    
        plt.show()
        
    def calving_graph(self,data):
        import matplotlib.pyplot as plt
        plt.style.use('dark_background')
        
# =============================================================================
#         #remove grounded icebergs
#         yearlist = []
#         for key in data.keys():
#             if int(key) % 2 == 0:
#                 yearlist.append(key)
#             else:
#                 yearlist.append("_")
# 
#         print(yearlist)
# =============================================================================
        fig = plt.figure(figsize=(12,6))
        
        ax = fig.add_subplot(111)
        
        plt.bar(range(1975,2021), list(data.values()), align='center',color="darkred")
#         plt.xticks(range(len(newdict)), list(newdict.keys()))
    
        plt.ylabel('size in km2')    
    # =============================================================================
    #     ax.text(0.52, 0.07, r'Location data: US NIC', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
    #     ax.text(0.52, 0.04, r'Distance calculation: Nico Sun', fontsize=10,color='white',fontweight='bold',transform=ax.transAxes)
    # =============================================================================
        ax.text(0.75, -0.08, 'cryospherecomputing.com/Icebergs',
            transform=ax.transAxes,color='grey', fontsize=10)
        ax.text(0.35, 1.02, 'Iceberg calving size per year',
            transform=ax.transAxes, fontsize=12,fontweight='bold')
        fig.tight_layout(pad=1)
    
        fig.savefig("temp/Icebergs_calving_size.png".format(year))
    
        plt.show()
        
    
    
    def convert_to_radian(self,*args):
        aaa = []
        for x in args:
            aaa.append(math.radians(x))
        return aaa
            
    
    def calctravel(self,lat1,lat2,lon1,lon2):
        
        lat1,lat2,lon1,lon2 = self.convert_to_radian(lat1,lat2,lon1,lon2)
        
        distance = math.acos(min(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1),1 )) * 6371000
        
    #    print(distance/1000)
        return distance
    
    def load_list(self,filename):
        import csv
        dictaa = {}
        with open(filename, newline='') as csvfile:
            tempreader = csv.reader(csvfile, delimiter=',')
            templist = list(tempreader)
        for xxx in templist:
            dictaa[xxx[0]] = xxx[1]
        self.create_graph(dictaa)


#calctravel(-72.52,-72.82,-172.31,-172.83)

listname = 'temp/Original_Iceberg_sizes.csv'


if __name__ == '__main__':
    action = Iceberg_calculator()
    action.load_csvfiles()
#     action.load_list(listname)
    
    
    



