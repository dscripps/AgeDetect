# encoding: utf-8
import numpy as np
import cv
import cv2
import math
import glob
import os
import sys
from PyML import *
from PyML.classifiers.svm import SVR
from PyML.classifiers.svm import loadSVM

#kernel size = image width/filter width?
#kernel_size = 21
#aspect ratio 2??? 
#orientation th
#effective width sigma
#wavelength lambda
#filter size 

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

pos_th_arr = [0,45,90,135] #0, 45, 90, 135
kernel_size = 0
pos_psi = 90


#get the mean of a list of numbers
def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

#turns [[1,2][3,4]] to [1,2,3,4]
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

#creates kernel image for s1 stage
def mkKernel(ks, sig, th , lm, ps):
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
def Process_S1(image_file, im, src_f, case):
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
    for pos_th in pos_th_arr:
        th = pos_th
        ps = pos_psi
        kernel = mkKernel(kernel_size, sig, th, lm, ps )
        #kernelimg = kernel/2.+0.5
        kernelimg = kernel
        dest = cv2.filter2D(src_f, cv2.CV_32F,kernel)
        n = np.asarray(dest)
        output_file = "../../output/s1/{0}_{1}_{2}.jpg".format(image_file, str(filter_size), str(pos_th))
        cv.SaveImage(output_file, cv.fromarray(dest*255))

#apply s1 step to all images in database
def S1():
    for image_file in glob.glob("*.jpg"):
    #for image_file in glob.glob("00_143.jpg"):
        #file_path = "fg-net/images/{0}".format(image_file)
        file_path = image_file
        print "Processing {0}".format(file_path)
        image = cv2.imread(file_path, 1)
        im = cv.LoadImageM(file_path)
        src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        src_f = np.array(src, dtype=np.float32) / 255.
        for case in s1_inputs:
            Process_S1(image_file, im, src_f, case)

#given 2 arrays of same length, returns greater value at each position
def max_values(src_1, src_2):
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
def std_at(start_row, start_col, kernel_size, src_f):
    area_rows = src_f[start_row:start_row+kernel_size]
    area = []
    for row in area_rows:
        area_cols = row[start_col:start_col+kernel_size]
        area.append(area_cols)
    #get all area pixels as 1-dimensional array
    area_pixels = flatten(area)
    #get the average of all pixels in the area
    avg = mean(area_pixels)
    #calculate the standard deviation for all pixels in area
    area_pixels_squared = sum(pixel**2 for pixel in area_pixels)
    std = math.sqrt( (area_pixels_squared/len(area_pixels)) - avg**2 )
    return std

def Process_C1(kernel_size, src_f):
    c_values = []
    for start_row in range(0, len(src_f), kernel_size/2) :
        for start_col in range(0, len(src_f[0]), kernel_size/2):
            #print "{0},{1}".format(start_row,start_col)
            c_values.append(std_at(start_row, start_col, kernel_size, src_f))
    return c_values
    

def C1(test_set):
    file_name = "../../output/c1/{0}.data".format(test_set)
    f = open(file_name, 'w')
    for image_file in glob.glob("*.jpg"):
        print "Processing {0}...".format(image_file)
        age = int(image_file[0:2])
        
        for case in c1_inputs:
            case = c1_inputs[0]
            pool_grid_size = case[0]
            for rotation in ['0', '45', '90', '135']:
            #for rotation in ['0']:
                s1_img1 = "../../output/s1/{0}_{1}_{2}.JPG".format(image_file, case[1], rotation)
                s1_img2 = "../../output/s1/{0}_{1}_{2}.JPG".format(image_file, case[2], rotation)
                image1 = cv2.imread(s1_img1,1);
                src1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                src_f1 = np.array(src1, dtype=np.float32) / 255.
                image2 = cv2.imread(s1_img2,1);
                src2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
                src_f2 = np.array(src2, dtype=np.float32) / 255.
                #first, the MAX pooling is performed on the 2 maps resulting in a maximum map
                src_max = max_values(src_f1, src_f2)
                #then the "STD" operation is performed on the max map using the c1 pool grid size
                kernel_size = int(math.floor(len(src_max[0])/pool_grid_size))
                c_values = Process_C1(kernel_size, src_max)
                f.write(",".join([str(x) for x in c_values]))
                f.write(",")
        
        
        f.write(str(age))
        f.write("\n")
    
    f.close()
    
#def train(test_set):
#    data_file = "../../output/c1/faces_google.data"
#    data = SparseDataSet(data_file, labelsColumn = -1, numericLabels = True)
#    s = SVR()
#    s.train(data)
#    test_data = SparseDataSet("../../output/c1_test/{0}.data".format(test_set), labelsColumn = -1, numericLabels = True)
#    results = s.test(test_data)
#    predicted_results = results[0].Y
#    actual_results = results[0].givenY
#    total = 0
#    for i in range(0, len(predicted_results)):
#        total = total + abs(int(predicted_results[i]-actual_results[i]))
#        print "{0},{1} ({2})".format(str(int(predicted_results[i])), str(int(actual_results[i])), str(int(predicted_results[i]-actual_results[i])))
#    avg = total / len(predicted_results)
#    print avg
    



if __name__ == '__main__':
    test_set = sys.argv[1]
    os.chdir("input/{0}".format(test_set))
    S1()
    C1(test_set)
    #train(test_set)
