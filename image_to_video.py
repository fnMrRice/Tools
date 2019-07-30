# -*- coding: utf-8 -*-

import argparse
import cv2
import os

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i,--input', dest='input', required=True,type=str,
                    help='Path of input directory.')
parser.add_argument('-o,--ouput', dest='output', required=True,type=str,
                    help='Path of output file.')
parser.add_argument('-c,--count', dest='count', required=True,type=int,
                    help='Count of the input image.')
parser.add_argument('-r,--frame-rate', dest='frame_rate', default=30,type=int,
                    help='Frame rate of output video.')
parser.add_argument('-s,--show-frame', dest='show', default=False,type=bool,
                    help='Set if you want to show the number of frame in the video.')
parser.add_argument('-e,--img_ext', dest='img_ext',type=str,
                    default='jpg',
                    help='Extension name of input image.')
args = parser.parse_args()

if '__main__'==__name__:
    rate=args.frame_rate
    ext=args.img_ext
    in_path=args.input
    out_path=args.output
    count=args.count
    ff=cv2.imread('%s/%d.%s'%(in_path,1,ext))
    size=(ff.shape[1],ff.shape[0])
    if (not ff.size):
        print('Please rename the input images like this: 1.%s, 2.%s,...'%(ext,ext))
    vw = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), rate,size)
    if (not vw.isOpened()):
        print('Unknown error occured. Please retry.')

    print('Video size: %dx%d@%.2f fps, total %.3fs'%(size[0],size[1],rate,count/rate))
    print('Writing to file, please wait.')
    counter=0
    for i in range(1,count+1):
        img  = cv2.imread('%s/%d.%s'%(args.input,i,args.img_ext))
        # print('%s/%d.%s'%(args.input,i,args.img_ext))
        if (not img.size):
            break
        # cv2.imshow('video',img)
        if (args.show):
            cv2.putText(img,'%d'%i,(0,size[1]),cv2.FONT_HERSHEY_PLAIN,2.0,(0,0,255),2)
        vw.write(img)
        counter+=1
    print('Total %d of %d images has been written to file.'%(counter,count))
    vw.release()