# coding:utf8
from chardet import detect
import os

def trans(txtFile):
    if not os.path.isfile(txtFile):
        raise RuntimeError('PathError')
        return False
    fp=open(txtFile,'rb')
    cont=fp.read()
    if detect(cont)['confidence']<0.9:
        raise RuntimeError('FileError')
        return False
    
    fp.close()

    fp=open(txtFile+'.bak','wb')
    fp.write(cont)
    fp.close()

    cont=cont.decode(detect(cont)['encoding']).encode('utf8')

    fp=open(txtFile,'wb')
    fp.write(cont)
    fp.close()

def transDir(file_dir,subdir=False):
    if not os.path.isdir(file_dir):
        raise RuntimeError('PathError')
    for root,dirs,files in os.walk(file_dir):
        for f in files:
            fPath=os.path.join(root,f)
            try:
                trans(fPath)
                print(fPath)
            except RuntimeError as e:
                print(e+': '+fPath)
        #print(files)

if '__main__'==__name__:
    transDir('E:\\GameUnpack\\まいてつ\\data\\scenario')