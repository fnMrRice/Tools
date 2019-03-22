# -*- coding: utf-8 -*-
from struct import unpack,pack
import os
OS='Win'

def divideWs2(file,outbin='',outtxt=''):
    fp=open(file,'rb')
    if ''==outbin:
        fb=open(file+'.bin','wb+')
    else:
        fb=open(outbin,'wb+')
    if ''==outtxt:
        ft=open(file+'.txt','wb+')
    else:
        ft=open(outtxt,'wb+')

    cont=fp.read()
    fp.close()

    index=0
    Text_flag=0
    Quat_flag=0
    Name_flag=0
    while index<len(cont):
        if 0==Name_flag:
            if b'%LC'==cont[index:index+3]:
                fb.write(b'%LC')
                ft.write(b'---- ')
                index+=3
                Name_flag=1
                continue
        if 1==Name_flag:
            if b'\x00'!=cont[index] and 0!=cont[index]:
                ft.write(pack('B',cont[index]))
                index+=1
                continue
            else:
                Name_flag=0
                fb.write(pack('B',cont[index]))
                ft.write(b' ----\n')
                index+=1
                continue
        if 0==Text_flag:
            if b'char\x00'==cont[index:index+5]:
                fb.write(b'char\x00')
                Text_flag=1
                index+=5
                continue
            fb.write(pack('B',cont[index]))
            index+=1
            continue
        if 1==Text_flag:
            if b'%K'==cont[index:index+2]:
                fb.write(b'%K')
                Text_flag=0
                index+=2
                ft.write(b'\n\n')
                continue
            if b'\\d'==cont[index:index+2]:
                if 0==Quat_flag:
                    ft.write(b'[')
                    Quat_flag=1
                elif 1==Quat_flag:
                    ft.write(b']')
                    Quat_flag=0
                index+=2
                continue
            if b'\\n'==cont[index:index+2]:
                ft.write(b'\n')
                index+=2
                continue
            
            ft.write(pack('B',cont[index]))
            index+=1
            continue
    fb.close()
    ft.close()

def makeWs2(txt,bin,output):
    fb=open(bin,'rb')
    ft=open(txt,'r',encoding='utf-8')
    fp=open(output,'wb+')
    cont=fb.read()
    text=ft.readlines()
    fb.close()
    ft.close()

    index=0
    txt_index=0
    while index<len(cont) and txt_index<len(text):
        if b'%LC'==cont[index:index+3]:
            #print(1)
            fp.write(b'%LC')
            index+=3
            while txt_index<len(text) and text[txt_index].replace('\n','')=='':
                txt_index+=1
            if '---- '==text[txt_index][:5] and ' ----'==text[txt_index].replace('\n','')[-5:]:
                fp.write(text[txt_index].replace('\n','')[5:-5].encode())
                txt_index+=1
            else:
                print(text[txt_index][-5:])
                print('Text in line %d doesn\'t match.'%txt_index)
                exit(1)
            continue
        if b'char\x00'==cont[index:index+5]:
            fp.write(b'char\x00')
            index+=5
            while txt_index<len(text) and text[txt_index].replace('\n','')=='':
                txt_index+=1
            to_write=text[txt_index].replace('[','\\d').replace(']','\\d').replace('\n','')
            txt_index+=1
            while txt_index<len(text) and text[txt_index].replace('\n','')!='':
                to_write+='\\n'+text[txt_index].replace('[','\\d').replace(']','\\d').replace('\n','')
                txt_index+=1
            fp.write(to_write.encode())
            continue
        fp.write(pack('B',cont[index]))
        index+=1
    fp.close()

def left(ch):
    if tuple==type(ch):
        ch=ch[0]
    return ((ch<<1)|(ch>>7))&0xFF
def right(ch):
    if tuple==type(ch):
        ch=ch[0]
    return (ch>>1)|((ch&1)<<7)&0xFF

