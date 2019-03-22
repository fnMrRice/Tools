# -*- coding:utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup as bs4

def validateFileName(name):
	return ' '.join(re.split('[/\\:\*\?"<>|]',str(name)))
	
URL='http://www.wenku8.com/novel/1/1269/index.htm'  #下载的小说页面
BaseURL='/'.join(URL.split('/')[:-1])+'/'  #小说内容的页面

req=requests.get(URL)  #获取目录
req.encoding='utf-8'
req.encoding='gbk'  #改变编码
req=bs4(req.text,"html.parser")
test=req.find('table',class_='css').find_all('td')  #获取全部目录
VolName=''  #卷名

for td in test:
	if b'\xc2\xa0'==td.text.encode('utf-8'):  #如果没有目录
		continue
	if td.has_attr('colspan'):  #如果是章节名
		print(VolName)
		VolName=td.text
		continue
	ChapName=td.text  #章节名
	print('获取章节: '+VolName+' '+ChapName,end='...   ')
	ChapURL=td.contents[0]['href']  #获取下载url
	content=requests.get(BaseURL+ChapURL)  #获取内容页面
	content.encoding='utf-8'
	content.encoding='gbk'
	content=bs4(content.text,"html.parser")
	#content=bs4(open('123.html').read(),"html.parser")
	content=content.find(id='content')
	article=content.text[40:-50].replace('\n\r\n\xa0\xa0\xa0\xa0','\r\n')#.encode()  #获取小说
	imgs=content.findChildren('img')  #获取网页中的图片
	print('完成')
		
	#文件夹操作
	VolName=validateFileName(VolName)
	ChapName=validateFileName(ChapName)
	if not os.path.exists(VolName):
		os.mkdir(VolName)
		
	#写入文件
	for imgLink in imgs:
		if not os.path.exists(VolName+'/'+ChapName):
			os.mkdir(VolName+'/'+ChapName)
		imgLocal=str(imgLink['src']).split('/')[-1]
		print('下载图片: '+imgLink,end='...   ')
		imgContent=requests.get(imgLink['src']).content
		fp=open(VolName+'/'+ChapName+'/'+imgLocal,'wb')
		fp.write(imgContent)
		fp.close()
		print('完成')
	if article.replace('\n','').replace('\r','').replace(' ','')=='':
		continue
	print('写入小说内容...   ',end=' ')
	fp=open(VolName+'/'+ChapName+'.txt','w')
	fp.write(VolName+"\n"+ChapName+"\n"+article)
	fp.close()
	print('完成')
	
