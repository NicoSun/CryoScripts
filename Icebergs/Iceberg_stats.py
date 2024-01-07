import math
import pandas as pd
import os

class Iceberg_calculator:

    
    def __init__  (self):
        self.iceberg_dict = {}
        self.iceberg_dict_new = {}
        self.iceberg_dict_start = {}
        self.speed_list = []
        
        self.namelist = []
        
    def iceberg_speed(self):
        data = self.load_csvfiles()
        for row in data:
            speed_dict = self.calc_speed(row['df'],row['name'])
            for item in speed_dict:
                self.speed_list.append(item)
        self.write_speed_data('iceberg_speed.csv')
        
    def iceberg_age(self):
        data = self.load_csvfiles()
        for row in data:
            self.calc_age(row['name'],row['name2'],row['df'])
        self.write_dict_keys('iceberg_age.csv')
        
    def iceberg_size(self):
        data = self.load_csvfiles()
        for row in data:
            self.iceberg_dict[row['name']] = self.calc_size(row['df'])
            self.write_dict_keys('iceberg_size.csv')
            
    def iceberg_original_size(self):
        self.iceberg_size()
        self.size_original_iceberg()
        self.write_dict_keys('iceberg_original_size.csv')
        
    def iceberg_distance(self):
        data = self.load_csvfiles()
        for row in data:
            self.iceberg_dict[row['name']] = self.calc_distance(row['df'])
            self.write_dict_keys('iceberg_distance.csv')
            
    def iceberg_furthest_north(self):
        data = self.load_csvfiles()
        for row in data:
            self.iceberg_dict[row['name']] = self.furthest_north(row['df'])
            self.write_dict_keys('furthest_north.csv')
            
    def iceberg_calved_size(self):
        
        for year in range(1978,2024):
            self.iceberg_dict[str(year)] = 0
        
        data = self.load_csvfiles()
        for row in data:
            self.namelist.append(row['name2'])
                
            if row['name'] != self.namelist: # ensures only original icebergs are counted
                # print(iceberg_name)
                year = str(row['df']['date'].tolist()[0])[0:4]
                area = self.calc_size(row['df'])
                try:
                    self.iceberg_dict[year] += area
                except:
                    print('ignore:', year)
                
        self.write_dict_keys('iceberg_calved_size.csv')
        
    def iceberg_combined_area(self):
        
        for year in range(1980,2024):
            self.iceberg_dict[str(year)] = 0
            self.iceberg_dict[f'{str(year)}.25'] = 0
            self.iceberg_dict[f'{str(year)}.50'] = 0
            self.iceberg_dict[f'{str(year)}.75'] = 0
        
        data = self.load_csvfiles()
        for row in data:
            self.calc_iceberg_combined_area(row['df'])
                
        self.write_dict_keys('iceberg_combined_area.csv')
            

    def load_csvfiles(self):
        all_data = []
        filepath = 'database_main_bergs'
        for file in os.listdir(filepath):
            iceberg_name = file[0:-4]
            iceberg_name_2 = file[0:3]
            
            df = pd.read_csv(f'{filepath}/{file}',sep=",")
            all_data.append( {'df': df,'name': iceberg_name,'name2': iceberg_name_2})
        return all_data
        
        
    def write_meltout_data(self, filename):
        with open(f"temp/{filename}", "w", newline="") as f:
            for key in self.iceberg_dict.keys():
                f.write("%s,%s,%s,%s\n"%(key,self.iceberg_dict[key][0],self.iceberg_dict[key][1],self.iceberg_dict[key][2]))
        
        
    def write_speed_data(self,filename):
        with open(f"temp/{filename}", "w", newline="") as f:
            for item in self.speed_list:
                f.write("%s,%s,%s,%s\n"%(item[0],item[1],item[2],item[3]))
    
    def write_dict_keys(self,filename):
        with open(f"temp/{filename}", "w", newline="") as f:
            for key in self.iceberg_dict.keys():
                f.write("%s,%s\n"%(key,self.iceberg_dict[key]))
        
        
    def size_original_iceberg(self):
        
        for iceberg in self.iceberg_dict:
            if self.iceberg_dict[iceberg] > 0:
                self.iceberg_dict_new[iceberg] = self.iceberg_dict[iceberg]
            if not iceberg[0:3] in self.iceberg_dict:
                self.iceberg_dict_new[iceberg[0:3]] = self.iceberg_dict[iceberg]
             
        for iceberg in self.iceberg_dict_new:
            try:
                if self.iceberg_dict_new[iceberg] > self.iceberg_dict_new[iceberg[0:3]]:
                    self.iceberg_dict_new[iceberg[0:3]] = self.iceberg_dict_new[iceberg]
                    # print(iceberg)
            except:
                pass
        
        
        self.iceberg_dict = {}
        
        #remove child bergs
        for iceberg in self.iceberg_dict_new:
            if len(iceberg) < 4:
                # print(iceberg)
                self.iceberg_dict[iceberg] = self.iceberg_dict_new[iceberg]
        

    def calc_speed(self,df,iceberg_name):
        
        dates = df['date']
        sensor = ['nic_','ascat_','sass_','ers_','nscat_','oscat_','qscat_']
        
        speed_list = []
        for xxx in range(0,len(dates)-2):
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
                londiff = Longitude - Longitude2

                if (abs(londiff) < 300):
                    mean_lat = (Latitude + Latitude2 ) /  2
                    mean_lon = (Longitude + Longitude2 ) /  2


                    days = (df['date'][xxx+1] - df['date'][xxx])
                    if days < 8:
                        distance = self.calctravel(Latitude,Latitude2,Longitude,Longitude2) / 1000
                        distance = distance / days

                        # if distance > 250:
                        #     print(iceberg_name,df['date'][xxx])
                        
                        #removes grounded icebergs and likely false data 
                        if 1 < distance < 100:
                            speed_list.append([iceberg_name,mean_lat,mean_lon,distance])
    
        return speed_list
        
    
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
        
        self.iceberg_dict_start[iceberg_name_2] = year1, day1
        
