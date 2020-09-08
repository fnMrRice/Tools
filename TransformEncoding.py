# coding:utf8
from chardet import detect
import os


def trans(txtFile):
    if not os.path.isfile(txtFile):
        raise RuntimeError('PathError')
    cont = None
    with open(txtFile, 'rb') as fp:
        cont = fp.read()
        if detect(cont)['confidence'] < 0.9:
            raise RuntimeError('FileError')

    os.rename(txtFile, txtFile+'.bak')
    # fp = open(txtFile+'.bak', 'wb')
    # fp.write(cont)
    # fp.close()

    cont = cont.decode(detect(cont)['encoding']).encode('utf8')

    with open(txtFile, 'w+', encoding='utf-8') as fp:
        fp.write(cont)
    # fp = open(txtFile, 'wb')
    # fp.write(cont)
    # fp.close()


def transDir(file_dir, subdir=False):
    if not os.path.isdir(file_dir):
        raise RuntimeError('PathError')
    for root, dirs, files in os.walk(file_dir):
        for f in files:
            fPath = os.path.join(root, f)
            try:
                trans(fPath)
                print(fPath)
            except RuntimeError as e:
                print(e+': '+fPath)
        # print(files)


if '__main__' == __name__:
    transDir('E:\\GameUnpack\\まいてつ\\data\\scenario')
