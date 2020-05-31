#! python
# -*- coding: iso-8859-1 -*-
###########################################################################
# 
# File:            fms_rka.py
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
# Description:     Map service class for Retkikartta.fi.
#
# Requirements:    Python interpreter 2.4 or newer (www.python.org)
#                  (tested with 2.4.1)
# 
#                  Python Imaging Library (tested with 1.1.5) 
#                  (www.pythonware.org/products/pil/)
#
# Version history: ** 18.02.2009 v3.0a (Olli Lammi) **
#                  First implementation.
#
#                  ** 19.02.2009 v3.0b (Olli Lammi) **
#                  Changes to the map construction mathematics and calibration.
#
#                  ** 23.03.2009 v3.0d (Olli Lammi) **
#                  Small change to service code.
#
#                  ** 26.03.2009 v3.0e (Olli Lammi) **
#                  Small change to service code.
#
#                  ** 27.09.2010 v3.0j (Olli Lammi) **
#                  Support for changed Retkikartta.fi platform.
#
#                  ** 03.11.2010 v3.0k (Olli Lammi) **
#                  Changed scale names to match scale name
#                  changes in the Retkikartta.fi.
#
#                  ** 30.01.2012 v3.1a (Olli Lammi) **
#                  Layer support.
#
#                  ** 20.02.2012 v3.1g (Olli Lammi) **
#                  Changes to FetchPic interface. Corrections
#                  to layer interface.
#
#                  ** 22.02.2012 v3.1h (Olli Lammi) **
#                  Corrections to a gross mistake in cache directory naming.
#
#                  ** 23.02.2012 v3.1i (Olli Lammi) **
#                  Improved error handling in layer loading.
#
###########################################################################

# Imports

import sys, os, string
import math, re, os.path
import time, random
import tempfile, shutil

import urllib2

from PIL import Image  # Python Imaging Library 
                       # (http://www.pythonware.com/products/pil/)

import coordinates  # KKJ to and from WGS84 coordinate transforms

import fms

###########################################################################

# Constants

MOD_VERSION = 'v3.1i'
SERVICE_CODE = 'rka'

# constants for the picture and distance sizes and ratios
PIC_ORIG_SIZEX = 256
PIC_ORIG_SIZEY = 256
PIC_SIZEX = PIC_ORIG_SIZEX
PIC_SIZEY = PIC_ORIG_SIZEY

PIC_SCALES = { '1:5000': [5000, 1.411246], \
               '1:8000': [8000, 2.116577], \
               '1:16000': [16000, 4.234905], \
               '1:25000': [25000, 6.614597], \
               '1:50000': [50000, 13.229193], \
               '1:100000': [100000, 26.458386], \
               '1:500000': [500000, 132.291931], \
               '1:1000000': [1000000, 264.639239], \
               '1:3000000': [3000000, 794.034895] }

PIC_SCALE_DEFAULT = '1:16000'

