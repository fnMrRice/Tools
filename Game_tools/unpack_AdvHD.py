# coding:utf-8
from struct import unpack,pack
import os
#from PIL import Image
SYS='Win'

'''
struct ArcFile{
    unsigned int FileCount;
    unsigned int FileInfoSize;
    FileInfo FileInfos[FileCount];
}
struct FileInfo{
    unsigned int FileSize;
    unsigned int OffsetWithFilrstFile;
    char *FileName; // UTF-16
}
'''

'''
Files of If My Heart Had Wings Steam Edition English:
    BGM.arc:             BGMs
    *Chip1.arc:          BGs
    *CHIP2.arc:          Common CGs, Ageha CGs
    *CHIP3.arc:          Asa CGs, Yoru CGs
    *CHIP4.arc:          Anim Effects
    *CHIP5.arc:          Kotori CGs
    *CHIP6.arc:          Amane CGs
        *.MOS in CGs:    Mosaic png File
    *Graphic.arc:        Anim Effects and Tachie File(.pna)
    *Rio.arc:            Game Script File
    Script.arc:          lua Scripts
    SE.arc:              Sound Effect
    SysGraphic.arc:      wtf PNA files
    SysVoice.arc:        System Sound Effects
    *Voice.arc:          Voices
'''

def UnpackArc(FileName,SaveDir='/',HeadOnly=False,log=True):
    # Can be used in If My Heart Had Wings Steam Edition
    try:
        fp=open(str(FileName),'rb')
    except:
        if log:
            print("Error when reading file %s"%FileName)
        return False
    
    # Get File Info
    Count=unpack("I",fp.read(0x04))[0]
    InfoSize=unpack("I",fp.read(0x04))[0]
    if log:
        print("Unpacking: %s, %d files in it."%(FileName,Count))
    offset=0x08
    HeadInfos=[]

    # Handle Dir Name
    if 'Linux' is SYS:
        Name=str(SaveDir).replace('\\','/')
        if '/'!=Name[-1]:
            Name+='/'
    elif 'Win' is SYS:
        Name=str(SaveDir).replace('/','\\')
        if '\\'!=Name[-1]:
            Name+='\\'
    else:
        return
    if not os.path.exists(Name):
        os.makedirs(Name)
    
    # Get and Write File Contents
    for i in range(Count):
        FileSize=unpack("I",fp.read(0x04))[0]
        OffsetTo=unpack("I",fp.read(0x04))[0]+InfoSize+0x08

        Ffn=""
        while True:
            cc=fp.read(0x02).decode("utf16")
            if '\0'==cc:
                break
            Ffn+=cc
        _Name=Name+Ffn
        if log:
            print("  File: %s"%_Name)
        HeadInfos.append({'Name':Ffn,'Size':FileSize})

        if not HeadOnly:
            offset=fp.tell()
            fp.seek(OffsetTo)
            fpp=open(_Name,'wb+')
            fpp.write(fp.read(FileSize))
            fpp.close()

            if 'ws2'==_Name.split('.')[-1]:
                decryptWs2(_Name)
                if log:
                    print('  + Decrypting File: %s'%_Name)

            fp.seek(offset)

    fp.close()
    return HeadInfos

def getInArcFiles(fname):
    return UnpackArc(fname,HeadOnly=True,log=False)

def diffArc(file1,file2):
    info1=getInArcFiles(file1)
    info2=getInArcFiles(file2)

    ret=[i for i in info1 if i not in info2]
    return ret

'''
struct PNAHeader
{
    // 0x14 bytes
    const char[4]="PNAP"; // 4 bytes
    unsigned int wtf; // 4 bytes
    unsigned int wtf; // 4 bytes
    unsigned int wtf; // 4 bytes
    unsigned int fileCounts; // 4 bytes
};
struct InPNAFileHeader{
    // 0x28 bytes
    const int[4]={0};
    unsigned int index;
    // Last 0x20
    unsigned int offsetX;
    unsigned int offsetY;
    unsigned int width;
    unsigned int height;
    // Last 0x10
    const int[8]={0};
    const int[4]={0,0,0xF0,0x3F};
    unsigned int fileSize;
}
'''

