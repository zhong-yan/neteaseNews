import json
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from multiprocessing.pool import Pool
# 引入json文档原始链接,和webdriver配置信息
from selenium import webdriver
from neteasenews.spider.config import JSON_INDEX_URLS, URLs, MONGODB_TABLE_1, MONGODB_TABLE_2, MONGODB_TABLE_3
# 处理跳转信息的方法,网易正文, 数读平台, 图集, 网易号
from neteasenews.spider.contents import info_datalog, info_news, info_dy, info_photoview, options, json_details
# 数据库处理方法,包括更新数据库
from neteasenews.spider.db import updatedata


# 获取首页里面的头部导航链接.
def top_navs():
    navs = []
    response = requests.get(URLs[0])
    if response.status_code == 200:
        page = BeautifulSoup(response.text, 'lxml')
        nav = page.select('div.N-nav-channel.JS_NTES_LOG_FE > a')
        for item in nav:
            navs.append(item.get('href'))
        return navs


# 处理头部导航方法
def basic(url):
    html_index = requests.get(url)
    try:
        if html_index.status_code == 200:
            page_gongyi = BeautifulSoup(html_index.text, 'lxml')
            links = page_gongyi.findAll('a')
            pattern_index = re.compile(r'^http://[\w]+\.163\.com/.*\.html')
            index_list = []
            for link in links:
                if link.get('href'):
                    if re.search(pattern_index, link.get('href')):
                        re_links = re.search(pattern_index, link.get('href')).group(0)
                        index_list.append(re_links)
            return index_list
            # return index_list
    except ConnectionError:
        print('网络连接失败')
        basic(url)
    except RequestException:
        print('请求失败,重试中')
        basic(url)


def no_js_spider():
    basic_links = []
    nav = top_navs()
    for item in nav:
        basic_links.append(basic(item))
    for item_url in basic_links:
        item_url = item_url.strip().decode()
        response = requests.get(item_url)
        page = BeautifulSoup(response.text, 'lxml')
        try:
            # 标题
            title = page.findAll('title')[0].get_text()
            data_blogs = info_datalog(item_url)
            data_news = info_news(item_url)
            data_dy = info_dy(item_url)
            pictures = info_photoview(item_url)
            if title:
                if data_news:
                    data_new = {
                        'title': title,
                        'url':  item_url,
                        'info': data_news
                    }
                    updatedata(data_new, MONGODB_TABLE_1)
                elif data_blogs:
                    data_blog = {
                        'title': title,
                        'url': item_url,
                        'info': data_blogs
                    }
                    updatedata(data_blog, MONGODB_TABLE_1)
                elif data_dy:
                    data_blog = {
                        'title': title,
                        'url': item_url,
                        'info': data_dy
                    }
                    updatedata(data_blog, MONGODB_TABLE_1)
                elif pictures:
                    picture = {
                        'title': title,
                        'url': item_url,
                        'info': pictures
                    }
                    updatedata(picture, MONGODB_TABLE_3)
        except IndexError:
            print('无法获取该页面标题')
            pass


# 爬取首页要闻,广州,社会,国内,国际,独家,军事,财经,科技,体育,娱乐,时尚,汽车,房产,航空,健康,无人机
# 现在这个方法可以解析所有json
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
                        # 标题:
                        'title': item.get('title'),
                        # 文章url,数据库文档索引
                        'url': item.get('docurl'),
                        # 文章信息,包含内容,来源,责任编辑,文中图片等
                        'info': data_news,
                        # 关键字
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        # 分类:
                        'label': item.get('label'),
                        # 评论量:
                        'comments': item.get('tienum'),
                        # 更新时间:
                        'updatetime': item.get('time')
                    }
                    updatedata(infomation_news, MONGODB_TABLE_2)
                elif data_datablog:
                    infomation_datalog = {
                        'title': item.get('title'),
                        'url': item.get('docurl'),
                        'info': data_datablog,
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time')
                    }
                    updatedata(infomation_datalog, MONGODB_TABLE_2)
                elif data_dy:
                    infomation_dy = {
                        'title': item.get('title'),
                        'url': item.get('docurl'),
                        'info': {
                            'pictures': data_dy['pictures'],
                            'contents': data_dy['contents']
                        },
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time')
                    }
                    updatedata(infomation_dy, MONGODB_TABLE_2)
        elif response.status_code == 404:
            print('该json文档不存在', url)
    # 处理请求失败异常:
    except RequestException:
        print('请求异常')
        pass
    except ConnectionError:
        print('连接失败,请重试!')
        parse(url)


