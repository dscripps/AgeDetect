#!/usr/bin/env python
import os
import sys
import cv2
import numpy as np
import glob
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "age_detect.settings")
from age_detect_app.models import AgeGuesser
from age_detect import settings


def read_images(path, sz=None):
    
    X,files = [], []
    filenames = glob.glob("{0}train/{1}*.jpg".format(settings.PROJECT_ROOT, path))
    for filename in filenames:
        im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        image_data = np.asarray(im, dtype=np.uint8)
        X.append(image_data)
        name_arr = filename.split('/')
        files.append(name_arr[len(name_arr)-1])
    return [X,files]

if __name__ == "__main__":
    
    
    if len(sys.argv) < 2:
        print "USAGE: guess_age.py </path/to/test/images/>"
        sys.exit()
    
    [X,files] = read_images(sys.argv[1])
    
    ageGuesser = AgeGuesser()
    
    for i in range(0,len(X)):
        
        
        
        image = X[i]
        file = files[i]
        age = file[0:2]
        
        guessed_age = ageGuesser.guess_age(image)
        print "{0},{1}".format(age, guessed_age[2])
    