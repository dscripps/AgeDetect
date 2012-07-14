#!/usr/bin/python
"""
This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
"""
import sys
import cv2.cv as cv
from optparse import OptionParser
import glob

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
# for accurate yet slow object detection. For a faster operation on real video 
# images the settings are: 
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
# min_size=<minimum possible face size

#min_size = (20, 20)
min_size = (2, 2)
image_scale = 2
haar_scale = 1.2
min_neighbors = 1
#min_neighbors = 2
haar_flags = 0

def detect_and_draw(img, cascade, result_name, input_name):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
			       cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        #print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            #print "found a face!"
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the 
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                #cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                
                cropped = cv.CreateImage((int(w * image_scale), int(h * image_scale)), img.depth, img.nChannels)
                src_region = cv.GetSubRect(img, (int(x * image_scale), int(y * image_scale), int(w * image_scale), int(h * image_scale)))
                cv.Copy(src_region, cropped)
                #if int(w * image_scale) >= 60 and int(w * image_scale) >= 60:
                print "saving image from {0} to {1}".format(input_name, result_name)
                cv.SaveImage(result_name,cropped)

    #cv.ShowImage("result", img)

if __name__ == '__main__':
    cascade_type = 'mcs_eyepair_big'
    #cascade_type = 'profileface'
    image_dir = 'test'
    #image_dir = 'fg-net'
    image_type = 'jpg'
    #image_type = 'JPG'
    cascade = cv.Load("haarcascades/haarcascade_{0}.xml".format(cascade_type))
    ctr = 1
    for input_name in glob.glob("images/{0}/*.{1}".format(image_dir, image_type)):
        image = cv.LoadImage(input_name, 1)
        #age = (input_name[18:20])
        #age = (input_name[14:16])
        age = (input_name[12:14])
        #result_name = "{0}_{1}_output.jpg".format(input_name, cascade_type)
        result_name = "images/output/{0}_{1}.jpg".format(age, ctr)
        ctr = ctr + 1
        #print "Cropping face from {0}...".format(input_name)
        detect_and_draw(image, cascade, result_name, input_name)
