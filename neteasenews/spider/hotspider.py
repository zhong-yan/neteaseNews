import re
import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
from neteasenews.spider.config import JSON_INDEX_URLS, options
from neteasenews.spider.contents import info_datalog, info_news, info_photoview, info_dy
from neteasenews.spider.db import updatedata, MONGODB_TABLE_1, MONGODB_TABLE_2, MONGODB_TABLE_4
from selenium import webdriver


# 爬取首页要闻,广州,社会,国内,国际,独家,军事,财经,科技,体育,娱乐,时尚,汽车,房产,航空,健康,无人机
# 现在这个方法可以所有json
def parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 解析json,运用replace()使得该字符串符合json语法,否则会出现编码解码异常,即无法loads()
            response_json = json.loads(response.text.replace('data_callback(', '').replace(')', ''))
            for item in response_json:
                # 网易正文
                data_news = info_news(item.get('docurl'))
                # 数读平台
                data_datablog = info_datalog(item.get('docurl'))
                # 网易号:
                data_dy = info_dy(item.get('docurl'))
                if data_news:
                    infomation_news = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_news
                    }
                    updatedata(infomation_news, MONGODB_TABLE_1)
                elif data_datablog:
                    infomation_datalog = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_datablog
                    }
                    updatedata(infomation_datalog, MONGODB_TABLE_1)
                elif data_dy:
                    infomation_dy = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_dy
                    }
                    updatedata(infomation_dy, MONGODB_TABLE_1)
    except RequestException:
        pass
    except ConnectionError:
        print('连接失败,请重试!')
        pass


# 在广东有两个callback.js,默认广东,这个是根据请求头里面IP来判断的
# http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE
def gd_city_infos():
    # 存储指定城市的json
    news_city = []
    citys = []
    response = requests.get('http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE')
    if response.status_code == 200:
        response_city = json.loads(response.text.replace('XW_NEWS_PROVINCE(', '').replace(')', ''))
        for k in response_city.values():
            if k.get('inc'):
                # 存储到最初的列表
                citys.append(k.get('inc'))
    city_domain = 'http://house.163.com/special/00078GU7/'
    # ajax变化规律在foshan_xw_news_v1.js,v1那里,修改并递进
    for a_city in citys:
        city_name = a_city.split('/')[5]
        for num in range(2, 6):
            next_city = city_domain + city_name.split('.')[-2] + '_0{}'.format(num) + '.js'
            # 存储变化的列表
            news_city.append(next_city)
    gd_city = citys + news_city
    return gd_city
# 返回所有关于广东各城市的新闻文档


# 处理所有json文档的下一步,即js渲染的ajax内容
def get_next_urls():
    link = []
    for item in JSON_INDEX_URLS:
        for num in range(2, 11):
            new_item = item.split('.js')[0] + '_0{}'.format(num) + '.js'
            link.append(new_item)
    links = link + JSON_INDEX_URLS + gd_city_infos()
    return links


def hotspider():
    pool = Pool(5)
    pool.map(parse, JSON_INDEX_URLS)


def spider():
    url_data = get_next_urls()
    pool = Pool(5)
    pool.map(parse, url_data)


# Rank_url里面包含许多links,可以用map()方法建立进程,否则可以遍历赋予url
# requests方法失效,需要用selenium库操作
# http://news.163.com/rank/
def get_rank_urls():
    rank_urls = []
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://news.163.com/rank/')
    response = browser.page_source
    page_rank = BeautifulSoup(response, 'html.parser')
    nav = page_rank.select('.subNav > a')
    for item in nav:
        rank_urls.append(item.get('href'))
    browser.close()
    return rank_urls


