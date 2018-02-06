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

def mpk_unpatch(fn,output=""):
	if ""==output:
		output="."
	fp=open(fn,"rb")
	FILE_TAG=fp.read(4)
	if(b"MPK\x00"!=FILE_TAG):
		print("Please input a valid MPK file.")
	del FILE_TAG
	path=output+"\\"+fn.split('\\')[-1].split('.')[0]+"\\"
	fp.seek(8)
	nums=unpack("I",fp.read(4))[0]
	for i in range(nums):
		fp.seek(0x40+0x100*i)
		fp.read(8)
		offset=unpack("Q",fp.read(8))[0]
		fp.read(8)
		size=unpack("Q",fp.read(8))[0]
		name=fp.read(0x30).split(b"\x00")[0].decode("utf-8")
		fp.seek(offset)
		data=fp.read(size)
		PATH=""
		for p in (path+name).split("\\")[:-1]:
			PATH+=p+"\\"
		dirEx(PATH)
		dest=open(path+name,"wb")
		dest.write(data)
		dest.close()
	fp.close()