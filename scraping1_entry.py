#coding: UTF-8
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pprint

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
    # print(se)
    df2 = df2.append(se, columns) # データフレームに行を追加
    print(df2)
"""
# -------------------------------------------------------
# 作成したデータフレームをCSVに変換
#pandasの.to_csv(“ファイル名.csv”)でcsvファイルを作成できます。
# -------------------------------------------------------
"""
filename = '../study_dainote/cf_information.csv'
df2.to_csv(filename, encoding = 'utf-8')
print('csvファイルを出力しました')