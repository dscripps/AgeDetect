#!/usr/bin/python
import os
import sys
import glob
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "age_detect.settings")
from age_detect_app.models import FeaturesExtractor
from age_detect import settings



def get_age(input_name):
    name_arr = input_name.split('/')
    filename = name_arr[len(name_arr)-1]
    return filename[0:2]

#def get_ctr(input_name):
#    ctr = input_name[len(input_name)-5:len(input_name)-4]
#    return ctr


if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print "USAGE: features_extractor.py </path/to/input/images/> </path/to/output/folder/>"
        sys.exit()
        
    
    featuresExtractor = FeaturesExtractor()
    
    for file in glob.glob("{0}train/{1}*.jpg".format(settings.PROJECT_ROOT, sys.argv[2])):
        os.remove(file)
    #for input_name in glob.glob("{0}train/input/deleteme/*.jpg".format(settings.PROJECT_ROOT)):
    ctr = 0
    age = 0
    for input_name in glob.glob("{0}train/{1}*.jpg".format(settings.PROJECT_ROOT, sys.argv[1])):
        print input_name
        new_age = get_age(input_name)
        if age != new_age:
            ctr = 0
        age = new_age
        ctr = ctr + 1
        result_name = "{0}train/{1}{2}_{3}".format(settings.PROJECT_ROOT, sys.argv[2], age, ctr)
        featuresExtractor.detect_and_draw(result_name, input_name, False)
