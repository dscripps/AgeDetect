# encoding: utf-8
import sys
sys.path.insert(0, '/usr/local/lib/python2.6/site-packages')
from django.db import models
#from PyML import *
#from PyML.classifiers.svm import SVR
#from PyML.classifiers.svm import loadSVM



class AgeSVR:
    
    class __impl:
        
        svr = None
        
        def setSVR(self, dataset):
            data = SparseDataSet(dataset, labelsColumn = -1, numericLabels = True)
            self.svr = SVR()
            self.svr.train(data)
            
        def getSVR(self):
            return self.svr

    
    
    # storage for the instance reference
    __instance = None
    

    def __init__(self, dataset):
        """ Create singleton instance """
        # Check whether we already have an instance
        if AgeSVR.__instance is None:
            # Create and remember instance
            AgeSVR.__instance = AgeSVR.__impl()
            AgeSVR.__instance.setSVR(dataset)

        # Store instance reference as the only member in the handle
        self.__dict__['_AgeSVR__instance'] = AgeSVR.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    