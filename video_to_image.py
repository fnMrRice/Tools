# -*- coding: utf-8 -*-

import argparse
import cv2
import os

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i,--input', dest='input', required=True,type=str,
                    help='Path of input file.')
parser.add_argument('-o,--ouput', dest='output', required=True,type=str,
                    help='Path of output directory.')
parser.add_argument('-s,--skip', dest='skip', default=0, type=int,
                    help='Get the frame each "skip" times.')
parser.add_argument('-e,--img_ext', dest='img_ext',type=str,
                    default='jpg',
                    help='Extension name of output image.')
args = parser.parse_args()

if '__main__'==__name__:
    cap=cv2.VideoCapture(args.input)
    if (not cap.isOpened()):
        print('File %s invalid.'%args.input)
    # 7 CV_CAP_PROP_FRAME_COUNT
    frame_count=cap.get(7)
    print('Total frame count is %d'%frame_count)
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    cur=0
    last=0
    assert args.skip>=0
    print('Start to extract frames, you can press q to quit at any time.')
    while cv2.waitKey(1)!=ord('q') or cur<frame_count:
        cur+=1
        if (cur-last!=args.skip+1):
            continue
        last=cur
        retval, img=cap.read()
        if retval:
            cv2.imshow('video',img)
            cv2.imwrite('%s/%d.%s'%(args.output,cur,args.img_ext),img)
        else:
            break
    cap.release()