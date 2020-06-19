# -*- coding: utf-8 -*-
import requests
import time
import os
import multiprocessing
import re
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Upgrade-Insecure-Requests':'1'}
def saveFile(url,path):
    response = requests.get(url,headers=headers)
    with open(path, 'wb') as f:
        f.write(response.content)
        f.flush()
def getWebsite(url,time1,spath):
    site    = requests.get(url,headers = headers)
    content = site.text
    soup    = BeautifulSoup(content, 'lxml') 
    divs    = soup.find_all(class_ = 'gdtm')
    title   = soup.h1.get_text()
    rr=r"[\/\\\:\*\?\"\<\>\|]" 
    new_title2 = re.sub(rr, "-", title) 
    page    = 0
    i       = 0
    for div in divs:
        picUrl = div.a.get('href')
        page   = page+1
        print('下载中 '+new_title2+str(page)+'.jpg')
        try:
            saveFile(getPicUrl(picUrl),spath+new_title2+'/'+new_title2+str(page)+'.jpg')
        except:
            print('无法下载'+new_title2+str(page)+'.jpg')
        else:
            print('成功')
            i = i+1
    print('成功 下载'+str(page)+' 个文件,'+str(i))
    endTime1 = time.time()
    print("耗时：",end=' ')
    print(endTime1-time1)
    print("再撸一个？")
    menu()
def getPicUrl(url):
    site_2      = requests.get(url,headers = headers)
    content_2 = site_2.text
    soup_2    = BeautifulSoup(content_2, 'lxml') 
    imgs      = soup_2.find_all(id="img")
    for img in imgs: 
        picSrc=img['src']
        return picSrc
def menu():
    print('只能爬取e-hentai表站下的内容')
    url = input('输入 url\n')
    spath = input('输入完整的保存路径,结尾以    / 结束(注意使用正斜杠"/")\n')
    startTime1 = time.time()
    if (url.find('https://e-hentai.org/g/') != -1):
        print('--获取信息中--')
        try:
            site    = requests.get(url,headers = headers)
            content = site.text
            soup    = BeautifulSoup(content, 'lxml') 
            divs    = soup.find_all(class_ = 'gdtm')
            title   = str(soup.h1.get_text())
            page    = 0
            for div in divs:
                page = page+1
        except:
            print('错误，重试')
            menu()
        else:
            print('本子名 '+title+',共 '+str(page)+' 页,开始爬取')
            rr=r"[\/\\\:\*\?\"\<\>\|]" 
            new_title = re.sub(rr, "-", title) 
            if os.path.exists(spath+new_title):
                getWebsite(url,startTime1,spath)
            else:
                os.mkdir(spath+new_title)
                getWebsite(url,startTime1,spath)
    else:
        print('非e-hentai url,重新输入\n')
        menu()
menu()
