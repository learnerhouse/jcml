# -*- coding: utf-8 -*-
'''
Created on 2017年6月28日

@author: wyq
'''
import  url_manager, html_downloader, html_outputer
import  html_parser


class SpiderMain(object):

    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()



    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try :
                new_url = self.urls.get_new_url()
                print('craw %d : %s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)


                if count == 100:
                    break
                count = count + 1
            except Exception as e:
                print('craw failed',e)

        self.outputer.output_html()                 #输出网页文件
        self.outputer.output_excel()                #输出excel格式
        print("Work Done!")

if __name__ == "__main__":
    root_url = "https://baike.baidu.com/item/QQ"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)