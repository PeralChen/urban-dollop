# -*- encoding: utf-8 -*-
# Created on 2018/05/20 By:Eddy
# Project: proxydb
from pyspider.libs.base_handler import *
import re
import os


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://proxydb.net/', callback=self.index_page)  # 访问主页

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')  # 提取页面所有链接

    def detail_page(self, response):
        for each in response.doc('td > a').items():
            self.crawl(each.attr.href, callback=self.ip_page, fetch_type='js')  # 提取IP详情页链接
            
    def ip_page(self, response):
            wall_proxy = response.doc('h4').text()  # 从h4得到字符串等待正则提取
            string=wall_proxy 
            proxy = re.findall(r"\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}:\d{0,5}",string)  # 正则提取IP端口            
            f = open('/home/proxy.txt','a')  # 将代理写入txt文件，文件在home下
            f.writelines(['\n',str(proxy)])
            f.close()
                
            return {
            "Proxy": proxy           
                }
  