#!/usr/bin/env python
import os
import sys
import cv2.cv as cv
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
        #im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        im = cv.LoadImageM(file, cv2.IMREAD_GRAYSCALE)
        image_data = np.asarray(im, dtype=np.uint8)
        return image_data
    
    def get_message(self, guessed_age, part):
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
        
    def guess_age(self, image, language):
        
        guessed_age = {
            'min':0,
            'max':0,
            'age':0,
            'decade':0,
            'is_youth':False,
            'is_old':False,
            'is_20s':False,
            'is_30s':False,
            'message_forehead': '',
            'message_left_eye': '',
            'message_right_eye': '',
            'message_nose_mouth': '',
            'language': language
        }
        
        
        is_male_model = cv2.createFisherFaceRecognizer()
        decade_model = cv2.createFisherFaceRecognizer()#14-19=10,20-29=20,30=39=30s,40-49=40
        is_youth_model = cv2.createFisherFaceRecognizer()#is youth? (4-13 yes, 19+ no)
        is_old_model = cv2.createFisherFaceRecognizer()#is old (10-25 no, 40+ yes)
        is_20s_model = cv2.createFisherFaceRecognizer()
        is_30s_model = cv2.createFisherFaceRecognizer()
        
        is_male_model.load("{0}train/data/is_male.data".format(settings.PROJECT_ROOT))
        
        #first, predict if male or female
        is_male = (is_male_model.predict(image)[0] == 1)
        #confidence = predicted_label[1]
        #if is_male:
        if True:
            #load male age datasets
            decade_model.load("{0}train/data/male_decade.data".format(settings.PROJECT_ROOT))
            is_youth_model.load("{0}train/data/male_is_youth.data".format(settings.PROJECT_ROOT))
            is_old_model.load("{0}train/data/male_is_old.data".format(settings.PROJECT_ROOT))
            is_20s_model.load("{0}train/data/male_is_20s.data".format(settings.PROJECT_ROOT))
            is_30s_model.load("{0}train/data/male_is_30s.data".format(settings.PROJECT_ROOT))
        else:
            #load female age datasets
            decade_model.load("{0}train/data/female_decade.data".format(settings.PROJECT_ROOT))
            is_youth_model.load("{0}train/data/female_is_youth.data".format(settings.PROJECT_ROOT))
            is_old_model.load("{0}train/data/female_is_old.data".format(settings.PROJECT_ROOT))
            
        
        #guess age
        guessed_age['is_male'] = is_male
        guessed_age['is_youth'] = (is_youth_model.predict(image)[0] == 1)
        guessed_age['is_old'] = (is_old_model.predict(image)[0]  == 1)
        guessed_age['is_20s'] = (is_20s_model.predict(image)[0] == 1)
        guessed_age['is_30s'] = (is_30s_model.predict(image)[0] == 1)
        guessed_age['decade'] = decade_model.predict(image)[0]
        
        
        if guessed_age['is_youth'] and not guessed_age['is_old'] and not guessed_age['is_20s'] and not guessed_age['is_30s']:
            guessed_age['min'] = 14
            guessed_age['max'] = 20
            guessed_age['age'] = random.randint(14, 20)
        elif guessed_age['is_old'] and not guessed_age['is_youth'] and not guessed_age['is_20s'] and not guessed_age['is_30s']:
            guessed_age['min'] = 40
            guessed_age['max'] = 60
            guessed_age['age'] = random.randint(40, 50)
        else:
            #image is neither young nor old
            #guess the decade
            decade = decade_model.predict(image)[0]
            guessed_age['decade'] = decade
            
            total_cats = 1
            total_age = decade+5
            
            #guess 20s/30s
            
            if guessed_age['is_20s']:
                total_cats = total_cats + 1
                total_age = total_age + 25
            
            if guessed_age['is_30s']:
                total_cats = total_cats + 1
                total_age = total_age + 35
            #guessed_age['min'] = decade
            #guessed_age['max'] = decade+9
            
            #guessed_age['age'] = random.randint(decade, decade+5)
            guessed_age['age'] = int(total_age/total_cats)


        guessed_age['message_forehead'] = self.get_message(guessed_age, 'forehead')
        guessed_age['message_left_eye'] = self.get_message(guessed_age, 'left_eye')
        guessed_age['message_right_eye'] = self.get_message(guessed_age, 'right_eye')
        guessed_age['message_nose_mouth'] = self.get_message(guessed_age, 'nose_mouth')
        
        return guessed_age
    