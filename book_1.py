import  requests
from bs4 import BeautifulSoup
import json


url = 'https://athena.eslite.com/api/v1/products/1004128571081642'
userAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67'


headers={'Referer': 'https://www.eslite.com/product/1004128571081642'}
res = requests.get(url,headers=headers)
jsonData = json.loads(res.text)
bookname = jsonData['name']   #書名
bookURL='https://www.eslite.com/product/{}'
bookauthor=jsonData['auth']   #作者
booksupplier=jsonData['supplier']   #出版社
bookisbn13=jsonData['isbn13']    #ISBN
bookphotos=jsonData['photos']
picture='https://s.eslite.dev/'+bookphotos['large_path']  #圖片網址




print(bookname)
print(bookURL)
print(bookauthor)
print(booksupplier)
print(bookisbn13)
print(picture)

