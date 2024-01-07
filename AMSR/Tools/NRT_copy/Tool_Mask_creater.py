import numpy as np
import CryoIO
import netCDF4
# import gzip


def read_mask_nc_nh():
    filename = 'temp/nh_regional_3km.nc'
    ncvar = '__xarray_dataarray_variable__'
    
    latmask = CryoIO.readnumpy('Masks/AMSR2_nh_latitude.npz')
    lonmask = CryoIO.readnumpy('Masks/AMSR2_nh_longitude.npz')
    
    with netCDF4.Dataset(filename, mode='r') as nc:
        # print(nc.variables)
        region_map = np.array(nc[ncvar])
        region_map = region_map[200:3500,100:2200] #north
        region_map[2732:2846,1132] = 9
        region_map = region_map.flatten()
        latmask = latmask.flatten()
        lonmask = lonmask.flatten()
        for index,lon in enumerate(lonmask):
            if lon == 180 or lon == -188:
                if 52 < latmask[index] < 65:
                    region_map[index] = 14
                
        region_map = region_map.reshape(3300,2100)
        map_show(region_map)
    # CryoIO.savenumpy('Masks/AMSR2_nh_region', region_map)
    # CryoIO.savenumpy('Masks/AMSR2_nh_polehole', region_map)
    
def read_mask_nc_sh():
    filename = 'temp/sh_regional_3km.nc'
    ncvar = '__xarray_dataarray_variable__'
    
    latmask = CryoIO.readnumpy('Masks/south/AMSR2_sh_latitude.npz')
    lonmask = CryoIO.readnumpy('Masks/south/AMSR2_sh_longitude.npz')
    
    with netCDF4.Dataset(filename, mode='r') as nc:
        print(nc.variables)
        region_map = np.array(nc[ncvar])
        region_map = region_map[0:2500,300:2500] # south
        map_show(region_map)
    # CryoIO.savenumpy('Masks/south/AMSR2_sh_region', region_map)
        
        
def map_show(region_map):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(11, 11))
    
    
    cmap1 = plt.colormaps["coolwarm"]
    cmap1.set_bad('black',0.6)
    ax.axis('off')
    ax.imshow(region_map, interpolation='nearest')
    
    
    plt.show()
    
def fill_pole_hole():
    import time
    import os
    start = time.time()
    
    import pandas
    Columns = ['A']
    csvdata = pandas.read_csv('Masks/polehole.csv', names=Columns,dtype=int)
    icepole = csvdata.A.tolist()
             
    Columns = ['A']
    csvdata = pandas.read_csv('Masks/polering.csv', names=Columns,dtype=int)
    icepole_ring = csvdata.A.tolist()
    combo_list = icepole + icepole_ring
    
    for year in range(2023,2024):
        filepath = f'DataFiles/north/{year}'
        for file in os.listdir(filepath):
            print(file)
            icemap = CryoIO.readnumpy(os.path.join(filepath,file))
            icemap = icemap.flatten()
            icemap = formatdata(icemap,icepole,icepole_ring)
            
            icemap = icemap.reshape(3300,2100)
            icemap = np.clip(icemap,a_min=0,a_max=255)
            icemap = np.array(icemap,dtype=np.uint8)
            # CryoIO.savenumpy(os.path.join(filepath,file), icemap)
    
    end = time.time()
    print(end-start)
    
def formatdata(icemap,combo_list,icepole_ring):
    icepolecon = []
    for val in icepole_ring:
        if icemap[val] != 255:
            icepolecon.append (icemap[val])
        
    icepolecon = np.mean(icepolecon)
    
    for val2 in combo_list:
        if icemap[val2] == 255:
            icemap[val2] = icepolecon
    return icemap

def pixel_area():
    import pyproj
    
    lat = 70
    lon = 0
    
    pol_n = pyproj.Proj("+int=EPSG:3411") #NSIDC Polar Sterographic North
    pol_s = pyproj.Proj("+int=EPSG:3412") #NSIDC Polar Sterographic South
    
    A_n = 1/ pol_n.get_factors(lon,lat).areal_scale #area correction mask
    
    print(pol_n)
    print(pol_s)
    print(A_n)
    
# =============================================================================
#     with open('Masks/imslat_24km.bin', 'rb') as fr:
#         latmask = np.fromfile(fr, dtype='float32')
# 
#     conversionlist = np.loadtxt('Masks/Pixel_area_vs_Latitude.csv',delimiter=',',skiprows=1)
# #    print(conversionlist[:,0])
#     pixelareamask = np.zeros(len(latmask))
#     for x,y in enumerate(latmask):
#         latitude = y
#         listindex = []
#         for xx in conversionlist[:,0]:
#             listindex.append(abs(latitude-xx))
# 
#         index = listindex.index(min(listindex))
#         try:
#             pixelareamask[x] = conversionlist[index,1]
#         except:
#             pixelareamask[x] = 'nan'
# 
#     pixelareamask = pixelareamask.reshape(1024,1024)
#     plt.imshow(pixelareamask)
#     plt.show()
#     pixelareamask = np.array(pixelareamask,dtype='float32')
# =============================================================================

def readNumpyfile(hemi,year,month,day):
    import AMSR2_maps
    
    datestring = f'{year}-{month}-{day}'
    landmask = CryoIO.readnumpy(f'Masks/{hemi}/AMSR2_{hemi}_land.npz').flatten()
    icemean = CryoIO.readnumpy(f'DataFiles/Mean_12_23/{hemi}/AMSR2_{hemi}_Mean_{month}{day}.npz').flatten()
    icemap = CryoIO.readnumpy(f'DataFiles/{hemi}/{year}/AMSR2_{hemi}_v110_{year}{month}{day}.npz').flatten()
    anom_map = icemap - icemean
    
    for index,xxx in enumerate(landmask):
        if xxx == 1:
            anom_map[index] = 222
    
    icemap = icemap.reshape(3300,2100)
    anom_map = anom_map.reshape(3300,2100)
    # map_show(anom)
    AMSR2_maps.action.normalshow(icemap, hemi, datestring,icesum=0)
    AMSR2_maps.action.anomalyshow(anom_map, hemi, datestring,icesum=0)

# fill_pole_hole()
# readNumpyfile('Masks/AMSR2_nh_polehole.npz')
# read_mask_nc_nh()
# read_mask_nc_sh()
# readNumpyfile('DataFiles/sh/2023/AMSR2_sh_v110_20230414.npz')
readNumpyfile('nh',2023,'10','17')
# readNumpyfile('DataFiles/Mean_12_23/nh/AMSR2_nh_Mean_0101.npz')


'''
shape:
nh: 3300, 2100
sh: 2500, 2200

Regionmask:
0: Ocean
1: Land
2: Central Arctic
3: Beaufort
4: Chukchi
5: East Siberian
6: Laptev Sea
7: Kara Sea
8: Barents Sea
9: East Greenland
10: Baffin Bay
11: St_Lawrence
12: Hudson Bay
13: Canadian Arch
14: Bering
15: Okhotsk
16: Japan
17:Bohai
18: Baltic
19: Gulf of Alaska
'''
