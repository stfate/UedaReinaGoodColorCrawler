#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package api.py
@brief
@author stfate
"""

import subprocess
import os
import json


CRAWLER_DIR = os.path.dirname( os.path.abspath(__file__) )

def get_page_urls():
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "good-color-crawl",
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)
    os.chdir(cur_dir)

    return output_dict

def download_images(article_dict):
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "good-color-download",
        "-a", f"url={article_dict['url']}",
        "-a", f"date={article_dict['date']}",
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)
    os.chdir(cur_dir)

    return output_dict
