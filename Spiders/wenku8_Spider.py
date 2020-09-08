# -*- coding:utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup as bs4
import time


class Wenku8Spider():
    def __init__(self):
        self.__HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
            'referer': 'https://www.wenku8.net/index.php',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        self.__wenku8_session = requests.Session()

    def __getHTMLContent(self, url: str):
        return bs4(self.__wenku8_session.get(url, headers=self.__HEADERS).content, 'html.parser')

    def __toValidFileName(self, file_name: str):
        return '-'.join(re.split(r'[/\\:\*\?"<>|]', file_name))

    def __getNovelInfoUrlFromId(self, id: int):
        url = 'https://www.wenku8.net/book/%d.htm' % id
        return self.__getHTMLContent(url)

    def __getNovelCatalogFromId(self, id: int):
        url = 'https://www.wenku8.net/novel/%d/%d/index.htm' % (
            int(id/1000), id)
        return self.__getHTMLContent(url)

    def GetNovelInfoById(self, begin_id: int, end_id: int):
        with open('Infos.csv', 'w+', encoding='utf-8') as fp:
            for id in range(begin_id, end_id+1):
                info_page = self.__getNovelInfoUrlFromId(id)
                try:
                    (name, author, wenku,
                     _) = info_page.title.contents[0].split(' - ')
                    all_tds = info_page.find_all('td', width='20%')
                    status = all_tds[2].string.split('：')[1]
                    last_update = all_tds[3].string.split('：')[1]
                    length = all_tds[4].string.split('：')[1]
                except KeyboardInterrupt:
                    print('You canceled the operation. Current: %d' % id)
                    exit(0)
                except:
                    print('%04d, Cannot get informations.' % id)
                    continue
                line = '%04d,%s,%s,%s,%s,%s,%s\n' % (
                    id, name, author, wenku, status, last_update, length)
                print(line, end='')
                fp.write(line)
                time.sleep(1)

    def GetNovelContent(self, id: int):
		base_url = 'https://www.wenku8.net/novel/%d/%d/%s' % (int(id/1000), id)
        category_page = self.__getNovelCatalogFromId(id)  # 小说内容的页面

        main_menu = category_page.find(
            'table', class_='css').find_all('td')  # 获取全部目录
        VolName = ''  # 卷名

        for td in main_menu:
            if not td.find('a'):  # 如果没有目录
                continue
            if td.has_attr('colspan'):  # 如果是章节名
                print(VolName)
                VolName = td.text
                continue
            ChapName = td.text  # 章节名
            print('获取章节: '+VolName+' '+ChapName, end='...   ')
            ChapURL = td.find('a')['href']  # 获取下载url
            print('Chapter URL: %s' % (base_url%ChapURL))
            content = self.__getHTMLContent(base_url%ChapURL)  # 获取内容页面
            # content=bs4(open('123.html').read(),"html.parser")
            content = content.find(id='content')
            article = content.string  # 获取小说
            imgs = content.find_all('img')  # 获取网页中的图片
            print('完成')

            # 文件夹操作
            VolName = validateFileName(VolName)
            ChapName = validateFileName(ChapName)
            if not os.path.exists(VolName):
                os.makedirs(VolName)

            # 写入文件
            for imgLink in imgs:
                if not os.path.exists(VolName+'/'+ChapName):
                    os.mkdir(VolName+'/'+ChapName)
                imgLocal = str(imgLink['src']).split('/')[-1]
                print('下载图片: '+imgLink, end='...   ')
                imgContent = requests.get(imgLink['src']).content
                fp = open(VolName+'/'+ChapName+'/'+imgLocal, 'wb')
                fp.write(imgContent)
                fp.close()
                print('完成')
            if article == '':
                continue
            print('写入小说内容...   ', end=' ')
            fp = open(VolName+'/'+ChapName+'.txt', 'w', encoding='utf-8')
            fp.write(VolName+"\n"+ChapName+"\n"+article)
            fp.close()
            print('完成')
            time.sleep(1)


if '__main__' == __name__:
    pass
