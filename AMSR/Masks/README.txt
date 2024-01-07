AWI AMSR2 ice concentration product 
-----------------------------------
Contact: lars.kaleschke@awi.de

Introduction
------------

The AWI AMSR2 ice concentration product is based on previous developments at the University of Bremen (UB) and the University of Hamburg (UHH) [1,2,3,4]. The level 1 brightness temperature data are provided by the Japan Aerospace Exploration Agency’s (JAXA) Advanced Microwave Scanning Radiometer 2 (AMSR2) [5]. 

Main features
-------------
 * Visually improved ice concentration with lead occurrences
 * 3 km resolution
 * Compressed GEOTIFF with optimized color scheme [6]
 * New landmask
 * Twice daily processing

Product specifications
----------------------
The product is generated twice daily for two different start times (filenames with AM or PM). 

    [PM] 12 - 12 UTC. The PM product starts with data after noon and is available in the evening.

    [AM] 00 - 24 UTC. The AM product is available in the morning of the next day.

The file name indicates the start time. For example, the file sh_20210307PM_SIC.tiff includes southern hemispheric ice concentration data from March 7 12:00 to March 8 12:00. The file is available in the afternoon of March 8.

After about 16-18 hours the spatial coverage is mostly complete but all data from 24 hours are included for consistency with other daily averaged products. The advantage of the twice daily processing is a reduced latency.

Leads: difference between SIC, LEADS and SIC-LEADS
--------------------------------------------------
There are three different products with the filename including SIC, LEADS and SIC-LEADS. The first is the traditional ASI ice concentration, the second contains the lead ice fraction [4], and the latter product contains the ice concentration minus half the lead fraction. The AMSR lead detection does not provide reasonable features during the melting period but is calculated anyhow throughout the year

Known issues
------------
The product has errors due to weather effects in particular along the coastlines. A minimum filter is applied along the coastlines which may also remove real drifting ice. 

Landmask
--------
Landmasks are derived from https://osmdata.openstreetmap.de/data/

An obvious difference to previous (UB and UHH) products is a correct representation of northeast Greenland, e.g. the Danmark Fjord, which was wrong in the previous landmask derived from The Global Self-consistent, Hierarchical, High-resolution Geography Database (GSHHG).

An experimental land mask (to be further improved and validated) including lakes and larger water bodies derived from 89 GHz channels is provided with the SIC-LEADS product. The SIC product includes the OSM land mask without these features.

Regional sea ice extent and area
--------------------------------
Regional sea ice extent and area are calculated based on the upsampled 25 km "NSIDC" regional mask "Arctic_region_mask_Meier_AnnGlaciol2007.msk" available at https://nsidc.org/data/g02135 [7]. 
Extent and area data are updated regularly and stored in the .csv file on the ftp-server: ftp://ftp.awi.de/sea_ice/product/amsr2/v106/analysis_nh/nh_awi_amsr2_regional_extent_area.csv

For comparison the same procedure was applied to the ASI 12.5 km SSMIS 5-day median filtered as provided by UHH [8]. The result is stored in the file nh_extent_SSMI_ASI_Regional_1992_2020.csv on the ftp-server.

Data formats
------------
NetCDF (only for SIC) and GeoTIFF.

NetCDF includes latitude and longitude grids and landmasks
INT16 scaled by 0.01f

Projection and grid
-------------------
https://epsg.io/3411 NSIDC Sea Ice Polar Stereographic North
https://epsg.io/3412 NSIDC Sea Ice Polar Stereographic South
Grid cell size 3125 meter

Data distribution
-----------------
For free without warranty ftp://ftp.awi.de/sea_ice/product/amsr2/


Acknowledgement
---------------
Thanks to X. Tian-Kunze for deriving AMSR2 lead fraction parameters (BMBF CATS project)

References:
-----------

[1] L. Kaleschke, C. Lüpkes, T. Vihma, J. Haarpaintner, A. Bochert, J. Hartmann & G. Heygster (2001) SSM/I Sea Ice Remote Sensing for Mesoscale Ocean-Atmosphere Interaction Analysis, Canadian Journal of Remote Sensing, 27:5, 526-537, DOI:10.1080/07038992.2001.10854892

[2] Spreen, G., L. Kaleschke, and G. Heygster (2008), Sea ice remote sensing using AMSR-E 89-GHz channels, J. Geophys. Res., 113, C02S03, doi:10.1029/2005JC003384.

[3] Beitsch, A.; Kaleschke, L.; Kern, S. Investigating High-Resolution AMSR2 Sea Ice Concentrations during the February 2013 Fracture Event in the Beaufort Sea. Remote Sens. 2014, 6, 3841-3856. https://doi.org/10.3390/rs6053841

[4] Röhrs, J. and Kaleschke, L.: An algorithm to detect sea ice leads by using AMSR-E passive microwave imagery, The Cryosphere, 6, 343–352, https://doi.org/10.5194/tc-6-343-2012, 2012.

[5] https://gportal.jaxa.jp/gpr/

[6] Thyng, K. M., Greene, C. A., Hetland, R. D., Zimmerle, H. M., & DiMarco, S. F. (2016). True colors of oceanography. Oceanography, 29(3), 10. https://doi.org/10.5670/oceanog.2016.66

[7] Meier, W. N., J. Stroeve, and F. Fetterer. 2007. Whither Arctic sea ice? A clear signal of decline regionally, seasonally and extending beyond the satellite record. Ann. Glaciol. 46: 428-434.

[8] https://www.cen.uni-hamburg.de/en/icdc/data/cryosphere/seaiceconcentration-asi-ssmi.html

-------------------------------------------------------------------------------------------------------------------------------
Changelog
---------
v104 2021-03-16 Corrected for the day in file name. Added date information text in GeoTiff and PNG. 
v104 2021-03-20 Replaced ocean mask with hand-picked ocean mask (to be validated). This should help against artificial boundaries. Thanks to Uniquorn ASIF post Re: Home brew AMSR2 extent & area calculation Reply #3571 on: December 05, 2020, 12:43:56 PM
v104 2021-03-20 Included lakes and larger water bodies over land derived from 89 GHz brightness temperature (to be validated). Isolated structures < 4 pixels removed.
v104 2021-03-23 Bug fixed: removal of incomplete orbits caused data gaps in Pacific sector.
v104 2021-03-26 Generate merged global GeoTiff to be used e.g. with Google Earth 
v105 2021-07-27 Update to Ubuntu-20 and code cleanup, no intentionally change of product. Further testing.
v106 2021-07-29 Repaired land mask at east Greenland coast. Included sea ice - leads product. Started first reprocessing, August and September, and MOSAiC period.
v106 2021-08-04 Reprocessed MOSAiC period published on ftp site.
