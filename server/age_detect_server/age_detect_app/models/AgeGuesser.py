#!/usr/bin/env python
import os
import sys
import cv2
import numpy as np
import glob
import random
from django.db import models
from age_detect import settings


class AgeGuesser(models.Model):
    
#    def __init__(self):
#        self.is_male_model = cv2.createFisherFaceRecognizer()
#        self.is_youth_model = cv2.createFisherFaceRecognizer()#is youth? (4-13 yes, 19+ no)
#        self.is_old_model = cv2.createFisherFaceRecognizer()#is old (10-25 no, 40+ yes)
#        self.decade_model = cv2.createFisherFaceRecognizer()#14-19=10,20-29=20,30=39=30s,40-49=40
    
    def get_image(self, file):
        im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        image_data = np.asarray(im, dtype=np.uint8)
        return image_data
    
    def guess_age(self, image):
        
        guessed_age = [0, 0, 0] #guessed age, min age, max age
        return guessed_age
        
        is_male_model = cv2.createFisherFaceRecognizer()
        is_youth_model = cv2.createFisherFaceRecognizer()#is youth? (4-13 yes, 19+ no)
        is_old_model = cv2.createFisherFaceRecognizer()#is old (10-25 no, 40+ yes)
        decade_model = cv2.createFisherFaceRecognizer()#14-19=10,20-29=20,30=39=30s,40-49=40
        
        
        is_male_model.load("{0}train/data/is_male.data".format(settings.PROJECT_ROOT))
        
        #first, predict if male or female
        #is_male = (is_male_model.predict(image)[0] == 1)
        is_male = True
        #confidence = predicted_label[1]
        if is_male:
            #load male age datasets
            is_youth_model.load("{0}train/data/male_is_youth.data".format(settings.PROJECT_ROOT))
            is_old_model.load("{0}train/data/male_is_old.data".format(settings.PROJECT_ROOT))
            decade_model.load("{0}train/data/male_decade.data".format(settings.PROJECT_ROOT))
        else:
            #load female age datasets
            is_youth_model.load("{0}train/data/female_is_youth.data".format(settings.PROJECT_ROOT))
            is_old_model.load("{0}train/data/female_is_old.data".format(settings.PROJECT_ROOT))
            decade_model.load("{0}train/data/female_decade.data".format(settings.PROJECT_ROOT))
        
        #guess age
        is_youth = (is_youth_model.predict(image)[0] == 1)
        is_old = (is_old_model.predict(image)[0]  == 1)
        
        
        
        if is_youth and not is_old:
            guessed_age = [0, 14, 14]
        elif is_old and not is_youth:
            guessed_age = [40, 60, random.randint(40, 50)]
        else:
            #image is neither young nor old, guess the decade
            decade = decade_model.predict(image)[0]
            guessed_age = [decade, decade+9, random.randint(decade, decade+9)]
            
        return guessed_age
    