LAYERS = { 'kesareitit': ['Kesäretkeilyreitit', 'retkikartta:kesaretkeilyreitit', 1.0], \
           'luontopolut': ['Luontopolut', 'retkikartta:luontopolut', 1.0], \
           'pyorailyreitit': ['Pyöräilyreitit', 'retkikartta:pyorailyreitit', 1.0], \
           'ladut': ['Ladut ja talviretkeilyreitit', 'retkikartta:ladutjatalviretkeilyreitit', 1.0], \
           'pyoratuolireitit': ['Pyörätuolireitit', 'retkikartta:pyoratuolireitit', 1.0], \
           'moottorikelkkareitit': ['Moottorikelkkailureitit ja -urat', 'retkikartta:moottorikelkkailureititjaurat', 1.0], \
           'kuntoradat': ['Kuntoradat', 'retkikartta:kuntoradat', 1.0], \
           'veneilyreitit': ['Veneily- ja vesiretkeilyreitit', 'retkikartta:veneilyjavesiretkeilyreitit', 1.0], \
           'pyydyslupa': ['Pyydyslupakohteet', 'retkikartta:pyydyslupakohteet', 0.7], \
           'viehekalastus': ['Viehekalastuskohteet', 'retkikartta:viehekalastuskohteet', 0.7], \
           'virkistyskalastus': ['Virkistyskalastuskohteet', 'retkikartta:virkistyskalastuskohteet', 0.7], \
           'pienriista': ['Pienriistan metsästysalueet', 'retkikartta:pienriista', 0.3], \
           'hirvialue': ['Hirvialueet', 'retkikartta:hirvialueet', 0.3], \
           'yleinenvesialue': ['Yleiset vesialueet', 'retkikartta:yleisetvesialueet', 0.3], \
           'kansallispuisto': ['Kansallispuistot', 'retkikartta:kansallispuistot', 0.3], \
           'suojelualue': ['Muut suojelualueet', 'retkikartta:muutsuojelualueet', 0.3], \
           'retkeilyalue': ['Retkeilyalueet', 'retkikartta:retkeilyalueet', 0.3], \
           'lapineramaa': ['Lapin erämaa-alueet', 'retkikartta:eramaaalueet', 0.3], \
           'muualue': ['Muut alueet', 'retkikartta:muutalueet', 0.3], \
           'kunnat': ['Kunnat', 'retkikartta:kunnat_view', 1.0] \
         }


###########################################################################

# Classes

