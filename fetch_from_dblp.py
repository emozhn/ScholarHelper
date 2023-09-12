from utils import get_header
import urllib.request
from lxml import etree


TARGET_LINK = "https://dblp.uni-trier.de/db/conf/icml/icml2015.html"
HEADER = get_header()

def get_html(url: str):
    headers = HEADER
    request = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(request, timeout=100)
    html = res.read().decode('utf-8')
    return html
    
html = get_html(TARGET_LINK)
html = etree.HTML(html.encode())
for each in html.xpath('//*[@class="title"]/text()'):
    print(each)