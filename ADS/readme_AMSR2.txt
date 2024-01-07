Format description of AMSR2 ADS dataset 

1.Directory structure
  /---
    |-/06H     :Brightness Temperature	6.9GHz H-pol [K]
    |-/06V     :Brightness Temperature	6.9GHz V-pol [K]
    |-/07H     :Brightness Temperature	6.9GHz H-pol [K]
    |-/07V     :Brightness Temperature	6.9GHz V-pol [K]
    |-/10H     :Brightness Temperature	10.65GHz H-pol [K]
    |-/10V     :Brightness Temperature	10.65GHz V-pol [K]
    |-/18H     :Brightness Temperature	18.7GHz H-pol [K]
    |-/18V     :Brightness Temperature	18.7GHz V-pol [K]
    |-/23H     :Brightness Temperature	23.8GHz H-pol [K]
    |-/23V     :Brightness Temperature	23.8GHz V-pol [K]
    |-/36H     :Brightness Temperature	36.5GHz H-pol [K]
    |-/36V     :Brightness Temperature	36.5GHz V-pol [K]
    |-/89H     :Brightness Temperature	89.0GHz H-pol [K]
    |-/89V     :Brightness Temperature	89.0GHz V-pol [K]
    |-/CLW     :Integrated cloud liquid water[kg/m2]
    |-/IC0     :Sea Ice Concentration [%]
    |-/IC0     :Sea Ice Concentration Image
    |-/PRC     :Precipitation[mm/h]
    |-/SIT     :Sea Ice Thikness[cm]
    |-/SMC     :Soil moisture[%]
    |-/SND     :Snow Depth[cm]
    |-/SST     :Sea Surface Temperature [degC]
    |-/SSW     :Sea surface wind speed[m/s]
    |-/TPW     :Integrated water vapor[kg/m2]
    |-/TML     :Scan time for low resolution CH.(for except 89GHz) [hhmm]
    | 
    |-/landmask_high_NP.gz :High resolution Land/Ocean flag for North Pole [-]
    |-/landmask_low_NP.gz  :Low  resolution Land/Ocean flag for Notth Pole [-]
    |-/latlon_high_NP.gz   :High resolution Latitude and Longitude for North Pole [degree]
    |-/latlon_low_NP.gz    :Low  resolution Latitude and Longitude for North Pole [degree]
    |
    |-/landmask_high_SP.gz :High resolution Land/Ocean flag for South Pole [-]
    |-/landmask_low_SP.gz  :Low  resolution Land/Ocean flag for South Pole [-]
    |-/latlon_high_SP.gz   :High resolution Latitude and Longitude for South Pole [degree]
    |-/latlon_low_SP.gz    :Low  resolution Latitude and Longitude for South Pole [degree]

2.File naming convention
    GW1A2Eyyyymmddo_vvvppprr.bin

      GW1AM2    : instrument : GCOM-W1(Shizuku) AMSR2
      yyyymmdd : observation date (UTC)
      o        : orbit direction : A(Ascending)/D(Descending)
      vvv      : product version
      ppp      : parameter
      rr       : region :NP(North Pole)/SP(South Pole)

3.Format
    Flat(Simply) binary

4.Pixel
    900 (low reso.)
   1800 (high reso.)

5.Line
    900 (low reso.)
   1800 (high reso.)

6.Layer(Channel)
    1 (except latlon)
    2 (latlon)

7.Grid size
    10km (low reso.)
     5km (high reso. : only 89GHz TB)

8.Data type
    1byte int (land/ocean flag)
    2byte int (others)

9.Scale factor
    0.01 (LatLon,PRC)
    0.001 (CLW)
    1 (IC0)
    0.1 (others)
  (actual value = stored value x scale factor)

10.Stored parameters
    -9999: missing value
    -8888: land (except TBs)
    -7777: open water (SIT)
    10001: melt pond 20%-30% (SIT)
    10002: melt pond 30%-40% (SIT)
    10003: melt pond 40%-50% (SIT)
    10004: melt pond 50%-100% (SIT)

11.Byte order
    Little endian

12.Map projection
    Polar stereo

13.Coverage

    [North Pole]
                                 [Low reso.]    [High reso.]
    Center of upper left  pixel: N35.64 E45.0   N35.61 E45.0
    Center of upper right pixel: N35.64 W45.0   N35.61 W45.0
    Center of lower right pixel: N35.64 W135.0  N35.61 W135.0
    Center of lower left  pixel: N35.64 E135.0  N35.61 E135.0


    [South Pole]
                                 [Low reso.]    [High reso.]
    Center of upper left  pixel: S35.64 W45.0   S35.61 W45.0
    Center of upper right pixel: S35.64 E45.0   S35.61 E45.0
    Center of lower right pixel: S35.64 E135.0  S35.61 E135.0
    Center of lower left  pixel: S35.64 W135.0  S35.61 W135.0
