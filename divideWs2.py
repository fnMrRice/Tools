from struct import pack
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
    ft=open(txt,'r')
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

if '__main__'==__name__:
    import sys
    args=sys.argv
    if 1==len(args):
        print('This program is used to unpack *.arc file.')
        print('Usage:\n python %s divide [ws2_file] [output_bin] [output_txt]\n python %s make [bin_input] [txt_input] [output]'%args[0])
    if 'divide'==args[1]:
        divideWs2(args[2],args[3])
    elif 'make'==args[1] and 5==len(args):
        makeWs2(args[2],args[3],args[4])
    #divideWs2('D:\\Games\\UnpackedFiles\\Rio\\CC_11A_en.ws2')
    #makeWs2('D:\\Games\\UnpackedFiles\\Rio\\CC_11A_en.ws2.txt','D:\\Games\\UnpackedFiles\\Rio\\CC_11A_en.ws2.bin','D:\\Games\\UnpackedFiles\\Rio\\CC_11A_en.ws2.test')