class FMSRetkikarttaFi(fms.FetchMapService):
    def __init__(self):
        self.SERVICE_CODE = SERVICE_CODE
          
        self.PIC_SCALE_DEFAULT = PIC_SCALE_DEFAULT
        self.SetScale(self.PIC_SCALE_DEFAULT)
     
    
    ###########################################################################
    # Function:    GetVersion
    ###########################################################################
    # Description: Returns the module version string. 
    ###########################################################################    
    def GetVersion(self):
        return MOD_VERSION
    
    
    ###########################################################################
    # Function:    HandleParameter
    ###########################################################################
    # Description: Handles command line parameter. Returns 0, if the parameter
    #              was invalid. Returns 1 if the parameter was ok. 
    ###########################################################################  
    def HandleParameter(self, param):    
        return 0


    ###########################################################################
    # Function:    SetScale
    ###########################################################################
    # Description: Initializes the service and values to retrieve map parts
    #              in given scale. The parameter must be one of the values
    #              returned by GetScales.
    ###########################################################################
    def SetScale(self, scale):
        # determine picture scale and ratio
        try:
            self.PIC_SIZEX = PIC_SIZEX
            self.PIC_SIZEY = PIC_SIZEY
            self.SCALE = scale
            self.SCALEVAL = PIC_SCALES[scale][0]
            self.PIC_RATIO = PIC_SCALES[scale][1]
            self.MAP_SIZEX = self.PIC_SIZEX * self.PIC_RATIO
            self.MAP_SIZEY = self.PIC_SIZEY * self.PIC_RATIO
        except:
            return 0
        return 1


    ###########################################################################
    # Function:    GetScales
    ###########################################################################
    # Description: Returns list of scales that the service supports
    ###########################################################################    
    def GetScales(self):
        scales = []
        for sc in PIC_SCALES.keys():
            scales.append([PIC_SCALES[sc], sc])
        scales.sort()
        scales2 = []
        for sc in scales:
            scales2.append(sc[1])
        return scales2
    
    
    ###########################################################################
    # Function:    GetPicIndexes
    ###########################################################################
    # Description: Returns two (x,y) tuples with indexes for map image that has
    #              the given (mapx, mapy) point and the lower left xy
    #              coordinates of the indexed map picture.
    ###########################################################################
    def GetPicIndexes(self, mapx, mapy):
        # calculate the tile column and row
        indx = int((mapx + (0.25 * self.PIC_RATIO)) / (self.PIC_RATIO * PIC_ORIG_SIZEX))
        indy = int((mapy + (0.25 * self.PIC_RATIO)) / (self.PIC_RATIO * PIC_ORIG_SIZEY))
        fetchx = self.PIC_RATIO * indx * PIC_ORIG_SIZEX
        fetchy = self.PIC_RATIO * indy * PIC_ORIG_SIZEY
        
        return ((indx, indy), (fetchx, fetchy))

    
    ###########################################################################
    # Method:      FetchPic
    ###########################################################################
    # Description: Fetches one map tile from Retkikartta.fi.
    #              Result file will saved in cachedir. Tempdir is used as temp directory  
    #              while downloading.
    ###########################################################################

    def FetchPic(self, fetchr, fetchc, cachedir, tempdir, layer):
        fname = cachedir + self.GetCacheName(fetchc, fetchr, layer)
        
        oldfnames = [cachedir + self.GetCacheName_pre_v31g(fetchc, fetchr, layer), \
                     cachedir + self.GetCacheName_v31g(fetchc, fetchr, layer) ]        
        # if there exists an old cache file for this position, use it
        # and move to new location
        for oldfname in oldfnames:
            if os.path.exists(oldfname):
                try:
                    dname = os.path.dirname(fname)
                    if not os.path.isdir(dname):
                        try:
                            os.makedirs(dname)
                        except:
                            pass
                    shutil.move(oldfname, fname)
                    tempdname = os.path.dirname(oldfname)
                    if os.path.isdir(tempdname) and len(os.listdir(tempdname)) <= 0:
                        try:
                            os.rmdir(tempdname)
                        except:
                            pass                
                    return 2 
                except:
                    pass
        
        tempfname = None
        if len(layer) > 0:
            tempfname = self.FetchPicLayer(fetchr, fetchc, tempdir, layer)
        else:            
            waitsize_x = PIC_ORIG_SIZEX
            waitsize_y = PIC_ORIG_SIZEY        
            url = 'http://ntile1.navici.com/t/retkikartta/maps/2393x' + str(self.PIC_RATIO) + 'x' + str(fetchc) + 'x' + str(fetchr) + '.png'
    
            USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4"
      
            res = ''
            try:
              req = urllib2.Request(url)
              req.add_header("User-Agent", USERAGENT)
      
              f = urllib2.urlopen(req)
              res = f.read()
              f.close()
            except:
              return 0
       
            tempfname = ''
            # create a temporary file name for the map
            try:
                (tempfd, tempfname) = tempfile.mkstemp('.png', 'tmpmap_', tempdir)
                os.close(tempfd)
            except:
                print 'ERROR: Cannot create temporary file for map image file'
                return 0
    
            try:
                f = open(tempfname,'wb')
                f.write(res)
                f.close()
            except:
                print "ERROR: Cannot write temporary map image file: " + tempfname
                return 0
        
            try:
                im = Image.open(tempfname)
                im.load()
        
                if im.size[0] != waitsize_x or im.size[1] != waitsize_y:
                    print 'ERROR: Retrieved image is of invalid size (received: ' + `im.size[0]` + 'x' + `im.size[1]` + ', expected: ' + `waitsize_x` + 'x' + `waitsize_y` + ')'
                    try:
                        os.unlink(tempfname)
                    except:
                        pass
                    return 0 
                        
                im.save(tempfname)
            except Exception, e:
                print "ERROR: Cannot convert map image or rewrite temporary map image file: " + tempfname
                print e.__str__()
                try:
                    os.unlink(tempfname)
                except:
                    pass
                return 0

        if tempfname == None:
            return 0
 
        # check if the map cache hash directory is created
        dname = os.path.dirname(fname)
        if not os.path.isdir(dname):
            try:
                os.makedirs(dname)
            except:
                print 'ERROR: Cannot create map image directory: ' + dname
                try:
                    os.unlink(tempfname)
                except:
                    pass
                return 0
    
        # move the temporary map file to the cache
        try:
            shutil.move(tempfname, fname)  
        except:
            print 'ERROR: Cannot move loaded temporary map image to map cache.'
            try:
                os.unlink(tempfname)
            except:
                pass
            return 0
  
        return 1


    def FetchPicLayer(self, fetchr, fetchc, tempdir, layer):
        LAYER_PIC_SIZES = [ (PIC_ORIG_SIZEX, PIC_ORIG_SIZEY), \
                            (3 * PIC_ORIG_SIZEX, 3 * PIC_ORIG_SIZEY), \
                            (5 * PIC_ORIG_SIZEX, 5 * PIC_ORIG_SIZEY), \
                            (7 * PIC_ORIG_SIZEX, 7 * PIC_ORIG_SIZEY) ]

        for lps in LAYER_PIC_SIZES:                    
            waitsize_x = lps[0]
            waitsize_y = lps[1]

            margin_x = (waitsize_x - PIC_ORIG_SIZEX) / 2.0
            margin_y = (waitsize_y - PIC_ORIG_SIZEY) / 2.0
            cropbox = (int(margin_x), int(margin_y), int(margin_x) + PIC_ORIG_SIZEX, int(margin_y) + PIC_ORIG_SIZEY)

            fetchx_ll = self.PIC_RATIO * fetchc * PIC_ORIG_SIZEX
            fetchy_ll = self.PIC_RATIO * fetchr * PIC_ORIG_SIZEY
            fetchx_ll = fetchx_ll - self.PIC_RATIO * margin_x
            fetchy_ll = fetchy_ll - self.PIC_RATIO * margin_y
            fetchx_ur = fetchx_ll + self.PIC_RATIO * waitsize_x
            fetchy_ur = fetchy_ll + self.PIC_RATIO * waitsize_y
            
            url = 'http://wms1.navici.com/wms/a9e9a1840ee69e32d59af86dd1ffeb44?'
            url = url + 'LAYERS=' + urllib2.quote(LAYERS[layer][1])
            url = url + '&STYLES=&TRANSPARENT=true&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap'
            url = url + '&FORMAT=image%2Fpng&SRS=EPSG%3A2393'
            url = url + '&BBOX=%f,%f,%f,%f' % (fetchx_ll, fetchy_ll, fetchx_ur, fetchy_ur)
            url = url + '&WIDTH=%d&HEIGHT=%d' % (waitsize_x, waitsize_y)
    
            USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4"
      
            res = ''
            try:
                req = urllib2.Request(url)
                req.add_header("User-Agent", USERAGENT)
      
                f = urllib2.urlopen(req)
                res = f.read()
                f.close()
            except:
                continue
       
            tempfname = ''
            # create a temporary file name for the map
            try:
                (tempfd, tempfname) = tempfile.mkstemp('.png', 'tmpmap_', tempdir)
                os.close(tempfd)
            except:
                print 'ERROR: Cannot create temporary file for map image file'
                return None
    
            try:
                f = open(tempfname,'wb')
                f.write(res)
                f.close()
            except:
                print "ERROR: Cannot write temporary map image file: " + tempfname
                return None
        
            try:
                im = Image.open(tempfname)
                im.load()
        
                if im.size[0] != waitsize_x or im.size[1] != waitsize_y:
                    print 'ERROR: Retrieved image is of invalid size (received: ' + `im.size[0]` + 'x' + `im.size[1]` + ', expected: ' + `waitsize_x` + 'x' + `waitsize_y` + ')'
                    try:
                        os.unlink(tempfname)
                    except:
                        pass
                    tempfname = None
                    continue
    
                im = im.crop(cropbox)    
                im.save(tempfname)
            except Exception, e:
                try:
                    os.unlink(tempfname)
                except:
                    pass
                tempfname = None
                continue
            
            break
            
        if tempfname == None:
            print "ERROR: Cannot fetch map layer image."
        return tempfname
 
         
         
    ###########################################################################
    # Method:    GetCacheName
    ###########################################################################
    # Description: Generates a name for the map image in cache according to
    #              location and other parameters.
    ###########################################################################
    def GetCacheName(self, x, y, layer):
        fname = `self.SCALEVAL` + '_' + `int(self.PIC_SIZEX)` + '_' + `int(self.PIC_SIZEY)`
  
        if len(layer) > 0:
            fname = fname + '_' + layer
  
        fetchx_ll = self.PIC_RATIO * x * PIC_ORIG_SIZEX
        fetchy_ll = self.PIC_RATIO * y * PIC_ORIG_SIZEY
        hashy = int(round(fetchy_ll)) 
        hashx = int(round(fetchx_ll))
        hash = `HashRound(hashy)` + '_' + `HashRound(hashx)`
        fname = fname + '/' + hash
  
        fname = fname + '/map_' + self.SERVICE_CODE + '_' + `self.SCALEVAL`  
        
        fname = fname + '_'+ repr(int(round(y))) + '_' + repr(int(round(x))) + '.png'

        return fname

    # hack function to "support" old invalid cache directory names of v3.1g
    def GetCacheName_v31g(self, x, y, layer):
        fname = `self.SCALEVAL` + '_' + `int(self.PIC_SIZEX)` + '_' + `int(self.PIC_SIZEY)`
  
        if len(layer) > 0:
            fname = fname + '_' + layer
  
        # calculate location hash
        # convert to zone 3
        xy = coordinates.KKJxy_ZoneShift( {'P': y, 'I': x}, 3 )
        hashy = int(round(xy['P'])) 
        hashx = int(round(xy['I']))
        hash = `HashRound(hashy)` + '_' + `HashRound(hashx)`
        fname = fname + '/' + hash
  
        fname = fname + '/map_' + self.SERVICE_CODE + '_' + `self.SCALEVAL`  
        
        fname = fname + '_'+ repr(int(round(y))) + '_' + repr(int(round(x))) + '.png'

        return fname

    # hack function to "support" old invalid cache directory names prior to v3.1g
    def GetCacheName_pre_v31g(self, x, y, layer):
        fname = `self.SCALEVAL` + '_' + `int(self.PIC_SIZEX)` + '_' + `int(self.PIC_SIZEY)`
  
        if len(layer) > 0:
            fname = fname + '_' + layer
  
        # calculate location hash
        # convert to zone 3
        xy = pre_v31g_KKJxy_ZoneShift( {'P': y, 'I': x}, 3 )
        hashy = int(round(xy['P'])) 
        hashx = int(round(xy['I']))
        hash = `HashRound(hashy)` + '_' + `HashRound(hashx)`
        fname = fname + '/' + hash
  
        fname = fname + '/map_' + self.SERVICE_CODE + '_' + `self.SCALEVAL`  
        
        fname = fname + '_'+ repr(int(round(y))) + '_' + repr(int(round(x))) + '.png'

        return fname


    ###########################################################################
    # Method:      PostProcess
    ###########################################################################
    # Description: Post processes the entire constructed map image according
    #              to service requirements.
    ###########################################################################    
    def PostProcess(self, im):
        pass


    ###########################################################################
    # Method:      TranslateToServiceCoordinatesXY
    ###########################################################################
    # Description: Does service require coordinates to be transferred to YKJ?
    #              Returns: tuple (type, x, y) where
    #              type - type string of the coordinate system
    #              x - easting or lon coordinate 
    #              y - northing or lat coordinate
    ###########################################################################       
    def TranslateToServiceCoordinatesXY(self, type, x, y):
        if (type != coordinates.COORD_TYPE_YKJ):
            temp = coordinates.Translate({'type': type, 'N': y, 'E': x}, \
                                         coordinates.COORD_TYPE_YKJ)
            return (temp['type'], temp['E'], temp['N'])
        return (type, x, y)

    
    ###########################################################################
    # Method:      GetHelp
    ###########################################################################
    # Description: Get service module specific help string.
    ###########################################################################    
    def GetHelp(self):
        return HELP_TEXT


    ###########################################################################
    # Method:      GetServiceDelayLimits
    ###########################################################################
    # Description: Get service specific delay times as tuple (min, max) in sec.
    ###########################################################################               
    def GetServiceDelayLimits(self):
        return (2, 6)
        
    ###########################################################################
    # Method:      GetAvailableLayers
    ###########################################################################
    # Description: Get dict of available layer names. 
    ###########################################################################               
    def GetAvailableLayers(self):
        tempd = {}
        for layer in LAYERS.keys():
            tempd[layer] = [LAYERS[layer][0], LAYERS[layer][2]]
        return tempd

        
