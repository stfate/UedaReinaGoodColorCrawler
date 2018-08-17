#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package
@brief
@author stfate
"""

import good_color_crawler
import progressbar


if __name__ == "__main__":
    articles = good_color_crawler.get_page_urls()

    bar = progressbar.ProgressBar()
    for _article in bar(articles):
        good_color_crawler.download_images(_article)
