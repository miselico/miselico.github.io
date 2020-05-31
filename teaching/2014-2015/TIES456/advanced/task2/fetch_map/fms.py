#! python
# -*- coding: iso-8859-1 -*-
###########################################################################
# 
# File:            fms.py
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
# Author:          Olli Lammi (olammi@iki.fi)
#
# Version:         3.1g
#
# Date:            20.02.2012
#
# Functions:       -
#                   
# Description:     Abstract map service class
#
# Requirements:    Python interpreter 2.4 or newer (www.python.org)
#                  (tested with 2.4.1)
# 
#                  Python Imaging Library (tested with 1.1.5) 
#                  (www.pythonware.org/products/pil/)
#
# Version history: ** 18.02.2009 v3.0a (Olli Lammi) **
#                  First class implementation. 
#
#                  ** 11.02.2010 v3.0h (Olli Lammi) **
#                  Changed the coordinate handling in the interfaces. 
#
#                  ** 30.01.2012 v3.1a (Olli Lammi) **
#                  Changed the HandleParameter return value intepretation. 
#                  Added support for layers.
#
#                  ** 20.02.2012 v3.1g (Olli Lammi) **
#                  Changed FetchPic parameters.
#
###########################################################################

# Classes

class FetchMapService: 
    def __init__(self):
        # service values describing the service, scale and map parts
        self.PIC_RATIO = 0           # meters per map pixel
        self.REVERSE_RATIO = 0       # multiplied by PIC_RATIO gives scale
        self.SCALE = ""              # current map scale
        self.PIC_SIZEX = 0           # X size of one map part
        self.PIC_SIZEY = 0           # Y size of one map part
        self.MAP_SIZEX = 0           # one map part X size in meters 
        self.MAP_SIZEY = 0           # one map part Y size in meters
        self.PIC_SCALE_DEFAULT = ""  # default service map scale
        self.SERVICE_CODE = ""       # service code of this service
        
    ###########################################################################
    # Function:    GetVersion
    ###########################################################################
    # Description: Returns the module version string. 
    ###########################################################################    
    def GetVersion(self): pass
    
    
    ###########################################################################
    # Function:    HandleParameter
    ###########################################################################
    # Description: Handles command line parameter. Returns 0, if the parameter
    #              was invalid. Returns number of consumed parameters, if the 
    #              parameter was ok. 
    ###########################################################################    
    def HandleParameter(self, param): pass
    
    
    ###########################################################################
    # Function:    SetScale
    ###########################################################################
    # Description: Initializes the service and values to retrieve map parts
    #              in given scale. The parameter must be one of the values
    #              returned by GetScales.
    ###########################################################################            
    def SetScale(self, scale): pass


    ###########################################################################
    # Function:    GetScales
    ###########################################################################
    # Description: Returns list of scales that the service supports
    ###########################################################################        
    def GetScales(self): pass

    
    ###########################################################################
    # Function:    GetPicIndexes
    ###########################################################################
    # Description: Returns two (x,y) tuples with indexes for map image that has
    #              the given (mapx, mapy) point and the lower left xy
    #              coordinates of the indexed map picture.
    ###########################################################################
    def GetPicIndexes(self, mapx, mapy): pass


    ###########################################################################
    # Method:      FetchPic
    ###########################################################################
    # Description: Fetches one map picture from the map service.
    #              Lower left corner will be (LL_y, LL_x), result file
    #              will be saved in cachedir. Tempdir is used as temp directory 
    #              while downloading.
    ###########################################################################    
    def FetchPic(self, LL_y, LL_x, cachedir, tempdir, layer): pass
 
 
    ###########################################################################
    # Method:      GetCacheName
    ###########################################################################
    # Description: Generates a name for the map image in cache according to
    #              location and service parameters.
    ###########################################################################       
    def GetCacheName(self, x, y, layer): pass    

        
    ###########################################################################
    # Method:      PostProcess
    ###########################################################################
    # Description: Post processes the entire constructed map image according
    #              to service requirements.
    ###########################################################################       
    def PostProcess(self, im): pass


    ###########################################################################
    # Method:      TranslateToServiceCoordinatesXY
    ###########################################################################
    # Description: Does service require coordinates to be transferred to YKJ?
    #              Returns: tuple (type, x, y) where
    #              type - type string of the coordinate system
    #              x - easting or lon coordinate 
    #              y - northing or lat coordinate
    ###########################################################################       
    def TranslateToServiceCoordinatesXY(self, type, x, y): pass

     
    ###########################################################################
    # Method:      GetHelp
    ###########################################################################
    # Description: Get service module specific help string.
    ###########################################################################               
    def GetHelp(self): pass
    
    ###########################################################################
    # Method:      GetServiceDelayLimits
    ###########################################################################
    # Description: Get service specific delay times as tuple (min, max) in sec.
    ###########################################################################               
    def GetServiceDelayLimits(self): pass

    ###########################################################################
    # Method:      GetAvailableLayers
    ###########################################################################
    # Description: Get dict of available layer names. 
    ###########################################################################               
    def GetAvailableLayers(self): pass
    