from bs4 import BeautifulSoup
from neteasenews.spider.mainSpider import savedata, details
from neteasenews.spider.config import MONGODB_TABLE_10, MONGODB_TABLE_11, MONGODB_TABLE_12, MONGODB_TABLE_13, URLs
import requests
import re


# http://dy.163.com/v2/article/detail/DDU6KM9B05118VJ5.html
# http://news.163.com/college

def get_college_urls():
    html_college = requests.get(URLs[10])
    pagecollege = BeautifulSoup(html_college.text, 'lxml')
    links = pagecollege.findAll('a')
    pattern_college = re.compile(r'^http:\/\/dy\.163\.com\/v2\/article\/detail\/\w+.html')
    colleges_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_college, link.get('href')):
                re_links = re.search(pattern_college, link.get('href')).group(0)
                colleges_list.append(re_links)
    return colleges_list


def get_gov_url():
    html_gov = requests.get(URLs[11])
    page_gov = BeautifulSoup(html_gov.text, 'lxml')
    links = page_gov.findAll('a')
    pattern_gov = re.compile(r'^http:\/\/gov\.163\.com\/18\/\d+\/\d+\/\w+.html')
    gov_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_gov, link.get('href')):
                re_links = re.search(pattern_gov, link.get('href')).group(0)
                gov_list.append(re_links)
    return gov_list


def get_gongyi_url():
    html_gongyi = requests.get(URLs[12])
    page_gongyi = BeautifulSoup(html_gongyi.text, 'lxml')
    links = page_gongyi.findAll('a')
    pattern_gongyi = re.compile(r'^http:\/\/gongyi\.163\.com\/\d+\/\d+\/\d+\/\w+.html')
    gongyi_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_gongyi, link.get('href')):
                re_links = re.search(pattern_gongyi, link.get('href')).group(0)
                gongyi_list.append(re_links)
    return gongyi_list


def get_media_url():
    html_media = requests.get(URLs[13])
    page_media = BeautifulSoup(html_media.text, 'lxml')
    links = page_media.findAll('a')
    pattern_media = re.compile(r'^http:\/\/media\.163\.com\/\d+\/\d+\/\d+\/\w+.html')
    media_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern_media, link.get('href')):
                re_links = re.search(pattern_media, link.get('href')).group(0)
                media_list.append(re_links)
    return media_list


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
                savedata(data_college, MONGODB_TABLE_10)


def govspider():
    gov_data = get_gov_url()
    for link in gov_data:
        gov_content = details(link)
        savedata(gov_content, MONGODB_TABLE_11)


def gongyispider():
    gongyi_data = get_gongyi_url()
    for url in gongyi_data:
        gongyi_content = details(url)
        savedata(gongyi_content, MONGODB_TABLE_12)


def mediaspider():
    media_data = get_media_url()
    for cat in media_data:
        media_content = details(cat)
        savedata(media_content, MONGODB_TABLE_13)


if __name__ == "__main__":
    # collegespider()
    # gongyispider()
    mediaspider()
