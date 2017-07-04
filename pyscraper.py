#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-03 11:35:52
# Project: bg

from pyspider.libs.base_handler import *
import os


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.beautylegmm.com/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        allpagenum = response.doc('.page-navigator').children().children().eq(-2).text()
        for each in range(1, (int(allpagenum)+1)):
            if each == 1:
                self.crawl("http://www.beautylegmm.com/", callback=self.albumlist_page)
            else:
                self.crawl("http://www.beautylegmm.com/index-%d.html" % each, callback=self.albumlist_page)
    
    @config(age=10 * 24 * 60 * 60)
    def albumlist_page(self, response):
        for each in response.doc('.post_weidaopic').children().items():
            self.crawl(each.attr.href, callback=self.album_page)

    @config(priority=2)
    def album_page(self, response):
        allpagenum = response.doc('.archives_page_bar').children().eq(-2).text()
        for each in range(1, (int(allpagenum)+1)):
            self.crawl((response.url + '?page=%d' % each), callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        albumpath = 'result/' + response.doc('.title').text() + '/'
        if os.path.exists(albumpath):
            pass
        else:
            os.makedirs(albumpath)
        for each in response.doc('.post').find('img').items():
            imgname = each.attr.alt
            file_path = albumpath + os.path.basename(each.attr.src)
            self.crawl(each.attr.src, callback=self.save_img, save={'file_path':file_path, 'img_name':imgname})
            
    @config(priority=2)
    def save_img(self, response):
        content = response.content
        img_name = response.save["img_name"]
        file_path = response.save["file_path"]
        f = open(file_path,"wb")
        f.write(content)
        f.close()
        return {
            'url': response.url,
            'title': img_name,
        }