###########################################################################

# Functions

def HashRound(x):
    return ((x / 10000) / 5) * 5 


###########################################################################
# Old coordinate functions to support cache name hash hack functions.
###########################################################################

pre_v31g_KKJ_ZONE_INFO = { 0: (18.0,  500000.0), \
                  1: (21.0, 1500000.0), \
                  2: (24.0, 2500000.0), \
                  3: (27.0, 3500000.0), \
                  4: (30.0, 4500000.0), \
                  5: (33.0, 5500000.0), \
                }

def pre_v31g_KKJxy_to_KKJlalo(KKJ, zone = None):  
  #
  # Scan iteratively the target area, until find matching
  # KKJ coordinate value.  Area is defined with Hayford Ellipsoid.
  #  
  LALO = {}

  ZoneNumber = zone
  if ZoneNumber == None:
      ZoneNumber = pre_v31g_KKJ_Zone_I(KKJ['I'])
    
  MinLa = math.radians(59.0)
  MaxLa = math.radians(70.5)
  MinLo = math.radians(16.0)
  MaxLo = math.radians(35.5)

  i = 1
  while (i < 35):
    DeltaLa = MaxLa - MinLa
    DeltaLo = MaxLo - MinLo

    LALO['La'] = math.degrees(MinLa + 0.5 * DeltaLa)
    LALO['Lo'] = math.degrees(MinLo + 0.5 * DeltaLo)

    KKJt = pre_v31g_KKJlalo_to_KKJxy(LALO, ZoneNumber)

    if (KKJt['P'] < KKJ['P']):
      MinLa = MinLa + 0.45 * DeltaLa
    else:
      MaxLa = MinLa + 0.55 * DeltaLa

    if (KKJt['I'] < KKJ['I']):
      MinLo = MinLo + 0.45 * DeltaLo
    else:
      MaxLo = MinLo + 0.55 * DeltaLo

    i = i + 1

  return LALO

