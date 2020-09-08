# -*- coding:utf-8 -*-
import re
import os
import urllib.parse
import urllib.request
from hashlib import md5


def md5Encode(str):  # MD5校检
    m = md5(str)
    m.update(bin)
    return m.hexdigest()


def md5sum(fname):
    fp = open(fname, 'rb')
    content = fp.read()
    fp.close()
    m = md5Encode(content)
    return m


def checkOK(fname, fmd5):
    r = False
    if fmd5 == md5sum(fname):
        r = True
    return r

# 文件操作


def dirEx(pat):  # 创建文件夹
    if not os.path.exists(pat):
        os.makedirs(pat)
    else:
        if not os.path.isdir(pat):
            os.remove(pat)
            os.makedirs(pat)
    return


def cd(pat):
    dirEx(pat)
    os.chdir(pat)


def toAllowed(name):  # 转换文件名为合法
    p = str(name)
    p = p.replace("/", "·").replace(":", "：").replace("*", "·")
    p = p.replace("?", "？").replace("\"", "'").replace("<", "《")
    p = p.replace(">", "》").replace("|", "·").replace("\\", "·")
    return p


def fileREAD(file):  # 读取文件
    F = open(file)
    f = F.read()
    F.close()
    return str(f)


def addAshow(msg, FILE, noEnter=False):  # 写入文件并回显
    if noEnter:
        FILE.write(msg)
        return(msg)
    FILE.write(msg+"\n")
    print(msg)


def exist(fname):  # 判断存在
    return os.path.exists(fname)


def getHTML(url, data=[], cookie=False):  # 获取网页操作
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    headers = {'User-Agent': UA}
    if not data:
        req = urllib.request.Request(url, headers=headers)
    else:
        req = urllib.request.Request(
            url, urllib.parse.urlencode(data), headers)
    if cookie:
        cookies = cookiejar.MozillaCookieJar(cookie)
        handler = request.HTTPCookieProcessor(cookies)
        opener = request.build_opener(handler)
        response = opener.open(req)
        response = response.read().decode("utf-8")
        return response
    response = urllib.request.urlopen(req)
    response = response.read().decode("utf-8")
    return response


def readcookie(file, url):
    cookie = cookiejar.MozillaCookieJar(file)
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    response = opener.open(url)
    cookie.save(ignore_discard=True, ignore_expires=True)
    return cookie


def findSTR(str, reg):
    pattern = re.compile(reg)
    lst = pattern.findall(str, re.M)
    return lst


def HTML_get(url, regexp):
    return findSTR(getHTML(url), regexp)


def spc2plus(str):  # 下载
    return urllib.parse.urlencode(str)


def download(url, path):
    urllib.request.urlretrieve(url, path)
