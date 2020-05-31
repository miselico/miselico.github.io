#! python
# -*- coding: iso-8859-1 -*-
###########################################################################
# 
# File:            fetch_map.py
#
#
# Licence:         Donationware, distributed as Freeware
#
#                  If you find this software useful to you and you would
#                  like to help the developer to maintain it also in the future, 
#                  please donate a small amount of your liking to the 
#                  PayPal account: olammi@iki.fi.
#
#                  This donation is not required to use the software and the 
#                  software is licenced as freeware.
#
#                  To individual and non-commercial use only! Script
#                  and source code may be used freely for non-commercial
#                  purposes. Not allowed to be used for mass downloading
#                  of maps!
#
#
HELP_TEXT = """
# Usage:           python fetch_map.py --help
#                  python fetch_map.py --info
#                  python fetch_map.py [options] <map_name> <coord_N> <coord_E> <size_x> <size_y> [scale]
#                  python fetch_map.py --corners [options] <map_name> <coord_bl_N> <coord_bl_E> <coord_tr_N> <coord_tr_E> [scale]
#
#                  Options:
#                    --help    - Prints out a help and exits.
#
#                    --info    - Prints out a list of supported service names,
#                                map scales, layers and supported calibration file types. 
#                                Exits without fetching any maps.   
#
#                    -s service_code
#                    --service service_code - Use the given service to retrieve
#                                the maps. Default is "kkp" = Kansalaisen 
#                                Karttapaikka. Use option --info to see the list 
#                                of supported services.
#
#                    --cachedonly - Uses only the cached images. Will not contact
#                                the actual service for new map data. If the 
#                                result map contains areas that are not found in 
#                                the cache, those areas will appear yellow in the
#                                result map.
#
#                    --cache directory - Use cache directory given with this 
#                                parameter. Default is "./map_cache/".
#
#                    --palette - Convert the result image to palette mode
#                                before saving. Default is RGB true color
#                                mode when the result file format supports
#                                it.
#
#                    --corners - If given, the script expects 4 coordinate values 
#                                (bottom left and top right corners of the map) 
#                                instead of the map center coordinate and size. 
#
#                    --force-coordinates - Unused since v3.0h
#
#                    --starttime HHMM - Start time for the download. For example
#                                option "--starttime 0200" will make the
#                                script wait until clock is 02:00 at night
#                                and then start the map download. By default
#                                the script will start the download right away.
#                                Using the cached map parts will not be delayed.
#
#                    --save type - Save a calibration file of given type. By 
#                                default the script will save the result map  
#                                image and map calibration file for OziExplorer. 
#                                Use option --info to see the list of supported 
#                                calibration file types. Multiple options may be
#                                given on same command line.
#
#                    --overlap Nx Ny overlap_km - Save multiple overlapped map 
#                                files from the configured area by paremeters. 
#                                When using this option, fetch_Map will create 
#                                multiple map images that overlap each other by 
#                                configured distance . The number of
#                                images in horisontal and vertical directions 
#                                are configured with parameters  and . 
#                                The map image location will be added to the map
#                                and calibration file names.
# 
#                                Example:
# 
#                                  python fetch_map.py --overlap 4 3 0.5 TestMap
#                                  6815986 2480962 6.0 5.0 1:16000
# 
#                                The above command would generate 12 separate map
#                                files TestMap_1_1.png, TestMap_1_2.png, ..., 
#                                TestMap_4_3.png. The generated map files next to
#                                other image will overlap each other by 
#                                0.5 kilometers.
#
#                    --layer layername - Add a named transparent layer provided by the
#                                map service. Use --info to see available layer names.
#
#                  Parameters:
#                    map_name  - Name of the map, result map will be outputted 
#                                to file <map_name>. If parameter contains
#                                no file extension, '.png' will be appended
#                                and PNG-picture format will be used by
#                                default.
#                    coord_N     - Northing coordinate of the middle point of  
#                                the result map
#                    coord_E     - Easting coordinate of the middle point of  
#                                the result map
#                    size_x    - width of the result map in kilometers 
#                                (approx), example: 10.2
#                    size_y    - height of the result map in kilometers
#                                (approx), example: 8.5
#                    coord_bl_N - Northing coordinate of the bottom left corner 
#                                of the result map (see --corners option).
#                    coord_bl_E - Easting coordinate of the bottom left corner 
#                                of the result map (see --corners option).
#                    coord_tr_N - Northing coordinate of the top right corner
#                                of the result map (see --corners option).
#                    coord_tr_E - Easting coordinate of the top right corner 
#                                of the result map (see --corners option).
#                    scale     - (optional parameter) scale of the result map. 
#                                 Use option --info to retrieve supported scales 
#                                 for services.
#
#                  Coordinates:
#
#                    Coordinates can be given in KKJ, YKJ, ETRS-TM35FIN and  
#                    WGS84 formats. WGS84 coordinates are lat and lon values  
#                    for northing and easting. Possible formats for WGS84   
#                    coordinate values are according to following examples:
# 
#                       61.451378 (for 61.451378 degrees)
#                       61,27.083 (for 61 degrees, 27.083 minutes)
#                       61,27,4.96 (for 61 degrees, 27 minutes, 4.96 seconds)
#
#                    Grid coordinate values with easting less than 1000000
#                    are considered as ETRS-TM35FIN coordinates and with
#                    with easting greater than or equal 1000000 are considered
#                    KKJ or YKJ.
#
#                    ATTENTION! Both lat and lon coordinates of a single map  
#                    point must always be given in the same coordinate system 
#                    (e.g. WGS84 or KKJ).  
#
#
#                  Example:
#                  Example command will fetch 6x5 kilometer map in 1:40000
#                  scale from Pirkkala area.
#
#                    python fetch_map.py Pirkkala 6815986 2480962 6.0 5.0 1:40000
#
#                  the same map using WGS84 coordinate system
#
#                    python fetch_map.py Pirkkala 61,27,4.96 23.639721 
#                    6.0 5.0 1:40000
#
#                  again the same map using ETRS-TM35FIN coordinate system
#
#                    python fetch_map.py Pirkkala 6817681 320897 6.0 5.0 1:40000
#
#                  same area but the map service is Retkikartta.fi and 
#                  scale 1:25000
#
#                    python fetch_map.py -s rka Pirkkala 61,27,4.96 
#                    23.639721 6.0 5.0 1:25000
#
"""
#
# Author:          Olli Lammi (olammi@iki.fi)
#
# Version:         3.1i
#
# Date:            23.02.2012
#
# Functions:       -
#                   
# Description:     Fetches a given size map from supported map services by
#                  retrieving needed map pictures and combining the pictures 
#                  to a larger map.
#
#                  Uses folder ./map_cache/ for caching the map pictures. 
#                  Fetches one map picture only once and caches it in this 
#                  folder.
#
#                  By default fetches 1:16000 maps from Kansalaisen Karttapaikka, 
#                  (http://www.karttapaikka.fi/) but can also be configured to 
#                  use other scales and map sites also.
#
# Requirements:    Python interpreter 2.4 or newer (www.python.org)
#                  (tested with 2.4.1)
# 
#                  Python Imaging Library (tested with 1.1.5) 
#                  (www.pythonware.org/products/pil/)
#
# Version history: ** 05.09.2005 v0.1a (Olli Lammi) **
#                  First public version. 
#
#                  ** 06.09.2005 v0.2a (Olli Lammi) **
#                  Map was twisted if coordinate band was
#                  in the middle of the map picture. Changed the way
#                  the script fetches the image from the Karttapaikka.
#
#                  ** 09.09.2005 v0.3a (Olli Lammi) **
#                  Added capability to fetch other scales than
#                  1:16000.
#
#                  ** 26.09.2005 v0.4a (Olli Lammi) **
#                  OziExplorer calibration file now improved to
#                  include correct KKJ-band (former it used YKJ-band
#                  for all maps)
#                  Included changes from Mikko Syrjä's code and
#                  suggestions:
#                  * support for more map picture output
#                    formats (whatever PIL-library version supports)
#                  * new optional command line parameter (--palette) to convert
#                    the result image from true color to palette mode.
#                    This will reduce the size of the image on disk,
#                    but also the picture quality might  be affected.
#                  * script outputs also Arcview and MapInfo calibration
#                    files (additional calibration file save functions
#                    by Mikko Syrjä <mikko@3d-system.fi>)
#
#                  ** 01.10.2005 v0.5a (Olli Lammi) **
#                  Improved conversion to palette mode.
#                  Coordinates will be converted to proper KKJ band
#                  automatically if --force-coordinates -option is not
#                  given in the command.
#
#                  ** 03.10.2005 v0.6a (Olli Lammi) **
#                  Corrected a bug in Mapinfo file format.
#
#                  ** 14.10.2005 v0.7a (Olli Lammi) **
#                  Added support for KKJ bands 0 and 5.
#
#                  ** 29.12.2005 v0.8a (Olli Lammi) **
#                  Corrected a bug in OziExplorer map file format.
#
#                  ** 04.06.2006 v0.9a (Olli Lammi) **
#                  Corrected a bug in OziExplorer map file format.
#                  Calibration coordinates were inaccurate because
#                  of false assumption with corner coordinate transforms.
#
#                  ** 11.06.2006 v1.0a (Olli Lammi) **
#                  Corrected minor spelling error in the output.
#                  Added random delay between the map part downloads.
#                  Added support for delaying the download start to given
#                  time of day.
#                  Added support for retrying map part download on failure.
#
#                  ** 23.08.2006 v1.1a (Olli Lammi) **
#                  Changed to support new version (released 22.8.2006) of
#                  Kansalaisen Karttapaikka site. 
#
#                  ** 28.08.2006 v1.2a (Olli Lammi) **
#                  Corrected the broken support for map scales.
#
#                  ** 28.10.2006 v1.3a (Olli Lammi) **
#                  Altered the maths a bit. Script now adds _one_ watermark
#                  back to the final picture. Corrected some minor
#                  issues with error handling.
#
#                  ** 28.10.2006 v1.3b (Olli Lammi) **
#                  Small bug.
#
#                  ** 30.10.2006 v1.3c-d (Olli Lammi) **
#                  Small change to default values when the wm is not 
#                  detected.
#
#                  ** 31.10.2006 v1.3e (Olli Lammi) **
#                  The script writes a log to the map cache directory
#                  of the fetch commands executed.
#
#                  ** 15.02.2008 v2.0a (Olli Lammi) **
#                  ** 25.02.2008 v2.0b (Olli Lammi) **
#                  ** 26.02.2008 v2.0c (Olli Lammi) **
#                  Major changes to the script. See CHANGELOG.
#
#                  ** 30.06.2008 v2.0d (Olli Lammi) **
#                  Support for new scales (1:2000, 1:4000, 1:8000) of
#                  Karttapaikka. Scale 1:16000 still the default.
#                  Experimental support for airplane pictures (--orto-parameter).
#
#                  ** 08.08.2008 v2.0e (Olli Lammi) **
#                  Bug fix. With --corners option there were possible coordinate
#                  calculation problems if coordinates are on different KKJ
#                  zones.
#
#                  ** 27.08.2008 v2.0f (Olli Lammi) **
#                  Bug fix. Esri world calibration file save did not work
#                  correctly with map scale 1:2000.
#
#                  ** 18.02.2009 v3.0a (Olli Lammi) **
#                  Retkikartta.fi support. Separated the map service code and
#                  map construction and calibration.
#
#                  ** 19.02.2009 v3.0b (Olli Lammi) **
#                  Changes to the map construction mathematics and calibration.
#
#                  ** 25.02.2009 v3.0c (Olli Lammi) **
#                  Corrections to accuracy of ESRI world and MapInfo 
#                  calibrations. Added check to KKP fetching for the 
#                  actual coordinates returned from the service. In some
#                  rare cases the service returns different area that is
#                  requested.  
#
#                  ** 23.03.2009 v3.0d (Olli Lammi) **
#                  Small change to Retkikartta.fi service code. 
#
#                  ** 26.03.2009 v3.0e (Olli Lammi) **
#                  Small change to Retkikartta.fi service code. 
#
#                  ** 06.05.2009 v3.0f (Olli Lammi) **
#                  Added informational printouts when fetching images.
#                  Script first executes a trial round to generate the
#                  map image and to calculate the number of map tiles
#                  in the image, cached tiles and tiles to download.
#
#                  ** 17.06.2009 v3.0f (Olli Lammi) **
#                  KKP: Added support for 1:8000000 scale. Removed 1:12000000
#                  scale, as it was no longer supported. Corrected the
#                  code about cropping the returned map image when
#                  the returned area is not the same as requested.
#
#                  ** 01.07.2009 v3.0g (Olli Lammi) **
#                  Added support for creating overlapped maps.
#
#                  ** 14.08.2009 v3.0g (Olli Lammi) **
#                  Added support GPSU GUX map calibration file.
#
#                  ** 10.02.2010 v3.0h (Olli Lammi) **
#                  Corrections to KKP map service code to handle
#                  the ETRS-TM35FIN coordinates. Changes to accept 
#                  also ETRS-TM35FIN coordinates as script parameters.
#                  Changes to the coordinate handling inside the
#                  actual fetch process.
#
#                  ** 05.08.2010 v3.0i (Olli Lammi) **
#                  Minor change to coordinates library.
#
#                  ** 27.09.2010 v3.0j (Olli Lammi) **
#                  Support for changed Retkikartta.fi platform. Minor
#                  changes in module interfaces. Correction to map-file
#                  projection setup with ETRS-TM35FIN system.
#
#                  ** 03.11.2010 v3.0k (Olli Lammi) **
#                  Correction to MapInfo tab-file projection setup with
#                  ETRS-TM35FIN system. Changed Retkikartta.fi scale values
#                  to match changed values in the web site.
#
#                  ** 10.04.2011 v3.0l (Olli Lammi) **
#                  Added support for Kansalaisen Karttapaikka
#                  "Kiinteistöjaotus" option. When giving a parameter
#                  "--ktjraja" for KKP query, the result map image will
#                  contain real estate border lines. (experimental) 
#
#                  ** 29.06.2011 v3.0l (Olli Lammi) **
#                  Added support for FreeTrack calibration files.
#                  Correction to OziExplorer .map calibration file
#                  projection setup with ETRS-TM35FIN.
#
#                  ** 30.01.2012 v3.1a (Olli Lammi) **
#                  Added support for transparent map layers.
#
#                  ** 01.02.2012 v3.1b (Olli Lammi) **
#                  Added support for KMZ save type.
#
#                  ** 04.02.2012 v3.1c (Olli Lammi) **
#                  Added support for olden KMZ LatLonBox-
#                  Overlay-type. KML2.2 versio support 
#                  maintains with kmz22 save type.
#
#                  ** 05.02.2012 v3.1d (Olli Lammi) **
#                  KML syntax tweaking for Garmin.
#
#                  ** 06.02.2012 v3.1e (Olli Lammi) **
#                  KMZ tile size tweaking and changed the
#                  Finland area detection algorithm.
#
#                  ** 10.02.2012 v3.1f (Olli Lammi) **
#                  Small fixes to coordinate transforms and fixed a 
#                  bug with layers and --cachedonly -parameter.
#
#                  ** 20.02.2012 v3.1g (Olli Lammi) **
#                  Rewritten KKJ coordinate transforms. Corrected
#                  Retkikartta layer interface problem.
#                  Introduced notification for new release version.
#
#                  ** 22.02.2012 v3.1h (Olli Lammi) **
#                  Bug corrections to rka module.
#
#                  ** 23.02.2012 v3.1i (Olli Lammi) **
#                  Improved layer loading with error conditions in 
#                  rka module.
#
############################################################################

