import requests
import re
import urllib.request
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

def extract_html_code(url,order):
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    selecter = etree.HTML(html.text)
    res = selecter.xpath(order)
    return res