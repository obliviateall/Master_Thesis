#extract keywords from the MAPI,totally 108 keywords,写入keywords.txt

import urllib.request
from bs4 import BeautifulSoup
import file_operation

keywords=[]
ks = []
kk = []

url = "http://aflowlib.duke.edu/aflowwiki/doku.php?id=documentation:all_keywords#optional_materials_keywords"
url2 = "https://wiki.materialsproject.org/api.php?action=parse&page=The_Materials_API&format=json&callback="
header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'}

def page_code(url):
    req = urllib.request.Request(url,headers=header)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()
    soup = BeautifulSoup(html,'html.parser')
    return soup

soup1 = page_code(url)
for i in soup1.find_all('div',class_='li'):
    key = i.get_text().strip()
    if key not in ks:
        ks.append(key)

keywords=ks[27:]
soup2 = page_code(url2)

for j in soup2.find_all('dt'):#,string='更多'
    keyword = j.get_text().strip()
    if keyword not in keywords:
        keywords.append(keyword)

filename = 'Doc_processing/'+'keywords.txt'
file_operation.write_file(filename,keywords)