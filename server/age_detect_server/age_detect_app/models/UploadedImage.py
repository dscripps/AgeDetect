# encoding: utf-8
import sys
sys.path.insert(0, '/usr/local/lib/python2.6/site-packages')
import os
from django.db import models
import json
#import numpy as np
#import cv
#import cv2
import math
import glob
import logging
from age_detect import settings
from age_detect_app.models.FeaturesExtractor import *
from age_detect_app.models import AgeGuesser


class UploadedImage(models.Model):
    image_upload_dir = settings.MEDIA_ROOT + "uploads"
    image_process_dir = "tmp/processing"
    image_results_dir = "tmp/results"
    udid = 0
    file = ''
    language = 'en'
    
    def handle_uploaded_file(self, udid, f, language):
        self.file = "{0}/{1}.jpg".format(self.image_upload_dir, udid)
        self.udid = udid
        self.language = language
        #save file on server
        with open(self.file, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        #save each part of face as separate file on server
        featuresExtractor = FeaturesExtractor()
        result_name = "{0}/{1}_result".format(self.image_upload_dir, udid)
        featuresExtractor.detect_and_draw(result_name, self.file, True)
        
    
    def get_age(self):
        ageGuesser = AgeGuesser()
        guessed_age = ageGuesser.guess_age(self.image_upload_dir, self.udid, self.language)
        
        return guessed_age
    
    def to_json(self):
        result = self.get_age()
        return json.dumps(result)
    
    
    #remove all files used in processing
    def cleanup(self):
        for file in glob.glob("{0}/{1}*.jpg".format(self.image_process_dir, self.udid)):
            os.remove(file)
        for file in glob.glob("{0}/{1}.data".format(self.image_results_dir, self.udid)):
            os.remove(file)
        return True
        
