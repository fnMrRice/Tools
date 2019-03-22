# -*- coding:utf-8 -*-
from mylib import exist,findSTR,toAllowed,cd
from EHentaiLib import GetLocalCookies as EHCookie, PrintOut as PAS, SetSessionCookie as SetNewC
import requests,time,random
from bs4 import BeautifulSoup

INFOPAGE_REG='<div class="id2"><a href="(.*?)">(.*?)</a></div><.*?"id3".*?src="(.*?)".*?id41.*?title="(.*?)".*?id42.*?>(.*?) files'
HEADERS = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection':'keep-alive',
	'Host':'',
	'Referer':'',
}
NOWPAGE=0

COOKIES=EHCookie()
LOGGIN=True if COOKIES else False
OUTERSITE='https://e-hentai.org/'
INNERSITE='https://exhentai.org/' if LOGGIN else OUTERSITE
HEADERS['Host']='exhentai.org' if LOGGIN else 'e-hentai.org'
HEADERS['Referer']='exhentai.org' if LOGGIN else 'e-hentai.org'
BASE_CONF='tl_j-dm_t-xl_1024x2048x1x1025x2049x20x1044x2068x30x1054x2078x40x1064x2088x50x1074x2098x60x1084x2108x70x1094x2118x80x1104x2128x90x1114x2138x100x1124x2148x110x1134x2158x120x1144x2168x130x1154x2178-ts_l' #Thumb Mode, Default JP title, Disable doujins not in Chinese, show detail page in big mode

DOWN_THUMB=False
while(DOWN_THUMB!='Y' and DOWN_THUMB!='N'):
	DOWN_THUMB=input("Download Thumb?(Y/N)")
KEYWORD=input("Input your keyword: ")
ADVANCE=input("Please input Advanced Option: ")

r=""
DOWN_THUMB=DOWN_THUMB is 'Y'
OPTION={'f_apply':'Apply Filter','f_search':KEYWORD}
for i in ['f_doujinshi','f_manga','f_artistcg','f_gamecg','f_western','f_non-h','f_imageset','f_cosplay','f_asianporn','f_misc']:
	OPTION[i]=1
if not ""==ADVANCE:
	ADVANCE=ADVANCE.split(';')
	A_OPTION={}
	for opt in ADVANCE:
		opt=opt.split('=')
		A_OPTION[opt[0]]=opt[1]
	if A_OPTION.get('CLASS'):# Search Galleries Class
		n=0
		for i in ['f_doujinshi','f_manga','f_artistcg','f_gamecg','f_western','f_non-h','f_imageset','f_cosplay','f_asianporn','f_misc']:
			if A_OPTION['CLASS'][n] is 0:
				OPTION[i]=0
			n+=1
	if A_OPTION.get('F'):# File Search
		files={'file': open(A_OPTION['F'])}
		if A_OPTION.get('FU'):# Use Similarity Scan
			if not A_OPTION['FU']=='F':
				OPTION["fs_similar"]='on'
		if A_OPTION.get('FO'):
			if A_OPTION['FO']=='Y':# Only Search Covers
				OPTION["fs_covers"]='on'
		if A_OPTION.get('FS'):
			if A_OPTION['FS']=='Y':# Show Expunged
				OPTION["fs_exp"]='on'
		r=requests.post(INNERSITE,params=FILE_SEARCH_OPTION,cookies=COOKIES,files=files,headers=HEADERS)
	else:# Advanced Search
		OPTION['advsearch']=1
		if A_OPTION.get('SGN'):# Search Gallery Name
			if not A_OPTION['SGN']=='F':
				OPTION["f_sname"]='on'
		if A_OPTION.get('SGT'):# Search Gallery Tags
			if not A_OPTION['SGT']=='F':
				OPTION["f_stags"]='on'
		if A_OPTION.get('SGD'):# Search Gallery Description
			if(A_OPTION['SGD']=='T'):
				OPTION["f_sdesc"]='on'
		if A_OPTION.get('ST'):# Search Torrent Filenames
			if(A_OPTION['ST']=='T'):
				OPTION["f_storr"]='on'
		if A_OPTION.get('O'):# Only Show Galleries With Torrents
			if(A_OPTION['O']=='T'):
				OPTION["f_sto"]='on'
		if A_OPTION.get('SL'):# Search Low-Power Tags
			if(A_OPTION['SL']=='T'):
				OPTION["f_sdt1"]='on'
		if A_OPTION.get('SD'):# Search Downvoted Tags
			if(A_OPTION['SD']=='T'):
				OPTION["f_sdt2"]='on'
		if A_OPTION.get('SE'):# Show Expunged Galleries
			if(A_OPTION['SE']=='T'):
				OPTION["f_sh"]='on'
		if A_OPTION.get('M'):# Minimum Rating
			if(2<=A_OPTION['M'] and A_OPTION['M']<=5):
				OPTION["f_sr"]='on'
				OPTION["f_srdd"]=A_OPTION['M']