def binaryRotate(input,bit,output=''):
    if str==type(input):
        fp=open_or_die(input,'rb')
        cont=fp.read()
        fp.close()
    elif bytes==type(input):
        cont=input
    else:
        raise TypeError('Input type invalid.')
    if bit<0:
        bit=(-bit)%8
        ROT=1
    else:
        ROT=0
        bit=bit%8
    if ''==output and str==type(input):
        fn=os.path.join(os.path.split(input)[0],'dec_'+os.path.split(input)[1])
    elif ''==output and bytes==type(input):
        fn=False
    else:
        fn=output
    if fn:
        fps=open(fn,'wb+')
    data=b''
    for ch in cont:
        for i in range(bit):
            ch=right(ch) if 0==ROT else left(ch)
        if fn:
            fps.write(pack('B',ch))
        data+=pack('B',ch)
    if fn:
        fps.close()
    return data

def open_or_die(fn,arg='rb'):
    try:
        return open(fn,arg)
    except:
        raise IOError('File open failed.')

def filePath(fn):
    if bytes==type(fn):
        fn=fn.decode()
    if str==type(fn):
        return os.path.split(fn)[0]
    else:
        raise TypeError()

def fileBaseName(fn):
    if bytes==type(fn):
        fn=fn.decode()
    if str==type(fn):
        return os.path.split(fn)[1]
    else:
        raise TypeError()

def fileBaseNameWithoutExtension(fn):
    if bytes==type(fn):
        fn=fn.decode()
    if str==type(fn):
        return '.'.join(fileBaseName(fn).split('.')[:-1])
    else:
        raise TypeError()

def fileExt(fn):
    if bytes==type(fn):
        fn=fn.decode()
    if str==type(fn):
        return fileBaseName(fn).split('.')[-1]
    else:
        raise TypeError()

def writeFile(source,begin,size,dest):
    cur=source.tell()
    source.seek(begin)
    if 'ws2'==fileExt(dest):
        binaryRotate(source.read(size),2,dest+'_autodecode')
    else:
        fp=open_or_die(dest,'wb+')
        fp.write(source.read(size))
        fp.close()
    source.seek(cur)

def unpackArc(FileName,SavePath='./'):
    fp=open_or_die(FileName,'rb')
    NameOnly=fileBaseNameWithoutExtension(FileName)
    if SavePath[-1]=='/' or SavePath[-1]=='\\':
        Path=SavePath+NameOnly
    else:
        Path=SavePath+'/'+NameOnly
    if not os.path.exists(Path):
        os.makedirs(Path)
    else:
        if not os.path.isdir(Path):
            Path+='.unpack'
            os.makedirs(Path)
    if b'PackFile    ' == fp.read(0x0C):
        is_typeA(fp,Path)
    else:
        fp.seek(0)
        is_typeB(fp,Path)

def is_typeA(fp,Path):
    FileCount = unpack('I', fp.read(4))[0]
    FileInfos=[]
    print('Find %d Files'%FileCount)
    for i in range(FileCount):
        fp.seek(0x10+i*0x20)
        #print(fp.read(0x10))
        fp.seek(0x10+i*0x20)
        FileName=fp.read(0x10).decode().replace('\0','')
        offset=unpack('I',fp.read(4))[0]
        FileSize=unpack('I',fp.read(4))[0]
        fp.read(8)
        FileInfos.append({'name':FileName,'offset':offset,'size':FileSize})
        #print(FileName)
    index=1
    if not os.path.exists(Path):
        os.makedirs(Path)
    for f in FileInfos:
        fp.seek(FileCount*0x20+0x10+f['offset'])
        data=fp.read(f['size'])
        print('Unpacking File %s (%d of %d)'%(f['name'],index,FileCount))
        name=Path+f['name']
        if 'Win'==OS:
            name=name.replace('/','\\')
        else:
            name=name.replace('\\','/')
        fp.seek(FileCount*0x20+0x10+f['offset']+0x40)
        if b'OggS'==fp.read(4):
            name+='.ogg'
            fp.seek(FileCount*0x20+0x10+f['offset']+0x08)
            size=unpack('I',fp.read(4))[0]
            fp.seek(FileCount*0x20+0x10+f['offset']+0x40)
            data=fp.read(size)
        out=open(name,'wb+')
        #print(Path)
        out.write(data)
        out.close()
        index+=1
    fp.close()
	
