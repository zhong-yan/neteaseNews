import re
from bs4 import BeautifulSoup
import requests
from neteasenews.spider.config import pattern, MONGODB_TABLE_0, \
    MONGODB_TABLE_10, MONGODB_TABLE_11, MONGODB_TABLE_12, MONGODB_TABLE_13, URLs, MONGODB_TABLE_1, RANK_URL
from neteasenews.spider.mainSpider import chrome_driver, details, updatedata


# http://news.163.com/
def get_index_urls():
    html_index = chrome_driver(URLs[0])
    page_index = BeautifulSoup(html_index, 'lxml')
    links = page_index.findAll('a')
    index_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern, link.get('href')):
                re_links = re.search(pattern, link.get('href')).group(0)
                index_list.append(re_links)
    return index_list


# http://news.163.com/college
def get_college_urls():
    html_college = requests.get(URLs[10])
    pagecollege = BeautifulSoup(html_college.text, 'lxml')
    links = pagecollege.findAll('a')
    pattern_college = re.compile(r'^http://dy\.163\.com/v2/article/detail/\w+.html')
    colleges_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_college, link.get('href')):
                re_links = re.search(pattern_college, link.get('href')).group(0)
                colleges_list.append(re_links)
    return colleges_list


# http://gov.163.com/
def get_gov_url():
    html_gov = requests.get(URLs[11])
    page_gov = BeautifulSoup(html_gov.text, 'lxml')
    links = page_gov.findAll('a')
    pattern_gov = re.compile(r'^http://gov\.163\.com/18/\d+/\d+/\w+.html')
    gov_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_gov, link.get('href')):
                re_links = re.search(pattern_gov, link.get('href')).group(0)
                gov_list.append(re_links)
    return gov_list


# http://gongyi.163.com/
def get_gongyi_url():
    html_gongyi = requests.get(URLs[12])
    page_gongyi = BeautifulSoup(html_gongyi.text, 'lxml')
    links = page_gongyi.findAll('a')
    pattern_gongyi = re.compile(r'^http://gongyi\.163\.com/\d+/\d+/\d+/\w+.html')
    gongyi_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_gongyi, link.get('href')):
                re_links = re.search(pattern_gongyi, link.get('href')).group(0)
                gongyi_list.append(re_links)
    return gongyi_list


# http://media.163.com/
def get_media_url():
    html_media = requests.get(URLs[13])
    page_media = BeautifulSoup(html_media.text, 'lxml')
    links = page_media.findAll('a')
    pattern_media = re.compile(r'^http://media\.163\.com/\d+/\d+/\d+/\w+.html')
    media_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_media, link.get('href')):
                re_links = re.search(pattern_media, link.get('href')).group(0)
                media_list.append(re_links)
    return media_list


def indexspider():
    all_urls = get_index_urls()
    for item in all_urls:
        data = details(item)
        if data:
            updatedata(data, MONGODB_TABLE_0)


def collegespider():
    college_data = get_college_urls()
    for item in college_data:
        html = requests.get(item)
        if html.status_code == 200:
            page_college = BeautifulSoup(html.text, 'lxml')
            # 标题
            title = page_college.select('title')[0].get_text().split('_')[0]
            # 前言
            font_contents = page_college.select('.intro')
            # 内容
            contents = page_college.select('#content')
            for font_content, content in zip(font_contents, contents):
                data_college = {
                    'title': title,
                    'articleUrl': item,
                    'font': font_content.get_text().replace('\n', ''),
                    'content': [page for page in content.stripped_strings]
                }
                updatedata(data_college, MONGODB_TABLE_10)


def govspider():
    gov_data = get_gov_url()
    for link in gov_data:
        gov_content = details(link)
        updatedata(gov_content, MONGODB_TABLE_11)


def gongyispider():
    gongyi_data = get_gongyi_url()
    for url in gongyi_data:
        gongyi_content = details(url)
        updatedata(gongyi_content, MONGODB_TABLE_12)


def mediaspider():
    media_data = get_media_url()
    for cat in media_data:
        media_content = details(cat)
        updatedata(media_content, MONGODB_TABLE_13)


# Rank_url里面包含许多links,可以用map()方法建立进程,否则可以遍历赋予url
# http://news.163.com/rank/
def rankspider():
    links_list = []
    patterns = re.compile(r'^http://[\w]+\.163\.com/\d+/\d+/\d+/\w+.html')
    for url in RANK_URL:
        html = requests.get(url)
        htmlpage = BeautifulSoup(html.text, 'lxml')
        links = htmlpage.findAll('a')
        for link in links:
            if link.get('href'):
                if re.search(patterns, link.get('href')):
                    re_links = re.search(patterns, link.get('href')).group(0)
                    links_list.append(re_links)
        for item in links_list:
            data = details(item)
            if data:
                updatedata(data, MONGODB_TABLE_1)


if __name__ == '__main__':
    mediaspider()
    rankspider()