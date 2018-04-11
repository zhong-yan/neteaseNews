import re
import json
import requests
from selenium import webdriver
from neteasenews.spider.db import updatedata, MONGODB_TABLE_4
from multiprocessing.pool import Pool


# Bug:在mainspider之间互相引用包,出现无法找到包来源(找不到解决方法,只有覆写方法,即updatedata())
# from neteasenews.spider.mainSpider import updatedata

# database config

# config chromedriver:
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        # 'javascript': 2
        # 'User-Agent': ua
    }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_argument('--headless')

# 图片url:
pic_tabs = ['http://news.163.com/photo/#Current'
            'http://news.163.com/photo/#Insight',
            'http://news.163.com/photo/#Week',
            'http://news.163.com/photo/#Special',
            'http://news.163.com/photo/#War',
            'http://news.163.com/photo/#Hk',
            'http://news.163.com/photo/#Discovery',
            'http://news.163.com/photo/#Paper']


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
    pool = Pool(5)
    pool.map(photo, pic_tabs)
