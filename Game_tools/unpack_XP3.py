from zlib import decompress
from struct import unpack,pack
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
	if '\\'!=output[-1]:
		output+='\\'
	
	fp=open(fn,"rb")
	FILE_TAG=fp.read(3)
	if(b"XP3"!=FILE_TAG):
		print("Please input a valid XP3 file.")

	fp.seek(0x0C)
	offset=0
	if b'\x00\x00\x00\x00'==fp.read(4):
		fp.seek(0x20)
		offset=unpack("Q",fp.read(0x8))[0]
		print('XP3 type 1')
	else:
		fp.seek(0x0B)
		offset=unpack("Q",fp.read(0x8))[0]
		print('XP3 type 2')
		#print('%d'%offset)
		#exit(0)

	fp.seek(offset)
	compressed=unpack("?",fp.read(1))[0]
	compressed_len=unpack("Q",fp.read(8))[0]
	uncompressed_len=unpack("Q",fp.read(8))[0]

	contents=fp.read(compressed_len)
	if compressed:
		contents=decompress(contents)
	#open('.\\123','wb+').write(contents)
	INFOS=contents.split(b"File")[1:] # [1] is null because str begin with 'File'
	print("Find %s file(s)." % len(INFOS))
	del FILE_TAG
	del contents,compressed,offset
	index=1
	total=len(INFOS)

	for info in INFOS:
		temp=info[0x08:]
		FileName=''
		FileStart=0
		FileSize_packed=0
		compressed=False
		while len(temp)>=4:
			if b'info'==temp[:0x04]:
				info_s=unpack('Q',temp[0x04:0x0C])[0]
				infos=temp[0x0C:0x0C+info_s]
				temp=temp[0x0C+info_s:]

				wtf=unpack('I',infos[:4])[0]
				FileSize_origin=unpack('Q',infos[0x04:0x0C])[0]
				FileSize_packed=unpack('Q',infos[0x0C:0x14])[0]
				NameSize=unpack('H',infos[0x14:0x16])[0]
				#print(FileSize_packed)
				FileName=infos[0x16:0x16+NameSize*2].decode("utf16")
				#print(FileName)
			elif b'segm'==temp[0:4]:
				segm_s=unpack('Q',temp[0x04:0x0C])[0]
				segms=temp[0x0C:0x0C+segm_s]
				temp=temp[0x0C+segm_s:]

				compressed=unpack('I',segms[:0x04])[0]
				FileStart=unpack('Q',segms[0x04:0x0C])[0]
				#print(FileStart)
			elif b'adlr'==temp[0:4]:
				adlr_s=unpack('Q',temp[0x04:0x0C])[0]
				adlrs=temp[0x0C:0x0C+adlr_s]
				temp=temp[0x0C+adlr_s:]
			elif b'time'==temp[0:4]:
				time_s=unpack('Q',temp[0x04:0x0C])[0]
				times=temp[0x0C:0x0C+time_s]
				temp=temp[0x0C+time_s:]
		if 0==FileSize_packed or ''==FileName:
			print('File invalid. (%d of %d)'%(index,total))
			continue
		FilePath=output+'.'.join(fn.split('\\')[-1].split('.')[:-1])+'\\'+FileName.replace('/','\\')
		Path='\\'.join(FilePath.split('\\')[:-1])
		dirEx(Path)
		print('Extracting: '+FilePath+' (%d of %d)'%(index,total))
		fp.seek(FileStart)
		try:
			fo=open(FilePath,"wb+")
			FileContent=fp.read(FileSize_packed)
			if compressed:
				FileContent=decompress(FileContent)
			fo.write(FileContent)
			fo.close()
		except:
			pass
		index+=1
	fp.close()

'''
def packXP3(dirName,saveFile):
	infos=[]
	fs=os.walk(dirName)
	fp=open(saveFile,'wb+')
	fp.write(b'XP3\x0D\x0A\x20\x0A\x1A\x8B\x67\x01\x17\x00\x00\x00\x00')
	fp.write(b'\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00')
	fp.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')
	for root,dirs,files in fs:
		for f in files:

			os.path.getsize(filePath)
			infos.append({
				'info':[
					'\x00\x00\x00\x00',
					pack('Q',os.path.getsize(os.path.join(root,f))),
					pack('Q',os.path.getsize(os.path.join(root,f))),
					pack('H',len(os.path.join(root,f).replace(fs[0][0]))),
					os.path.join(root,f).replace(fs[0][0]).encode('utf-16')
				],
				'segm':[
					pack('I',0)
					pack('Q',fp.tell())
				],
				'adlr':[
					'\x00'
				],
				'time':''
			})
			fp.write(open(os.path.join(root,f),'rb').read())
'''
	
if '__main__'==__name__:
	#for f in ["patch_append7","patch_append8","patch_append9","patch_append10","patch_append11","patch_append12","patch_append13","patch_append14"]:
	#	#name=f+".xp3"
	#	#xp3_unpatch(name,".\\unpatch")
	#xp3_unpatch('H:\\GalGame\\茂伸 -happy end-\\fgimage.xp3','E:\\GameUnpack\\MonoBeno')
	# xp3_unpatch('G:\\Game\\SteamLibrary\\steamapps\\common\\LoveSim\\data.xp3','E:\\GameUnpack\\LoveSim')
	#xp3_unpatch('H:\\GalGame\\[160325] [Lose] [爱上火车] まいてつ [日本語]\\data.xp3','E:\\GameUnpack\\まいてつ')
	xp3_unpatch("G:\\SteamLibrary\\steamapps\\common\\The Princess, the Stray Cat, and Matters of the Heart 2\\data.xp3",'G:\\GameUnpack\\NoraTo2')