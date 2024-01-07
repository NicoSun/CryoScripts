---------------------------------------------------------
-   BYU MERS Consolidated Antarctic Iceberg Database    -
-		Jeff Budge, BYU Nov 2016                -
- w/revisions by D.G. Long, BYU Nov 2017, Jun 2019, Aug 2019
---------------------------------------------------------

This readme is intended to explain the contents the database.
Details about how the database is created are contained in
J.S. Budge and D.G. Long, "A Comprehensive Database for Antarctic
Iceberg Tracking Using Scatterometer Data," IEEE Journal of
Selected Topics in Applied Earth Observations, accepted and
to appear, 2017. Related papers: K.M. Stuart and D.G. Long,
"Tracking large tabular icebergs using the SeaWinds Ku-band
microwave scatterometer", Deep-Sea Research Part II, 
doi:10.1016/j.dsr2.2010.11.004, Vol. 58, pp. 1285-1300, 2011.
D.G. Long, Jarom Ballantyne, and C. Bertoia, "Is the Number of
Icebergs Really Increasing?" EOS, Transactions of the American
Geophysical Union, Vol. 83, No. 42, pp. 469 & 474, 15 Oct 2002.


FILES

Each file in the consolidated database contains information on one
named iceberg. The name of the iceberg is also the name of the file
with a .csv extension. The headers of each file show the date,
sensors, and sizes associated with that iceberg. A few notes:

-Each file shows only the sensors that have data available for that
 iceberg. This means that the number of columns in each file is
 variable.

-Each sensor has at least two columns associated with it, namely
 'sensor_1' and 'sensor_2' where "sensor" is replaced with the actual
 sensor name.  'sensor_1' is the latitude and 'sensor_2' is the
 longitudinal measurement from each sensor on the given date.
 The values of 0,0 are used for no data.

-Most sensors have a third column, 'sensor_3' that is a binary flag
 that indicates if the measurement is an observation (1) or has
 been interpolated (0) for that day or not. Where possible, daily
 position reports are provided by interpolating sensor observations.
 Interpolation is only used when (1) the time gap is less than 14
 days and (2) the spatial displacement between observation is less
 than 3 deg latitude or longitude.  Interpolated positions that end
 up over land are not included.

-Dates are shown in JD format, with the four digit year first followed
 by the three digit day of the year.

-'size_1' and 'size_2' show the length of the major and minor axes of
 the iceberg on the date, as given by the NIC, in nautical miles. To
 convert to km, multiply the value by 1.852.

-Standard NIC icebergs names begin with a, b, c, or d which gives the
 origin quadrant. Additional icebergs were identified in scatterometer
 data.  These unnamed icebergs are stored in files that begin with 
 sa (SASS 1978), e (ERS1/2 1992-2001), or uk (1999-present).

KNOWN ISSUES

NIC positions are derived from NIC reports.  Some inconsistencies and
errors exist in these reports. NIC observation dates are irregular
and infrequent, especially in the early days. There are occasions
when the NIC reports for a single iceberg seem to have been actually
from two different icebergs. While some corrections have been made,
NIC reports are generally used as is. While icebergs due not grow
in size, some NIC reports show size increase. This may be due to
(1) quantization of the reported dimensions by NIC and/or (2) variations
in the subjectively choosen axes used to infer dimensions.

Scatterometer sensor position estimates have gaps due to loss of data
and backscatter constrast, especially during summer months, but
typically are available on a daily basis. The iceberg center in
scatterometer data reports is subjectively determined based on
scatterometer backscatter images may not coincide with the center
identified in NIC reports.


RELEASE NOTES

v1.2: fixed some position reports for some icebergs

v2.0: bugs in earlier releases fixed, additional position addd
Note that NIC changed their minimum tracking size threshold from
10 nM to 20 nM in 2017.  Starting in 2017 OSCAT2 positions were
not separately reported, but are included in ASCAT position reports.

V3.0: additional icebergs included. corrected a number of size and 
position reporting errors.