# Imports

import sys, os, string
import math, os.path
import time, random
import re, urllib2
import StringIO, zipfile

from PIL import Image  # Python Imaging Library 
                       # (http://www.pythonware.com/products/pil/)

import coordinates  # KKJ to and from WGS84 coordinate transforms

import fms
import fms_kkp, fms_rka

###########################################################################

# Constants

VERSION = 'v3.1i'

# directory for caching the map image files
DEFAULT_PIC_CACHE = './map_cache/'

# command log file in the cache directory
LOG_FILE = 'fetch_map.log'

# default download delay times in seconds
DELAY_MIN = 30
DELAY_MAX = 60

# max retry count for a map part
RETRY_MAX = 3

SAVE_TYPES = { 'map': 'Ozi Explorer map data file', \
               'tab': 'MapInfo tab file', \
               'esri': 'Esri world file', \
               'gux': 'GPSU GUX file', \
               'cal': 'FreeTrack CAL file', \
               'kmz': 'KML archive file', \
               'kmz22': 'KML2.2 archive file' }
SAVE_TYPE_DEFAULT = 'map'

SERVICE_CODES = { 'kkp': 'Kansalaisen Karttapaikka', \
                  'rka': 'Retkikartta.fi' }
SERVICE_CODE_DEFAULT = 'kkp'

# cachedonly option empty background color
EMPTY_BACKGROUND_COLOR = (255, 255, 128)
EMPTY_LAYER_BACKGROUND_COLOR = (255, 255, 255)

###########################################################################

# Functions

def GetFMService(code):
    # check service code
    if not code in SERVICE_CODES.keys():
      print "ERROR: Invalid map service code: " + code
      sys.exit(1) 

    fmservice = None
    try:
        if code == 'kkp':
            fmservice = fms_kkp.FMSKansalaisenKarttapaikka()
        elif code == 'rka':
            fmservice = fms_rka.FMSRetkikarttaFi()
    except:
        fmservice = None
    if fmservice == None:
        print "ERROR: Cannot find or create Fetch_map service provider module for service code: " + code
        sys.exit(1)

    return fmservice


