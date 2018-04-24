import json
import re
from multiprocessing.pool import Pool
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from selenium import webdriver
from neteasenews.spider.db import MONGODB_TABLE_1, MONGODB_TABLE_3, updatedata
from neteasenews.spider.config import URLs
from neteasenews.spider.contents import info_dy, info_photoview, info_news, info_datalog, options


# 排行标签:rankspider()
# 数读标签:datablogspider()
# 新闻学院标签:collegespider()
# 政务标签:govspider()
# 公益标签:gongyispider()
# 媒体标签:mediaspider()


def get_rank_urls():
    rank_urls = []
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(URLs[1])
    response = browser.page_source
    page_rank = BeautifulSoup(response, 'lxml')
    # 获取导航页所有分类link
    nav = page_rank.select('.subNav > a')
    for item in nav:
        rank_urls.append(item.get('href'))
    browser.close()
    return rank_urls


# 获取每个分类的文章url
def rank_next_url(url):
    links_list = []
    # 这里有时候,requests会出现连接池数量不够的情况,异常,暂时不做处理.
    html = requests.get(url)
    htmlpage = BeautifulSoup(html.text, 'lxml')
    patterns = re.compile(r'^http://[\w]+\.163\.com/\d+/\d+/\d+/\w+.html')
    links = htmlpage.findAll('a')
    for link in links:
        if link.get('href'):
            if re.search(patterns, link.get('href')):
                re_links = re.search(patterns, link.get('href')).group(0)
                links_list.append(re_links)
    return links_list


# 处理每一个文章url跳转内容:
def parse_rank(url):
    links = rank_next_url(url)
    for item in links:
        response = requests.get(item)
        page = BeautifulSoup(response.text, 'lxml')
        try:
            # 标题
            title = page.findAll('title')[0].get_text()
            data_blogs = info_datalog(item)
            data_news = info_news(item)
            data_dys = info_dy(item)
            data_photos = info_photoview(item)
            if title:
                if data_news:
                    data_new = {
                        'title': title,
                        'url':  item,
                        'info': data_news
                    }
                    updatedata(data_new, MONGODB_TABLE_1)
                elif data_blogs:
                    data_blog = {
                        'title': title,
                        'url': item,
                        'info': data_blogs
                    }
                    updatedata(data_blog, MONGODB_TABLE_1)
                elif data_dys:
                    data_dy = {
                        'title': title,
                        'url': item,
                        'info': data_blogs
                    }
                    updatedata(data_dy, MONGODB_TABLE_1)
                elif data_photos:
                    data_photo = {
                        'title': title,
                        'url': item,
                        'info': data_photos
                    }
                    updatedata(data_photo, MONGODB_TABLE_3)
        except IndexError:
            print('无法获取该页面标题')
            pass


# 部署爬取新闻排行榜流程:
def rankspider():
    rank_urls = get_rank_urls()
    pool = Pool(5)
    pool.map(parse_rank, rank_urls)


# http://data.163.com/special/datablog/
def datablogspider():
    html = requests.get(URLs[6])
    try:
        if html.status_code == 200:
            pattern = re.compile(r'var ohnofuchlist=\[(.*?)"a"\];', re.S)
            result = re.search(pattern, html.text)
            if result:
                # js代码最后多了一个逗号,字符串切片
                results = result.group(1)[:-6]
                results_add = '[' + results + ']'
                # 解决单引号包含数字
                result_num = results_add.replace('"comment":\'', '"comment":').replace('\',', ',')
                # 解决单引号包含汉字,替换成None
                results_json = re.sub('\'.*?\'', '\"None\"', result_num)
                js_result = json.loads(results_json)
                for item in js_result:
                    d_datablog = details(item.get('url'))
                    if d_datablog:
                        data_datablog = {
                            'title': item.get('title'),
                            'url': item.get('url'),
                            'info': {
                                'pictures': item.get('img'),
                                'updatetime': item.get('time'),
                                'comments': item.get('comment'),
                                # 只需要内容,不包含图片
                                'contents': d_datablog['contents']
                            }
                        }
                        updatedata(data_datablog, MONGODB_TABLE_1)
    except ConnectionError:
        print('网络连接失败')
        datablogspider()
    except RequestException:
        print('请求失败,重试中')
        datablogspider()


