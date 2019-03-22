# -*- coding:utf-8 -*-
import requests
from mylib import exist

COOKIE_FILE='./ehcookie'
REQ_HEAD= {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection':'keep-alive',
	'Host':'',
	'Referer':'',
}
'''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Host: forums.e-hentai.org
Referer: https://forums.e-hentai.org/index.php?
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36
'''

def GetLocalCookies(LOCAL_FILE="eh-cookie"):
	if not exist(LOCAL_FILE):
		LOGGIN=input('是否登陆（Y/N）：')
		if ('Y'==LOGGIN or 'y'==LOGGIN):
			UN=input('输入用户名：')
			UP=input('输入密码：')
			reqURL='https://forums.e-hentai.org/index.php?act=Login&CODE=01'
			data={'referer':'https://forums.e-hentai.org/index.php?','b':'','bt':'','UserName':UN,'PassWord':UP,'CookieDate':'1','submit':'Log me in'}
			r=requests.post(reqURL,data=data).cookies.items()
			F=open(LOCAL_FILE,"a+")
			cookies={r[0][0]:r[0][1],r[1][0]:r[1][1]}
			F.write(str(cookies))
			F.close()
		else:
			return False
	if exist(LOCAL_FILE):# 读取用户
		return eval(open(LOCAL_FILE).read())
	else:
		return False

def PrintOut(msg):
	print(msg,end='')
	return msg

def SetSessionCookie(req,file="eh-cookie"):
	cookies=GetLocalCookies(file)
	for c in req:
		cookies[c[0]]=c[1]
	F=open(file,'w')
	F.write(str(cookies))
	F.close()
	return cookies
'''
class EHLogin():
	def __init__(self):
		self.loginForm={
			"referer":"https://forums.e-hentai.org/index.php?",
			"b":"",
			"bt":"",
			"UserName":'',
			"PassWord":'',
			"CookieDate":"1",
			"Privacy":"1",
			"submit":"Log me in"
		}
		if exist(COOKIE_FILE):
			Logout=input('Do you want to logout?')
			if Logout:
				self.clearCookie(COOKIE_FILE)
		else:
			method=0
			while method==1 or method==2:
				method=input('whitch way do you want to login?\n1. username and password\n2. cookie')
			if method==1:
				name=input('Enter your username: ')
				pw=input('Enter your password:')
				reqURL='https://forums.e-hentai.org/index.php?act=Login&CODE=01'
				data={'referer':'https://forums.e-hentai.org/index.php?','b':'','bt':'','UserName':name,'PassWord':pw,'CookieDate':'1','submit':'Log me in'}
				cookies=requests.post(reqURL,data=data).cookies.items()
			elif method==2:
				cookies={}
				cookies[2]=input('Please input your "ipb_member" cookie')
			storeCookie=open(COOKIE_FILE,'a+')
			C={}
			for i in cookies:
				C[cookies[i][0]]=cookies[i][1]
			storeCookie.write(C)
			storeCookie.close()
	def checkCookie(self):
		try:
			cookies=eval(open(COOKIE_FILE,'r').read())
		except:
			return False
		if type(cookies) is not 'dict':
			return False
		elif cookies['']:
			return False
	def getCookie(self):
		if checkCookie():
			return {[]:cookies[],[]:cookies[]}
		else:
			return False
	def refreshCookie(self,Req):
    	cookies=Req.cookies.items()
		storeCookie=open(COOKIE_FILE,'a+')
		C={}
		for i in cookies:
			C[cookies[i][0]]=cookies[i][1]
		storeCookie.write(C)
		storeCookie.close()
	def isLoggin(self):
		return self.checkCookie()


class EHPage():
    def __init__(self, tags='',page=0,isLoggin=False):
		OPTION={'f_apply':'Apply Filter','f_search':tags}
		for i in ['f_doujinshi','f_manga','f_artistcg','f_gamecg','f_western','f_non-h','f_imageset','f_cosplay','f_asianporn','f_misc']:
			OPTION[i]=1
'''
		