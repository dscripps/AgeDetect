#!/usr/bin/env python

import os
import sys
import cv2
import numpy as np
import glob
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
    
    
    if len(sys.argv) < 3:
        print "USAGE: test.py </path/to/test/images/> </path/to/data/file/>"
        sys.exit()
    
    [X,files] = read_images(sys.argv[1])
    data_file = sys.argv[2]
    
    model = cv2.createFisherFaceRecognizer()
    model.load(data_file)
    
    for i in range(0,len(X)):
        
        image = X[i]
        file = files[i]
        predicted_label = model.predict(image)
        print "{0}={1},{2}".format(file, predicted_label[0], predicted_label[1])
        predicted_answer = predicted_label[0]
        confidence = predicted_label[1]
    
    