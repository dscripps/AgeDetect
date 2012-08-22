#!/usr/bin/python
import sys
import os
import cv2.cv as cv
import cv2
from optparse import OptionParser
import glob
from django.db import models



class FeaturesExtractor(models.Model):
    
    
    def detect_and_draw(self, result_name, input_name):
        
        
        img = cv.LoadImage(input_name, 1)
        
        # Parameters for haar detection
        # From the API:
        # The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned 
        # for accurate yet slow object detection. For a faster operation on real video 
        # images the settings are: 
        # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
        # min_size=<minimum possible face size
        
        #face_size_coef = 2./3.
        face_size_coef = 1.
        min_size = (40,40)
        image_scale = 2
        haar_scale = 1.2
        #min_neighbors = 1
        min_neighbors = 2
        haar_flags = 0
        
        cascade = cv.Load("training_data/haarcascades/haarcascade_frontalface_alt2.xml")
        eyeCascade = cv.Load("training_data/haarcascades/haarcascade_eye.xml")
        #noseCascade = cv.Load("training_data/haarcascades/haarcascade_mcs_nose.xml")
        
        # allocate temporary images
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                       cv.Round (img.height / image_scale)), 8, 1)
    
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        
    
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        cv.EqualizeHist(small_img, small_img)
    
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
                
                pt1 = (int(x * image_scale) + int(w * (1-face_size_coef)), int(y * image_scale) + int(h * (1-face_size_coef)))
                pt2 = (int((x + w) * image_scale) - int(w * (1-face_size_coef)), int((y + h) * image_scale) - int(w * (1-face_size_coef)))
                
                
                #crop face area
                cv.SetImageROI(img, (pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]))
                
                # Detect the eyes
                eyes = cv.HaarDetectObjects(img, eyeCascade,
                    cv.CreateMemStorage(0),
                    haar_scale, min_neighbors,
                    haar_flags, (20,15)
                )
                
                left_eye = None
                right_eye = None
                # If eyes were found
                if eyes:
                    
                    # For each eye found
                    for eye in eyes:
                        #figure out if this is the left eye or right eye
                        if left_eye is None:
                            left_eye = eye
                        elif eye[0][0] < left_eye[0]:
                            right_eye = left_eye
                            left_eye = eye
                        else:
                            right_eye = eye
                        print "({0},{2}) w{1} h{3}".format(eye[0][0],eye[0][1],eye[0][0] + eye[0][2],eye[0][1] + eye[0][3])
                
                #fix eyes
                if left_eye and right_eye:
                    if len(eyes) > 2:
                        left_eye = None
                        right_eye = None
                    else:
                        if left_eye[0][0] > right_eye[0][0]:
                            tmp = left_eye
                            left_eye = right_eye
                            right_eye = tmp
                        if right_eye[0][0] <= left_eye[0][0] + left_eye[0][2]:
                            #right eye is inside left eye
                            left_eye = None
                            right_eye = None
                            
                if left_eye and right_eye:
    
                    #draw rectange around our real face ROI
                    
                    #see which eye is higher
                    top_y = 0
                    bottom_y = 0
                    if left_eye[0][1] < right_eye[0][1]:
                        top_y = left_eye[0][1]
                        bottom_y = right_eye[0][1] + right_eye[0][3]
                        nose_y = right_eye[0][1]
                    else:
                        top_y = right_eye[0][1]
                        bottom_y = left_eye[0][1] + left_eye[0][3]
                        nose_y = left_eye[0][1]
                    #cv.Rectangle(img,
                    #     (left_eye[0][0], top_y),
                    #     (right_eye[0][0] + right_eye[0][2], h * image_scale-3),
                    #     cv.RGB(255, 0, 0), 1, 8, 0
                    #)
                    
                    #draw eyes
                    left_eye_width = int(left_eye[0][2]*1.25)
                    left_eye_height = left_eye[0][3]
                    left_eye_rect = [
                        left_eye[0][0] - int(left_eye[0][2]*0.25),
                        left_eye[0][1],
                        left_eye[0][0] + left_eye[0][2],
                        left_eye[0][1] + left_eye_height
                    ]
                    cv.Rectangle(img,
                         (left_eye_rect[0],left_eye_rect[1]),
                         (left_eye_rect[2],left_eye_rect[3]),
                         cv.RGB(255, 0, 0), 1, 8, 0
                    )
                    right_eye_width = int(right_eye[0][2]*1.25)
                    right_eye_height = right_eye[0][3]
                    right_eye_rect = [
                        right_eye[0][0],
                        right_eye[0][1],
                        right_eye[0][0] + right_eye_width,
                        right_eye[0][1] + right_eye_height
                    ]
                    cv.Rectangle(img,
                         (right_eye_rect[0],right_eye_rect[1]),
                         (right_eye_rect[2],right_eye_rect[3]),
                         cv.RGB(255, 0, 0), 1, 8, 0
                    )
                    mouth_nose_width = int((right_eye[0][0] + right_eye[0][2] - left_eye[0][0]) * 0.8)
                    mouth_nose_height = left_eye[0][3]
                    mouth_nose_rect = [
                        left_eye[0][0] + int(left_eye[0][2]*.25),
                        bottom_y,
                        left_eye[0][0] + int(left_eye[0][2]*.25) + mouth_nose_width,
                        bottom_y + mouth_nose_height
                    ]
                    #draw nose/mouth area
                    cv.Rectangle(img,
                        #start x, start y
                        #end x, end y
                        (mouth_nose_rect[0], mouth_nose_rect[1]),
                        (mouth_nose_rect[2], mouth_nose_rect[3]),
                        cv.RGB(255, 0, 0), 1, 8, 0
                    )
                    forehead_width = right_eye[0][0] + right_eye[0][2] - left_eye[0][0]
                    forehead_height = left_eye[0][1]
                    forehead_rect = [
                        left_eye[0][0],
                        0,
                        left_eye[0][0] + forehead_width,
                        0 + forehead_height
                    ]
                    #draw forehead area
                    cv.Rectangle(img,
                        #start x, start y
                        #end x, end y
                        (forehead_rect[0], forehead_rect[1]),
                        (forehead_rect[2], forehead_rect[3]),
                        cv.RGB(255, 0, 0), 1, 8, 0
                    )
                    
                    
                    #cropped = cv.CreateImage((int(w * face_size_coef * image_scale), int(h * face_size_coef * image_scale)), img.depth, img.nChannels)
                    #src_region = cv.GetSubRect(img, (int(x * image_scale) + int(w * (1-face_size_coef)), int(y * image_scale) + int(h * (1-face_size_coef)), int(w * face_size_coef * image_scale), int(h * face_size_coef * image_scale)))
                    #cv.Copy(src_region, cropped)
                    
                    #scale image
                    #thumbnail = cv.CreateMat(min_size[0], min_size[1], cv.CV_8UC3) 
                    
                    
                    
                    #cv.Resize(img, thumbnail)
                    
                    #save different features
                    #cv.SetImageROI(img,
                    #     (pt1[0] + left_eye[0][0], pt1[1] + top_y, right_eye[0][0] + right_eye[0][2] - left_eye[0][0], h * image_scale - top_y)
                    #)
                    self.save_image(img, input_name, result_name + "face.jpg")
                    cv.SetImageROI(img,
                         #(pt1[0] + left_eye[0][0], pt1[1] + left_eye[0][1], left_eye[0][2], left_eye[0][3])
                         (pt1[0] + left_eye_rect[0], pt1[1] + left_eye_rect[1], left_eye_width, left_eye_height)
                    )
                    self.save_image(img, input_name, result_name + "left_eye.jpg")
                    cv.SetImageROI(img,
                         #(pt1[0] + right_eye[0][0], pt1[1] + right_eye[0][1], right_eye[0][2], right_eye[0][3])
                         (pt1[0] + right_eye_rect[0], pt1[1] + right_eye_rect[1], right_eye_width, right_eye_height)
                    )
                    self.save_image(img, input_name, result_name + "right_eye.jpg")
                    
                    #nose/mouth
                    cv.SetImageROI(img,
                        (pt1[0] + mouth_nose_rect[0], pt1[1] + mouth_nose_rect[1], mouth_nose_width, mouth_nose_height)
                    )
                    self.save_image(img, input_name, result_name + "nose_mouth.jpg")
                    
                    #forehead
                    cv.SetImageROI(img,
                        (pt1[0] + forehead_rect[0], pt1[1] + forehead_rect[1], forehead_width, forehead_height)
                    )
                    self.save_image(img, input_name, result_name + "forehead.jpg")
                    
                    
    
                    
    
        #cv.ShowImage("result", img)
    
    def save_image(self, img, input_name, result_name):
        
        print "saving image from {0} to {1}".format(input_name, result_name)
        
        #cv.SaveImage(result_name,thumbnail)
        cv.SaveImage(result_name,img)
        
        saved_image = cv.LoadImage(result_name, 1)
        
        saved_gray = cv.CreateImage((saved_image.width,saved_image.height), 8, 1)
        cv.CvtColor(saved_image, saved_gray, cv.CV_BGR2GRAY)
        
        #normalize colors
        normalized = cv.CreateImage((saved_image.width,saved_image.height), 8, 1)
        cv.EqualizeHist(saved_gray,normalized)
        
        cv.SaveImage(result_name,normalized)
    
    
#    if __name__ == '__main__':
#        #cascade_type = 'mcs_eyepair_big'
#        cascade_type = 'frontalface_alt2'
#        image_type = 'jpg'
#        ctr = 1
#        #remove previous results
#        for file in glob.glob("output/features/*.jpg"):
#            os.remove(file)
#        for input_name in glob.glob("input/before/*.{0}".format(image_type)):
#            print input_name
#            
#            ctr = ctr + 1
#            result_name = "output/features/{0}".format(ctr)
#            #ctr = ctr + 1
#            print "Cropping face from {0} to {1}...".format(input_name, result_name)
#            self.detect_and_draw(result_name, input_name)
