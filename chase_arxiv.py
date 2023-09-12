import urllib.request
import pickle
from lxml import etree
from collections import defaultdict
import datetime

        
            
subareas = ["AI", "LG", "RO"]
key_words = ["plan", "decision", 
            ("generat", "plan"), ("decision", "transformer"), ("plan", "diffusion")]
HEADER = "Your own header"

def get_html(url: str):
    headers = HEADER
    request = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(request, timeout=60)
    html = res.read().decode('utf-8')
    return html

def get_day(past_offset: int):
    today = datetime.date.today()
    return today + datetime.timedelta(days=-past_offset)

def get_paper_list(subareas, key_words, is_dump=False):
    paper_list = defaultdict(list)
    for area in subareas:
        url = f"https://arxiv.org/list/cs.{area}/pastweek?show=1000"
        print(url)
        try:
            html = get_html(url)
        except Exception as e:
            print(e)
            print(area)
        if is_dump:
            pickle.dump(html, open(f"./rec_{area}.html", "wb"))
        # html = pickle.load(open(f"./rec_{area}.html", "rb"))
        html = etree.HTML(html.encode())
        for day in range(1, 6):
            date = get_day(day - 1)
            print(date)
            k = 0
            while True:
                k += 1
                title_x_path = f"//*[@id=\"dlpage\"]/dl[{day}]/dd[{k}]/div/div[1]/text()"
                link_x_path = f"//*[@id=\"dlpage\"]/dl[{day}]/dt[{k}]/span/a[1]/text()"
                
                title = html.xpath(title_x_path)
                if len(title) == 0:
                    break
                title = title[1].strip().lower()
                
                link = html.xpath(link_x_path)[0].split(":")[1]
                link = f"https://arxiv.org/abs/{link}"
                
                # select
                for word in key_words:
                    if type(word) is str and word in title:
                        paper_list[date].append((title, link))
                        break
                    elif type(word) is tuple and all([w in title for w in word]):
                        paper_list[date].append((title, link))
                        break
            paper_list[date] = list(set(paper_list[date]))
    return paper_list




paper_list = get_paper_list(subareas, key_words, is_dump=False)
# out put
lines = []
for date in paper_list:
    lines.append(f"## {date}\n")
    for paper in paper_list[date]:
        lines.append(f"- [{paper[0]}]({paper[1]})\n")        
with open("README.md", "w") as f:
    f.writelines(lines)