import urllib.request
import re
import json
from tqdm import tqdm
from selenium import webdriver
import pickle
import os
from utils import get_header

LINK_PREFIX = "https://scholar.google.com/scholar?q="
# PATTERN = re.compile(r'Cited by \d+')
PATTERN = re.compile(r'被引用次数：\d+')
HEADER = get_header()
USE_DRIVER = True

if USE_DRIVER:
    driver = webdriver.Chrome()

def parse_json(file_path: str):
    titles = []
    with open(file_path, 'r') as json_file:
        all = json.load(json_file)
        contents = all["result"]["hits"]["hit"]
        for item in contents:
            title = item["info"]["title"]
            titles.append(title)
    return titles
    

def get_html(url: str):
    if USE_DRIVER:
        driver.get(url)
        html = driver.execute_script("return document.documentElement.outerHTML")
    else:
        headers = HEADER
        request = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(request, timeout=100)
        html = res.read().decode('utf-8')
    return html
    

def get_citation(titles: list[str]):
    if os.path.exists("cache.pkl"):
        name_citation_dict = pickle.load(open("cache.pkl", "rb"))
    else:
        name_citation_dict = dict()
    try:
        for k, title in tqdm(enumerate(titles), total=len(titles)):
            if title in name_citation_dict:
                continue
            name = title.replace(' ', '+')
            url = LINK_PREFIX + name
            try:
                html = get_html(url)
                m = PATTERN.search(html)
                if m:
                    to_be_parse = m.group(0)
                    k = len(to_be_parse) - 1
                    while k >= 0 and to_be_parse[k] in "0123456789":
                        k -= 1
                    citation = int(to_be_parse[k + 1:])
                else:
                    citation = 0
            except Exception as e:
                print(e)
                try:
                    print("some error happens!")
                    input()
                    html = get_html(url)
                    m = PATTERN.search(html)
                    if m:
                        to_be_parse = m.group(0)
                        k = len(to_be_parse) - 1
                        while k >= 0 and to_be_parse[k] in "0123456789":
                            k -= 1
                        citation = int(to_be_parse[k + 1:])
                    else:
                        citation = 0
                except Exception:
                    citation = -1
            name_citation_dict[title] = citation
    except KeyboardInterrupt:
        print(k)
        pickle.dump(name_citation_dict, open("cache.pkl", "wb"))
    pickle.dump(name_citation_dict, open("cache.pkl", "wb"))
    name_citation_pair = [(name, name_citation_dict[name]) for name in name_citation_dict]
    return name_citation_pair

    

titles_all = []
# for file in ["iclr13.json", "iclr14.json", "iclr15.json", "iclr16.json", "iclr17.json", "iclr18.json", "iclr19.json"]:
#     titles = parse_json("jsons/" + file)
#     titles_all.extend(titles)

for file in ["icml15.txt", "icml16.txt", "icml17.txt", "icml18.txt", "icml19.txt", "icml20.txt"]:
    with open("lists/" + file, "r") as f:
        lines = f.readlines()
        while lines:
            titles_all.extend([line.strip() for line in lines])
            lines = f.readlines()
for title in titles_all:
    print(title)
title_citations = get_citation(titles_all)
title_citations.sort(key=lambda x: -x[1])
print("+++++++++++++")
for title, citation in title_citations:
    print(title, citation)