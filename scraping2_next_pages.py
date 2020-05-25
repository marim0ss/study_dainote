#coding: UTF-8
# https://code.dividable.net/tutorials/scraping-category-pages/
import requests
import pandas as pd
from bs4 import BeautifulSoup
import pprint

html_doc = requests.get("https://dividable.net/").text
category_li_path = "nav#category ul li a"  # カテゴリ名はnav#category > ul > li > a の中

soup = BeautifulSoup(html_doc, 'html.parser')

category_html_list = soup.select(category_li_path) #select: CSSセレクタが使える
# pprint.pprint(category_html_list)

"""
# -------------------------------------------------------
データを扱いやすいよう、辞書型のデータ
 {key: value, key: value, ....} の形式
に変換
# -------------------------------------------------------
"""
category_dict = {}
for category_html in category_html_list:
    # URL                                       # 名前
    category_dict[category_html.get("href")] = category_html.string
pprint.pprint(category_dict)
"""
{'https://dividable.net/category/career/': 'IT転職',
 'https://dividable.net/category/freelance/': 'ITフリーランス',
 'https://dividable.net/category/nisotsu-tenshoku/': '一般転職',   ......}
"""
# カテゴリURLにアクセスする
category_res = requests.get("https://dividable.net/category/python/").text  # python学習のページ
# print(category_res)

# -------------------------------------------------------
# 「次へ」があれば、次のページに遷移する (「次へ」はclass "next")
# -------------------------------------------------------
soup = BeautifulSoup(category_res, 'html.parser')
a_next_tag = soup.find_all("a", {"class": "next"})  # 次へがあるか確認するコード
# pprint.pprint(a_next_tag)
""" 考え方：
#2ページ目で「次へ」を探す→ちゃんとある
category_res = requests.get("https://dividable.net/category/python/page/3").text
soup = BeautifulSoup(category_res, 'html.parser')
a_next_tag= soup.find_all("a", {"class": "next"}) # 次へがあるか確認するコード
print (a_next_tag)

#最後のページで試した場合、a_next_tagは空になる
category_res = requests.get("https://dividable.net/category/python/page/5").text
soup = BeautifulSoup(category_res, 'html.parser')
a_next_tag= soup.find_all("a", {"class": "next"}) # 次へがあるか確認するコード
print (a_next_tag)   # -> []
"""
page_count = 1
category_res = ""
while True:
    # str() : 数値を文字列に変換する。→文字列に数値を連結できる（変換しないと連結できない）
    category_res = requests.get("https://dividable.net/category/python/" + "page/" + str(page_count)).text
    # print(category_res)
    soup = BeautifulSoup(category_res, 'html.parser')
    print("{}ページ目".format(page_count))
    a_next_tag = soup.find_all("a", {"class": "next"})  # 次へがあるか確認するコード
    if a_next_tag:
        page_count += 1
        continue  # 次のループへ
    break         # a_next_tagがなくなったら処理を中断
print("完了")