# =============================================================================
#         #for unique iceberg age
#         self.iceberg_dict[iceberg_name] = lifespan
# =============================================================================
        
        if iceberg_name_2 not in self.iceberg_dict:
            self.iceberg_dict[iceberg_name_2] = lifespan
        elif iceberg_name_2 in self.iceberg_dict:
            lifespan = self.calc_lifespan2(df,self.iceberg_dict_start[iceberg_name_2])
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
        
        return area * 0.9
    
    def calc_iceberg_combined_area(self,df):
        
        for xxx in range(0,len(df['date'])):
            year = str(df['date'][xxx])[0:4]
            day = int(str(df['date'][xxx])[4:7])
            try:
                size1 = df['size_1'][xxx]
                size2 = df['size_2'][xxx]
            except: # no size data
                continue
            if int(year) > 1979:
                if size1 != 0:
                    area = size1 * size2 * 1.852 * 1.852
                    if day < 90:
                        self.iceberg_dict[year] += area
                    elif 91 < day < 182:
                        self.iceberg_dict[f'{year}.25'] += area
                    elif 182 < day < 273:
                        self.iceberg_dict[f'{year}.50'] += area
                    elif 273 < day:
                        self.iceberg_dict[f'{year}.75'] += area
                
    
    def furthest_north(self,df):
        
        dates = df['date']
        sensor = ['nic_','ascat_','sass_','ers_','nscat_','oscat_','qscat_']
        
        max_lat = -90
        date = 'no date'
        long_pair = ''
        for xxx in range(0,len(dates)):
            for yyy in sensor:
                try:
                    Latitude = df[f'{yyy}1'][xxx]
                    if Latitude != 0:
                        date2 = dates[xxx]
                        Longitude = df[f'{yyy}2'][xxx]
#                         print('break')
                        break #no need to check other sensors once one is found
                except:
                    continue
#                     print(f'sensor {yyy}')
            
            if Latitude != 0 and Latitude > max_lat:
                max_lat = Latitude
                long_pair = Longitude
                date = date2
    
        return date, max_lat , long_pair
    

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
        
        
    def makejsonfile(self):
        import csv
        import json
        
        with open("temp/furthest_north.csv",'r') as csvfile_ind:
            reader_ind = csv.DictReader(csvfile_ind)
            jsonrows = []
            for row in reader_ind:
                info = {}
                try: 
    #                print(row["Iceberg"])
                    
                    info["Iceberg"] = row["Iceberg"]+'; Date: ' + row["Date"] + ' \n'+' Lat:'+row["Latitude"]+' Lon:'+row["Longitude"]
                    info["Latitude"] = float(row["Latitude"])
                    info["Longitude"] = float(row["Longitude"])
                    jsonrows.append(info)
                except:
                    pass
    
        with open("temp/furthest_north.json", 'w') as json_file_ind:
            json.dump(jsonrows, json_file_ind, sort_keys=False, indent=4, separators=(',', ': '))
            

if __name__ == '__main__':
    action = Iceberg_calculator()
    # action.iceberg_speed()
    # action.iceberg_age()
    # action.iceberg_size()
    # action.iceberg_original_size()
    # action.iceberg_distance()
    # action.iceberg_furthest_north()
    # action.iceberg_calved_size()
    action.iceberg_combined_area()

    # action.makejsonfile()
    

