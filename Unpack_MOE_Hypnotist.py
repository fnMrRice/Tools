from struct import unpack

# G:\\Game\\SteamLibrary\\steamapps\\common\\MOE Hypnotist\\resources\\app\\init_a.asar
# G:\\Game\\SteamLibrary\\steamapps\\common\\MOE Hypnotist\\resources\\app\\texture.asar
# G:\\Game\\SteamLibrary\\steamapps\\common\\MOE Hypnotist\\resources\\app\\unpack\\

def readfile(filepath):
    fp=open(filepath,'rb')
    sign=fp.read(4)
    if (b'\x04\x00\x00\x00'!=sign):
        print('invalid file.')
        return
    fp.seek(0x08)
    header_offset=unpack('I',fp.read(4))[0]
    header_len=unpack('I',fp.read(4))[0]
    # print(header_len)
    header=eval(fp.read(header_len))['files']['asset']['files']
    global_offset=header_offset+0x0C
    for name in header:
        # print(header[name])
        size=header[name]['size']
        offset=int(header[name]['offset'])+global_offset
        fp.seek(offset)
        if (b'RIFF'==fp.read(4)):
            continue
            print('This is a RIFF file.')
            print('Size: %d, Offset: %d'%(size,offset))
            fp.read(4)
            if (b'WEBP'==fp.read(4)):
                print('This is a Webp File.')
                fp.seek(offset)
                cont=fp.read(size)
                fpath='G:\\Game\\SteamLibrary\\steamapps\\common\\MOE Hypnotist\\resources\\app\\unpack\\'+name+'.webp'
                out_fp=open(fpath,'wb')
                out_fp.write(cont)
                out_fp.close()
        if (b'OggS'==fp.read(4)):
            print('This is a MP3 file.')