def main():
  print "********** Fetch_Map.py, " + VERSION + \
        " ****** Olli Lammi, 2005-2012 **********"
  print
  print "Donationware, distributed as Freeware."
  print 
  print "If you find this software useful to you and you would like to help"
  print "the developer to maintain it also in the future, please donate " 
  print "a small amount of your liking to the PayPal account: olammi@iki.fi."
  print 
  print "Jos tämä sovellus on mielestäsi hyödyllinen ja haluat auttaa sitä" 
  print "kehittymään myös jatkossa, voit lahjoittaa pienen sopivaksi katsomasi"
  print "summan kehittäjän PayPal-tilille: olammi@iki.fi. Sovelluksen käyttö"
  print "ei edellytä lahjoitusta." 
  print 

  CheckReleasedVersion()

  parameters = {}
  CORNERS = 0
  parameters["NOWNOW"] = 0
  parameters["CACHEDONLY"] = 0
  parameters["PIC_CACHE"] = DEFAULT_PIC_CACHE
  SAVET = []
  LAYERS = []
  SERVICE_CODE = SERVICE_CODE_DEFAULT
  parameters["STARTTIME"] = ''
  parameters["DELAY_MIN"] = DELAY_MIN
  parameters["DELAY_MAX"] = DELAY_MAX
  OVERLAP = 0
  OVERLAP_X = 0
  OVERLAP_Y = 0
  OVERLAP_O = 0.0
  
  fmservice = GetFMService(SERVICE_CODE)
  
  i = 1
  while i < len(sys.argv):
    if sys.argv[i][0] != '-':
      break
  
    if sys.argv[i] == '--palette':
      parameters["PALETTE_MODE"] = 1
    elif sys.argv[i] == '--force-coordinates':
      print "The option --force-coordinates is no longer valid. Option ignored."
    elif sys.argv[i] == '--corners':
      CORNERS = 1
    elif sys.argv[i] == '--nownow':
      parameters["NOWNOW"] = 1
    elif sys.argv[i] == '--starttime' and i+1 < len(sys.argv):
      parameters["STARTTIME"] = sys.argv[i+1] 
      i = i + 1
    elif sys.argv[i] == '--cache' and i+1 < len(sys.argv):
      parameters["PIC_CACHE"] = sys.argv[i+1]
      i = i + 1
    elif sys.argv[i] == '--help':
      Help()
      sys.exit(1)
    elif sys.argv[i] == '--info':
      Info()
      sys.exit(1)
    elif sys.argv[i] == '--cachedonly':
      parameters["CACHEDONLY"] = 1
    elif sys.argv[i] == '--save' and i+1 < len(sys.argv):
      SAVET.append(sys.argv[i+1])
      i = i + 1
    elif sys.argv[i] == '--layer' and i+1 < len(sys.argv):
      LAYERS.append(sys.argv[i+1])
      i = i + 1
    elif (sys.argv[i] == '-s' or sys.argv[i] == '--service') and i+1 < len(sys.argv):
      SERVICE_CODE = sys.argv[i+1]
      fmservice = GetFMService(SERVICE_CODE)
      i = i + 1
    elif (sys.argv[i] == '--overlap' and i+3 < len(sys.argv)):
      OVERLAP = 1
      OVERLAP_X = int(sys.argv[i+1])
      OVERLAP_Y = int(sys.argv[i+2])
      OVERLAP_O = float(sys.argv[i+3])
      i = i + 3
    else:
      temp = fmservice.HandleParameter(sys.argv[i])
      if temp <= 0:
        print "ERROR: Invalid option: " + sys.argv[i]
        Usage()
        sys.exit(1)
      else:
        i = i + temp - 1
        
    i = i + 1

  # check leftover command line parameters
  if len(sys.argv)-i > 6 or len(sys.argv)-1 < 4:
    Usage()
    sys.exit(1)

  # check configured layers
  if len(LAYERS) > 0:
      for layer in LAYERS:
          if not fmservice.GetAvailableLayers().has_key(layer):
              print "ERROR: Unknown layer: " + layer
              sys.exit(1)
  parameters["LAYERS"] = LAYERS
  
  SCALE = fmservice.SCALE
  COORDTYPE = coordinates.COORD_TYPE_YKJ
  try:
    MAP_NAME = sys.argv[i]
    
    if CORNERS:
      bl = HandleCoordinates(sys.argv[i+1], sys.argv[i+2])
      ur = HandleCoordinates(sys.argv[i+3], sys.argv[i+4])
      bl = coordinates.Translate(bl, coordinates.COORD_TYPE_YKJ)
      ur = coordinates.Translate(ur, coordinates.COORD_TYPE_YKJ)
  
      YKJ_P = (ur['N'] + bl['N']) / 2
      YKJ_I = (ur['E'] + bl['E']) / 2
      SIZE_X = float(abs(ur['E'] - bl['E']) / 1000.0)
      SIZE_Y = float(abs(ur['N'] - bl['N']) / 1000.0)
    else:
      kp = HandleCoordinates(sys.argv[i+1], sys.argv[i+2])
      kp = coordinates.Translate(kp, coordinates.COORD_TYPE_YKJ)
      (YKJ_P, YKJ_I) = (kp['N'], kp['E'])
      SIZE_X = float(sys.argv[i+3])
      SIZE_Y = float(sys.argv[i+4])
      
    if len(sys.argv)-i > 5:
      SCALE = sys.argv[i+5]
  except:
    Usage()
    sys.exit(1)

  # check save types
  # by default OziExplorer calibration file is saved
  if len(SAVET) <= 0:
      SAVET = [ SAVE_TYPE_DEFAULT ]
  for savetype in SAVET:
    if not savetype in SAVE_TYPES.keys():
      print "ERROR: Invalid calibration file save type: " + savetype
      sys.exit(1) 
  parameters["SAVETYPES"] = SAVET

  # check that the given coordinates are in Finland area
  temp_KKJ = { 'P': YKJ_P, 'I': YKJ_I }
  if not coordinates.KKJxy_in_Finland(temp_KKJ):
    print "ERROR: Map coordinates seem to be invalid and not in the Finland area."
    print "       Check the coordinates and see that the north coordinate is given"
    print "       before the east coordinate in the command line."  
    sys.exit(1)
  
  if not fmservice.SetScale(SCALE):
    print "ERROR: Invalid map scale: " + SCALE + "\n\nAvailable scales for service " + SERVICE_CODE + ":"
    for scale in fmservice.GetScales():
      print "  " + scale
    sys.exit(1)

  # test for the map cache
  if len(parameters["PIC_CACHE"]) <= 0:
    parameters["PIC_CACHE"] = './'
  elif parameters["PIC_CACHE"][len(parameters["PIC_CACHE"])-1] != '/':
    parameters["PIC_CACHE"] = parameters["PIC_CACHE"] + '/'
  try:
    if not os.path.isdir(parameters["PIC_CACHE"]):
      print 'Map cache directory ' + parameters["PIC_CACHE"] + ' not found. Creating cache.'
      os.mkdir(parameters["PIC_CACHE"])
  except:
    print "ERROR: Error accessing or creating map cache: " + parameters["PIC_CACHE"]
    sys.exit(1) 

  # insert command to log file
  try:
    outf = open(parameters["PIC_CACHE"] + LOG_FILE, 'a')
    outf.write('fetch_map.py ' + string.join(sys.argv[1:], ' ') + '\n')
    outf.close()
  except:
    print 'Could not write log file: ' + parameters["PIC_CACHE"] + LOG_FILE

  (COORDTYPE, C_E, C_N) = fmservice.TranslateToServiceCoordinatesXY(COORDTYPE, YKJ_I, YKJ_P)
  
  if OVERLAP:
      print "Overlapping result images. Requested a grid of " + \
            "(%d,%d)=%d map images overlapping by %.1f kilometers." \
            % (OVERLAP_X, OVERLAP_Y, OVERLAP_X * OVERLAP_Y, OVERLAP_O)
      
      if OVERLAP_X <= 0 or OVERLAP_Y <= 0:
          print "ERROR: Size of overlap grid is invalid."
          sys.exit(1)
      
      if OVERLAP_O >= SIZE_X or OVERLAP_O >= SIZE_Y:
          print "ERROR: Overlap amount too large compared to area size."
          sys.exit(1) 
          
      oo = OVERLAP_O * 1000.0
      ox = (SIZE_X * 1000.0 + (OVERLAP_X - 1) * oo) / float(OVERLAP_X)
      oy = (SIZE_Y * 1000.0 + (OVERLAP_Y - 1) * oo) / float(OVERLAP_Y)
      LL_N = C_N - (int(SIZE_Y * 1000) / 2)
      LL_E = C_E - (int(SIZE_X * 1000) / 2)      
      (mname, mext) = os.path.splitext(MAP_NAME)

      y = 0
      while y < OVERLAP_Y:
          x = 0
          while x < OVERLAP_X:
              tp = LL_N + (OVERLAP_Y - y - 1) * (oy - oo) + 0.5 * oy  
              ti = LL_E + x * (ox - oo) + 0.5 * ox           
              tempname = mname + "_" + repr(x+1) + "_" + repr(y+1) + mext
              print
              print
              Fetch_Map(fmservice, COORDTYPE, tp, ti, ox / 1000.0, oy / 1000.0, tempname, parameters)
              x = x + 1
          y = y + 1             
  else:
      Fetch_Map(fmservice, COORDTYPE, C_N, C_E, SIZE_X, SIZE_Y, MAP_NAME, parameters)


