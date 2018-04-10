import json
import re
from bs4 import BeautifulSoup
import requests
from neteasenews.spider.db import MONGODB_TABLE_3, updatedata
from neteasenews.spider.config import URLs
from neteasenews.spider.contents import info_dy, info_photoview, info_news, info_datalog


# 数读标签:datablogspider()
# 新闻学院标签:collegespider()
# 政务标签:govspider()
# 公益标签:gongyispider()
# 媒体标签:mediaspider()


# http://data.163.com/special/datablog/
def datablogspider():
    html = requests.get('http://data.163.com/special/datablog/')
    pattern = re.compile(r'var ohnofuchlist=\[(.*?)"a"\];', re.S)
    result = re.search(pattern, html.text)
    if result:
        # 后面多了一个逗号,我真是草你麻痹, 烦 烦 烦 烦,如何去掉最后一个逗号,字符串切片,没有别的方法了 我算是服了
        results = result.group(1)[:-6]
        results_add = '[' + results + ']'
        # 解决单引号包含数字
        result_num = results_add.replace('"comment":\'', '"comment":').replace('\',', ',')
        # 解决单引号包含汉字,替换成None, keyword,老子不要你了,艹 耗费我2个小时转换你,你也是厉害
        results_json = re.sub('\'.*?\'', '\"None\"', result_num)
        # 出现json.decoder.JSONDecodeError,证明要转换的字符串不符合json格式.卧槽
        js_result = json.loads(results_json)
        for item in js_result:
            d_datablog = details(item.get('url'))
            if d_datablog:
                data_datablog = {
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'img': item.get('img'),
                    'time': item.get('time'),
                    'comments': item.get('comment'),
                    # 只需要内容,不包含图片
                    'contents': d_datablog['contents']
                }
                updatedata(data_datablog, MONGODB_TABLE_3)


def details(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'lxml')
    # 标题
    title = page.select('title')[0].get_text()
    data_news = info_news(url)
    data_blog = info_datalog(url)
    data_photo = info_photoview(url)
    data_dy = info_dy(url)
    # 是否为网易正文
    if data_news:
        data_new = {
            'title': title,
            'url': url,
            'dutyeditor': data_news['dutyeditor'],
            'source': data_news['source'],
            'pictures': data_news['pictures'],
            'contents': data_news['contents']
        }
        return data_new
    # 是否为数读平台
    elif data_blog:
        data_blogs = {
            'title': title,
            'url': url,
            'source': '数读',
            'comments': data_blog['comments'],
            'publishTime': data_blog['publishTime'],
            'pictures': data_blog['pictures'],
            'contents': data_blog['contents']
        }
        return data_blogs
    # 是否为图片轮播
    elif data_photo:
        data_photos = {
            'title': title,
            'url': url,
            'dutyeditor': data_photo['dutyeditor'],
            'datetime': data_photo['datetime'],
            'source': data_photo['source'],
            'pictures': data_photo['pictures'],
            'contents': data_photo['contents']
        }
        return data_photos
    # 是否为网易号
    elif data_dy:
        data_dy = {
            'title': title,
            'url': url,
            'font-contents': data_dy['font-contents'],
            'contents': data_dy['contents']
        }
        return data_dy


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


def collegespider():
    college_data = get_college_urls()
    for item in college_data:
        data_college = info_dy(item)
        updatedata(data_college, MONGODB_TABLE_3)


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


def govspider():
    gov_data = get_gov_url()
    for link in gov_data:
        gov_content = details(link)
        updatedata(gov_content, MONGODB_TABLE_3)


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


def gongyispider():
    gongyi_data = get_gongyi_url()
    for url in gongyi_data:
        gongyi_content = details(url)
        updatedata(gongyi_content, MONGODB_TABLE_3)


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


def mediaspider():
    media_data = get_media_url()
    for cat in media_data:
        media_content = details(cat)
        updatedata(media_content, MONGODB_TABLE_3)
