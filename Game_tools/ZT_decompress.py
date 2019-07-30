import os
from zlib import decompress
from struct import unpack

# struct {
#     byte    sign[0x00,0x00,0x00,0x00]; // 0x04
#     u32     block_size;                // 0x08
#     offset* next_block;                // 0x0C
#     unknown block_type;                // 0x10
#     char    name[block_length-0x10];   // block_length
# };

# struct {
#     u64 block_size;
#     u64 block_size-0x0C;
#     char name[0x0104];
#     u32 compressed_size;
#     u32 decompressed_size;
# }

def main(FileName):
    with open(FileName,'rb') as fp:
        fp.read(0x10)
        counter=0
        while(b'\0'!=fp.read(1)):
            continue
        dir_name_end=fp.tell()-0x10
        fp.seek(0x10)
        origin_path=fp.read(dir_name_end-1)
        origin_path=origin_path.decode()
        fp.seek(0x08)
        temp=fp.read(4)
        # print(temp)
        fp.seek(fp.tell()+unpack('I',temp)[0])
        # print(hex(fp.tell()))
        if (not os.path.exists(origin_path)):
            os.makedirs(origin_path)
        file_name=origin_path

        flag=True
        while flag:
            block_size=fp.read(4)
            if (b''==block_size):
                break
            block_size=unpack('I',block_size)[0]
            if (0==block_size):
                block_size=unpack('I',fp.read(4))[0]
                if (0==block_size):
                    fp.read(0x08)
                    name_begin=fp.tell()
                    while(b'\0'!=fp.read(1)):
                        continue
                    name_end=fp.tell()
                    fp.seek(name_begin)
                    name=fp.read(name_end-name_begin-1).decode()
                    if ('Thumbs.db'==name):
                        continue
                    file_name+='/'+name
                    print(file_name)
                    fp2=open(file_name,'wb+')
                    fp.seek(name_begin)
                    fp.read(0x0104)
                    comp_size=unpack('I',fp.read(4))[0]
                    decomp_size=unpack('I',fp.read(4))[0]
                    cont=fp.read(comp_size)
                    try:
                        de_cont=decompress(cont)
                        if (decomp_size!=len(de_cont)):
                            print('1 File length not right')
                            break
                        fp2.write(de_cont)
                    except:
                        print('1 Something wrong happened')
                        break
                    fp2.close()
                    flag=True
                    break

                jump_size=unpack('I',fp.read(4))[0]
                unknown=unpack('I',fp.read(4))[0]
                name_begin=fp.tell()
                print('d1 '+hex(fp.tell()))
                while(b'\0'!=fp.read(1)):
                    continue
                name_end=fp.tell()
                fp.seek(name_begin)
                name=fp.read(name_end-name_begin-1).decode()
                # file_name+='/'+name
                # print(file_name)
                if (not os.path.exists(file_name)):
                    os.makedirs(file_name)
                fp.seek(name_begin-0x04+jump_size)
                print('d2 '+hex(fp.tell()))
            else:
                fp.read(0x0C)
                name_begin=fp.tell()
                print('f1 '+hex(fp.tell()))
                while(b'\0'!=fp.read(1)):
                    continue
                print('f2 '+hex(fp.tell()))
                name_end=fp.tell()
                fp.seek(name_begin)
                name=fp.read(name_end-name_begin-1).decode()
                if ('Thumbs.db'==name):
                    continue
                file_name+='/'+name
                print(file_name)
                fp2=open(file_name,'wb+')
                fp.seek(name_begin)
                fp.read(0x0104)
                comp_size=unpack('I',fp.read(4))[0]
                decomp_size=unpack('I',fp.read(4))[0]
                cont=fp.read(comp_size)
                try:
                    de_cont=decompress(cont)
                    if (decomp_size!=len(de_cont)):
                        print('2 File length not right')
                        continue
                    fp2.write(de_cont)
                except:
                    print('2 Something wrong happened')
                    continue
                fp2.close()
                file_name=origin_path

if '__main__'==__name__:
    # main('ama.zt')
    # main('chi.zt')
    # main('jb.zt')
    # main('mak.zt')
    # main('mic.zt')
    # main('sac.zt')
    # main('yum.zt')
    # for i in range(1,57+1):
    #     main('grisaia_icon_%03d.zt'%(i))
    # for i in range(1,17+1):
    #     main('grisaia_wp_%02d.zt'%(i))

# 81+82=163