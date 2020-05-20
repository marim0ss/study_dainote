#coding: UTF-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pprint

# こちらで用意したHTML
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
# BeautifulSoupの初期化
soup = BeautifulSoup(html, 'html.parser') # BeautifulSoupの初期化
# print(soup.prettify())

# print(soup.title)  # titleタグの内容ごと取得
# print(soup.title.string) # titleタグの中身を取得(k中身が分断されてなければ)
# print(soup.body.text)      # bodyのテキスト部分のみ
tags = soup.find_all("a")
# pprint.pprint(tags)

for a_html in tags:     # aタグのテキストを抜き出し
    print(a_html.text)

#soup.a.get("href")     # aタグ内のURL部分（href）を取得する
for link in tags:
    print(link.get("href"))
# -------------------------------------------------------
# 実際のサイトのスクレイピング
# -------------------------------------------------------
# requests：requests.get(url)でページ情報取得→.textでHTML内容を取得
html_doc = requests.get("https://crossfor.co.jp/").text
soup = BeautifulSoup(html_doc, 'html.parser') 
# print(soup.prettify())
"""
a_tags = soup.find_all("a")

for tag in a_tags:
    pprint.pprint(tag.text)
for link in a_tags:
    print(link.get("href"))
"""
"""
# -------------------------------------------------------
# Classを指定して要素を取得
# -------------------------------------------------------
"""
p_tags = soup.find_all("p", {"class": "dateLabel"})
pprint.pprint(p_tags)

for tag in p_tags:
    print(list(tag.strings))   # pタグの中には２箇所テキストがある
    pprint.pprint(tag.time.string)
    pprint.pprint(tag.a.string)
    print(tag.a.get("href"))
"""
# -------------------------------------------------------
pandas: CSVにデータを保存しよう
# -------------------------------------------------------
"""
# まずは列名を作成
columns = ["name", "url"]
df2 = pd.DataFrame(columns=columns) # 列名を指定する
# print(df)
# 記事名と記事URLをデータフレームに追加
for tag in p_tags:
    name = tag.a.string
    url = tag.a.get("href")
    # 行の作成
    se = pd.Series([name, url], columns)
    print(se)
    df2 = df2.append(se, columns) # データフレームに行を追加
    print(df2)

# 作成したデータフレームをCSVに変換
#df.to_csv(“ファイル名.csv”)でcsvファイルを作成できます。