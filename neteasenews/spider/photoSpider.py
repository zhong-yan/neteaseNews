import re
import json
import time
import requests
from neteasenews.spider.config import webdriver, options, URLs, MONGODB_TABLE_2, neteasenews
# Bug:在mainspider之间互相引用包,出现无法找到包来源(找不到解决方法,只有覆写方法,即updatedata())
# from neteasenews.spider.mainSpider import updatedata


# http://news.163.com/photo/#Current
def photospider():
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(URLs[2])
    html_photo = browser.page_source
    # 原来结束符是\n,我真是草了.
    pattern_photo = re.compile('var galleryListData = (.*?);\n', re.S)
    result = re.search(pattern_photo, html_photo).group(1)
    if result:
        photo_json = json.loads(result)
        # json的键固定:
        result_keys = ['ss', 'kk', 'jx', 'ch', 'js', 'hk', 'ts', 'zm']
        if photo_json and "ss" in photo_json.keys():
            for items in result_keys:
                result_items = photo_json.get(items)
                for item in result_items:
                    data_list = json_details(item.get('seturl'))
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
                    updatedata(data, MONGODB_TABLE_2)
    time.sleep(5)
    browser.close()


# 针对某些网页为图片浏览形式,正则匹配关键字段,加载为json文档.
def json_details(picture_url):
    html = requests.get(picture_url)
    pattern_pictures = re.compile(r'<textarea name="gallery-data" style="display:none;">(.*?)</textarea>',re.S)
    results = re.search(pattern_pictures, html.text).group(1)
    result_json = json.loads(results)
    if result_json and 'info' in result_json.keys():
        item_info = result_json.get('info')
        item_pic = result_json.get('list')
        pic_list = {
            'title': item_info.get('setname'),
            'source': item_info.get('source'),
            'dutyeditor': item_info.get('dutyeditor'),
            'datetime': item_info.get('lmodify'),
            'imgsum': item_info.get('imgsum'),
            'pictures': [item.get('img') for item in item_pic]
        }
        return pic_list


def updatedata(data, tablename):
    if neteasenews[tablename].update({'url': data['url']}, {'$set': data}, True):
        print('--------------------------------------------------------------------------------------\n')
        print('更新存储到mongodb数据库成功,目前文档数:{0}\t\n\n数据展示:{1}'.format(neteasenews[tablename].find().count(), data))
        return True


if __name__ == '__main__':
    photospider()
