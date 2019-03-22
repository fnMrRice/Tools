# -*- coding:utf-8 -*-
import requests
from mylib import exist,findSTR,toAllowed,cd
from EHentaiLib import GetLocalCookies as EHCookie,PrintOut as PAS, SetSessionCookie

TORRPAGE_REGS=[
	'([0-9]+) torrents? w[\w]{2,3} found for this gallery',
	'name="gtid" value="([0-9]+)".*?\n.*?\n.*?\n.*?Posted:</span> (.*?)</td>.*?\n.*?Size:</span> (.*?)</td>.*?\n.*?\n.*?Seeds:</span> ([0-9]+).*?\n.*?Peers:</span> ([0-9]+).*?\n.*?Downloads:</span> ([0-9]+).*?\n.*?\n.*?\n.*?Uploader:</span> (.*?)</td>.*?\n.*?\n.*?\n.*?\n.*?\n.*?href="(https://ehtracker.org/get/[0-9]+/[0-9a-z]+.torrent)" onclick="document.location=\'(https://ehtracker.org/get/[0-9]+/[0-9a-z]+.torrent\?p=.*?)\'.*?>(.*?)</a>'
]
HEADERS = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection':'keep-alive',
	'Host':'',
	'Referer':'',
}

COOKIES=EHCookie()
LOGGIN=True if COOKIES else False
OUTERSITE='https://e-hentai.org/'
INNERSITE='https://exhentai.org/' if LOGGIN else OUTERSITE
HEADERS['Host']='exhentai.org' if LOGGIN else 'e-hentai.org'
HEADERS['Referer']='exhentai.org' if LOGGIN else 'e-hentai.org'
BASE_CONF='tl_j-dm_t-xl_1024x2048x1x1025x2049x20x1044x2068x30x1054x2078x40x1064x2088x50x1074x2098x60x1084x2108x70x1094x2118x80x1104x2128x90x1114x2138x100x1124x2148x110x1134x2158x120x1144x2168x130x1154x2178' #Thumb Mode, Default JP title, show Chinese and Japanese only, big pic mode in detail page

def DownloadTorrent(Page):
	global HEADERS,COOKIES,INNERSITE,OUTERSITE
	TorCount=int(findSTR(Page,TORRPAGE_REGS[0])[0])
	#print(TorCount)
	if 0!=TorCount:
		TorDetail=findSTR(Page,TORRPAGE_REGS[1])
		print(str(TorCount)+" torrents found")
		if(len(TorDetail)<TorCount):
			print(str(TorCount-len(TorDetail))+"torrents are unavailable now")
			if(0==len(TorDetail)):
				return False
		index=1
		for Tor in TorDetail:
			print("\n"+str(index)+".\tFile Name: "+Tor[9]+"\n\tFile Size: "+Tor[2]+"\n\tUpload Time: "+Tor[1]+"\n\tTorrent Number: "+Tor[0]+"\n\tDownloaded: "+Tor[5]+"\n\tUploader: "+Tor[6])
			index+=1
		isDownloadTorrent=input("Download Torrent?(Y/N): ")
		isDownloadTorrent='y'==isDownloadTorrent or 'Y'==isDownloadTorrent
		if isDownloadTorrent:
			Torrent=1 if TorCount==1 else 0
			while(int(Torrent)>TorCount or Torrent<=0):
				Torrent=int(input("Which torrent do you want to download?(1 - "+str(TorCount)+")"))
			TorFile=TorDetail[Torrent-1][7].split('/')[5]
			Torrent=requests.get(TorDetail[Torrent-1][7],headers=HEADERS,cookies=COOKIES).content
			TorFile=open(os.path.join('Downloads',Tor[9]+"_"+TorFile),'wb')
			TorFile.write(Torrent)
			TorFile.close()
			return True
		return False
	else:
		#print(TorPage)
		print("Cannot find Torrents")
		return False

