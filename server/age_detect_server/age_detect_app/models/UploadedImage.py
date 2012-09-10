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
    
    def handle_uploaded_file(self, udid, f):
        self.file = "{0}/{1}.jpg".format(self.image_upload_dir, udid)
        self.udid = udid
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
        image_file = "{0}/{1}_resultface_aligned.jpg".format(self.image_upload_dir, self.udid)
        image = ageGuesser.get_image(image_file)
        guessed_age = ageGuesser.guess_age(image)
        male = 'F'
        if guessed_age['is_male']:
            male = 'M'
        youth = 'y'
        if guessed_age['is_youth']:
            youth = 'Y'
        old ='o'
        if guessed_age['is_old']:
            old = 'O'
        return "{0}{1}{2}".format(male,youth,old)
    
    def to_json(self):
        result = {}
        #result['age'] = 33
        result['age'] = self.get_age()
        return json.dumps(result)
    
    
    #remove all files used in processing
    def cleanup(self):
        for file in glob.glob("{0}/{1}*.jpg".format(self.image_process_dir, self.udid)):
            os.remove(file)
        for file in glob.glob("{0}/{1}.data".format(self.image_results_dir, self.udid)):
            os.remove(file)
        return True
        
