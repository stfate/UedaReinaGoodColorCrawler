#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package
@brief
@author stfate
"""

import subprocess
import os
import json


CRAWLER_DIR = os.path.dirname( os.path.abspath(__file__) )

def get_page_urls():
    """ 各記事のURLを取得する
    @param None
    @return 下記dictionaryのリスト
        {
            "title": 記事タイトル,
            "url": 記事URL,
            "date": 記事の日付
        }
    """
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

def download_article(article_dict, output_dir):
    """ 各記事のメタデータ&画像を保存する
    @param article_dict get_page_urls()の出力の1要素
    @param output_dir 保存先ディレクトリパス
    @return
        meta = {
            "title": 記事タイトル,
            "url": 記事URL,
            "date": 記事の日付,
            "text": 記事本文のタグ付きテキスト,
            "info_box": プロフィールやお店情報が記載された部分のタグ付きテキスト,
            "img_urls": 画像URLのリスト
        }
    """
    output_dir = os.path.abspath(output_dir)
    cur_dir = os.getcwd()
    os.chdir(CRAWLER_DIR)

    cmd = [
        "scrapy", "crawl", "good-color-download",
        "-a", f"url={article_dict['url']}",
        "-a", f"date={article_dict['date']}",
        "-a", f"out={output_dir}",
        "-t", "json",
        "-o", "-"
    ]
    output_str = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")
    output_dict = json.loads(output_str)
    os.chdir(cur_dir)

    return output_dict