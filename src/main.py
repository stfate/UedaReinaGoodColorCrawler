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

    bar = progressbar.ProgressBar()
    for _article in bar(articles):
        good_color_crawler.download_article(_article, output_dir)
