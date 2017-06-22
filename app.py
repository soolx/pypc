# -*- coding: utf-8 -*-

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os

def htmlparser(url):
    try:
        html = urlopen(url)
    except:
        print(url + '打开失败')
        try:
            html = urlopen(url)
        except:
            print(url + '再试打开失败')
    else:
        bsObj = BeautifulSoup(html, 'html.parser')
        return bsObj

folder = 'image'
def path(bsObj):
    albumname = bsObj.find('div', {'class':'title'}).h2.get_text()
    albumpath = folder + '/' + albumname
    return albumpath


def imagedownload(url):
    bsObj = htmlparser(url)
    imagelist = bsObj.find('div', {'class':'post'}).findAll('a',recursive=False)
    albumpath = path(bsObj)
    if os.path.exists(albumpath):
        pass
    else:
        os.makedirs(albumpath)   
    for image in imagelist:
        imagename = image.img.attrs['alt']
        imageurl = "http://www.beautylegmm.com/" + image.img.attrs['src']
        filename = os.path.basename(imageurl)
        print('正在下载' + imagename)
        try:
            urlretrieve(imageurl, '%s/%s' % (albumpath, filename))
        except:
            print(imagename + '下载失败')
            try:
                print('重试下载' + imagename)
                urlretrieve(imageurl, '%s/%s' % (albumpath, filename))
            except:
                print(imagename + '再次下载失败')

        print('下载完成')


def albumparser(albumurl):
    bsObj = htmlparser(albumurl)
    albumindexlist = bsObj.find('div', {'class':'archives_page_bar'}).findAll('a')
    count = albumindexlist[-2].get_text()
    print('开始下载新写真集')
    imagedownload(albumurl)
    for i in range(2, int(count)+1):
        imagedownload(albumurl + '?page=%s' % str(i))


albumlist = []
for i in range(1,71):
    if i == 1:
        bsObj = htmlparser("http://www.beautylegmm.com/")
    else:
        bsObj = htmlparser("http://www.beautylegmm.com/index-%d.html" % i)
    albumlist = albumlist + bsObj.findAll('div', {'class':'post_weidaopic'})
    print('完成第%d页索引' % i)

print('写真集索引完成')

for album in albumlist:
    albumurl = album.find('a').attrs['href']
    albumparser(albumurl)
