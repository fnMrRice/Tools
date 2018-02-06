from zlib import decompress
from struct import unpack
import os
def dirEx(pat):
	if not os.path.exists(pat):
		os.makedirs(pat)
	else:
		if not os.path.isdir(pat):
			os.remove(pat)
			os.makedirs(pat)
	return

def xp3_unpatch(fn,output=""):
	if ""==output:
		output="."
	fp=open(fn,"rb")
	FILE_TAG=fp.read(3)
	if(b"XP3"!=FILE_TAG):
		print("Please input a valid XP3 file.")
	del FILE_TAG
	fp.seek(0x20)
	offset=unpack("Q",fp.read(0x8))[0]
	fp.seek(offset)
	compressed=unpack("?",fp.read(1))[0]
	compressed_len=unpack("Q",fp.read(8))[0]
	uncompressed_len=unpack("Q",fp.read(8))[0]
	contents=fp.read(compressed_len)
	if compressed:
		#print("Compressed.")
		contents=decompress(contents)
	INFOS=contents.split(b"File")[1:]
	print("Find %s file(s)." % len(INFOS))
	for info in INFOS:
		ENCRYPTED=unpack("I",info[0x14:0x18])[0]
		FILE_SIZE_ORIGIN=unpack("Q",info[0x18:0x20])[0]
		FILE_SIZE_PACKED=unpack("Q",info[0x20:0x28])[0]
		FILE_NAME_SIZE=unpack("H",info[0x28:0x2a])[0]
		FILE_NAME=info[0x2a:0x2a+FILE_NAME_SIZE*2].decode("utf16")
		FILE_PATH=output+"\\"+fn.split('\\')[-1].split('.')[0]+"\\"+FILE_NAME
		FILE_PATH_0=FILE_PATH.split("\\")[:-1]
		FILE_PATH_1=FILE_PATH.split("\\")[-1].split("/")[:-1]
		FILE_NAME=FILE_PATH.split("\\")[-1].split("/")[-1]
		PATH=""
		for p in FILE_PATH_0:
			PATH+=p+"\\"
		for p in FILE_PATH_1:
			PATH+=p+"\\"
		dirEx(PATH)
		temp=0x2a+FILE_NAME_SIZE*2+0x4+0x8
		FILE_COMPRESSED=unpack("I",info[temp:temp+0x4])[0]
		temp+=0x4
		FILE_OFFSET=unpack("Q",info[temp:temp+0x8])[0]
		temp+=0x8*3+0x4
		ADDON_SIZE=unpack("Q",info[temp:temp+0x8])[0]
		KEY=info[temp+0x8:temp+0x8+ADDON_SIZE]
		print(PATH+FILE_NAME)
		fp.seek(FILE_OFFSET)
		fo=open(PATH+FILE_NAME,"wb+")
		fo.write(fp.read(FILE_SIZE_PACKED))
	fp.close()
	
for f in ["bgimage","bgm","data","fgimage","image","others","sound","video"]:
	name=f+".xp3"
	xp3_unpatch(name,".\\unpatch")