isContinue=True
DOWN_LINK=input("Type Address or Download Number: ")
while(isContinue):
	TorrParams={}
	COOKIES['uconfig']=BASE_CONF
	if 2==len(DOWN_LINK.split(' ')):
		T=DOWN_LINK.split(' ')
		DOWN_LINK=INNERSITE+'g/'+T[0]+'/'+T[1]+'/'
		TorrParams={'gid':T[0],'t':T[1]}
		AlyzParams=[T[0],T[1]]
	else:
		T=DOWN_LINK.split('/')
		TorrParams={'gid':T[4],'t':T[5]}
		AlyzParams=[T[4],T[5]]
	TorPage=requests.get(INNERSITE+'gallerytorrents.php',params=TorrParams,headers=HEADERS,cookies=COOKIES)
	COOKIES=SetSessionCookie(TorPage.cookies.items())
	COOKIES['uconfig']=BASE_CONF
	if not DownloadTorrent(TorPage.text):
		Anlyz=requests.get(OUTERSITE+'g/'+AlyzParams[0]+'/'+AlyzParams[1]+'/',headers=HEADERS,cookies=COOKIES)
		if findSTR(Anlyz.text,"This gallery has been removed or is unavailable."):
			Anlyz=requests.get(INNERSITE+'g/'+AlyzParams[0]+'/'+AlyzParams[1]+'/',headers=HEADERS,cookies=COOKIES)
		'''
		Anlyz=open('test.html','rb').read().decode('utf-8','ignore')
		
		REGS=[
			'<h1 id="gn">(.*?)</h1>',
			'<h1 id="gj">(.*?)</h1>',
			'<div id="gdn"><a href="https://exhentai.org/uploader/(.*?)">',
			'Posted:</td><td class="gdt2">(.*?)</td>',
			'Parent:</td><td class="gdt2"><a href="(.*?)">(.*?)</a></td>',
			'Visible:</td><td class="gdt2">(.*?)</td>',
			'Language:</td><td class="gdt2">(.*?) .*?;</td>',
			'File Size:</td><td class="gdt2">(.*?)</td>',
			'Length:</td><td class="gdt2">(.*?)</td>',
			'Favorited:</td><td class="gdt2".*?>(.*?)</td>',
			'Rating:</td>.*?rating_count">([0-9]+)</span>.*?Average: ([0-9\.]+)</td>',
			'((<tr><td class="tc">(.*?):</td><td>(<div id=.*? class=.*? style=.*?><a id=.*? href=.*? class=.*? onclick=.*?>(.*?)</a></div>)+</td></tr>)+)',
			'(<div class="gdtm".*?<a href="(.*?)">)',
			'<table class="ptb".*?<tr>((<td.*?</td>)+)</tr>'
		]
		
		print(Anlyz.url)
		Anlyz=Anlyz.text
		
		DoujiInfo="\nRomaonn Title: "+('Null' if []==findSTR(Anlyz,REGS[0]) else findSTR(Anlyz,REGS[0])[0])
		DoujiInfo+='\nJapanese Titlte: '+('Null' if []==findSTR(Anlyz,REGS[1]) else findSTR(Anlyz,REGS[1])[0])
		DoujiInfo+="\nUploader: "+('Null' if []==findSTR(Anlyz,REGS[2]) else findSTR(Anlyz,REGS[2])[0])
		DoujiInfo+="\nPost Time: "+('Null' if []==findSTR(Anlyz,REGS[3]) else findSTR(Anlyz,REGS[3])[0])
		DoujiInfo+="\nParent: "+("Null" if []==findSTR(Anlyz,REGS[4]) else findSTR(Anlyz,REGS[4])[0][0])
		DoujiInfo+="\nVisible: "+findSTR(Anlyz,REGS[5])[0]
		DoujiInfo+="\nLanguage: "+findSTR(Anlyz,REGS[6])[0]
		DoujiInfo+="\nFile Size: "+findSTR(Anlyz,REGS[7])[0]
		DoujiInfo+="\nLength: "+findSTR(Anlyz,REGS[8])[0]
		DoujiInfo+="\nFavorited Time: "+findSTR(Anlyz,REGS[9])[0]
		DoujiInfo+="\nRating Time: "+findSTR(Anlyz,REGS[10])[0][0]
		DoujiInfo+="\nAverage Rating: "+findSTR(Anlyz,REGS[10])[0][1]
		print(DoujiInfo)
		
		DoujinClasses={}
		temp=findSTR(findSTR(Anlyz,REGS[11])[0][0],'<tr><td class="tc">(.*?):</td><td>(.*?)</td>')
		for Class in temp:
			DoujinClasses[Class[0]]=findSTR(Class[1],'<a.*?>(.*?)</a>')
		print(DoujinClasses)
		DoujinPages='1'
		temp=findSTR(findSTR(Anlyz,REGS[13])[0][0],'<a.*?>(.*?)</a>')
		if(len(temp)>1): DoujinPages=temp[-2]
		print(DoujinPages)
		'''
		# get download link
		DoujinDownPages=[]
		temp=findSTR(Anlyz.text,b"(<div class=\"gdtm\".*?<a href=\"(.*?)\">)")
		for Page in temp:
			DoujinDownPages+=[Page[1]]
			print(Page[1])
		if 1 < int(DoujinPages):
			for i in range(1,int(DoujinPages)+1):
				temp=findSTR(requests.get(INNERSITE+'g/'+AlyzParams[0]+'/'+AlyzParams[1]+'/',params={'p':str(i)},headers=HEADERS,cookies=COOKIES).text,REGS[12])
				for Page in temp:
					DoujinDownPages+=[Page[1]]
					print(Page[1])
		print(DoujinDownPages)
			
	
	for reg in REGS:
		print(findSTR(Anlyz.text,reg))
		
		#print(TorPage)
		print(TorCount)
		print(TorNum)
		'''
		'''
	isContinue=input("\n继续下载？（Y/N）：")
	isContinue='y'==isContinue or 'Y'==isContinue