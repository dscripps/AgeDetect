#!/usr/bin/python
import sys
import os
import cv2.cv as cv
import cv2
import numpy as np
from optparse import OptionParser
import glob
import sys, math, Image
from django.db import models
from age_detect import settings



class FeaturesExtractor(models.Model):    
    
    def Distance(self, p1,p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx*dx+dy*dy)
    
    def ScaleRotateTranslate(self, image, angle, center = None, new_center = None, scale = None, resample=Image.BICUBIC):
        if (scale is None) and (center is None):
            return image.rotate(angle=angle, resample=resample)
        nx,ny = x,y = center
        sx=sy=1.0
        if new_center:
            (nx,ny) = new_center
        if scale:
            (sx,sy) = (scale, scale)
        cosine = math.cos(angle)
        sine = math.sin(angle)
        a = cosine/sx
        b = sine/sx
        c = x-nx*a-ny*b
        d = -sine/sy
        e = cosine/sy
        f = y-nx*d-ny*e
        return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=resample)
    
    def CropFace(self, image, eye_left=(0,0), eye_right=(0,0), offset_pct=(0.2,0.2), dest_sz = (70,70)):
        # calculate offsets in original image
        offset_h = math.floor(float(offset_pct[0])*dest_sz[0])
        offset_v = math.floor(float(offset_pct[1])*dest_sz[1])
        # get the direction
        eye_direction = (eye_right[0] - eye_left[0], eye_right[1] - eye_left[1])
        # calc rotation angle in radians
        rotation = -math.atan2(float(eye_direction[1]),float(eye_direction[0]))
        # distance between them
        dist = self.Distance(eye_left, eye_right)
        # calculate the reference eye-width
        reference = dest_sz[0] - 2.0*offset_h
        # scale factor
        scale = float(dist)/float(reference)
        # rotate original around the left eye
        image = self.ScaleRotateTranslate(image, center=eye_left, angle=rotation)
        # crop the rotated image
        crop_xy = (eye_left[0] - scale*offset_h, eye_left[1] - scale*offset_v)
        crop_size = (dest_sz[0]*scale, dest_sz[1]*scale)
        image = image.crop((int(crop_xy[0]), int(crop_xy[1]), int(crop_xy[0]+crop_size[0]), int(crop_xy[1]+crop_size[1])))
        # resize it
        image = image.resize(dest_sz, Image.ANTIALIAS)
        return image
    
    
    
    def detect_and_draw(self, result_name, input_name, is_upload):
        
        img_orig = cv.LoadImage(input_name, 1)
        
        if is_upload:
        #if True:
            #from iphone, rotate image first
            img = cv.CreateImage((img_orig.height,img_orig.width), img_orig.depth, img_orig.channels) # transposed image
            cv.Transpose(img_orig,img)
            cv.Flip(img,img,flipMode=1)
        else:
            img = img_orig
        #self.save_image(timg, input_name, result_name + "rotated.jpg")
        
        
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
        
        cascade = cv.Load("{0}training_data/haarcascades/haarcascade_frontalface_alt2.xml".format(settings.PROJECT_ROOT))
        eyeCascade = cv.Load("{0}training_data/haarcascades/haarcascade_eye.xml".format(settings.PROJECT_ROOT))
        #noseCascade = cv.Load("training_data/haarcascades/haarcascade_mcs_nose.xml")
        
        # allocate temporary images
        gray = cv.CreateImage((img.width,img.height), 8, 1)
        small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                       cv.Round (img.height / image_scale)), 8, 1)
    
        # convert color input image to grayscale
        cv.CvtColor(img, gray, cv.CV_BGR2GRAY)
        
    
        # scale input image for faster processing
        cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
        
        #normalize the image
        #cv.EqualizeHist(small_img, small_img)
    
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        #print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        if faces:
            #print "found a face!"
            for ((x, y, w, h), n) in faces:
                #print "face!"
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
                        #print "eye!"
                        #figure out if this is the left eye or right eye
                        if left_eye is None:
                            left_eye = eye
                        elif eye[0][0] < left_eye[0]:
                            right_eye = left_eye
                            left_eye = eye
                        else:
                            right_eye = eye
                        #print "({0},{2}) w{1} h{3}".format(eye[0][0],eye[0][1],eye[0][0] + eye[0][2],eye[0][1] + eye[0][3])
                
                #fix eyes
                if left_eye and right_eye:
                    #if len(eyes) > 2:
                    if False:
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
                    #cv.Rectangle(img,
                    #     (left_eye_rect[0],left_eye_rect[1]),
                    #     (left_eye_rect[2],left_eye_rect[3]),
                    #     cv.RGB(255, 0, 0), 1, 8, 0
                    #)
                    right_eye_width = int(right_eye[0][2]*1.25)
                    right_eye_height = right_eye[0][3]
                    right_eye_rect = [
                        right_eye[0][0],
                        right_eye[0][1],
                        right_eye[0][0] + right_eye_width,
                        right_eye[0][1] + right_eye_height
                    ]
                    #cv.Rectangle(img,
                    #     (right_eye_rect[0],right_eye_rect[1]),
                    #     (right_eye_rect[2],right_eye_rect[3]),
                    #     cv.RGB(255, 0, 0), 1, 8, 0
                    #)
                    mouth_nose_width = int((right_eye[0][0] + right_eye[0][2] - left_eye[0][0]) * 0.8)
                    mouth_nose_height = left_eye[0][3]
                    mouth_nose_rect = [
                        left_eye[0][0] + int(left_eye[0][2]*.25),
                        bottom_y,
                        left_eye[0][0] + int(left_eye[0][2]*.25) + mouth_nose_width,
                        bottom_y + mouth_nose_height
                    ]
                    #draw nose/mouth area
                    #cv.Rectangle(img,
                    #    #start x, start y
                    #    #end x, end y
                    #    (mouth_nose_rect[0], mouth_nose_rect[1]),
                    #    (mouth_nose_rect[2], mouth_nose_rect[3]),
                    #    cv.RGB(255, 0, 0), 1, 8, 0
                    #)
                    forehead_width = right_eye[0][0] + right_eye[0][2] - left_eye[0][0]
                    forehead_height = left_eye[0][1]
                    forehead_rect = [
                        left_eye[0][0],
                        0,
                        left_eye[0][0] + forehead_width,
                        0 + forehead_height
                    ]
                    #draw forehead area
                    #cv.Rectangle(img,
                    #    #start x, start y
                    #    #end x, end y
                    #    (forehead_rect[0], forehead_rect[1]),
                    #    (forehead_rect[2], forehead_rect[3]),
                    #    cv.RGB(255, 0, 0), 1, 8, 0
                    #)
                    
                    #scale image
                    #thumbnail = cv.CreateMat(min_size[0], min_size[1], cv.CV_8UC3) 
                    #cv.Resize(img, thumbnail)
                    
                    #save different features
                    #self.save_image(img, input_name, result_name + "face.jpg")
                    #if is_upload:
                    if True:
                        cv.SetImageROI(img,
                             (pt1[0] + left_eye_rect[0], pt1[1] + left_eye_rect[1], left_eye_width, left_eye_height)
                             #(pt1[0] + left_eye_rect[0] + ((28-left_eye_width)/2), pt1[1] + left_eye_rect[1] + ((24-left_eye_height)/2), 28, 24)
                        )
                        thumbnail = cv.CreateMat(65, 85, cv.CV_8UC3)
                        cv.Resize(img, thumbnail)
                        self.save_image(thumbnail, input_name, result_name + "left_eye.jpg")
                        #self.save_image(img, input_name, result_name + "left_eye.jpg")
                    if is_upload:
                        cv.SetImageROI(img,
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
                    
                    
                    cv.SetImageROI(img,
                         (0,0,img.width,img.height)
                    )
                    self.save_image(img, input_name, result_name + "face_orig.jpg")
                    
                    
                    
                    image =  Image.open(result_name + "face_orig.jpg")
                    #image.save(result_name + "face2.jpg")
                    #self.CropFace(image, eye_left=(pt1[0] + left_eye_rect[0], pt1[1] + left_eye_rect[1]), eye_right=(pt1[0] + right_eye_rect[0], pt1[1] + right_eye_rect[1]), offset_pct=(0.1,0.1), dest_sz=(200,200)).save(result_name + "face2.jpg")
                    
                    self.CropFace(
                                  image, 
                                  eye_left=(pt1[0]+left_eye[0][0]+(left_eye[0][2]/2), pt1[1]+left_eye[0][1]+(left_eye[0][3]/2)), 
                                  eye_right=(pt1[0]+right_eye[0][0]+(right_eye[0][2]/2), pt1[1]+right_eye[0][1]+(right_eye[0][3]/2)), 
                                  offset_pct=(0.2,0.2), dest_sz=(50,50)).save(result_name + "face_aligned.jpg")
                    os.remove(result_name + "face_orig.jpg")
                    #68x116
                    #print left_eye_rect
                    #print pt1/image_scale
                    #print pt2/image_scale
                    
                    
                    
    
                    
    
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
        #cv.SaveImage(result_name,saved_gray)
        #cv.SaveImage(result_name,saved_image)