def readEhPage():
	global NOWPAGE,OPTION,COOKIES,HEADERS,INNERSITE,dirName
	COOKIES['uconfig']=BASE_CONF
	if(0!=NOWPAGE):
		OPTION['page']=NOWPAGE
	if ""==OPTION['f_search']:
		r=requests.get(INNERSITE,cookies=COOKIES,headers=HEADERS)
	else:
		r=requests.get(INNERSITE,params=OPTION,cookies=COOKIES,headers=HEADERS)
	HEADERS['Referer']=r.url
	COOKIES=SetNewC(r.cookies.items())
	#print(r.text)
	RetHTMLs = BeautifulSoup(r.text, "html.parser").find('div',{"class": "itg"}).find_all('div',{"class":'id1'})
	RetHTML=[]
	for i in RetHTMLs:
		id2=i.find('div',{'class':'id2'}).a.contents[0]
		id2h=i.find('div',{'class':'id2'}).a['href']
		id3=i.find('div',{'class':'id3'}).find('img')['src']
		id41=i.find('div',{'class':'id41'})['title']
		id42=i.find('div',{'class':'id42'}).contents[0]
		RetHTML.push([id2,id2a,id3,id41,id42])

	#RetHTML=findSTR(r.text,INFOPAGE_REG)
	#print(INFOPAGE_REG)
	if []==RetHTML:
		return False
	INFO=""
	for info in RetHTML:
		INFO+=PAS("JPname: "+info[1]+"\nDownload Address: "+info[0]+"\nType:"+info[3]+"\nPicture Count: "+info[4]+"\nDownload Number: ")
		T_info=info[0].replace(INNERSITE+'g/', "").split('/')
		INFO+=PAS(T_info[0]+' '+T_info[1]+'\n')
		if DOWN_THUMB:
			cd(dirName+'.detail')
			cd('Page_'+str(NOWPAGE+1))
			thumb=requests.get(info[2],cookies=COOKIES,headers=HEADERS)
			print("Downloading Thumb: "+thumb.url)
			F=open(T_info[0]+'_'+T_info[1]+'_'+toAllowed(info[1])+'.jpg', 'wb')
			F.write(thumb.content)
			F.close()
			cd('..')
			cd('..')
		INFO+=PAS('\n')
	cd(dirName+'.detail')
	open(dirName+"_Page_"+str(NOWPAGE+1)+'.txt','w+b').write(INFO.encode("utf-8",'ignore'))
	cd('..')
	return True

Next="y"
dirName='EhInfo.'+toAllowed(KEYWORD)+'.'+str(time.time())
while('y'==Next or 'Y'==Next):
	if(not readEhPage()):
		print("Error When Reading Data!")
		break
	NOWPAGE+=1
	Next=input("Do you want to read next page?(Y/N)")
	