def parse_rank(url):
    links_list = []
    html = requests.get(url)
    htmlpage = BeautifulSoup(html.text, 'lxml')
    patterns = re.compile(r'^http://[\w]+\.163\.com/\d+/\d+/\d+/\w+.html')
    links = htmlpage.findAll('a')
    for link in links:
        if link.get('href'):
            if re.search(patterns, link.get('href')):
                re_links = re.search(patterns, link.get('href')).group(0)
                links_list.append(re_links)
    for item in links_list:
        response = requests.get(item)
        page = BeautifulSoup(response.text, 'lxml')
        try:
            # 标题
            title = page.select('title')[0].get_text()
            data_blog = info_datalog(item)
            data_news = info_news(item)
            data_photo = info_photoview(item)
            if title:
                if data_news:
                    data_new = {
                        'title': title,
                        'url':  item,
                        'dutyeditor': data_news['dutyeditor'],
                        'source': data_news['source'],
                        'pictures': data_news['pictures'],
                        'contents': data_news['contents']
                    }
                    updatedata(data_new, MONGODB_TABLE_2)
                elif data_blog:
                    data_blogs = {
                        'title': title,
                        'url': item,
                        'source': '数读',
                        'comments': data_blog['comments'],
                        'publishTime': data_blog['publishTime'],
                        'pictures': data_blog['pictures'],
                        'contents': data_blog['contents']
                    }
                    updatedata(data_blogs, MONGODB_TABLE_2)
                elif data_photo:
                    data_photos = {
                        'title': title,
                        'url': item,
                        'dutyeditor': data_photo['dutyeditor'],
                        'datetime': data_photo['datetime'],
                        'source': data_photo['source'],
                        'pictures': data_photo['pictures'],
                        'contents': data_photo['contents']
                    }
                    updatedata(data_photos, MONGODB_TABLE_2)
        except IndexError:
            print('无法获取该页面标题')
            pass


def rankspider():
    rank_urls = get_rank_urls()
    pool = Pool(5)
    pool.map(parse_rank, rank_urls)


# Bug:在mainspider之间互相引用包,出现无法找到包来源(找不到解决方法,只有覆写方法,即updatedata())
# from neteasenews.spider.mainSpider import updatedata
# http://news.163.com/photo/#Current
# 是否需要不断点击右侧刷新图片.有待考虑
def get_photo_source(url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    response = requests.get(url)
    if response.status_code == 200:
        return browser.page_source


def photo(tab_url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(tab_url)
    html_photo = browser.page_source
    # 原来结束符是\n,我真是草了.
    pattern_photo = re.compile('var galleryListData = (.*?);\n', re.S)
    result = re.search(pattern_photo, html_photo)
    if result:
        photo_json = json.loads(result.group(1))
        # json的键固定:
        result_keys = ['ss', 'kk', 'jx', 'ch', 'js', 'hk', 'ts', 'zm']
        if photo_json and "ss" in photo_json.keys():
            for items in result_keys:
                result_items = photo_json.get(items)
                for item in result_items:
                    data_list = json_details(item.get('seturl'))
                    if data_list:
                        data = {
                            'title': item.get('setname'),
                            'url': item.get('seturl'),
                            'desc': item.get('desc'),
                            'createdate': item.get('createdate'),
                            'source': data_list['source'],
                            'dutyeditor': data_list['dutyeditor'],
                            'imgsum': item.get('imgsum'),
                            'pictures': data_list['pictures']
                        }
                        updatedata(data, MONGODB_TABLE_4)
    browser.close()


# 针对某些网页为图片浏览形式,正则匹配关键字段,加载为json文档.
def json_details(picture_url):
    html = get_photo_source(picture_url)
    pattern_pictures = re.compile(r'<textarea name="gallery-data" style="display:none;">(.*?)</textarea>', re.S)
    results = re.search(pattern_pictures, html)
    if results:
        result_json = json.loads(results.group(1))
        if result_json and 'info' in result_json.keys():
            item_info = result_json.get('info')
            item_pic = result_json.get('list')
            pic_list = {
                'title': item_info.get('setname'),
                'source': item_info.get('source'),
                'dutyeditor': item_info.get('dutyeditor'),
                'datetime': item_info.get('lmodify'),
                'imgsum': item_info.get('imgsum'),
                'pictures': [item.get('img') for item in item_pic],
                'contents': item_info.get('prevue')
            }
            return pic_list


def photospider():
    # 图片url:
    pic_tabs = ['http://news.163.com/photo/#Current'
                'http://news.163.com/photo/#Insight',
                'http://news.163.com/photo/#Week',
                'http://news.163.com/photo/#Special',
                'http://news.163.com/photo/#War',
                'http://news.163.com/photo/#Hk',
                'http://news.163.com/photo/#Discovery',
                'http://news.163.com/photo/#Paper']
    for item_url in pic_tabs:
        photo(item_url)


if __name__ == '__main__':
    spider()