# 在广东有两个callback.js,默认广东,这个是根据请求头里面IP来判断的
# http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE
def gd_city_infos():
    # 存储指定城市的json链接
    news_city = []
    # 所有广东城市json链接
    citys = []
    response = requests.get('http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE')
    if response.status_code == 200:
        response_city = json.loads(response.text.replace('XW_NEWS_PROVINCE(', '').replace(')', ''))
        for k in response_city.values():
            if k.get('inc'):
                # 存储到指定城市列表
                citys.append(k.get('inc'))
    # 此类json链接的公共部分:
    city_domain = 'http://house.163.com/special/00078GU7/'
    # ajax变化规律在foshan_xw_news_v1.js,v1那里,修改并递进
    for a_city in citys:
        # 获取被修改部分字符串
        city_name = a_city.split('/')[5]
        for num in range(2, 6):
            # 组合新的被要求的url
            next_city = city_domain + city_name.split('.')[-2] + '_0{}'.format(num) + '.js'
            # 存储新的列表
            news_city.append(next_city)
    # 原来的加上变化的,等同所有符合要求的url
    gd_city = citys + news_city
    return gd_city
# 返回所有关于广东各城市的新闻文档


# 处理所有json(包括首页)文档的下一步,即js渲染的ajax内容
def get_all_urls():
    link = []
    for item in JSON_INDEX_URLS:
        for num in range(2, 11):
            new_item = item.split('.js')[0] + '_0{}'.format(num) + '.js'
            link.append(new_item)
    # 类似
    links = link + JSON_INDEX_URLS + gd_city_infos()
    return links


# 部署爬取首页等类似布局的标签
def mainspider():
    no_js_spider()
    url_data = get_all_urls()
    pool = Pool(10)
    pool.map(parse, url_data)


# 处理图片标签
def get_photo_source(url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    response = requests.get(url)
    if response.status_code == 200:
        response.close()
        return browser.page_source


# 获取图片首页各个图片信息.
def photo(tab_url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(tab_url)
    html_photo = browser.page_source
    # js代码结束符是;\n,注意!否则会出现无法转换json文档异常,需要对json文档正确形式了解
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
                            # 标题:
                            'title': item.get('setname'),
                            # 图片链接:
                            'url': item.get('seturl'),
                            'info': {
                                # 图片描述信息:
                                'desc': item.get('desc'),
                                # 图片创建时间:
                                'createdate': item.get('createdate'),
                                # 图片来源:
                                'source': data_list['source'],
                                # 图片责任编辑:
                                'dutyeditor': data_list['dutyeditor'],
                                # 图片数目:
                                'imgsum': item.get('imgsum'),
                                # 图片集:
                                'pictures': data_list['pictures']
                            }
                        }
                        updatedata(data, MONGODB_TABLE_3)
    browser.close()


# # 针对某些网页为图片浏览形式,正则匹配关键字段,加载为json文档.
# def json_details(picture_url):
#     html = get_photo_source(picture_url)
#     # 正则匹配源代码里面的js代码并且处理并且生成json文档,这里处理操作简单.
#     pattern_pictures = re.compile(r'<textarea name="gallery-data" style="display:none;">(.*?)</textarea>', re.S)
#     results = re.search(pattern_pictures, html)
#     if results:
#         result_json = json.loads(results.group(1))
#         if result_json and 'info' in result_json.keys():
#             item_info = result_json.get('info')
#             item_pic = result_json.get('list')
#             pic_list = {
#                 'title': item_info.get('setname'),
#                 'source': item_info.get('source'),
#                 'dutyeditor': item_info.get('dutyeditor'),
#                 'updatetime': item_info.get('lmodify'),
#                 'imgsum': item_info.get('imgsum'),
#                 'pictures': [item.get('img') for item in item_pic],
#                 'contents': item_info.get('prevue')
#             }
#             return pic_list


def photospider():
    # 获取所有json文档:
    json_links = get_all_urls()
    for url_js in json_links:
        # 处理json文档中符合图集的链接
        response = requests.get(url_js)
        if response.status_code == 200:
            # 解析json,运用replace()使得该字符串符合json语法,否则会出现编码解码异常,即无法loads()
            response_json = json.loads(response.text.replace('data_callback(', '').replace(')', ''))
            for item in response_json:
                data_photo = info_photoview(item.get('docurl'))
                if data_photo:
                    infomation_photo = {
                        'title': item.get('title'),
                        'url': item.get('docurl'),
                        'info': data_photo
                    }
                    # 存储到另外的pictures表里
                    updatedata(infomation_photo, MONGODB_TABLE_3)
    # 处理导航标签的图片各个标签url:
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
    mainspider()
