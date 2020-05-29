#coding: UTF-8
# https://code.dividable.net/tutorials/scraping-category-pages/
import requests
import pandas as pd
from bs4 import BeautifulSoup
import pprint

"""
全カテゴリからデータを収集しよう
"""
# -------------------------------------------------------
# 2.title, url, categoryを列に持ったDataFrameを作成
# -------------------------------------------------------
columns = ["title", "url", "category"]  # 列名を作成
df = pd.DataFrame(columns=columns) # 列名を指定する
# print(df)


html_doc = requests.get("https://dividable.net/").text
category_li_path = "nav#category ul li a"  # カテゴリ名はnav#category > ul > li > a の中

soup = BeautifulSoup(html_doc, 'html.parser')

category_html_list = soup.select(category_li_path) #select: CSSセレクタが使える
# pprint.pprint(category_html_list)
# -------------------------------------------------------
# 3.カテゴリURLとカテゴリ名を持った辞書型オブジェクトを作成
# -------------------------------------------------------
category_dict = {}
for category_html in category_html_list:
    category_dict[category_html.get("href")] = (category_html.string)
# pprint.pprint(category_dict)

# 辞書型category_dictからカテゴリを一つ一つを取り出す
# dict.items()を利用すると、forの要素にkeyとvalueを二つ代入して、それぞれを回せる
for key, value in category_dict.items():
   """
   key: url
   value: カテゴリ名
   """
   print("カテゴリ名: " + value)
   # -------------------------------------------------------
   # 4.カテゴリを一つ一つ取り出して、ページャーの最後まで記事を取得してください。
   # -------------------------------------------------------
   # カテゴリページにアクセスする
   # category_res = requests.get("https://dividable.net/category/python/page/2").text

   category_res = ""
   page_count = 1
   soup = ""

   # それぞれのカテゴリページから、記事の内容を取り出す
   # それぞれのページからタイトルとURLを取り出したい（h3とその中のaタグのリンク）
   while True:
    print("------------{} ページ目------------".format(page_count))
    category_res = requests.get(key + "page/" + str(page_count)).text
    # print("アクセスページ： " + category_res)

    soup = BeautifulSoup(category_res, 'html.parser')
    # 次へを探す
    a_next_tag = soup.find("a", {"class": "next"})
    # print(a_next_tag)

    soup = BeautifulSoup(category_res, 'html.parser')
    h3_path = "div.posts div.post-content h3"
    h3_contents = soup.select(h3_path)

    for h3_content in h3_contents:
        url = h3_content.a.get("href")
        title = h3_content.string
        # pprint.pprint(h3_content.a.get("href"))
        # pprint.pprint(h3_content.string)

        # 行の作成
        se = pd.Series([title, url, value], columns)
        # print(se)
        df = df.append(se, columns) # データフレームに行を追加
        # print(df)
    a_next_tag = soup.find("a", {"class": "next"}) # 次へがあるかどうか調べる
    if a_next_tag:
        page_count += 1
        continue
    break
print("完了")
filename = '../study_dainote/result.csv'
df.to_csv(filename, encoding = 'utf-8')
print('csvファイルを出力しました')