def pre_v31g_KKJlalo_to_KKJxy(INP, ZoneNumber):
  Lo = math.radians(INP['Lo']) - math.radians(pre_v31g_KKJ_ZONE_INFO[ZoneNumber][0])

  a  = 6378388.0            # Hayford ellipsoid
  f  = 1/297.0

  b  = (1.0 - f) * a
  bb = b * b              
  c  = (a / b) * a        
  ee = (a * a - bb) / bb  
  n = (a - b)/(a + b)     
  nn = n * n              
  cosLa = math.cos(math.radians(INP['La']))
  NN = ee * cosLa * cosLa 
  LaF = math.atan(math.tan(math.radians(INP['La'])) / math.cos(Lo * math.sqrt(1 + NN)))
  cosLaF = math.cos(LaF)
  t   = (math.tan(Lo) * cosLaF) / math.sqrt(1 + ee * cosLaF * cosLaF)
  A   = a / ( 1 + n )
  A1  = A * (1 + nn / 4 + nn * nn / 64)
  A2  = A * 1.5 * n * (1 - nn / 8)
  A3  = A * 0.9375 * nn * (1 - nn / 4)
  A4  = A * 35/48.0 * nn * n

  OUT = {}
  OUT['P'] = A1 * LaF - \
        A2 * math.sin(2 * LaF) + \
            A3 * math.sin(4 * LaF) - \
                A4 * math.sin(6 * LaF)
  OUT['I'] = c * math.log(t + math.sqrt(1+t*t)) + \
        500000.0 + ZoneNumber * 1000000.0

  return OUT

def pre_v31g_KKJ_Zone_I(KKJI):
  ZoneNumber = math.floor((KKJI/1000000.0))
  if ZoneNumber < 0 or ZoneNumber > 5:
      ZoneNumber = -1
      
  return ZoneNumber

def pre_v31g_KKJxy_ZoneShift(KKJ, zone):
  kkjlalo = pre_v31g_KKJxy_to_KKJlalo(KKJ)
  return pre_v31g_KKJlalo_to_KKJxy(kkjlalo, zone)  