def is_typeB(fp,savedir):
    fp.seek(0)
    FILE_COUNT=unpack('I',fp.read(4))[0]
    FILE_OFFSET_BEGIN=unpack('I',fp.read(4))[0]+0x08
    
    for fileIndex in range(1,FILE_COUNT+1):
        size = unpack('I',fp.read(4))[0]
        offset=unpack('I',fp.read(4))[0]
        name=b''
        temp=fp.read(2)
        while b'\x00\x00' != temp:
            name+=temp
            temp=fp.read(2)
        name=name.decode('utf-16')
        
        writeFile(fp,FILE_OFFSET_BEGIN+offset,size,'%s/%s'%(savedir,name))
        print('Get file: %s (%d of %d)'%('%s/%s'%(savedir,name),fileIndex,FILE_COUNT))

def pack_typeB(dir,savefile):
    files=list(os.walk(dir))
    basedir_len=len(files[0][0])
    file_info=b'\x00\x00\x00\x00\x00\x00\x00\x00'
    file_count=0
    CUR_OFFSET=0
    for i in files:
        if len(i[0])>basedir_len:
            dire=(i[0][basedir_len+1:]+'/').replace('\\','/')
        else:
            dire=''
        for fn in i[2]:
            size=os.path.getsize(os.path.join(i[0],fn))
            file_info+=pack('I',size)+pack('I',CUR_OFFSET)
            CUR_OFFSET+=size
            file_info+=(dire+fn).encode('utf-16')[2:]+b'\x00\x00'
            file_count+=1
    FILE_OFFSET_START=len(file_info)
    file_info=pack('I',file_count)+pack('I',len(file_info)-8)+file_info[8:]

    print(savefile)
    fp=open(savefile,'wb+')
    fp.write(file_info)
    for i in files:
        dire=(i[0][basedir_len+1:]+'/').replace('\\','/')
        for fn in i[2]:
            f=os.path.join(i[0],fn)
            temp=open(os.path.join(i[0],fn),'rb')
            print('Catch file: %s'%f)
            if 'ws2'==fileExt(f):
                fp.write(binaryRotate(temp.read(),-2))
            else:
                fp.write(temp.read())
            temp.close()
    fp.close()
        
'''
struct ARC_HDR {
    char[0x0B]="PackFile    ";
    unsigned int FileCount;
    [FileCount] FileInfos;
};

struct ARC_INF {
    char[0x10] FileName;
    unsigned int offsetBegin;
    unsigned int FileSize;
};

// Start from FileCount*0x20+0x10;
'''

def printHelp():
        print(
'''This program is used to do things with *.arc file.')
Usage:   %s unpack input_arc output_dir
         %s pack input_dir output_arc
         %s divide input_ws2 output_bin output_txt
         %s mix input_bin input_txt output_ws2
'''%('python '+args[0],'python '+args[0],'python '+args[0],'python '+args[0]))

if '__main__'==__name__:
    import sys
    args=sys.argv
    if 1==len(args):
        printHelp()
        exit(0)
    if 'unpack'==args[1] and 4==len(args):
        unpackArc(args[2],args[3])
    elif 'pack'==args[1] and 4==len(args):
        pack_typeB(args[2],args[3])
    elif 'divide'==args[1] and 5==len(args):
        divideWs2(args[2],args[3],args[4])
    elif 'mix'==args[1] and 5==len(args):
        makeWs2(args[3],args[2],args[4])
    else:
        printHelp()
    #pack_typeB('D:\\Games\\UnpackedFiles\\Chip1','D:\\Games\\UnpackedFiles\\Chip1.arc')