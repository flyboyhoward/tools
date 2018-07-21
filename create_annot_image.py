# Description:
# can load images and annotaions from vedio detection iamges files 
# change the form of anntation into we need
# read different sequences of iamges and reload into one folder randomly
# finally annotation files corresponding to iamges
#
# In this case:
# annotation form is 102,0,38,666,71,88,1,1,1,0 e.g
# each origin annotation file name is the same as sequence name
# random file named from random number 1-10000
# function parse_args() is useless, because I set them in the main function
# ########################################################################

import numpy as np
import os
import re 
import argparse
from PIL import Image
import scipy
from scipy.signal import *
import cv2
import random

def parse_args():
    parse = argparse.ArgumentParser(description='Draw ground truth bounding boxes.')
    parse.add_argument('--annots_dir', dest='annots_dir', help='Annotations directory')
    parse.add_argument('--images_dir', dest='images_dir', help='Images directory')
    parse.add_argument('--output_dir', dest='output_dir', help='Image output directory')

    args = parse.parse_args()
    return args


def load_gt_bbox(filepath,index_file,annot_readfilename):

    with open(annot_readfilename) as f:
        data = f.read()

    objs = re.findall('\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+', data)

    objs_str = str(objs)
    objs_list = objs_str.replace(',',' ')
    objs = re.findall('\d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+ \d+',objs_list)
    # print objs
    #print str(objs) + 'this is objs'
    nums_obj = len(objs)
    myf = open(filepath,'w')
    myf.close()

    for idx, obj in enumerate(objs):
        #print 'load',obj 
        info = re.findall('\d+', obj)
        catgr = int(info[7])
        index = int(info[0])
        
        myf = open(filepath,'a')
        if index == index_file:
            if catgr > 0 and catgr <12:
                #print 'obj catgory',str(catgr)
                #print 'write into',filepath,obj

                x1 = info[2]
                y1 = info[3]
                x2 = info[4]
                y2 = info[5]
                #print info
                myf.write(str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+
                    ',1,'+str(catgr)+','+str(info[8])+','+str(info[9])+'\n')
    myf.close()
    print 'Write annotation into: ',filepath

def main():
    args = parse_args()

    args.images_dir = '/home/wwh/Desktop/VisDrone2018-VID-val/sequences'
    args.annots_dir = '/home/wwh/Desktop/VisDrone2018-VID-val/ann'
    args.output_dir = '/home/wwh/Desktop/VisDrone2018-VID-val/Images'

    annotation_dir = '/home/wwh/Desktop/VisDrone2018-VID-val/annotations'
    i = 0
    population = list(range(0,2846))
    random_filenames = random.sample(population,2846)

    for image_foldername in os.listdir(args.images_dir):
   
        base_annotaionname = (image_foldername.strip().split('.'))[0]
        image_foldername = args.images_dir + '/' + image_foldername

        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print image_foldername
        print base_annotaionname
        print '...................................'

        for image_filename in os.listdir(image_foldername):
            random_filename = str(random_filenames[i])
            random_filename = random_filename.zfill(6)
            i = i + 1
            base_filename = (image_filename.strip().split('.'))[0]
            index_file = int(base_filename)
            print 'this is the ',index_file,' images in ',image_foldername,' folder'
            #load image
            im = Image.open(image_foldername + '/' + image_filename).convert('RGB')
            im = np.array(im).T
            im_copy = np.copy(im)
            #save image
            output_filepath = args.output_dir + '/' + random_filename + '.jpg'
            scipy.misc.imsave(output_filepath, im_copy.T)
            print 'Save image into: ' + output_filepath
            #wirte annotation
            annot_filename = random_filename + '.txt'
            annot_readfilename = annotation_dir + '/' + base_annotaionname + '.txt'
            gtBBs = load_gt_bbox(args.annots_dir + '/' + annot_filename,index_file,annot_readfilename)


if __name__=='__main__':
    main()
