# -*- coding: utf-8 -*-

"""
@package good_color.py
@brief 上田麗奈さん「この色、いいな」(https://webnewtype.com/column/color/)のクローラ
@author stfate
"""

import scrapy
import requests
import datetime
import os
import json
import time


class GoodColorCrawlSpider(scrapy.Spider):
    name = "good-color-crawl"
    ROOT_URL = "https://webnewtype.com"
    
    def start_requests(self):
        urls = [
            f"{self.ROOT_URL}/column/color/",
            f"{self.ROOT_URL}/column/color/p2/",
            f"{self.ROOT_URL}/column/color/p3/",
            f"{self.ROOT_URL}/column/color/p4/"
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
                "url": f"{self.ROOT_URL}{page_url}",
                "date": date
            }

class GoodColorDownloadSpider(scrapy.Spider):
    name = "good-color-download"
    
    def start_requests(self):
        self.url = getattr(self, "url", None)
        self.date = getattr(self, "date", None)
        self.output_root = getattr(self, "out", None)

        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        meta = {
            "title": "",
            "url": self.url,
            "date": self.date,
            "text": "",
            "info_box": "",
            "img_urls": []
        }

        # title
        div_title = response.css("div.column_titleBox")
        title = div_title.css("h1::text").extract_first()
        meta["title"] = title

        # main text
        div_main_text = response.css("div.column_mainTextBox_second")
        main_text = "".join(div_main_text.css("div *").extract())
        meta["text"] = main_text

        # additional text
        div_add_text = response.css("div.column_additionalBox")
        add_text = "".join(div_add_text.css("div *").extract())
        meta["info_box"] = add_text

        # images
        div_img_area = response.css("div.related_imgArea")
        li_list = div_img_area.css("li")
        for _li in li_list:
            img_src = _li.css("li a div.imgArea div.imgBox img::attr(src)").extract_first()
            img_src = img_src.replace("/w98h98/", "")
            meta["img_urls"].append(img_src)
            img_save_dir = os.path.join( self.output_root, self.date, "images")
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

        meta_save_dir = os.path.join(self.output_root, self.date)
        meta_fn = os.path.join(meta_save_dir, "meta.json")
        json.dump(meta, open(meta_fn, "w"), ensure_ascii=False, indent=2, sort_keys=True)

        return meta
