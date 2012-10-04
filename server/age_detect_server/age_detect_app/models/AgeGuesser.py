# encoding: utf-8
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
        
        message = ''
        part = part[1:]
        
        if guessed_age['language'] == 'ja':
            if guessed_age['is_male']:
                if guessed_age['is_youth']:
                    message = 'ずいぶん若い'
                elif guessed_age['is_old']:
                    message = '渋い'
                elif guessed_age['is_20s']:
                    message = 'イケメンの'
                elif guessed_age['is_30s']:
                    message = '紳士な'
                else:
                    message = '普通な'
            else:
                if guessed_age['is_youth']:
                    message = 'かわいい'
                elif guessed_age['is_old']:
                    message = '年増美人の'
                elif guessed_age['is_20s']:
                    message = 'セクシーな'
                elif guessed_age['is_30s']:
                    message = '女性らしい'
                else:
                    message = '普通な'
            if part == 'forehead':
                message = "{0}お凸".format(message)
            elif part == 'nose_mouth':
                message = "{0}お鼻".format(message)
            elif part == 'left_eye' or part == 'right_eye':
                message = "{0}目".format(message)
            else:
                message = ""
        else:
            if guessed_age['is_male']:
                if guessed_age['is_youth']:
                    message = "very youthful"
                elif guessed_age['is_old']:
                    message = "mature"
                elif guessed_age['is_20s']:
                    message = "handsome"
                elif guessed_age['is_30s']:
                    message = "gentlemanly"
                else:
                    message = "average"
            else:
                if guessed_age['is_youth']:
                    message = "cute"
                elif guessed_age['is_old']:
                    message = "developed"
                elif guessed_age['is_20s']:
                    message = "sexy"
                elif guessed_age['is_30s']:
                    message = "womanly"
                else:
                    message = "average"
            print part
            if part == 'forehead':
                message = "You have a {0} forehead".format(message)
            elif part == 'nose_mouth':
                message = "You have a {0} nose".format(message)
            elif part == 'left_eye' or part == 'right_eye':
                message = "You have {0} eyes".format(message)
            else:
                message = ""
        #return "{0}{1}{2}".format(male,youth,old)
        return message
    
    def guess_age(self, image_upload_dir, udid, language):
        #face
        body_part = 'face_aligned'
        image_file = "{0}/{1}_result{2}.jpg".format(image_upload_dir, udid, body_part)
        image = self.get_image(image_file)
        guessed_age = self.guess_age_part(image, language, body_part)
        
        #individual parts
        body_part = 'forehead'
        image_file = "{0}/{1}_result{2}.jpg".format(image_upload_dir, udid, body_part)
        image = self.get_image(image_file)
        forehead = self.guess_age_part(image, language, body_part)
        guessed_age['message_forehead'] = forehead['message']
        
        body_part = 'nose_mouth'
        image_file = "{0}/{1}_result{2}.jpg".format(image_upload_dir, udid, body_part)
        image = self.get_image(image_file)
        nose_mouth = self.guess_age_part(image, language, body_part)
        guessed_age['message_nose_mouth'] = nose_mouth['message']
        
        
        body_part = 'left_eye'
        image_file = "{0}/{1}_result{2}.jpg".format(image_upload_dir, udid, body_part)
        image = self.get_image(image_file)
        left_eye = self.guess_age_part(image, language, body_part)
        guessed_age['message_left_eye'] = left_eye['message']
                
        #body_part = 'right_eye'
        #image_file = "{0}/{1}_result{2}.jpg".format(image_upload_dir, udid, body_part)
        #image = self.get_image(image_file)
        #right_eye = self.guess_age_part(image, language, body_part)
        right_eye = left_eye
        guessed_age['message_right_eye'] = right_eye['message']
        
        return guessed_age
    
    def guess_age_part(self, image, language, body_part):
        
        body_part = "_{0}".format(body_part)
        if body_part == '_face_aligned':
            body_part = ''
        
        guessed_age = {
            'min':0,
            'max':0,
            'age':0,
            'decade':0,
            'is_youth':False,
            'is_old':False,
            'is_20s':False,
            'is_30s':False,
            'language': language,
            'message': ''
        }
        
        
        is_male_model = cv2.createFisherFaceRecognizer()
        decade_model = cv2.createFisherFaceRecognizer()#14-19=10,20-29=20,30=39=30s,40-49=40
        is_youth_model = cv2.createFisherFaceRecognizer()#is youth? (4-13 yes, 19+ no)
        is_old_model = cv2.createFisherFaceRecognizer()#is old (10-25 no, 40+ yes)
        is_20s_model = cv2.createFisherFaceRecognizer()
        is_30s_model = cv2.createFisherFaceRecognizer()
        
        is_male_model.load("{0}train/data/is_male{1}.data".format(settings.PROJECT_ROOT, body_part))
        
        #first, predict if male or female
        is_male = (is_male_model.predict(image)[0] == 1)
        #confidence = predicted_label[1]
        #if is_male:
        if True:
            #load male age datasets
            
            print "{0}train/data/male_is_old{1}.data".format(settings.PROJECT_ROOT, body_part)
            
            is_youth_model.load("{0}train/data/male_is_youth{1}.data".format(settings.PROJECT_ROOT, body_part))
            is_old_model.load("{0}train/data/male_is_old{1}.data".format(settings.PROJECT_ROOT, body_part))
            try:
                decade_model.load("{0}train/data/male_decade{1}.data".format(settings.PROJECT_ROOT, body_part))
                is_20s_model.load("{0}train/data/male_is_20s{1}.data".format(settings.PROJECT_ROOT, body_part))
                is_30s_model.load("{0}train/data/male_is_30s{1}.data".format(settings.PROJECT_ROOT, body_part))
            except:
                decade_model = None
                is_20s_model = None
                is_30s_model = None
        else:
            #load female age datasets
            decade_model.load("{0}train/data/female_decade.data".format(settings.PROJECT_ROOT))
            is_youth_model.load("{0}train/data/female_is_youth.data".format(settings.PROJECT_ROOT))
            is_old_model.load("{0}train/data/female_is_old.data".format(settings.PROJECT_ROOT))
            
        
        #guess age
        guessed_age['is_male'] = is_male
        guessed_age['is_youth'] = (is_youth_model.predict(image)[0] == 1)
        guessed_age['is_old'] = (is_old_model.predict(image)[0]  == 1)
        
        if decade_model:
            #guess the age
            guessed_age['decade'] = decade_model.predict(image)[0]
            guessed_age['is_20s'] = (is_20s_model.predict(image)[0] == 1)
            guessed_age['is_30s'] = (is_30s_model.predict(image)[0] == 1)
            
            
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
                
                
                guessed_age['age'] = int(total_age/total_cats)
                
        #guessed_age['message_right_eye'] = self.get_message(guessed_age, 'right_eye')
        guessed_age['message'] = self.get_message(guessed_age, body_part)
        
        
        return guessed_age
    