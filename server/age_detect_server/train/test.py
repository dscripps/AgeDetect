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

#def normalize(X, low, high, dtype=None):
#    """Normalizes a given array in X to a value between low and high."""
#    X = np.asarray(X)
#    minX, maxX = np.min(X), np.max(X)
#    # normalize to [0...1].    
#    X = X - float(minX)
#    X = X / float((maxX - minX))
#    # scale to [low...high].
#    X = X * (high-low)
#    X = X + low
#    if dtype is None:
#        return np.asarray(X)
#    return np.asarray(X, dtype=dtype)



if __name__ == "__main__":
    
    
    if len(sys.argv) < 3:
        print "USAGE: test.py </path/to/test/images/> </path/to/data/file/>"
        sys.exit()
    
    [X,files] = read_images(sys.argv[1])
    data_file = sys.argv[2]
    
    model = cv2.createFisherFaceRecognizer()
    model.load(data_file)
    
    #eigenvectors = model.getMat("eigenvectors")
    #for i in xrange(min(len(X), 16)):
    #i = 0
    #eigenvector_i = eigenvectors[:,i].reshape(X[0].shape)
    #eigenvector_i_norm = normalize(eigenvector_i, 0, 255, dtype=np.uint8)
    #cv2.imshow("eigenface", cv2.applyColorMap(eigenvector_i_norm, cv2.COLORMAP_JET))
    #cv2.imshow("face", X[i])
    #cv2.waitKey(0)
    ones = 0
    twos = 0
    for i in range(0,len(X)):
        
        image = X[i]
        file = files[i]
        predicted_label = model.predict(image)
        #print "{0}={1},{2}".format(file, predicted_label[0], predicted_label[1])
        print predicted_label[0]
        
        if predicted_label[0] == 1:
            ones = ones + 1
        else:
            twos = twos + 1
        predicted_answer = predicted_label[0]
        confidence = predicted_label[1]
    print ones
    print twos
    