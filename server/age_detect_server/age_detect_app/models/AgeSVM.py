# encoding: utf-8
import sys
sys.path.insert(0, '/usr/local/lib/python2.6/site-packages')
from django.db import models
import logging
#from PyML import *
#from PyML.classifiers.svm import SVR
#from PyML.classifiers.svm import loadSVM


class AgeSVM:
    
    class __impl:
        
        svm = None
        ages = [[0,15,None],[16,100,None],[0,3,None],[4,12,None],[13,19,None],[20,29,None],[30,39,None],[40,49,None],[50,100,None]]
        #ages = [[0,15,None],[16,100,None]]
        
        def setSVMs(self):
            for age_range in self.ages:
                dataset = "training_data/face_bw_{0}_{1}.data".format(age_range[0], age_range[1])
                data = SparseDataSet(dataset, labelsColumn = -1)
                s = SVM()
                s.train(data)
                age_range[2] = s
            
        def getSVMs(self):
            return self.ages

    
    
    # storage for the instance reference
    __instance = None
    

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if AgeSVM.__instance is None:
            # Create and remember instance
            AgeSVM.__instance = AgeSVM.__impl()
            AgeSVM.__instance.setSVMs()

        # Store instance reference as the only member in the handle
        self.__dict__['_AgeSVM__instance'] = AgeSVM.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)



    
