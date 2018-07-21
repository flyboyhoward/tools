# Description:
# write number into file 
#########################################

import numpy as np
import os
import re 
import argparse
from PIL import Image
import scipy
from scipy.signal import *
import cv2


def main():

    test_txt = '/home/wwh/Desktop/VisDrone2018-VID-val/test.txt'

    myf = open(test_txt,'a')
    image_filenames = list(range(0,2846))

    for image_filename in image_filenames:
        image_filename = str(image_filename)
        image_filename = image_filename.zfill(6)
        myf.write(image_filename + '\n')

    myf.close()
        

if __name__=='__main__':
    main()