###########################################################################
# Function:    Fetch_Map(FetchMapService, coordType, centerN, centerE, size_x, size_y, 
#                          map_name, Parameters) 
###########################################################################
def Fetch_Map(fmservice, C_TYPE, C_N, C_E, SIZE_X, SIZE_Y, MAP_NAME, parameters):
  # determine the pixel size of the result map picture
  MAPSIZE_X = int(round(SIZE_X * 1000.0 / fmservice.PIC_RATIO))
  MAPSIZE_Y = int(round(SIZE_Y * 1000.0 / fmservice.PIC_RATIO))
        
  # determine N and E for lower left corner of the result map. 
  LL_N = C_N - (int(SIZE_Y * 1000) / 2)
  LL_E = C_E - (int(SIZE_X * 1000) / 2)
  
  # calculate the closest actual pixel coordinate for this map
  ((indx, indy), (tempx, tempy)) = fmservice.GetPicIndexes(LL_E, LL_N)
  LL_E = tempx + round((LL_E - tempx) / fmservice.PIC_RATIO) * fmservice.PIC_RATIO
  LL_N = tempy + round((LL_N - tempy) / fmservice.PIC_RATIO) * fmservice.PIC_RATIO

  # determine N and E for upper right corner of the result map.
  UR_N = LL_N + MAPSIZE_Y * fmservice.PIC_RATIO
  UR_E = LL_E + MAPSIZE_X * fmservice.PIC_RATIO


  # print out basic parameters
  print "Creating map image: "
  print "  Result map scale:   1:" + `fmservice.SCALEVAL`
  print "  Lower left corner:  %.2f, %.2f (%s: N, E)" % (LL_N, LL_E, C_TYPE)
  print "  Upper right corner: %.2f, %.2f (%s: N, E)" % (UR_N, UR_E, C_TYPE)
  print "  Result map size:    %.2f, %.2f (width, height in meters)" % (UR_E-LL_E, UR_N-LL_N) 
  print "  Result image size:  " + `MAPSIZE_X` + ", " \
           + `MAPSIZE_Y` + " (x,y)"
  if len(parameters["LAYERS"]) > 0:
      print
      for layer in parameters["LAYERS"]:
          print "  Additional layer:   " + fmservice.GetAvailableLayers()[layer][0]
  print

  (parameters["DELAY_MIN"], parameters["DELAY_MAX"]) = fmservice.GetServiceDelayLimits()

  print "Running a test run to calculate the required resources to produce"
  print "the result map..."
  
  # do a dry run to calculate the mep parts
  (nCached, nFetched, nBlanked) = DoFetch(1, None, fmservice, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y, parameters)
  
  print
  print "The fetch_map process will generate the result map from " + `nCached+nFetched+nBlanked`
  print "separate map images (cached/fetched/blank: " + `nCached` + "/" + `nFetched` + "/" + `nBlanked` + ")"
  print
  
  # create result image for the service
  im = Image.new("RGB", (MAPSIZE_X, MAPSIZE_Y))

  # do the actual map build process
  parameters["TILEAMOUNTS"] = (nCached, nFetched, nBlanked)
  DoFetch(0, im, fmservice, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y, parameters)
      
  print

  # check extension
  (MAP_NAME, MAP_EXT) = os.path.splitext(MAP_NAME)
  if len(MAP_EXT) <= 0:
    MAP_EXT = '.png'
  FILE_NAME = MAP_NAME + MAP_EXT
  
  # save the image file
  try:
    fmservice.PostProcess(im)
    if parameters.has_key("PALETTE_MODE") and parameters["PALETTE_MODE"]:
      im = im.convert("P", dither=Image.NONE, palette=Image.ADAPTIVE)
      print "Converted the result map image to palette mode."
    im.save(FILE_NAME)
    print "Saved result map image to " + FILE_NAME
  except:
    print "ERROR: Cannot save result map: " + FILE_NAME
    sys.exit(1)

  # save different calibration files
  for savetype in parameters["SAVETYPES"]:
    if savetype == "map":
      SaveMapCalibration(MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'tab': 
      SaveMapInfoTab(MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'esri':
      SaveEsriWorld(MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'gux':
      SaveGpsuGux(MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'cal':
      SaveFreeTrackCal(MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'kmz':
      SaveKMZCal(im, MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)
    elif savetype == 'kmz22':
      SaveKMZCal2_2(im, MAP_NAME, MAP_EXT, C_TYPE, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y)





###########################################################################
# Function:    DoFetch
###########################################################################
def DoFetch(DRYRUN, im, fmservice, LL_N, LL_E, UR_N, UR_E, MAPSIZE_X, MAPSIZE_Y, parameters):
  nCached = 0
  nFetched = 0
  nBlanked = 0
  nECached = 0
  nEFetched = 0
  nEBlanked = 0
  nErrors = 0  
  LOADED_PARTS = 0
  STARTTIME = parameters["STARTTIME"]
  layers = [""] + list(parameters["LAYERS"])
  skipwait = False
  
  if not DRYRUN and parameters.has_key("TILEAMOUNTS"):  
    (nECached, nEFetched, nEBlanked) = parameters["TILEAMOUNTS"]
    
  # loops to fetch and build the result data  
  mapy = LL_N
  while mapy < UR_N - (0.25 * fmservice.PIC_RATIO):
    mapx = LL_E
    while mapx < UR_E - (0.25 * fmservice.PIC_RATIO):
      # get indexes and lower left corner of the map pic to be fetched
      # that has the point (mapx, mapy) in it
      ((indx, indy), (fetchx, fetchy)) = fmservice.GetPicIndexes(mapx, mapy)

      for layer in layers: 
          # fetch the picture, if cache does not contain it already
          cdirname = parameters["PIC_CACHE"] + fmservice.SERVICE_CODE + '/'
          fname = cdirname + fmservice.GetCacheName(indx, indy, layer)  
    
          if not DRYRUN:
            print 'Progress: %.1f %%, images left %d (cached, fetched, blank: %d, %d, %d)' % (100.0 * float((nCached + nFetched + nBlanked)) / float((nECached + nEFetched + nEBlanked)), nECached - nCached + nEFetched - nFetched + nEBlanked - nBlanked, nECached - nCached, nEFetched - nFetched, nEBlanked - nBlanked)
                      
          if not os.path.exists(fname) and not parameters["CACHEDONLY"]:
            nFetched = nFetched + 1
            if not DRYRUN:
              retry = 0
              while 1:            
                # if starttime is set, wait for the given time before beginning the
                # download
                if len(STARTTIME) > 0:
                  start_time = STARTTIME
                  STARTTIME = "" 
                  if not WaitForStartTime(start_time):
                    print "ERROR: Invalid start time (--starttime parameter): " + start_time
                    sys.exit(1)
                
                # delay for random time
                if not parameters["NOWNOW"] and LOADED_PARTS > 0 and not skipwait:
                  delaytime = random.randint(parameters["DELAY_MIN"], parameters["DELAY_MAX"])
                  print "Sleeping " + `delaytime` + " seconds..."
                  time.sleep(delaytime)
                skipwait = False
    
                LOADED_PARTS = LOADED_PARTS + 1
                if retry > 0:
                    print "Retrying..."
                stat = fmservice.FetchPic(indy, indx, cdirname, parameters["PIC_CACHE"], layer)
                if stat == 1:
                  print "Fetched map image (N,E)=(%.2f, %.2f) %s" % (fetchy, fetchx, layer)
                  break
                elif stat == 2:
                  skipwait = True
                  print "Moved map image from old cache (N,E)=(%.2f, %.2f) %s" % (fetchy, fetchx, layer)
                  break
                else:
                  print "ERROR: Cannot get image for (N,E)=(%.2f, %.2f) %s" % (fetchy, fetchx, layer)
                  retry = retry + 1
                  if retry > RETRY_MAX:
                    print "ERROR: Exceeded retry count limit. Using blank image..."
                    nErrors = nErrors + 1
                    break          
          elif not os.path.exists(fname) and parameters["CACHEDONLY"]:
            nBlanked = nBlanked + 1
            if not DRYRUN:
              print "Map image not found in the cache. Using blank image due to --cachedonly option."
          else:
            nCached = nCached + 1
            if not DRYRUN:
              print "Using cached map image (N,E)=(%.2f, %.2f) %s" % (fetchy, fetchx, layer)
            
          # determine the amount to crop the picture
          pllx = int(round((mapx - fetchx) / fmservice.PIC_RATIO))
          plly = int(round((mapy - fetchy) / fmservice.PIC_RATIO))          
          if (fetchx + fmservice.MAP_SIZEX) > UR_E:
            purx = int(round((UR_E - fetchx) / fmservice.PIC_RATIO))
          else:
            purx = int(round(fmservice.MAP_SIZEX / fmservice.PIC_RATIO))
          if (fetchy + fmservice.MAP_SIZEY) > UR_N:
            pury = int(round((UR_N - fetchy) / fmservice.PIC_RATIO))
          else:
            pury = int(round(fmservice.MAP_SIZEY / fmservice.PIC_RATIO))
          piccrop = ( pllx, fmservice.PIC_SIZEY - pury, purx, fmservice.PIC_SIZEY - plly)
      
          if not DRYRUN:
            tempim = None
            if parameters["CACHEDONLY"] and not os.path.exists(fname):
                if len(layer) <= 0:
                  tempim = Image.new("RGB", (fmservice.PIC_SIZEX, fmservice.PIC_SIZEY), EMPTY_BACKGROUND_COLOR)
                else:
                  tempim = None
            else: 
              # load, crop and paste required data to the result image
              try:  
                tempim = Image.open(fname)
                tempim.load()
              except:
                tempim = None
                print "ERROR: Cannot load map image: " + fname
              
          picx = int(round((mapx - LL_E) / fmservice.PIC_RATIO))
          picy = int(round((mapy - LL_N) / fmservice.PIC_RATIO))
          
          if not DRYRUN:
            if len(layer) <= 0:
              if tempim == None:
                tempim = Image.new("RGB", (fmservice.PIC_SIZEX, fmservice.PIC_SIZEY), EMPTY_BACKGROUND_COLOR)
              im.paste( tempim.crop(piccrop), (picx, MAPSIZE_Y - picy - (pury - plly)) )
            elif tempim != None:
              maskimg = tempim.crop(piccrop)  
              transratio = fmservice.GetAvailableLayers()[layer][1]
              AdjustAlpha(maskimg, transratio)          
              im.paste( maskimg, (picx, MAPSIZE_Y - picy - (pury - plly)), maskimg)
              maskimg = 0
          
      mapx = mapx + (purx - pllx) * fmservice.PIC_RATIO

    mapy = mapy + (pury - plly) * fmservice.PIC_RATIO

  if nErrors > 0:
    print 
    print "Errors during fetch. %d images left blank." % nErrors
      
  return (nCached, nFetched, nBlanked)


###########################################################################
# Function:    Usage
###########################################################################

def Usage():    
  print 'USAGE:  python fetch_map.py --help'
  print '        python fetch_map.py --info'
  print '        python fetch_map.py [options] <map_name> ' + \
        '<coord_N> <coord_E> <size_x> <size_y> [scale]'
  print '        python fetch_map.py --corners [options] <map_name> ' + \
        '<coord_bl_N> <coord_bl_E> <coord_tr_N> <coord_tr_E> [scale]'


###########################################################################
# Function:    Help
###########################################################################

def Help():  
  temps = string.split(HELP_TEXT, '\n')
  for temp in temps:
    if len(temp) > 0 and temp[0] == '#':
      temp = temp[1:]
    if len(temp) > 0 and temp[0] == ' ':
      temp = temp[1:]
    print temp

  for s in SERVICE_CODES.keys():
      tempserv = GetFMService(s)
      temps = tempserv.GetHelp()

      if len(temps) > 0: 
        print "\nMap service related help: " + SERVICE_CODES[s] + "\n"
        temps = string.split(temps, '\n')
        for temp in temps:
            if len(temp) > 0 and temp[0] == '#':
                temp = temp[1:]
            if len(temp) > 0 and temp[0] == ' ':
                temp = temp[1:]
            print temp
        
  
  
###########################################################################
# Function:    Info
###########################################################################

def Info():
  # list possible map services (--service)
  print 'Available map service codes, scales and layers:'
  print   
  for s in SERVICE_CODES.keys():
    tempservice = GetFMService(s)
    temps = '  ' +  s + ' - ' + SERVICE_CODES[s] + ' (' + tempservice.GetVersion() + ')'  
    if s == SERVICE_CODE_DEFAULT:
      temps = temps + ' (default)'
    print temps
      
    for sc in tempservice.GetScales():
      temps = '    ' + sc
      if sc == tempservice.PIC_SCALE_DEFAULT:
        temps = temps + ' (default)'
      print temps
    print 
    
    templayers = tempservice.GetAvailableLayers()
    if len(templayers.keys()) > 0:
      print '    Available layers:'
      for lk in templayers.keys():
        print '      ' + lk + ': ' + templayers[lk][0]
    print
        
  print
  print 
  
  print 'Available calibration file save types:'
  print 
  for s in SAVE_TYPES.keys():
    temps = '  ' +  s + ' - ' + SAVE_TYPES[s]  
    if s == SAVE_TYPE_DEFAULT:
      temps = temps + ' (default)'
    print temps
  

###########################################################################
# Function:    Info
###########################################################################

def CheckReleasedVersion():  
    url = 'http://olammi.iki.fi/sw/fetch_map/current_release.txt'
    res = ''
    try:
        USERAGENT = "FetchMap/" + VERSION + " (Python/" + "%d.%d.%d.%s.%d" % sys.version_info + "; Sys/" + sys.platform + ")"
        req = urllib2.Request(url)
        req.add_header("User-Agent", USERAGENT)
        f = urllib2.urlopen(req)
        res = f.readlines()
        f.close()
    except:
        return

    if len(res) <= 0:
        return

    res = string.strip(string.split(res[0], '\n')[0])
    if len(res) <= 0:
        return

    if VERSION < res:
        print
        print "######################################################################"
        print "#    There is a newer release version of Fetch_Map available in "
        print "# "
        print "#                  http://olammi.iki.fi/sw/fetch_map/"
        print "# "
        print "#    Current version: %s    Available release version: %s" % (VERSION, res)
        print "######################################################################"
        time.sleep(5)
        print
        
  
  
###########################################################################
# Function:    HandleCoordinates(string, string)
###########################################################################
# Description: Takes two coordinate strings and returns a map coordinate
#              point (IN KKJ) that corresponds to the given location.
###########################################################################

def HandleCoordinates(c1, c2):
  cval1 = coordinates.Str_to_CoordinateValue(c1)
  cval2 = coordinates.Str_to_CoordinateValue(c2)
  
  if (cval1 != coordinates.INVALID_COORDINATE):
      if (cval2 == coordinates.INVALID_COORDINATE):
          msg = 'Coordinate pair values not in the same coordinate system.'
          print 'ERROR: ' + msg
          raise Exception, msg
      wgs = {}
      wgs['N'] = cval1
      wgs['E'] = cval2
      wgs['type'] = coordinates.COORD_TYPE_WGS84
      return wgs
  else:
      if (cval2 != coordinates.INVALID_COORDINATE):
          msg = 'Coordinate pair values not in the same coordinate system.'
          print 'ERROR: ' + msg
          raise Exception, msg
      n = int(c1)
      e = int(c2)

      type = coordinates.COORD_TYPE_YKJ
      if (e < 1000000.0):
          type = coordinates.COORD_TYPE_ETRSTM35FIN
      elif (e / 1000000 != 3):
          type = coordinates.COORD_TYPE_KKJ
          
      return {'type': type, 'N': n, 'E': e}


###########################################################################
# Function:    AdjustAlpha
###########################################################################
# Description: Adjust image alpa channel by factor
###########################################################################

def AdjustAlpha(image, factor):
    idata = list(image.getdata())
    tempdata = []
    for dp in idata:
        tempdata.append( ( dp[0], dp[1], dp[2], int(round(dp[3] * factor)) ) )
    image.putdata(tempdata)    
            
            
###########################################################################
# Function:    WaitForStartTime
###########################################################################
# Description: Waits until a given time of day is reached.
###########################################################################

def WaitForStartTime(stime):
  # check the startime format
  regstr = '^(?P<hh>[0-2][0-9])(?P<mm>[0-5][0-9])$'
  m = re.compile(regstr).findall(stime)
  if m != None and len(m) > 0:
    s_hour = int(m[0][0])
    s_min = int(m[0][1])
    s_time = int(stime)
  else:
    return 0

  if s_hour < 0 or s_hour > 23:
    return 0
  if s_min < 0 or s_min > 59:
    return 0

  # get the current time of day
  lt = time.localtime()
  now_time = lt[3] * 100 + lt[4]

  lt = (lt[0], lt[1], lt[2], s_hour, s_min, 0, lt[6], lt[7], lt[8])
  target_time = time.mktime(lt)

  # if wanted time is tomorrow, add one day
  # to target time
  if now_time > s_time:
    target_time = target_time + 86400

  # wait until the target time
  print "Waiting until it is " + stime + " o'clock..."
  while (time.time() < target_time):
      time.sleep(int(target_time - time.time()))
  print "Starting download at " + time.asctime()

  return 1
  


###########################################################################
# Function:  SaveMapCalibration
###########################################################################
# Input:     mapname - name of the map (filename without extension)
#            mapext  - extension of the saved map picture
#            c_type  - coordinate type
#            ll_n    - N coordinate of the lower left corner
#            ll_e    - E coordinate of the lower left corner
#            ur_n    - N coordinate of the upper right corner
#            ur_e    - E coordinate of the upper right corner
#            picx    - widht of the map picture in pixels
#            picy    - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################

def SaveMapCalibration(mapname, mapext, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):
  RATIO = float(ur_e-ll_e) / float(picx)

  try:
    f = open(mapname + '.map', 'w')
  except:
    print "ERROR: Cannot open .map file: " + mapname + ".map"
    return 0

  if (c_type == coordinates.COORD_TYPE_KKJ):
    (long0, centerm) = coordinates.KKJ_ZONE_INFO[ coordinates.KKJ_Zone_I(ll_e) ]
    projection = 'Transverse Mercator'
    factor = 1.0000
  elif (c_type == coordinates.COORD_TYPE_YKJ):
    (long0, centerm) = coordinates.KKJ_ZONE_INFO[ 3 ]
    projection = 'Transverse Mercator'
    factor = 1.0000
  elif (c_type == coordinates.COORD_TYPE_ETRSTM35FIN):
    (long0, centerm, projection, factor) = (27.0, 500000.0, 'Transverse Mercator', 0.9996)
  else:
    (long0, centerm, projection, factor) = (27.0, 3500000.0, 'Transverse Mercator', 1.0000)

  outlines = []

  outlines.append('OziExplorer Map Data File Version 2.2\n')
  outlines.append(mapname + '\n')
  outlines.append(mapname + mapext + '\n')
  outlines.append('1 ,Map Code,\n')
  outlines.append('WGS 84,WGS 84,   0.0000,   0.0000,WGS 84\n')
  outlines.append('Reserved 1\n')
  outlines.append('Reserved 2\n')
  outlines.append('Magnetic Variation,,,E\n')
  outlines.append('Map Projection,' + projection + ',PolyCal,No,AutoCalOnly,No,BSBUseWPX,No\n')
                  
                  
  # determine 9 points on the map to calibrate
  #
  # formula to determine xy-coordinates for a given point (x,y) in the
  # map image if the coordinates of the center of the lower left corner 
  # pixel are (N,E)=(ll_n, ll_e)
  # (N) ppy = ll_n + (picy - y - 0.5) * RATIO
  # (E) ppx = ll_e + (x + 0.5) * RATIO
  i = 0
  while (i < 9):
    y = int(round((int(math.floor(i / 3)) + 1) * (picy / 4.0)))
    x = int(round(((i % 3) + 1) * (picx / 4.0)))
    ppy = ll_n + (picy - y - 0.5) * RATIO
    ppx = ll_e + (x + 0.5) * RATIO
    WGS = coordinates.Translate( {'type': c_type, 'N': ppy, 'E': ppx}, coordinates.COORD_TYPE_WGS84 )
    outlines.append('Point%(i)02i,xy, ' % {'i':i+1})
    outlines.append('%(x)i, %(y)i,in, deg, ' % {'x': x, 'y': y})
    (b, a) = math.modf(WGS['N'])
    outlines.append( `int(a)` + ', ' )
    outlines.append( '%(b)3.3f' % {'b': b * 60.0} )

    outlines.append(',N, ')
    (b, a) = math.modf(WGS['E'])
    outlines.append( `int(a)` + ', ' )
    outlines.append( '%(b)3.3f' % {'b': b * 60.0} )

    outlines.append(',E, ')
    outlines.append('grid, , , , N\n')
    i = i + 1

  while (i < 30):
    outlines.append('Point' + `i+1` + ',xy,,,in,deg,,,,,,, grid,,,,\n')
    i = i + 1

  outlines.append('Projection Setup, 0.000000000, ')
  outlines.append(repr(float(long0)))            
  outlines.append(', %(fac).4f, ' % {'fac': factor})
  outlines.append(repr(float(centerm)))
  outlines.append(', 0.00,,,,,\n')
  outlines.append('Map Feature = MF ; Map Comment = MC     These follow if they exist\n')
  outlines.append('Track File = TF      These follow if they exist\n')
  outlines.append('Moving Map Parameters = MM?    These follow if they exist\n')
  outlines.append('MM0,Yes\n')
  outlines.append('MMPNUM,4\n')
  outlines.append('MMPXY,1,0,0\n')
  outlines.append('MMPXY,2,' + `picx` + ',0\n')
  outlines.append('MMPXY,3,' + `picx` + ',' + `picy` + '\n')
  outlines.append('MMPXY,4,0,' + `picy` + '\n')

  WGSll = coordinates.Translate( {'type': c_type, 'N': ll_n, 'E': ll_e}, coordinates.COORD_TYPE_WGS84)
  WGSlr = coordinates.Translate( {'type': c_type, 'N': ll_n, 'E': ur_e}, coordinates.COORD_TYPE_WGS84)
  WGSul = coordinates.Translate( {'type': c_type, 'N': ur_n, 'E': ll_e}, coordinates.COORD_TYPE_WGS84)
  WGSur = coordinates.Translate( {'type': c_type, 'N': ur_n, 'E': ur_e}, coordinates.COORD_TYPE_WGS84)

  outlines.append('MMPLL,1, %(E)6.6f, %(N)6.6f\n' % WGSul)
  outlines.append('MMPLL,2, %(E)6.6f, %(N)6.6f\n' % WGSur)
  outlines.append('MMPLL,3, %(E)6.6f, %(N)6.6f\n' % WGSlr)
  outlines.append('MMPLL,4, %(E)6.6f, %(N)6.6f\n' % WGSll)

  outlines.append('MM1B, %2.2f\n' % RATIO)
  outlines.append('MOP,Map Open Position,0,0\n')
  outlines.append('IWH,Map Image Width/Height,' + `picx` + ',' + `picy` + '\n')

  try:
    f.writelines(outlines)
    f.close()
  except:
    print "ERROR: Cannot write .map file: " + mapname + ".map"
    return 0

  print "Saved map calibration file to " + mapname + ".map"
  return 1



###########################################################################
# Function:  SaveMapInfoTab
#
# Author:    Mikko Syrjä (mikko@3d-system.fi)
#
###########################################################################
# Input:     mapname   - name of the map (filename without extension)
#            extension - map file extension
#            c_type    - coordinate type
#            ll_n      - N coordinate of the lower left corner
#            ll_e      - E coordinate of the lower left corner
#            ur_n      - N coordinate of the upper right corner
#            ur_e      - E coordinate of the upper right corner
#            picx      - widht of the map picture in pixels
#            picy      - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################

def SaveMapInfoTab(mapname, extension, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):

  try:
    f = open(mapname + '.tab', 'w')
  except:
    print "ERROR: Cannot open .tab file: " + mapname + ".tab"
    return 0

  if (c_type == coordinates.COORD_TYPE_KKJ):
    (longitude, easting) = coordinates.KKJ_ZONE_INFO[ coordinates.KKJ_Zone_I(ll_e) ]
    coordsys = 'CoordSys Earth Projection 24, 1016, "m", ' + repr(int(longitude)) + ', 0, 1, ' + repr(int(easting)) + ', 0'
  elif (c_type == coordinates.COORD_TYPE_YKJ):
    (longitude, easting) = coordinates.KKJ_ZONE_INFO[ 3 ]
    coordsys = 'CoordSys Earth Projection 24, 1016, "m", ' + repr(int(longitude)) + ', 0, 1, ' + repr(int(easting)) + ', 0'
  elif (c_type == coordinates.COORD_TYPE_ETRSTM35FIN):
    (longitude, easting) = (27.0, 500000.0)
    coordsys = 'CoordSys Earth Projection 8, 115, "m", 27, 0, 0.9996, 500000, 0'
  else:
    (longitude, easting) = (27.0, 3500000.0)
    coordsys = 'CoordSys Earth Projection 24, 1016, "m", ' + repr(int(longitude)) + ', 0, 1, ' + repr(int(easting)) + ', 0'

  outlines = []
  outlines.append('!table\n')
  outlines.append('!version 400\n')
  outlines.append('!charset WindowsLatin1\n')
  outlines.append('Definition Table\n')
  outlines.append('File "' + mapname + extension + '"\n')
  outlines.append('Type "RASTER"\n')
  outlines.append('(' + repr(float(ll_e)) + ',' + repr(float(ur_n)) + ') (' + repr(0) + ',' + repr(0) + ') Label "Pt 1",\n')
  outlines.append('(' + repr(float(ur_e)) + ',' + repr(float(ur_n)) + ') (' + repr(picx) + ',' + repr(0) + ') Label "Pt 2",\n')
  outlines.append('(' + repr(float(ur_e)) + ',' + repr(float(ll_n)) + ') (' + repr(picx) + ',' + repr(picy) + ') Label "Pt 3",\n')
  outlines.append('(' + repr(float(ll_e)) + ',' + repr(float(ll_n)) + ') (' + repr(0) + ',' + repr(picy) + ') Label "Pt 4"\n')
  outlines.append(coordsys + '\n')
  outlines.append('Units \"m\"\n')
                  
  try:
    f.writelines(outlines)
    f.close()
  except:
    print "ERROR: Cannot write .tab file: " + mapname + ".tab"
    return 0

  print "Saved MapInfo tab file to " + mapname + ".tab"
  return 1



###########################################################################
# Function:  SaveEsriWorld
#
# Author:    Mikko Syrjä (mikko@3d-system.fi)
#            (corrections to calibration accuracy: O.Lammi)
#
###########################################################################
# Input:     mapname   - name of the map (filename without extension)
#            extension - map file extension
#            c_type    - coordinate type
#            ll_n      - N coordinate of the lower left corner
#            ll_e      - E coordinate of the lower left corner
#            ur_n      - N coordinate of the upper right corner
#            ur_e      - E coordinate of the upper right corner
#            picx      - widht of the map picture in pixels
#            picy      - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################

def SaveEsriWorld(mapname, extension, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):

  worldext = extension[1] + extension[3] + "w"

  try:
    f = open(mapname + '.' + worldext, 'w')
  except:
    print "ERROR: Cannot open ." + worldext + " file: " + mapname + '.' + worldext
    return 0

  pixelsizex = (ur_e - ll_e) / float(picx)
  pixelsizey = (ur_n - ll_n) / float(picy)

  outlines = []
  outlines.append(repr(float(pixelsizex)) + '\n')
  outlines.append(repr(0.0) + '\n')
  outlines.append(repr(0.0) + '\n')
  outlines.append(repr(float(-pixelsizey)) + '\n')
  outlines.append(repr(ll_e + pixelsizex / 2.0) + '\n')
  outlines.append(repr(ur_n - pixelsizey / 2.0) + '\n')

  try:
    f.writelines(outlines)
    f.close()
  except:
    print "ERROR: Cannot write Esri world file: " + mapname + "." + worldext
    return 0

  print "Saved Esri world file to " + mapname + "." + worldext
  return 1




###########################################################################
# Function:  SaveGpsuGux
###########################################################################
# Input:     mapname - name of the map (filename without extension)
#            mapext  - extension of the saved map picture
#            c_type  - coordinate type
#            ll_n    - N coordinate of the lower left corner
#            ll_e    - E coordinate of the lower left corner
#            ur_n    - N coordinate of the upper right corner
#            ur_e    - E coordinate of the upper right corner
#            picx    - widht of the map picture in pixels
#            picy    - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################

def SaveGpsuGux(mapname, mapext, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):
  RATIO = float(ur_e-ll_e) / float(picx)

  try:
    f = open(mapname + '.gux', 'w')
  except:
    print "ERROR: Cannot open .gux file: " + mapname + ".gux"
    return 0

  outlines = []

  outlines.append('I GPSU 5,01\n')
  outlines.append('M E               WGS 84 100  0,0000000E+00  0,0000000E+00 0 0 0\n')
  outlines.append('U LAT LON DM\n')
  outlines.append('S Image=' + mapname + mapext + '\n')

  # determine 4 points on the map to calibrate
  #
  # formula to determine xy-coordinates for a given point (x,y) in the
  # map image if the coordinates of the center of the lower left corner 
  # pixel are (N,E)=(ll_n, ll_e)
  # (N) ppy = ll_n + (picy - y - 0.5) * RATIO
  # (E) ppx = ll_e + (x + 0.5) * RATIO
  i = 0
  while (i < 4):
    y = int(round((int(math.floor(i / 2)) + 1) * (picy / 3.0)))
    x = int(round(((i % 2) + 1) * (picx / 3.0)))
    ppy = ll_n + (picy - y - 0.5) * RATIO
    ppx = ll_e + (x + 0.5) * RATIO
    WGS = coordinates.Translate( {'type': c_type, 'N': ppy, 'E': ppx}, coordinates.COORD_TYPE_WGS84 )

    outlines.append('S CalPoint%i=' % (i+1, ))
    
    (b, a) = math.modf(WGS['N'])
    outlines.append('N%02i°%02.4f\' ' % (int(a), b * 60.0) )
    (b, a) = math.modf(WGS['E'])
    outlines.append('E%03i°%02.4f\'' % (int(a), b * 60.0) )
    outlines.append('= %i %i\n' % (x, y))

    i = i + 1
    
  try:
    f.writelines(outlines)
    f.close()
  except:
    print "ERROR: Cannot write .gux file: " + mapname + ".gux"
    return 0

  print "Saved GPSU GUX file to " + mapname + ".gux"
  return 1



###########################################################################
# Function:  SaveFreeTrackCal
###########################################################################
# Input:     mapname - name of the map (filename without extension)
#            mapext  - extension of the saved map picture
#            c_type  - coordinate type
#            ll_n    - N coordinate of the lower left corner
#            ll_e    - E coordinate of the lower left corner
#            ur_n    - N coordinate of the upper right corner
#            ur_e    - E coordinate of the upper right corner
#            picx    - width of the map picture in pixels
#            picy    - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################

def SaveFreeTrackCal(mapname, mapext, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):
  RATIO = float(ur_e-ll_e) / float(picx)

  try:
    f = open(mapname + mapext + '.cal', 'w')
  except:
    print "ERROR: Cannot open .cal file: " + mapname + mapext + ".cal"
    return 0

  outlines = []

  outlines.append('title = ' + mapname + '\n')
  outlines.append('description = ' + mapname + '\n')

  # determine 4 points on the map to calibrate
  #
  # formula to determine xy-coordinates for a given point (x,y) in the
  # map image if the coordinates of the center of the lower left corner 
  # pixel are (N,E)=(ll_n, ll_e)
  # (N) ppy = ll_n + (picy - y - 0.5) * RATIO
  # (E) ppx = ll_e + (x + 0.5) * RATIO
  i = 0
  while (i < 4):
    y = int(round((int(math.floor(i / 2)) + 1) * (picy / 3.0)))
    x = int(round(((i % 2) + 1) * (picx / 3.0)))
    ppy = ll_n + (picy - y - 0.5) * RATIO
    ppx = ll_e + (x + 0.5) * RATIO
    WGS = coordinates.Translate( {'type': c_type, 'N': ppy, 'E': ppx}, coordinates.COORD_TYPE_WGS84 )

    outlines.append('point%i = ' % (i+1, ))
    outlines.append('%i,%i %f,%f\n' % (x, y, WGS['N'], WGS['E']))

    i = i + 1
    
  outlines.append('version = 1.2.0\n')
  
  try:
    f.writelines(outlines)
    f.close()
  except:
    print "ERROR: Cannot write .cal file: " + mapname + mapext + ".cal"
    return 0

  print "Saved FreeTrack CAL file to " + mapname + mapext + ".cal"
  return 1


###########################################################################
# Function:  SaveKMZCal, SaveKMZCal2_2
###########################################################################
# Input:     im      - result image object
#            mapname - name of the map (filename without extension)
#            mapext  - extension of the saved map picture
#            c_type  - coordinate type
#            ll_n    - N coordinate of the lower left corner
#            ll_e    - E coordinate of the lower left corner
#            ur_n    - N coordinate of the upper right corner
#            ur_e    - E coordinate of the upper right corner
#            picx    - widht of the map picture in pixels
#            picy    - height of the map picture in pixels
# Output:    1 - file saved ok
#            0 - errors in saving the file
###########################################################################
KMZ_TILE_SIZE = 1000
def RotateLocation(point, center, angle):
    dE = point['E'] - center['E']
    dN = point['N'] - center['N']
    si = math.sin( math.radians(angle) )
    co = math.cos( math.radians(angle) )
    nE = dE * co - dN * si
    nN = dN * co + dE * si
    return {'type': point['type'], 'E': center['E'] + nE, 'N': center['N'] + nN}

def toWGSLaLo(point):
    temppoint = point
    if temppoint['type'] != coordinates.COORD_TYPE_WGS84:
        temppoint = coordinates.Translate(temppoint, coordinates.COORD_TYPE_WGS84)
    return {'La': temppoint['N'], 'Lo': temppoint['E']}

def SaveKMZCal(im, mapname, mapext, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):
    XRATIO = float(ur_e-ll_e) / float(picx)
    YRATIO = float(ur_n-ll_n) / float(picy)

    try:
        zf = zipfile.ZipFile(mapname + '.kmz', 'w')
    except:
        print "ERROR: Cannot open .kmz file: " + mapname + ".kmz"
        return 0

    kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml = kml + '<kml xmlns="http://www.opengis.net/kml/2.2" '
    kml = kml + 'xmlns:gx="http://www.google.com/kml/ext/2.2" '
    kml = kml + 'xmlns:kml="http://www.opengis.net/kml/2.2" '
    kml = kml + 'xmlns:atom="http://www.w3.org/2005/Atom">\n'
    kml = kml + '<Folder>\n'
    kml = kml + '  <name>' + mapname + '</name>\n'

    j = 1
    y = 0
    while y < picy:
        sy = KMZ_TILE_SIZE
        if picy - y < sy:
            sy = picy - y

        i = 1
        x = 0
        while x < picx:
            sx = KMZ_TILE_SIZE
            if picx - x < sx:
                sx = picx - x

            ifname = mapname + "_%d_%d" % (i, j)

            cropbox = ( x, picy - sy - y, x + sx, picy - y)
            strio = StringIO.StringIO()
            im.crop(cropbox).save(strio, 'jpeg')
            zf.writestr('files' + os.path.sep + ifname + '.jpg', strio.getvalue())
            strio.close()

            pll_e = ll_e + x * XRATIO
            pll_n = ll_n + y * YRATIO
            pur_e = pll_e + sx * XRATIO
            pur_n = pll_n + sy * YRATIO

            pLL = {'type': c_type, 'N': pll_n, 'E': pll_e}
            pLR = {'type': c_type, 'N': pll_n, 'E': pur_e}
            pUR = {'type': c_type, 'N': pur_n, 'E': pur_e}
            pUL = {'type': c_type, 'N': pur_n, 'E': pll_e}
            pN = {'type': c_type, 'N': pur_n, 'E': (pll_e + pur_e) / 2.0}
            pS = {'type': c_type, 'N': pll_n, 'E': (pll_e + pur_e) / 2.0}
            pW = {'type': c_type, 'N': (pll_n + pur_n) / 2.0, 'E': pll_e}
            pE = {'type': c_type, 'N': (pll_n + pur_n) / 2.0, 'E': pur_e}
            pC = {'type': c_type, 'N': (pur_n + pll_n) / 2.0, 'E': (pur_e + pll_e) / 2.0}
            
            wgsN = toWGSLaLo(pN)
            wgsS = toWGSLaLo(pS)
            wgsW = toWGSLaLo(pW) 
            wgsE = toWGSLaLo(pE)
            wgsC = toWGSLaLo(pC)
            
            rotation = 0.0
            rotation = rotation + (0.0 - coordinates.WGS84bearing(wgsC, wgsN)[1]) % 360.0
            rotation = rotation + (90.0 - coordinates.WGS84bearing(wgsC, wgsE)[1]) % 360.0
            rotation = rotation + (180.0 - coordinates.WGS84bearing(wgsC, wgsS)[1]) % 360.0
            rotation = rotation + (-90.0 - coordinates.WGS84bearing(wgsC, wgsW)[1]) % 360.0
            rotation = rotation / 4.0

            rpUR = RotateLocation(pUR, pC, -rotation)
            rpLR = RotateLocation(pLR, pC, -rotation)
            rpLL = RotateLocation(pLL, pC, -rotation)
            rpUL = RotateLocation(pUL, pC, -rotation)

            rwgsUR = coordinates.Translate(rpUR, coordinates.COORD_TYPE_WGS84)
            rwgsLR = coordinates.Translate(rpLR, coordinates.COORD_TYPE_WGS84)
            rwgsLL = coordinates.Translate(rpLL, coordinates.COORD_TYPE_WGS84)
            rwgsUL = coordinates.Translate(rpUL, coordinates.COORD_TYPE_WGS84)

            north = max(rwgsUL['N'], rwgsUR['N'])
            south = min(rwgsLL['N'], rwgsLR['N'])
            west = min(rwgsLL['E'], rwgsUL['E'])
            east = max(rwgsLR['E'], rwgsUR['E'])

            kml = kml + '    <GroundOverlay>\n'
            kml = kml + '      <name>' + ifname + '</name>\n'
            kml = kml + '      <drawOrder>50</drawOrder>\n'
            kml = kml + '      <Icon>\n'
            kml = kml + '        <href>files/' + ifname + '.jpg</href>\n'
            kml = kml + '      </Icon>\n'
            kml = kml + '      <LatLonBox>\n'
            kml = kml + "        <north>%f</north>\n" % north
            kml = kml + "        <south>%f</south>\n" % south
            kml = kml + "        <east>%f</east>\n" % east
            kml = kml + "        <west>%f</west>\n" % west
            kml = kml + "        <rotation>%f</rotation>\n" % rotation
            kml = kml + '      </LatLonBox>\n'
            kml = kml + '    </GroundOverlay>\n'

            i = i + 1
            x = x + sx
            
        j = j + 1
        y = y + sy

    kml = kml + '</Folder>\n</kml>\n'

    zf.writestr('doc.kml', kml)
    zf.close()

    print "Saved KMZ archive file to " + mapname + ".kmz"
    return 1

# KML version 2.2
def SaveKMZCal2_2(im, mapname, mapext, c_type, ll_n, ll_e, ur_n, ur_e, picx, picy):
    XRATIO = float(ur_e-ll_e) / float(picx)
    YRATIO = float(ur_n-ll_n) / float(picy)

    try:
        zf = zipfile.ZipFile(mapname + '.kmz', 'w')
    except:
        print "ERROR: Cannot open .kmz file: " + mapname + ".kmz"
        return 0

    kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml = kml + '<kml xmlns="http://www.opengis.net/kml/2.2" '
    kml = kml + 'xmlns:gx="http://www.google.com/kml/ext/2.2" '
    kml = kml + 'xmlns:kml="http://www.opengis.net/kml/2.2" '
    kml = kml + 'xmlns:atom="http://www.w3.org/2005/Atom">\n'
    kml = kml + '<Folder>\n'
    kml = kml + '  <name>' + mapname + '</name>\n'

    j = 1
    y = 0
    while y < picy:
        sy = KMZ_TILE_SIZE
        if picy - y < sy:
            sy = picy - y

        i = 1
        x = 0
        while x < picx:
            sx = KMZ_TILE_SIZE
            if picx - x < sx:
                sx = picx - x

            ifname = mapname + "_%d_%d" % (i, j)

            cropbox = ( x, picy - sy - y, x + sx, picy - y)
            strio = StringIO.StringIO()
            im.crop(cropbox).save(strio, 'jpeg')
            zf.writestr('files' + os.path.sep + ifname + '.jpg', strio.getvalue())
            strio.close()

            pll_e = ll_e + x * XRATIO
            pll_n = ll_n + y * YRATIO
            pur_e = pll_e + sx * XRATIO
            pur_n = pll_n + sy * YRATIO

            WGSll = coordinates.Translate( {'type': c_type, 'N': pll_n, 'E': pll_e}, coordinates.COORD_TYPE_WGS84)
            WGSlr = coordinates.Translate( {'type': c_type, 'N': pll_n, 'E': pur_e}, coordinates.COORD_TYPE_WGS84)
            WGSul = coordinates.Translate( {'type': c_type, 'N': pur_n, 'E': pll_e}, coordinates.COORD_TYPE_WGS84)
            WGSur = coordinates.Translate( {'type': c_type, 'N': pur_n, 'E': pur_e}, coordinates.COORD_TYPE_WGS84)

            kml = kml + '    <GroundOverlay>\n'
            kml = kml + '      <name>' + ifname + '</name>\n'
            kml = kml + '      <drawOrder>50</drawOrder>\n'
            kml = kml + '      <Icon>\n'
            kml = kml + '        <href>files/' + ifname + '.jpg</href>\n'
            kml = kml + '      </Icon>\n'
            kml = kml + '      <gx:LatLonQuad>\n'
            kml = kml + '        <coordinates>\n'
            kml = kml + '         '
            kml = kml + " %(E)f,%(N)f" % WGSll
            kml = kml + " %(E)f,%(N)f" % WGSlr
            kml = kml + " %(E)f,%(N)f" % WGSur
            kml = kml + " %(E)f,%(N)f" % WGSul
            kml = kml + '\n'
            kml = kml + '        </coordinates>\n'
            kml = kml + '      </gx:LatLonQuad>\n'
            kml = kml + '    </GroundOverlay>\n'

            i = i + 1
            x = x + sx
            
        j = j + 1
        y = y + sy

    kml = kml + '</Folder>\n</kml>\n'

    zf.writestr('doc.kml', kml)
    zf.close()

    print "Saved KMZ archive file to " + mapname + ".kmz"
    return 1
###########################################################################

if __name__ == "__main__":
  main()

