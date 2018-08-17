# -*- coding: utf-8 -*-

"""
@package good_color.py
@brief 上田麗奈さん「この色、いいな」の画像クローラ
@author stfate
"""

import scrapy
import requests
import datetime
import os
import time


class GoodColorCrawlSpider(scrapy.Spider):
    name = "good-color-crawl"
    ROOT_URL = "https://webnewtype.com"
    
    def start_requests(self):
        urls = [
            "{}/column/color/".format(self.ROOT_URL),
            "{}/column/color/p2/".format(self.ROOT_URL),
            "{}/column/color/p3/".format(self.ROOT_URL),
            "{}/column/color/p4/".format(self.ROOT_URL)
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        section_column_list = response.css("section#columnList div.listBox")
        li_list = section_column_list.css("ul li")
        for _li in li_list:
            # title
            title = _li.css("li div.leftText p.columnTitle::text").extract_first()

            # url
            page_url = _li.css("li a::attr(href)").extract_first()

            # date
            date_str = _li.css("li div.infoArea span.columnDate::text").extract_first()
            date_str = date_str.lstrip().split(" ")[0]
            d = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
            date = "{:04d}{:02d}{:02d}".format(d.year, d.month, d.day)

            yield {
                "title": title,
                "url": "{}{}".format(self.ROOT_URL, page_url),
                "date": date
            }

class GoodColorDownloadSpider(scrapy.Spider):
    name = "good-color-download"
    download_root = "../../data/downloads"
    
    def start_requests(self):
        self.url = getattr(self, "url", None)
        self.date = getattr(self, "date", None)

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        div_img_area = response.css("div.related_imgArea")
        li_list = div_img_area.css("li")
        for _li in li_list:
            img_src = _li.css("li a div.imgArea div.imgBox img::attr(src)").extract_first()
            img_save_dir = os.path.join( self.download_root, self.date)
            if not os.path.exists(img_save_dir):
                os.makedirs(img_save_dir)
            img_save_fn = os.path.join( img_save_dir, os.path.basename(img_src) )
            with open(img_save_fn, "wb") as fo:
                response = requests.get(img_src, stream=True)

                if not response.ok:
                    print(response)
                
                for block in response.iter_content(1024):
                    if not block:
                        break

                    fo.write(block)
            
            time.sleep(1.0)

            yield {"url": img_src}
