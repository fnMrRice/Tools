# -*- coding:utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup as bs4
import time

def validateFileName(name):
	return '-'.join(re.split('[/\\:\*\?"<>|]',str(name)))

def getHTMLContent(url,sess):
	Headers={
		'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		'accept-encoding':'gzip, deflate, br',
		'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
		'referer':'https://www.wenku8.net/index.php',
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
	}
	return sess.get(url,headers=Headers).content

def getBookURLFormID(id):
	try:
		id=int(id)
	except ValueError:
		raise ValueError('ID must can be converted into int')
	return 'https://www.wenku8.net/book/%04d.htm'%id

def getNovelURLFromID(id):
	try:
		id=int(id)
	except ValueError:
		raise ValueError('ID must can be converted into int')
	return 'https://www.wenku8.net/novel/%01d/%04d/'%(id/1000,id)
	
# 获取全部小说名称之类的信息
# fp=open('Infos.csv','w+')
# for i in range(1,4000):
# 	book_url='https://www.wenku8.net/book/%04d.htm'%i
# 	novel_url='https://www.wenku8.net/novel/%01d/%04d/index.htm'%(i/1000,i)
# 	cont=getHTMLContent(book_url,wenku8_session)
# 	soup=bs4(cont,'html.parser')
# 	try:
# 		(name,author,wenku,_)=soup.title.contents[0].split(' - ')
# 		all_tds=soup.find_all('td',width='20%')
# 		status=all_tds[2].string.split('：')[1]
# 		last_update=all_tds[3].string.split('：')[1]
# 		length=all_tds[4].string.split('：')[1]
# 	except KeyboardInterrupt as e:
# 		print('You canceled the operation. Current: %04d'%i)
# 		exit(0)
# 	except:
# 		print('%04d, Cannot get informations.'%i)
# 		continue
# 	line = '%04d,%s,%s,%s,%s,%s,%s\n'%(i,name,author,wenku,status,last_update,length)
# 	print(line,end='')
# 	fp.write(line)
# 	time.sleep(1)
# fp.close()
# exit(0)

wenku8_session=requests.Session()
Novel_URL=getNovelURLFromID(1269)  #小说内容的页面
Menu_URL=Novel_URL+'index.htm'  #下载的小说页面

print('Novel URL: %s'%Menu_URL)

req=getHTMLContent(Menu_URL,wenku8_session)
req=bs4(req,'html.parser')

main_menu=req.find('table',class_='css').find_all('td')  #获取全部目录
VolName=''  #卷名

for td in main_menu:
	if not td.find('a'):  #如果没有目录
		continue
	if td.has_attr('colspan'):  #如果是章节名
		print(VolName)
		VolName=td.text
		continue
	ChapName=td.text  #章节名
	print('获取章节: '+VolName+' '+ChapName,end='...   ')
	ChapURL=td.find('a')['href']  #获取下载url
	print('Chapter URL: %s'%(Novel_URL+ChapURL))
	content=bs4(getHTMLContent(Novel_URL+ChapURL,wenku8_session),"html.parser")  #获取内容页面
	#content=bs4(open('123.html').read(),"html.parser")
	content=content.find(id='content')
	article=content.string  #获取小说
	imgs=content.find_all('img')  #获取网页中的图片
	print('完成')
		
	#文件夹操作
	VolName=validateFileName(VolName)
	ChapName=validateFileName(ChapName)
	if not os.path.exists(VolName):
		os.makedirs(VolName)
		
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
	if article=='':
		continue
	print('写入小说内容...   ',end=' ')
	fp=open(VolName+'/'+ChapName+'.txt','w')
	fp.write(VolName+"\n"+ChapName+"\n"+article)
	fp.close()
	print('完成')
	time.sleep(1)
	