def UnpackPna(fileName,SaveDir='/',log=True):
    try:
        fp=open(fileName,'rb')
    except:
        if log:
            print("Error when reading file %s"%fileName)
        return False
    HEADER=fp.read(0x04)
    if b'PNAP'!=HEADER:
        if log:
            print("%s is not a PNA file"%fileName)
        return
    
    fp.read(0x0C)
    Count=unpack("I",fp.read(0x04))[0]
    ContentOffset=0x14+Count*0x28
    if log:
        print('Totally %3d Files.'%(Count))

    # Handle Dir Name
    if 'Linux' is SYS:
        Name=str(SaveDir).replace('\\','/')
        if '/'!=Name[-1]:
            Name+='/'
    elif 'Win' is SYS:
        Name=str(SaveDir).replace('/','\\')
        if '\\'!=Name[-1]:
            Name+='\\'
    else:
        return
    if not os.path.exists(Name):
        os.makedirs(Name)
    
    for i in range(Count):
        fp.seek(0x14+i*0x28+0x08)
        offX=unpack("I",fp.read(0x04))[0]
        offY=unpack("I",fp.read(0x04))[0]
        width=unpack("I",fp.read(0x04))[0]
        height=unpack("I",fp.read(0x04))[0]
        fp.read(0x0C)
        FileLen=unpack("I",fp.read(0x04))[0]

        if log:
            print('File%3d: \n  Width:%4d, Height:%4d\n  offsetX:%4d, offsetY%4d\n  File length:%d'%(Count-i-1,width,height,offX,offY,FileLen))

        fp.seek(ContentOffset)
        fpp=open('%sfile%d_%dx%d_o_%dx%d.png'%(Name,Count-i-1,width,height,offX,offY),'wb+')
        #fpp=open(Name+'file'+str(Count-i-1)+'.png','wb+')
        fpp.write(fp.read(FileLen))
        fpp.close()
        ContentOffset=fp.tell()

    fp.close()

def Compose(base,cover,output,log=True):
    try:
        if log:
            print('Trying to load from memory.')
        bs=Image.open(base['Content'])
        cv=Image.open(cover['Content'])
        pX=cover['X']-base['X']
        pY=cover['Y']-base['Y']

        box=(pX,pY,cover['width'],cover['height'])
        reg=cv

        bs.paste(reg,box)
        bs.save(output)
    except TypeError:
        try:
            if log:
                print('Trying to load from file by file name.')
            bs=Image.open(base)
            cv=Image.open(cover)
            bsInfo=base.split('/')[-1].split('\\')[-1].split('.')[0].split('_')
            cvInfo=cover.split('/')[-1].split('\\')[-1].split('.')[0].split('_')

            bsX=int(bsInfo[3].split('x')[0])
            bsY=int(bsInfo[3].split('x')[1])

            cvWidth=int(cvInfo[1].split('x')[0])
            cvHeight=int(cvInfo[1].split('x')[1])
            cvX=int(cvInfo[3].split('x')[0])
            cvY=int(cvInfo[3].split('x')[1])

            pX=cvX-bsX
            pY=cvY-bsY

            box=(pX,pY)
            print(cv.size)
            print('%d %d'%(cvWidth,cvHeight))

            if log:
                print('Starting Composing...')
            bs.paste(cv.convert("RGBA"),box,cv)
            if log:
                print('Saving file...')
            bs.save(output)
        except:
            if log:
                print('Please input a valid file.')
            return
    except:
            if log:
                print('Please input a valid file.')
            return

def rightRot(val,bit):
    # char t=0000 0000b;
    retval=val << (8-bit)
    retval |= (val >> bit)
    return retval&0xFF

def decryptWs2(inFile,outFile=False,bit=2):
    rMovBit=bit%8 if bit>0 else 8-(bit%8)
    fp=open(inFile,'rb')
    if outFile:
        fpp=open(outFile,'wb+')
        while True:
            try:
                c=fp.read(1)
                c=unpack('B',c)[0]
                fpp.write(pack('B',(rightRot(c,rMovBit))))
                continue
            except:
                break
    else:
        cont=fp.read()
        fp.close()
        fp=open(inFile+'.bak','wb+')
        fp.write(cont)
        fpp=open(inFile,'wb+')
        for ch in cont:
            c=ch
            fpp.write(pack('B',(rightRot(c,rMovBit))))
        
    fp.close()
    fpp.close()

