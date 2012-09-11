#!/usr/bin/env python

import os
import sys
import cv2
import numpy as np
import glob
from age_detect import settings
from random import shuffle

def normalize(X, low, high, dtype=None):
    """Normalizes a given array in X to a value between low and high."""
    X = np.asarray(X)
    minX, maxX = np.min(X), np.max(X)
    # normalize to [0...1].    
    X = X - float(minX)
    X = X / float((maxX - minX))
    # scale to [low...high].
    X = X * (high-low)
    X = X + low
    if dtype is None:
        return np.asarray(X)
    return np.asarray(X, dtype=dtype)

def read_images(path, sz=None):
    
    
    X,y = [], []
    #testSample = None
    #testSampleAnswer = 0
    #testSampleFile = ''
    filenames = glob.glob("{0}train/{1}*.jpg".format(settings.PROJECT_ROOT, path))
    shuffle(filenames)
    
    for filename in filenames:
        im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        answer = get_correct_answer(filename)
        if answer > 0:
            image_data = np.asarray(im, dtype=np.uint8)
            #if testSample is None:
            #    #print "{0}".format(filename)
            #    testSample = image_data
            #    testSampleAnswer = answer
            #    testSampleFile = filename
            #else:
            X.append(image_data)
            y.append(answer)
    return [X,y]

def get_correct_answer(input_name):
    name_arr = input_name.split('/')
    filename = name_arr[len(name_arr)-1]
    age = int(filename[0:2])
    return age
    #if age < 4:
    #if age >= 4 and age < 12:
    #if age >= 12 and age < 17:
    #if age >= 22 and age < 30:
    #if age >= 30 and age < 45:
    #    #print "age={0}".format(age)
    #    return 1
    #elif age >= 46:
    #    return 2
    #0 means don't use this image
    #return 0

if __name__ == "__main__":
    
    
    # This is where we write the images, if an output_dir is given
    # in command line:
    out_dir = None
    # You'll need at least a path to your image data, please see
    # the tutorial coming with this source code on how to prepare
    # your image data:
    if len(sys.argv) < 2:
        print "USAGE: facerec_demo.py </path/to/train/images> </path/to/data/file/>"
        sys.exit()
    
    
    #data_file = "data/0_3_or_above_45.data"
    #data_file = "data/4_11_or_above_45.data"
    #data_file = "data/12_16_or_above_45.data"
    #data_file = "data/17_21_or_above_45.data"
    #data_file = "data/30_45_or_above_45.data"
    #data_file = "data/all.data"
    data_file = sys.argv[2]
    
    
    # Now read in the image data. This must be a valid path!
    #[X,y,testSample,testSampleAnswer] = read_images(sys.argv[1])
    #model = cv2.createFisherFaceRecognizer()
    #model.train(X,np.asarray(y))
    
    #right = 0
    #wrong = 0
    
    #for i in range(1,10):
        
    #print i
    #print '.'
    #look at test images
    #[testXs,testYs] = read_images(sys.argv[2])
    #for i in range(0,len(testXs)):
    #for i in range(0,1000):
        #testSample = testXs[i]
    #testSampleAnswer = testYs[i]
    
    [X,y] = read_images(sys.argv[1])
    model = cv2.createFisherFaceRecognizer()
    model.train(X,np.asarray(y))
    #model.setDouble("threshold", 1000.0)
    #model.set("threshold",1000.0)
    #predictedLabel = model.predict(testSample)
    #print predictedLabel
    #print "{0}={1}?".format(predictedLabel[0],testSampleAnswer)
    #if predictedLabel[0] == testSampleAnswer:
    #    #print 'RIGHT'
    #    right = right + 1
    #else:
    #    #print "mv {0} ~/Desktop/wrong".format(testSampleFile)
    #    #print "WRONG"
    #    wrong = wrong + 1
        
        
        
    #print float(right) / float(right + wrong)
    model.save(data_file)
    mean = model.getMat("mean")
    mean_norm = normalize(mean, 0, 255, dtype=np.uint8)
    mean_resized = mean_norm.reshape(X[0].shape)
    cv2.imshow("mean", mean_resized)
    
    #eigenvectors = model.getMat("eigenvectors")
    #eigenvalues = model.getMat("eigenvalues")
    #eigenvectors_norm = normalize(eigenvectors, 0, 255, dtype=np.uint8)
    #eigenvectors_resized = eigenvectors_norm.reshape(X[0].shape)
    #cv2.imshow("eigenvectors", eigenvectors_resized)
    #cv2.imshow("eigenvectors", eigenvectors_norm)
    
    
    
    #sample = normalize(eigenvectors[0], 0 , 255)
    #cv2.applyColorMap(sample, cv2.COLORMAP_BONE)
    #cv2.imshow("colormap", sample)
    
#    // Display or save the first, at most 16 Fisherfaces:
#    for (int i = 0; i < min(16, W.cols); i++) {
#        string msg = format("Eigenvalue #%d = %.5f", i, eigenvalues.at<double>(i));
#        cout << msg << endl;
#        // get eigenvector #i
#        Mat ev = W.col(i).clone();
#        // Reshape to original size & normalize to [0...255] for imshow.
#        Mat grayscale = norm_0_255(ev.reshape(1, height));
#        // Show the image & apply a Bone colormap for better sensing.
#        Mat cgrayscale;
#        applyColorMap(grayscale, cgrayscale, COLORMAP_BONE);
#        // Display or save:
#        if(argc == 2) {
#            imshow(format("fisherface_%d", i), cgrayscale);
#        } else {
#            imwrite(format("%s/fisherface_%d.png", output_folder.c_str(), i), norm_0_255(cgrayscale));
#        }
#    }
    
    
    
    #cv2.waitKey(0)
    