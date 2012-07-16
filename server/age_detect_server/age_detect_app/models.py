# encoding: utf-8
from django.db import models
import json
import numpy as np
import cv
import cv2
import math
import glob
import os
import sys
import logging
from PyML import *
from PyML.classifiers.svm import SVR
from PyML.classifiers.svm import loadSVM


class UploadedImage(models.Model):
    #training data for SVR to generate age
    training_data_file = "training_data/training_data.data"
    image_upload_dir = "tmp/uploads"
    image_process_dir = "tmp/processing"
    image_results_dir = "tmp/results"
    udid = 0
    file = ''
    
    
    s1_inputs = [
        [5,2.0,2.5],#filter size, sigma, lambda
        [7,2.8,3.5],
        [9,3.6,4.6],
        [11,4.5,5.6],
        [13,5.4,6.8],
        [15,6.3,7.9],
        [17,7.3,9.1],
        [19,8.2,10.3],
        [21,9.2,11.5],
        [23,10.2,12.7],
        [25,11.3,14.1],
        [27,12.3,15.4],
        [29,13.4,16.8],
        [31,14.6,18.2],
        [33,15.8,19.7],
        [35,17.0,21.2]
    ]
    
    c1_inputs = [
        [6,5,7],#6x6 pools filters 5 and 7
        [8,9,11],
        [10,13,15],
        [12,17,19],
        [14,21,23],
        [16,25,27],
        [18,29,31],
        [20,33,35],
    ]
    
    pos_th_arr = [0,45,90,135] #orientations for s_1 step
    pos_psi = 90
    
    def handle_uploaded_file(self, udid, f):
        self.file = "{0}/{1}.jpg".format(self.image_upload_dir, udid)
        self.udid = udid
        with open(self.file, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    
    def get_age(self):
        self.S1()
        self.C1()
        return int(round(self.guess_age()))
        
    
    def to_json(self):
        age = self.get_age()
        result = {}
        result['age'] = age
        return json.dumps(result)
    
    
    #get the mean of a list of numbers
    def mean(self, numberList):
        if len(numberList) == 0:
            return float('nan')
        floatNums = [float(x) for x in numberList]
        return sum(floatNums) / len(numberList)

    #turns [[1,2][3,4]] to [1,2,3,4]
    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result

    #creates kernel image for s1 stage
    def mkKernel(self, ks, sig, th , lm, ps):
        if not ks % 2:
            exit(1)
        theta = th * np.pi/180.
        psi = ps * np.pi/180.
        xs = np.linspace(-1.,1.,ks)
        ys = np.linspace(-1.,1.,ks)
        lmbd = np.float(lm)
        x,y = np.meshgrid(xs,ys)
        sigma = np.float(sig)/ks
        x_theta = x * np.cos(theta) + y * np.sin(theta)
        y_theta = -x * np.sin(theta) + y * np.cos(theta)
        #return np.array(np.exp(-0.5*(x_theta**2 + 0.3*y_theta**2)/sigma**2)*np.cos(2*np.pi*x_theta/lmbd + psi),dtype=np.float32)
        return np.array(np.exp(-0.5*(x_theta**2 + y_theta**2)/sigma**2)*np.cos(2*np.pi*x_theta/lmbd + psi),dtype=np.float32)

    #save s1 image for further processing
    def Process_S1(self, im, src_f, case):
        filter_size = case[0]
        pos_sigma = case[1]
        pos_lm = case[2]
        #kernel size is the number of columns (width) divided by the filter size
        kernel_size = int(math.floor(im.cols/filter_size))
        if not kernel_size % 2:
            kernel_size += 1
        sig = pos_sigma
        #lm = 0.5+pos_lm/100.
        lm = pos_lm
        for pos_th in self.pos_th_arr:
            th = pos_th
            ps = self.pos_psi
            kernel = self.mkKernel(kernel_size, sig, th, lm, ps )
            #kernelimg = kernel/2.+0.5
            kernelimg = kernel
            dest = cv2.filter2D(src_f, cv2.CV_32F,kernel)
            n = np.asarray(dest)
            output_file = "{0}/{1}_{2}_{3}.jpg".format(self.image_process_dir, self.udid, str(filter_size), str(pos_th))
            cv.SaveImage(output_file, cv.fromarray(dest*255))

    #apply s1 step to all images in database
    def S1(self):
        logging.warning("Creating gabor-filtered images for {0}".format(self.file))
        image = cv2.imread(self.file, 1)
        im = cv.LoadImageM(self.file)
        src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        src_f = np.array(src, dtype=np.float32) / 255.
        for case in self.s1_inputs:
            self.Process_S1(im, src_f, case)
    
    #given 2 arrays of same length, returns greater value at each position
    def max_values(self, src_1, src_2):
        ret_arr = src_1
        rows = len(src_1)
        if len(src_2) != rows:
            #arrays must be same length
            exit(1)
        for i in range(0, rows):
            row_src_1 = src_1[i]
            row_src_2 = src_2[i]
            ret_col = []
            cols = len(row_src_1)
            if len(row_src_2) != cols:
                #arrays must be same length
                exit(1)
            for j in range(0, cols):
                if row_src_1[j] > row_src_2[j]: 
                    ret_col.append(row_src_1[j])
                else:
                    ret_col.append(row_src_2[j])
            ret_arr[i] = ret_col
        return ret_arr
    
    #for sampling c values, returns the standard deviation at a given region
    def std_at(self, start_row, start_col, kernel_size, src_f):
        area_rows = src_f[start_row:start_row+kernel_size]
        area = []
        for row in area_rows:
            area_cols = row[start_col:start_col+kernel_size]
            area.append(area_cols)
        #get all area pixels as 1-dimensional array
        area_pixels = self.flatten(area)
        #get the average of all pixels in the area
        avg = self.mean(area_pixels)
        #calculate the standard deviation for all pixels in area
        area_pixels_squared = sum(pixel**2 for pixel in area_pixels)
        std = math.sqrt( (area_pixels_squared/len(area_pixels)) - avg**2 )
        return std
    
    def Process_C1(self, kernel_size, src_f):
        c_values = []
        for start_row in range(0, len(src_f), kernel_size/2) :
            for start_col in range(0, len(src_f[0]), kernel_size/2):
                #print "{0},{1}".format(start_row,start_col)
                c_values.append(self.std_at(start_row, start_col, kernel_size, src_f))
        return c_values
        
    
    def C1(self):
        file_name = "{0}/{1}.data".format(self.image_results_dir, self.udid)
        f = open(file_name, 'w')
        logging.warning("Creating data matrix for {0}...".format(self.file))
        
        for case in self.c1_inputs:
            pool_grid_size = case[0]
            for rotation in self.pos_th_arr:
                s1_img1 = "{0}/{1}_{2}_{3}.JPG".format(self.image_process_dir, self.udid, case[1], rotation)
                s1_img2 = "{0}/{1}_{2}_{3}.JPG".format(self.image_process_dir, self.udid, case[2], rotation)
                image1 = cv2.imread(s1_img1,1);
                src1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                src_f1 = np.array(src1, dtype=np.float32) / 255.
                image2 = cv2.imread(s1_img2,1);
                src2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
                src_f2 = np.array(src2, dtype=np.float32) / 255.
                #first, the MAX pooling is performed on the 2 maps resulting in a maximum map
                src_max = self.max_values(src_f1, src_f2)
                #then the "STD" operation is performed on the max map using the c1 pool grid size
                kernel_size = int(math.floor(len(src_max[0])/pool_grid_size))
                c_values = self.Process_C1(kernel_size, src_max)
                f.write(",".join([str(x) for x in c_values]))
                f.write(",")
            
            
            f.write(str(100))#set 100 as age (not using this, since we're not training anymore)
            f.write("\n")
        
        f.close()
        
    def guess_age(self):
        data = SparseDataSet(self.training_data_file, labelsColumn = -1, numericLabels = True)
        s = SVR()
        s.train(data)
        test_data = SparseDataSet("{0}/{1}.data".format(self.image_results_dir, self.udid), labelsColumn = -1, numericLabels = True)
        results = s.test(test_data)
        predicted_results = results[0].Y
        actual_results = results[0].givenY
        return predicted_results[0]
        #total = 0
        #for i in range(0, len(predicted_results)):
        #    total = total + abs(int(predicted_results[i]-actual_results[i]))
        #    print "{0},{1} ({2})".format(str(int(predicted_results[i])), str(int(actual_results[i])), str(int(predicted_results[i]-actual_results[i])))
        #avg = total / len(predicted_results)
        #print avg
    
    #remove all files used in processing
    def cleanup(self):
        for file in glob.glob("{0}/{1}*.jpg".format(self.image_process_dir, self.udid)):
            os.remove(file)
        for file in glob.glob("{0}/{1}.data".format(self.image_results_dir, self.udid)):
            os.remove(file)
        return True
        