def extractText(inFile,outText,outBin=''):
    Chrt=0
    Text=1
    Bin=2
    def getType(msg):
        if b'%LC'==msg[0:3]:
            return Chrt
        elif b'char\0'==msg[0:5]:
            return Text
        else:
            return Bin

    fp=open(inFile,'rb')
    out=open(outText,'wb+')
    inContent=fp.read()
    fp.close()

    handledContent=inContent
    BinData=b''

    while len(handledContent)>0:
        if Bin==getType(handledContent):
            BinData+=pack('B',handledContent[0])
            handledContent=handledContent[1:]
            continue
        elif len(handledContent)>3 and Chrt==getType(handledContent):
            tc=3
            tcc=b''
            while len(handledContent)>tc and b'\0'!=pack('B',handledContent[tc]):
                tcc+=pack('B',handledContent[tc])
                tc+=1
            out.write(b'['+tcc+b']\n')
            handledContent=handledContent[tc:]
            BinData+=b'%LC'
            continue
        elif len(handledContent)>5 and Text==getType(handledContent):
            tc=5
            tcc=b''
            while len(handledContent)>tc and b'%'!=pack('B',handledContent[tc]):
                tcc+=pack('B',handledContent[tc])
                tc+=1
            out.write(tcc+b'\n\n')
            handledContent=handledContent[tc:]
            BinData+=b'char\0'
            continue
        BinData+=handledContent
        break
    if ''!=outBin:
        fp=open(outBin,'wb+')
        fp.write(BinData)
        fp.close()
    out.close()

'''
struct lngLen{
    unsigned short len; // 2byte
};
struct lngHeader{
    unsigned int sentenceCount; // 4byte
    lngLen lngs[sentenceCount];
};
'''
def extractLngText(inFile):
    return

if '__main__'==__name__:
    #decryptWs2(
    #    'C:\\Users\\11951\\Desktop\\123.txt',
    #    'C:\\Users\\11951\\Desktop\\123.txt.txt'
    #)
    #extractText(
    #    'E:\\GameUnpack\\IfMyHeart\\Rio.ori\\CO1_020_D.ws2.dec',
    #    'E:\\GameUnpack\\IfMyHeart\\Rio.ori\\CO1_020_D.ws2.dec.txt'
    #)
    #UnpackArc(
    #    'H:\\SteamLibrary\\steamapps\\common\\If My Heart Had Wings\\Rio.diffed',
    #    'E:\\GameUnpack\\IfMyHeart\\Rio.diff'
    #)
    #UnpackPna(
    #    'E:\\GameUnpack\\IfMyHeart\\SysGraphic.ori\\Sys_title.pna',
    #    'E:\\GameUnpack\\IfMyHeart\\SysGraphic.ori\\Sys_title'
    #)
    #decryptWs2(
    #    'E:\\GameUnpack\\IfMyHeart\\Rio.ori\\CO1_020_D.ws2',
    #    'E:\\GameUnpack\\IfMyHeart\\Rio.ori\\CO1_020_D.ws2.dec'
    #)
    #decryptWs2(
    #    'E:\\GameUnpack\\IfMyHeart\\CN\\Rio\\AGE_001.lng',
    #    'E:\\GameUnpack\\IfMyHeart\\CN\\Rio\\AGE_001.lng.dec',
    #    7
    #)
    #for i in diffArc(
    #    'H:\\SteamLibrary\\steamapps\\common\\If My Heart Had Wings\\CHIP2.arc',
    #    'H:\\SteamLibrary\\steamapps\\common\\If My Heart Had Wings\\CHIP2.arc.bkp'
    #):
    #    print(i)
	UnpackArc('H:\\GalGame\\[130125] [PULLTOP] [在这苍穹展翅，大空展翼 FLIGHT DIARY] この大空に、翼をひろげて FLIGHT DIARY  [日本語]\\Chip9.arc','E:\\Unpack')