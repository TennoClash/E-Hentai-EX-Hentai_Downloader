# -*- coding: utf-8 -*-
import requests
import time
import os
import tkinter as tk
from tkinter import filedialog
import urllib
import re
from bs4 import BeautifulSoup
from _overlapped import NULL

print("E-Hentai&EX-Hentai下载器V1.0")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1'}


def saveFile(url, path, cookiep):
    if (cookiep != NULL):
        response = requests.get(url, headers=headers, cookies=cookiep)
    else:
        response = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(response.content)
        f.flush()


def getWebsite(url, time1, spath, cookiep):
    if cookiep != NULL:
        site = requests.get(url, headers=headers, cookies=cookiep)
    else:
        site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    title = soup.h1.get_text()
    rr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title2 = re.sub(rr, "-", title)
    page = 0
    i = 0
    for div in divs:
        picUrl = div.a.get('href')
        page = page + 1
        print('下载中 ' + new_title2 + str(page) + '.jpg')
        try:
            saveFile(getPicUrl(picUrl, cookiep), spath + new_title2 + '/' + new_title2 + str(page) + '.jpg', cookiep)
        except:
            print('无法下载' + new_title2 + str(page) + '.jpg')
        else:
            print('成功')
            i = i + 1
    print('成功 下载' + str(page) + ' 个文件,' + str(i))
    endTime1 = time.time()
    print("耗时：", end=' ')
    print(endTime1 - time1)



def getPicUrl(url, cookiep):
    if (cookiep != NULL):
        site_2 = requests.get(url, headers=headers, cookies=cookiep)
    else:
        site_2 = requests.get(url, headers=headers)
    content_2 = site_2.text
    soup_2 = BeautifulSoup(content_2, 'lxml')
    imgs = soup_2.find_all(id="img")
    for img in imgs:
        picSrc = img['src']
        return picSrc


def menu_single_download(e_or_ex, cookies2):
    url = input('输入 url\n')
    print("选择保存位置文件夹")
    root = tk.Tk()
    root.withdraw()
    spath = filedialog.askdirectory() + "/"
    print('保存路径:', spath)
    startTime1 = time.time()
    if url.find('https://e-hentai.org/g/') != -1 or url.find('https://exhentai.org/g/') != -1:
        print('--获取信息中--')
        try:
            if (e_or_ex == "2"):
                site = requests.get(url, headers=headers, cookies=cookies2)
            else:
                site = requests.get(url, headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            divs = soup.find_all(class_='gdtm')
            title = str(soup.h1.get_text())
            page = 0
            for div in divs:
                page = page + 1
        except:
            print('错误,输入或网络问题')
            menu()
        else:
            print('本子名 ' + title + ',共 ' + str(page) + ' 页,开始爬取')
            rr = r"[\/\\\:\*\?\"\<\>\|]"
            new_title = re.sub(rr, "-", title)
            if os.path.exists(spath + new_title):
                getWebsite(url, startTime1, spath, cookies2)
            else:
                os.mkdir(spath + new_title)
                getWebsite(url, startTime1, spath, cookies2)
    else:
        print('非e站 url,重新输入\n')
        menu()


def menu_tag_urls(cookies2, f_tag, f_tag_num):
    page_line_count = 25
    urls = []
    if cookies2 != NULL:
        url = 'https://exhentai.org/?f_search=' + f_tag + '&page='
    else:
        url = 'https://e-hentai.org/?f_search=' + f_tag + '&page='

    print('爬取前' + str(f_tag_num) + '本')
    print('--获取信息中--')
    try:
        int_pages = f_tag_num // page_line_count
        line_mod = f_tag_num % page_line_count
        for int_page in range(0, int_pages + 1):
            if cookies2 != NULL:
                site = requests.get(url + str(int_page), headers=headers, cookies=cookies2)
            else:
                site = requests.get(url + str(int_page), headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            tds = soup.find_all(class_='glname')
            print('当前页面:' + url + str(int_page))
            for index, a in enumerate(tds):
                print(str(int_page * 25 + index + 1) + ':' + a.a['href'])
                urls.append(a.a['href'])

                if (25 > f_tag_num - 1 == index) or (
                        f_tag_num > 25 and int_page == int_pages and index == line_mod - 1):
                    break
    except:
        print('错误,输入或网络问题')
        menu()
    else:
        return urls


def menu_tag_download(m_urls, cookies2):
    print("选择保存位置文件夹")
    root = tk.Tk()
    root.withdraw()
    spath = filedialog.askdirectory() + "/"
    print('保存路径:', spath)
    startTime1 = time.time()
    print('--获取信息中--')
    for url in m_urls:
        try:
            if cookies2 != NULL:
                site = requests.get(url, headers=headers, cookies=cookies2)
            else:
                site = requests.get(url, headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            divs = soup.find_all(class_='gdtm')
            title = str(soup.h1.get_text())
            page = 0
            for div in divs:
                page = page + 1
        except:
            print('错误,输入或网络问题')
            menu()
        else:
            print('本子名 ' + title + ',共 ' + str(page) + ' 页,开始爬取')
            rr = r"[\/\\\:\*\?\"\<\>\|]"
            new_title = re.sub(rr, "-", title)
            if os.path.exists(spath + new_title):
                getWebsite(url, startTime1, spath, cookies2)
            else:
                os.mkdir(spath + new_title)
                getWebsite(url, startTime1, spath, cookies2)


def menu():
    cookies2 = NULL
    m_urls = []
    print('可爬取e-hentai和exhentai的表里站下的内容')
    print('Win10下使用可能会有卡住窗口缓冲区的问题，若遇到某张图片久久没有下载成功的情况，按任意键即可')
    print('*****注意*****需要爬取ehentai还是exhentai?')
    e_or_ex = input('ehentai输入1----exhentai输入2----按tag爬取输入3\n')
    if e_or_ex == "1":
        menu_single_download(e_or_ex, cookies2)
    if e_or_ex == "2":
        cookies_input = input('输入exhentai的cookies(在exhentai的页面下，在控制台中输入document.cookie所得到的内容)\n')
        cookies2 = dict(map(lambda x: x.split('='), cookies_input.split(";")))
        menu_single_download(e_or_ex, cookies2)
    if e_or_ex == "3":
        tag_e_or_ex = input('ehentai输入1----exhentai输入2\n')
        if tag_e_or_ex == '2':
            cookies_input = input('输入exhentai的cookies(在exhentai的页面下，在控制台中输入document.cookie所得到的内容)\n')
            cookies2 = dict(map(lambda x: x.split('='), cookies_input.split(";")))
        f_tag = input('输入tag--xxxx:xxx形式,多个tag示例--language:xx f:xxx--多个tag间用空格隔开\n')
        f_tag = urllib.parse.quote(f_tag)
        print(f_tag)
        f_tag_num = input('输入下载数量\n')
        f_tag_num = int(f_tag_num)
        m_urls = menu_tag_urls(cookies2, f_tag, f_tag_num)
        menu_tag_download(m_urls, cookies2)


menu()
