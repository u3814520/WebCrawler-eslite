import requests
import json
import os
import pandas as pd
import urllib.parse
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
ua = UserAgent()

if not os.path.exists('./WebCrawle-eslite'):
    os.mkdir('./WebCrawle-eslite')

keywords=str(input("請輸入搜尋關鍵字:"))
urlkeywords = urllib.parse.quote(keywords)
manypage=int(input("請輸入幾頁:"))
page=0

bookname=[]

bookURL=[]
bookauthor=[]
booksupplier=[]
bookisbn13=[]
picture=[]
description=[]


for p in range(0,manypage):
    url = 'https://athena.eslite.com/api/v2/search?q={}&final_price=0,&sort=_weight_+desc&size=20&start={}'.format(urlkeywords,page)
    # userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'

    headers = {
        'Referer': 'https://www.eslite.com/Search?keyword={}&final_price=0%2C&sort=_weight_+desc&size=20&start={}'.format(urlkeywords,page)}
    res = requests.get(url, headers=headers)
    jsonData = json.loads(res.text)
    tempid = jsonData['hits']['hit']


    for i in range(0, 20):
        try:
            bookid = tempid[i]['id']
        except IndexError:
            break
        book_URL = tempid[i]['fields']['url']
        bookURL.append(book_URL)
        newurl = 'https://athena.eslite.com/api/v1/products/{}'.format(bookid)
        newheaders = {'Referer': book_URL}
        newres = requests.get(newurl, headers=newheaders)
        newData = json.loads(newres.text)
        try:
            book_name = newData['name']  # 書名
            bookname.append(book_name)
        except KeyError:
            bookname.append('0')
        try:
            book_author = newData['auth']  # 作者
            bookauthor.append(book_author)
        except KeyError:
            bookauthor.append('0')
        try:
            book_supplier = newData['supplier']  # 出版社
            booksupplier.append(book_supplier)
        except KeyError:
            booksupplier.append('0')
        try:
            book_isbn13 = newData['isbn13']  # ISBN
            bookisbn13.append(book_isbn13)
        except KeyError:
            bookisbn13.append(' ')
        try:
            book_descriptions = newData['descriptions'] #書籍簡介
            book_description=book_descriptions[0]['description']  #書籍簡介
            red = BeautifulSoup(book_description, "html.parser")
            description.append(red.text)
        except:
            description.append('0')
        try:
            bookphotos = newData['photos']    #書籍圖片
            book_picture = 'https://s.eslite.dev' + bookphotos[0]['large_path']  # 書籍圖片
            picture.append(book_picture)
        except :
            picture.append('0')

        time.sleep(3)
        print('{},共{}頁'.format(book_name,manypage))
    print('==第{}頁=={}'.format(p,keywords))
    page += 1

eslite =pd.DataFrame({'書名': bookname,'書籍網址': bookURL,'作者': bookauthor,'出版社': booksupplier, 'ISBN': bookisbn13,'圖片網址': picture})
eslite.to_csv("./WebCrawle-eslite/eslite_{}.csv".format(keywords),encoding='utf-8-sig',index=False)
intro_eslite =pd.DataFrame({'ISBN': bookisbn13,'書籍簡介': description})
intro_eslite.to_csv("./WebCrawle-eslite/eslite_{}_intro.csv".format(keywords),encoding='utf-8-sig',index=False)



