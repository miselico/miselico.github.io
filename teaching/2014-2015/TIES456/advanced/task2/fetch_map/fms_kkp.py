#! python
# -*- coding: iso-8859-1 -*-
###########################################################################
# 
# File:            fms_kkp.py
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
# Module options:      --orto    - Fetch airplane pictures from Karttapaikka 
#                                  (experimental, not fully tested.)
#
#                      --ktjraja - Add real estate border lines (Kiinteistörajat) 
#                                  from Karttapaikka 
#                                  (experimental, not fully tested.)
"""
#
# Author:          Olli Lammi (olammi@iki.fi)
#
# Version:         3.1g
#
# Date:            20.02.2012
#
# Functions:       -
#                   
# Description:     Map service class for Kansalaisen Karttapaikka.
#
# Requirements:    Python interpreter 2.4 or newer (www.python.org)
#                  (tested with 2.4.1)
# 
#                  Python Imaging Library (tested with 1.1.5) 
#                  (www.pythonware.org/products/pil/)
#
# Version history: ** 18.02.2009 v3.0a (Olli Lammi) **
#                  First service class implementation. Taken off the main
#                  program. 
#
#                  ** 19.02.2009 v3.0b (Olli Lammi) **
#                  Changes to the map construction mathematics and calibration.
#
#                  ** 01.03.2009 v3.0c (Olli Lammi) **
#                  Added check for the actual coordinates returned from the 
#                  service. In some rare cases the service returns different 
#                  area that was requested.
#
#                  ** 17.06.2009 v3.0f (Olli Lammi) **
#                  Added support for 1:8000000 scale. Removed 1:12000000
#                  scale, as it was no longer supported. Corrected the
#                  code about cropping the returned map image when
#                  the returned area is not the same as requested.
#
#                  ** 10.02.2010 v3.0h (Olli Lammi) **
#                  Karttapaikka changed the native coordinate system
#                  to ETRS-TM35FIN. Changed the module to support
#                  this.
#
#                  ** 27.09.2010 v3.0j (Olli Lammi) **
#                  Minor changes in the interfaces.
#
#                  ** 10.04.2011 v3.0l (Olli Lammi) **
#                  Added ktjraja parameter and support for kiinteistö-
#                  rajat.
#
#                  ** 20.02.2012 v3.1g (Olli Lammi) **
#                  FetchPic interface changes.
#
###########################################################################

# Imports

import sys, os, string
import math, re, os.path
import time, random
import tempfile, shutil

import urllib2
import cookielib

from PIL import Image  # Python Imaging Library 
                       # (http://www.pythonware.com/products/pil/)

import coordinates  # coordinate transforms

import fms

###########################################################################

# Constants

MOD_VERSION = 'v3.1g'
SERVICE_CODE = 'kkp'

# possible watermark mask picture in the cache directory
WATERMARK_PIC = 'lib/kkp_wm2.png'

# constants for the picture and distance sizes and ratios
PIC_ORIG_SIZEX = 600
PIC_ORIG_SIZEY = 600
CROPBOX = (0, 20, PIC_ORIG_SIZEX, PIC_ORIG_SIZEY-35)
PIC_SIZEX = PIC_ORIG_SIZEX
PIC_SIZEY = PIC_ORIG_SIZEY - 20 - 35 

PIC_SCALES = { '1:2000': [2000, 0.5], \
               '1:4000': [4000, 1.0], \
               '1:8000': [8000, 2.0], \
               '1:16000': [16000, 4.0], \
               '1:40000': [40000, 10.0], \
               '1:80000': [80000, 20.0],\
               '1:200000': [200000, 50.0],\
               '1:400000': [400000, 100.0],\
               '1:800000': [800000, 200.0],\
               '1:2000000': [2000000, 500.0],\
               '1:4000000': [4000000, 1000.0],\
               '1:8000000': [8000000, 2000.0] }
PIC_SCALE_DEFAULT = '1:16000'

EMPTY_BACKGROUND_COLOR = (255, 255, 128)

###########################################################################

# Classes

class FMSKansalaisenKarttapaikka(fms.FetchMapService):
    def __init__(self):
        self.SERVICE_CODE = SERVICE_CODE
        self.ORTO = 0 
        self.NOWM = 0
        self.KTJRAJA = 0
     
        # load watermark mask image if available
        self.maskim = 0
        try:
            self.maskim = Image.open(WATERMARK_PIC)
            self.maskim.load()
        except:
            self.maskim = 0
     
        self.PIC_SCALE_DEFAULT = PIC_SCALE_DEFAULT
        self.SetScale(self.PIC_SCALE_DEFAULT)
     
        # create cookiejar
        self.cj = cookielib.MozillaCookieJar()

    
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
        if param == '--nowm':
            self.NOWM = 1
        elif param == '--orto':
            self.ORTO = 1
        elif param == '--ktjraja':
            self.KTJRAJA = 1
        else:
            return 0
        
        return 1


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
        # count lower left corner of the map picture with
        # point (P,I) = (mapy, mapx)
        fetchy = int(math.floor((mapy + (0.25 * self.PIC_RATIO)) / self.MAP_SIZEY)) * self.MAP_SIZEY
        fetchx = int(math.floor((mapx + (0.25 * self.PIC_RATIO)) / self.MAP_SIZEX)) * self.MAP_SIZEX

        return ((fetchx, fetchy), (fetchx, fetchy))

    
    ###########################################################################
    # Method:      FetchPic
    ###########################################################################
    # Description: Fetches one map picture from Kansalaisen karttapaikka.
    #              Lower left corner will be (N, E), result file
    #              will be saved in cachedir. Tempdir is used as temp directory while 
    #              downloading.
    ###########################################################################
    def FetchPic(self, n, e, cachedir, tempdir, layer):
        fname = cachedir + self.GetCacheName(e, n, layer)  
        
        # make N and E values of the center of the image to load       
        n = int(round(n + (((PIC_ORIG_SIZEY / 2.0) - 35) * self.PIC_RATIO)))
        e = int(round(e + ((PIC_ORIG_SIZEX / 2.0) * self.PIC_RATIO)))

        url = 'http://kansalaisen.karttapaikka.fi/tulosta.html'
        url = url + '?e=' + `e`
        url = url + '&n=' + `n`
        url = url + '&scale=' + repr(self.SCALEVAL)
        if self.ORTO:
            url = url + '&mode=orto'
        if self.KTJRAJA:
            url = url + '&feature=ktjraja'
        url = url + '&tool=siirra&lang=FI'
  
        USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4"

        res = ''
        try:
            req = urllib2.Request(url)
            req.add_header("User-Agent", USERAGENT)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
            f = opener.open(req)
            res = f.read()
            f.close()
        except:
            return 0

        regstr = 'img\s+class=\"karttakuva\"\s+src\=\"(?P<url>.+?)\"'
        m = re.compile(regstr).findall(res)
        if m != None and len(m) > 0:
            url = m[0]
            url = url.replace('&amp;', '&')    
        else:
            return 0
    
        # get the actual picture center N,E coordinates returned from the 
        # page
        retr_n = n
        retr_e = e
        regstr = 'Keskipisteen\skoordinaatit:\s*N\s*(?P<n>\d+)\s*,\s*E\s*(?P<e>\d+)\s*\(ETRS-TM35FIN'
        m = re.compile(regstr).findall(res)
        if m != None and len(m) > 0 and len(m[0]) > 0:
            (retr_n, retr_e) = m[0]
            retr_n = int(retr_n)
            retr_e = int(retr_e)

        if len(url) > 0 and url[0] == '/':
            url = 'http://kansalaisen.karttapaikka.fi' + url

        res = ''
        try:
            req = urllib2.Request(url)
            req.add_header("User-Agent", USERAGENT)
            self.cj.add_cookie_header(req)
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
    
            if im.size[0] != PIC_ORIG_SIZEX or im.size[1] != PIC_ORIG_SIZEY:
                print 'ERROR: Retrieved image is of invalid size (received: ' + `im.size[0]` + 'x' + `im.size[1]` + ', expected: ' + `PIC_ORIG_SIZEX` + 'x' + `PIC_ORIG_SIZEY` + ')'
                try:
                    os.unlink(tempfname)
                except:
                    pass
                return 0 
    
            im = im.crop(CROPBOX)
            if self.maskim:
                im = RemoveWatermark(im, self.maskim)
                
            # if the retrieved image is of different position, move the cropped area
            # to produce a correct image
            if (n != retr_n) or (e != retr_e):
                tempim = Image.new("RGB", (PIC_SIZEX, PIC_SIZEY), EMPTY_BACKGROUND_COLOR)
                
                dx = retr_e - e
                dy = retr_n - n
                (clx, cby, crx, cty) = (0, 0, 0, 0)
                (px, py) = (0, 0)
                if dx < 0:
                    clx = int(round(-dx / self.PIC_RATIO))
                else:
                    crx = int(round(dx / self.PIC_RATIO))
                    px = crx
                if dy < 0:
                    cby = int(round(-dy / self.PIC_RATIO))
                    py = cby
                else:
                    cty = int(round(dy / self.PIC_RATIO))    
                    py = 0
                    
                piccrop = (clx, cty, PIC_SIZEX - crx, PIC_SIZEY - cby)
                tempim.paste( im.crop(piccrop), (px, py) )
                im = tempim
            
            im.save(tempfname)
        except Exception, e:
            print "ERROR: Cannot convert map image or rewrite temporary map image file: " + tempfname
            print e.__str__()
            try:
                os.unlink(tempfname)
            except:
                pass
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
         
         
    ###########################################################################
    # Method:    GetCacheName
    ###########################################################################
    # Description: Generates a name for the map image in cache according to
    #              location and other parameters.
    ###########################################################################
    def GetCacheName(self, x, y, layer):
        fname = `self.SCALEVAL` + '_' + `int(self.PIC_SIZEX)` + '_' + `int(self.PIC_SIZEY)`
  
        if self.ORTO:
            fname = fname + '_orto'
        if self.KTJRAJA:
            fname = fname + '_ktjraja'
  
        hashy = int(round(y)) 
        hashx = int(round(x))
        hash = `HashRound(hashy)` + '_' + `HashRound(hashx)`
        fname = fname + '/' + hash
  
        fname = fname + '/map_' + self.SERVICE_CODE + '_' + `self.SCALEVAL`  
  
        if self.ORTO:
            fname = fname + '_orto'
        if self.KTJRAJA:
            fname = fname + '_ktjraja'
      
        fname = fname + '_'+ repr(int(round(y))) + '_' + repr(int(round(x))) + '.png'

        return fname


    ###########################################################################
    # Method:      PostProcess
    ###########################################################################
    # Description: Post processes the entire constructed map image according
    #              to service requirements.
    ###########################################################################    
    def PostProcess(self, im):
        if not self.NOWM and self.maskim:
            InsertWatermark(im, self.maskim)


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
        if (type != coordinates.COORD_TYPE_ETRSTM35FIN):
            temp = coordinates.Translate({'type': type, 'N': y, 'E': x}, \
                                         coordinates.COORD_TYPE_ETRSTM35FIN)
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
        return (30, 60)

      
    ###########################################################################
    # Method:      GetAvailableLayers
    ###########################################################################
    # Description: Get dict of available layer names. 
    ###########################################################################               
    def GetAvailableLayers(self):
        return {}
        
###########################################################################

# Functions

def HashRound(x):
    return ((x / 10000) / 5) * 5 


###########################################################################
# Function:    RemoveWatermark
###########################################################################
# Description: Removes watermark maskimg from image img.
###########################################################################

WM_MASK_DATA = [ \
    [-887.5272654, 0.941923886, -57.33910229, 1375.537846, 0.390903964, 407.1899933], \
    [-1191.492274, 0.949754715, -77.85158311, 1841.763281, 0.533938391, 548.5224555], \
    [-164.0302818, 0.960449739, -9.50489137, 271.2981724, 0.060302386, 72.59934995], \
    [-418.3487726, 0.968570036, -27.32173008, 638.0142368, 0.18756715, 193.258181], \
    [-0.152411531, 0.901185289, 1.000000012, -0.000000280, 0.0, -0.000000084] \
]

WM_MASK_DEFAULT = 2

def RemoveWatermark(img, maskimg):
  # estimate watermark offset from 
  (x_offset, y_offset, mask_i) = EstimateWMOffset(img, maskimg)

  orgdata = list(img.getdata())
  maskdata = list(maskimg.getdata())

  resdata = []
  (wid, hei) = img.size
  (mask_wid, mask_hei) = maskimg.size
  y = 0
  while y < hei:
    x = 0
    while x < wid:      
      orgpoint = orgdata[x + y * wid]
      mask_x = x - (wid / 2) + (mask_wid / 2)
      mask_y = y - (hei / 2) + (mask_hei / 2)
      if (mask_x - x_offset >= 0 and mask_x - x_offset < mask_wid and \
          mask_y - y_offset >= 0 and mask_y - y_offset < mask_hei):
          md = maskdata[mask_x - x_offset + (mask_y - y_offset) * mask_wid]
          if not md == (255,255,255):
              orgpoint = WMToPicPoint(orgpoint, md, mask_i, 1)
      resdata.append( orgpoint )
      x = x + 1
    y = y + 1

  newim = Image.new("RGB", (img.size[0], img.size[1]))
  newim.putdata(resdata)
  return newim

def EstimateWMOffset(img, maskimg):
    orgdata = list(img.getdata())
    maskdata = list(maskimg.getdata())
    maxmaskscore = 0
    maxscore = 0
    mask_id = WM_MASK_DEFAULT

    MAX_X_OFFSET = 10
    MAX_Y_OFFSET = 10
    (wid, hei) = img.size
    (m_wid, m_hei) = maskimg.size
    
    i = 0
    while (i < len(WM_MASK_DATA)):
        score = CalculateWMMaskScore(i, orgdata, maskdata, wid, hei, m_wid, m_hei)
        if (maxmaskscore < score):
            maxmaskscore = score
            mask_id = i
        i = i + 1

    scoreoffset = (int(MAX_X_OFFSET/2), int(MAX_Y_OFFSET / 2), mask_id)
    y_off = 0
    while (y_off < MAX_Y_OFFSET):
        x_off = 0
        while (x_off < MAX_X_OFFSET):
            score = CalculateWMScore(x_off, y_off, mask_id, orgdata, maskdata, wid, hei, m_wid, m_hei)

            if (maxscore < score):
                maxscore = score
                scoreoffset = (x_off, y_off, mask_id)
            x_off = x_off + 1    
        y_off = y_off + 1
    
    return scoreoffset

def CalculateWMMaskScore(mask_id, orgdata, maskdata, wid, hei, m_wid, m_hei):
    score = 0

    wmvalue = PicToWMColor(255, 229, mask_id)
    
    # partial windows of the watermark to be matched
    areas = [ (213, 58, 32, 24), \
              (214, 127, 30, 26), \
              (143, 194, 32, 30), \
              (75, 199, 25, 24) ]

    for area in areas:
        X_START = area[0]
        Y_START = area[1]
        X_SIZE = area[2]
        Y_SIZE = area[3]

        y = Y_START
        while (y < Y_START+Y_SIZE and y < m_hei):
            x = X_START
            while (x < X_START+X_SIZE and x < m_wid):
                md = maskdata[ y * m_wid + x ]
                if md == (229,229,229):
                    ox = x - (m_wid/2) + (wid/2)
                    oy = y - (m_hei/2) + (hei/2)
                    od = orgdata[oy*wid + ox]
                    if ( od[0] == wmvalue or \
                         od[1] == wmvalue or \
                         od[2] == wmvalue ):
                        score = score + 1
                x = x + 1
            y = y + 1

    return score

def CalculateWMScore(x_off, y_off, mask_i, orgdata, maskdata, wid, hei, m_wid, m_hei):
    score = 0

    # partial windows of the watermark to be matched
    areas = [ (108, 94, 12, 15), \
              (156, 27, 28, 8), \
              (266, 238, 13, 19), \
              (187, 312, 17, 15), \
              (193, 28, 2, 180), \
              (69, 97, 250, 3), \
              (262, 45, 3, 260), \
              (207, 29, 58, 21) ]

    for area in areas:
        X_START = area[0]
        Y_START = area[1]
        X_SIZE = area[2]
        Y_SIZE = area[3]

        y = Y_START
        while (y < Y_START+Y_SIZE and y < m_hei):
            x = X_START
            while (x < X_START+X_SIZE and x < m_wid):
                md = maskdata[ (y - y_off) * m_wid + (x - x_off) ]
                if not md == (255,255,255) and not md == (229,229,229):
                    ox = x - (m_wid/2) + (wid/2)
                    oy = y - (m_hei/2) + (hei/2)
                    mycol = WMToPicPoint(orgdata[oy*wid+ox], md, mask_i, 0)
                    if ( mycol[0] == 255 or \
                         mycol[1] == 255 or \
                         mycol[2] == 255 ):
                        score = score + 1
                x = x + 1
            y = y + 1
        
    return score

def PicToWMColor(col, mask, mask_id):
    md = WM_MASK_DATA[mask_id]
    m = float(255 - mask)
    c = float(255 - col)

    num = md[0] + \
          md[1] * c + \
          md[2] * m + \
          md[3] * (1.0 / m) + \
          md[4] * m * m + \
          md[5] * math.sqrt(m)
    
    return 255 - int( round( num ) )

def WMToPicColor(col, mask, mask_id, normalize):
    md = WM_MASK_DATA[mask_id]
    m = float(255 - mask)
    c = float(255 - col)

    num = (c - md[0] - \
          md[2] * m - \
          md[3] * (1.0 / m) - \
          md[4] * m * m - \
          md[5] * math.sqrt(m)) / md[1]

    num = 255 - int( round( num ) )
    if normalize:
      if num < 0:
        num = 0
      if num > 255:
        num = 255    
    return num

def PicToWMPoint(point, mask, mask_id):
    return (PicToWMColor(point[0], mask[0], mask_id), PicToWMColor(point[1], mask[1], mask_id), PicToWMColor(point[2], mask[2], mask_id))

def WMToPicPoint(point, mask, mask_id, normalize):
    return (WMToPicColor(point[0], mask[0], mask_id, normalize), WMToPicColor(point[1], mask[1], mask_id, normalize), WMToPicColor(point[2], mask[2], mask_id, normalize))

def InsertWatermark(img, maskimg):
  mask_id = 3
  
  iwid = img.size[0]
  ihei = img.size[1]
  mwid = maskimg.size[0]
  mhei = maskimg.size[1]

  xstart = (iwid - mwid) / 2
  ystart = (ihei - mhei) / 2

  box = (xstart, ystart, xstart + mwid, ystart + mhei)
  ipart = img.crop(box)

  orgdata = list(ipart.getdata())
  maskdata = list(maskimg.getdata())
  
  y = 0
  while y < mhei:
      x = 0
      while x < mwid:
          pos = y * mwid + x
          if pos < len(orgdata) and pos < len(maskdata):
              md = maskdata[pos]
              if not md == (255,255,255):
                  orgdata[pos] = PicToWMPoint(orgdata[pos], md, mask_id)              
          x = x + 1
      y = y + 1
  
  ipart.putdata(orgdata)
  img.paste(ipart, box)


