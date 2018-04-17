import re
import json
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
# 引入json文档原始链接,和webdriver配置信息
from neteasenews.spider.config import JSON_INDEX_URLS, options
# 处理跳转信息的方法,网易正文, 数读平台, 图集, 网易号
from neteasenews.spider.contents import info_datalog, info_news, info_photoview, info_dy
# 数据库处理方法,包括更新数据库
from neteasenews.spider.db import updatedata, MONGODB_TABLE_1, MONGODB_TABLE_3
from selenium import webdriver


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
                # 图集(由于需要chrome渲染结果,会导致速度变慢?)
                # 解决方案,图集交给专门处理photo的方法中,提取符合要求的URL即可.
                if data_news:
                    infomation_news = {
                        # 标题:
                        'title': item.get('title'),
                        # 分类:
                        'label': item.get('label'),
                        # 评论量:
                        'comments': item.get('tienum'),
                        # 更新时间:
                        'updatetime': item.get('time'),
                        # 关键字
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        # 文章url,数据库文档索引
                        'url': item.get('docurl'),
                        # 文章信息,包含内容,来源,责任编辑,文中图片等
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


# requests方法失效,需要用selenium库操作
# http://news.163.com/rank/
# 获取排行榜分类
def get_rank_urls():
    rank_urls = []
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://news.163.com/rank/')
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
        # mark, 需作异常处理,或者自动操作连接池?
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
                        'info': {
                            'dutyeditor': data_news['dutyeditor'],
                            'source': data_news['source'],
                            'pictures': data_news['pictures'],
                            'contents': data_news['contents']
                        }
                    }
                    updatedata(data_new, MONGODB_TABLE_1)
                elif data_blog:
                    data_blogs = {
                        'title': title,
                        'url': item,
                        'info': {
                            'source': '数读',
                            'comments': data_blog['comments'],
                            'publishTime': data_blog['publishTime'],
                            'pictures': data_blog['pictures'],
                            'contents': data_blog['contents']
                        }
                    }
                    updatedata(data_blogs, MONGODB_TABLE_1)
                elif data_photo:
                    data_photos = {
                        'title': title,
                        'url': item,
                        'info': {
                            'dutyeditor': data_photo['dutyeditor'],
                            'datetime': data_photo['datetime'],
                            'source': data_photo['source'],
                            'pictures': data_photo['pictures'],
                            'contents': data_photo['contents']
                        }
                    }
                    updatedata(data_photos, MONGODB_TABLE_1)
        except IndexError:
            print('无法获取该页面标题')
            pass


# Bug:在mainspider之间互相引用包,出现无法找到包来源(找不到解决方法,只有覆写方法,即updatedata())
# from neteasenews.spider.mainSpider import updatedata
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


# 针对某些网页为图片浏览形式,正则匹配关键字段,加载为json文档.
def json_details(picture_url):
    html = get_photo_source(picture_url)
    # 正则匹配源代码里面的js代码并且处理并且生成json文档,这里处理操作简单.
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


# 部署爬取新闻排行榜流程:
def rankspider():
    rank_urls = get_rank_urls()
    pool = Pool(5)
    pool.map(parse_rank, rank_urls)


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


# 部署爬取首页json文档,因为首页展示的信息具有实时性,所以用于热更新
def hotspider():
    pool = Pool(10)
    pool.map(parse, JSON_INDEX_URLS)


# 部署爬取所有json文档,内容包含以往,现在.
def spider():
    url_data = get_all_urls()
    pool = Pool(10)
    pool.map(parse, url_data)
