# -*- coding:utf-8 -*-
from mylib_linux import getHTML,findSTR,dirEx,toAllowed,download,addAshow,fileREAD,checkOK,cd
from os.path import exists as direxist

# yande.re专用下载
def downYande(Page = 1,Tag = ""):
	Page = str(Page)
	url = "https://yande.re/post?tags="+Tag+'&page='+Page
	reg = 'Post\.register\(\{"id":([0-9]*),"tags":"(.*?)".*?"author":"(.*?)".*?"source":"(.*?)".*?"md5":"(\w{32})","file_size":([0-9]*),"file_ext":"(.*?)","file_url":"(.*?)".*"rating":"(.).*"width":([0-9]*),"height":([0-9]*)'
	print("\n正在解析第( "+Page+" )页的文件信息\t标签："+("无" if (""==Tag) else Tag)+"\nURL: "+url)
	HTML = getHTML(url)
	list = findSTR(HTML,reg)
	if not "" == Tag:
		cd(Tag)
	cd("Page "+Page)
	INFO = open("FileINFO.txt","a+")
	s = str(INFO.read())
	print("解析完毕\n")
	for pic in list:
		id = pic[0]
		tags = pic[1]
		author = pic[2]
		source = pic[3]
		md5 = pic[4]
		fsize = pic[5]
		fext = pic[6]
		downURL = pic[7]
		rating = pic[8]
		width = pic[9]
		height = pic[10]
		downPATH = "yande.re "+id+" "+tags+"."+fext
		downPATH = toAllowed(downPATH)
		if not direxist(downPATH):
			if "e"==rating:
				dirEx("HX")
				downPATH = "HX/"+downPATH
			print("正在下载："+downPATH)
			download(downURL,downPATH)
		else:
			print("文件已存在！")
			if not checkOK(downPATH,md5):
				print("校检不正确，重新下载")
				print("正在下载："+downPATH)
				download(downURL,downPATH)
		if -1==s.find("图片 ID: "+id):
			print("正在添加图片信息：")
			addAshow("\t图片 ID: "+id,INFO)
			addAshow("\t标签: "+tags,INFO)
			addAshow("\t作者: "+author,INFO)
			addAshow("\t文件源: "+source,INFO)
			addAshow("\t图片MD5: "+md5,INFO)
			addAshow("\t文件大小: "+int(fsize)/1024/1024+" Mb",INFO)
			addAshow("\t图片分级: "+rating,INFO)
			addAshow("\t图片尺寸: "+width+"x"+height,INFO)
			addAshow("\t本地保存文件: "+downPATH+"\n",INFO)
		else:
			print("正在加载图片信息：")
			print(s[s.find("\t图片 ID: "+id):s.find("\t本地保存文件: "+downPATH)+len("\t本地保存文件: "+downPATH)+1]+"\n")
	INFO.close()
	cd("..")
	if not "" == Tag:
		cd("..")
	print("\n第 "+Page+" 页下载完成!")

# MAIN
tags = input("输入标签: ")
page = input("输入起始页(默认：1)：")
if ""==page:
	page = 1
count = input("输入下载页数(默认：1)：")
if ""==count:
	count = 1
for i in range(int(page),int(page)+int(count)):
	downYande(Page=i,Tag=tags)