def details(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, 'lxml')
    try:
        # 标题
        title = page.findAll('title')[0].get_text()
        data_news = info_news(url)
        data_blog = info_datalog(url)
        data_photo = info_photoview(url)
        data_dy = info_dy(url)
        # 是否为网易正文
        if title:
            if data_news:
                data_new = {
                    'title': title,
                    'url': url,
                    'info': {
                        'dutyeditor': data_news['dutyeditor'],
                        'source': data_news['source'],
                        'pictures': data_news['pictures'],
                        'contents': data_news['contents']
                    }
                }
                return data_new
            # 是否为数读平台
            elif data_blog:
                data_blogs = {
                    'title': title,
                    'url': url,
                    'info': {
                        'source': '数读',
                        'comments': data_blog['comments'],
                        'updatetime': data_blog['updatetime'],
                        'pictures': data_blog['pictures'],
                        'contents': data_blog['contents']
                    }
                }
                return data_blogs
            # 是否为图片轮播
            elif data_photo:
                data_photos = {
                    'title': title,
                    'url': url,
                    'info': {
                        'dutyeditor': data_photo['dutyeditor'],
                        'updatetime': data_photo['updatetime'],
                        'source': data_photo['source'],
                        'pictures': data_photo['pictures'],
                        'contents': data_photo['contents']
                    }
                }
                updatedata(data_photos, MONGODB_TABLE_3)
            # 是否为网易号
            elif data_dy:
                data_dy = {
                    'title': title,
                    'url': url,
                    'info': {
                        'pictures': data_dy['pictures'],
                        'contents': data_dy['contents']
                    }
                }
                return data_dy
    except IndexError:
        print('无法获取标题')
        pass


# http://news.163.com/college
def get_college_urls():
    html_college = requests.get(URLs[10])
    try:
        if html_college.status_code == 200:
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
    except ConnectionError:
        print('网络连接失败')
        get_college_urls()
    except RequestException:
        print('请求失败,重试中')
        get_college_urls()


def collegespider():
    college_data = get_college_urls()
    for item in college_data:
        data_college = info_dy(item)
        updatedata(data_college, MONGODB_TABLE_1)


# http://gov.163.com/
def get_gov_url():
    html_gov = requests.get(URLs[11])
    try:
        if html_gov.status_code == 200:
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
    except ConnectionError:
        print('网络连接失败')
        get_gov_url()
    except RequestException:
        print('请求失败,重试中')
        get_gov_url()


def govspider():
    gov_data = get_gov_url()
    for link in gov_data:
        gov_content = details(link)
        updatedata(gov_content, MONGODB_TABLE_1)


# http://gongyi.163.com/
def get_gongyi_url():
    html_gongyi = requests.get(URLs[12])
    try:
        if html_gongyi.status_code == 200:
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
    except ConnectionError:
        print('网络连接失败')
        get_gongyi_url()
    except RequestException:
        print('请求失败,重试中')
        get_gongyi_url()


def gongyispider():
    gongyi_data = get_gongyi_url()
    for url in gongyi_data:
        gongyi_content = details(url)
        updatedata(gongyi_content, MONGODB_TABLE_1)


# http://media.163.com/
def get_media_url():
    html_media = requests.get(URLs[13])
    try:
        if html_media.status_code == 200:
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
    except ConnectionError:
        print('网络连接失败')
        get_media_url()
    except RequestException:
        print('请求失败,重试中')
        get_media_url()


def mediaspider():
    media_data = get_media_url()
    for cat in media_data:
        media_content = details(cat)
        updatedata(media_content, MONGODB_TABLE_1)
