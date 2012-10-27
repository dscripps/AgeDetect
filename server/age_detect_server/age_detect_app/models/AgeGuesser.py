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
            responses = {
                'is_male': {
                    'forehead': {
                        'is_youth':"Your forehead is just starting to blossom.  It will be interesting to see how it evolves in the next few years.",
                        'is_old':"You have a mature forehead that commands respect.  Similar to Ted Danson or The Dalai Lama.  While not quite over the hill, your forehead shows wisdom and understands the impermanence of all things.",
                        'is_20s':"You have a handsome forehead.  Somewhere in its twenties, your forehead is at the peak of its youth.  Enjoy that forehead while you still can!  There will be a day when you will see a picture of your forehead and think, \"man, those were some good times\".",
                        'is_30s':"You have a gentlemanly forehead.  Your forehead is now in a place where it has matured, but still has a bit of youthful arrogance.  It is the kind of forehead that will attract a partner looking to settle down long-term.",
                        'other':"Your forehead doesn't seem to have anything out of the ordinary.  Just an average joe forehead."
                    },
                            
                    'nose_mouth': {
                        'is_youth':"Your nose and mouth are very young!  Compared to my massive database of mouths and noses, there's only a few that show up younger.  Seriously.",
                        'is_old':"\"If that mouth could only talk\", oh wait, I guess it can.  Your mouth and nose seem to have a history going back quite a ways.",
                        'is_20s':"Your nose and mouth are definitely in their prime.  You still got a few years in that mouth before the party ends and it comes time to settle down.",
                        'is_30s':"If I didn't know better, I'd say that's Prince Harry of Wales?  You have a very charming, princely nose and mouth.",
                        'other':"Your nose and mouth don't seem to have any redeeming characteristics.  Which is probably a good thing.  Perhaps a bit masculine."
                    },
                    'eye': {
                        'is_youth':"Is that Justin Bieber?  What cute baby eyes you have!",
                        'is_old':"Your eyes show a history rich of life, with all its ups and downs.  It'd be nice to have a chat some day with you, I'm sure you have a lot of interesting stories to tell about the things you saw with those eyes.",
                        'is_20s':"Hey handsome!  Those are some real nice eyes you have there.  Somebody in their twenties, maybe a recent college grad?",
                        'is_30s':"Your eyes suggest a man in his 30s.  There's a twinkle of youth, but a hint of cynicism as well.  Lighten up and try not to take life so seriously.",
                        'other':"Your eyes don't seem to give any information regarding your age.  Very mysterious."
                    }
                },
                'is_female': {
                    'forehead': {
                        'is_youth':"You have a beautiful, youthful forehead.",
                        'is_old':"Your forehead has a mature beauty wise beyond its years.",
                        'is_20s':"You have a beautiful forehead.  Somewhere in its twenties, your forehead is at the peak of its youth.  Enjoy that forehead while you still can!  There will be a day when you will see a picture of your forehead and think, \"boy oh boy, those were some good times\".",
                        'is_30s':"Your forehead screams beauty.  Think Angelina Jolie.",
                        'other':"Your forehead doesn't seem to have anything out of the ordinary.  Just an average forehead."
                    },
                    'nose_mouth': {
                        'is_youth':"Your nose and mouth have a youthful and suggest that you are still a child.",
                        'is_old':"Your mouth and nose have a wisdom and feminine charm.",
                        'is_20s':"Your lips and mouth resemble Elizabeth Taylor in her prime.",
                        'is_30s':"Your mouth and nose have the appeal of Marilyn Monroe.",
                        'other':"Your nose and mouth don't seem to have any redeeming characteristics.  Which is probably a good thing.  Perhaps a bit feminine."
                    },
                    'eye': {
                        'is_youth':"Your eyes are very young!  On top of that, they appear to be quite feminine.",
                        'is_old':"You have beautiful mature eyes like Michelle Pfeiffer.",
                        'is_20s':"Your eyes are the envy of the town.  Perhaps in their mid-twenties.",
                        'is_30s':"Your eyes suggest a woman in her thirties.",
                        'other':"Your eyes don't seem to give any information regarding your age.  Very mysterious."
                    }
                }
            }
            message_part = part
            if message_part == 'left_eye' or message_part == 'right_eye':
                message_part = 'eye'
            message_sex = 'is_male'
            if guessed_age['is_male'] != True:
                message_sex = 'is_female'
            if guessed_age['is_youth']:
                message_age = 'is_youth'
            elif guessed_age['is_old']:
                message_age = 'is_old'
            elif guessed_age['is_20s']:
                message_age = 'is_20s'
            elif guessed_age['is_30s']:
                message_age = 'is_30s'
            else:
                message_age = 'other'
            message = ''
            if message_part != '':
                message = responses[message_sex][message_part][message_age]
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
    