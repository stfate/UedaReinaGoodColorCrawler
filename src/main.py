#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package main.py
@brief a main script for good_color_crawler
@author stfate
"""

import good_color_crawler
import progressbar



if __name__ == "__main__":
    output_dir = "../data"

    articles = good_color_crawler.get_page_urls()

<<<<<<< HEAD:src/good_color_crawler.py
    # bar = progressbar.ProgressBar()
    # for _article in bar(articles):
        # good_color_crawler.download_images(_article)

    good_color_crawler.download_images(articles[0])
    
=======
    bar = progressbar.ProgressBar()
    for _article in bar(articles):
        good_color_crawler.download_article(_article, output_dir)
>>>>>>> 2207ea905b946fe51f5f84c5e3d4baea540bcb6c:src/main.py
