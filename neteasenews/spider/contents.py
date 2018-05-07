import json
import re
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from selenium import webdriver


# chromedriver配置信息:
options = webdriver.ChromeOptions()
# 开启无界面模式
options.add_argument('--headless')


# 如果跳转页面为网易正文
def info_news(url_news):
    try:
        page = requests.get(url_news)
        if page.status_code == 200:
            response = BeautifulSoup(page.text, 'lxml')
            # 正文内容
            article = response.select('.post_text')
            # 文章来源
            source = response.select('#ne_article_source')
            # 责任编辑
            author = response.select('.ep-editor')
            # 图片url
            pics = response.select('#endText > p.f_center > img')
            # 如果存在所选择的标签,我们则认为其为网易正文架构
            if article and author:
                for art, sou, au, in zip(article, source, author):
                    data_news = {
                        'dutyeditor': au.get_text().split('：')[1],
                        'source': sou.get_text(),
                        'pictures': [pic.get('src') for pic in pics],
                        'contents': [page for page in art.stripped_strings][:-2]
                    }
                    return data_news
    except ConnectionError:
        print('网络连接失败')
        info_news(url_news)
    except RequestException:
        print('请求失败,重试中')
        info_news(url_news)


# 如果跳转的是datalog页面
def info_datalog(url_blog):
    if 'data.163.com' in url_blog.split('/'):
        try:
            page = requests.get(url_blog)
            if page.status_code == 200:
                response = BeautifulSoup(page.text, 'lxml')
                pics = response.select('#endText > p > a.gallery.f_center > img')
                contents = response.select('.main-content')
                publishtimes_blog = response.select('#ptime')
                comments = response.select('#endpageUrl1 > a > span.js-tiejoincount')
                for content, publishtime, comment in zip(contents, publishtimes_blog, comments):
                    data_blog = {
                        'source': '数读',
                        'comments': comment.get_text(),
                        'updatetime': publishtime.get_text(),
                        'pictures': [pic.get('src') for pic in pics],
                        'contents': [item for item in content.stripped_strings]
                    }
                    return data_blog
        except ConnectionError:
            print('网络连接失败')
            info_datalog(url_blog)
        except RequestException:
            print('请求失败,重试中')
            info_datalog(url_blog)


# 如果跳转的是网易号页面
def info_dy(url_dy):
    if 'dy.163.com' in url_dy:
        try:
            html = requests.get(url_dy)
            if html.status_code == 200:
                page_college = BeautifulSoup(html.text, 'lxml')
                # 标题
                title = page_college.findAll('title')[0].get_text()
                # 摘要
                font_contents = page_college.select('.intro')
                # 内容
                contents = page_college.select('#content')
                # 图片
                pictures = page_college.select('#content > p > img')
                if title:
                    for font_content, content in zip(font_contents, contents):
                        font_c = font_content.get_text().replace('\n', '')
                        next_contents = [page for page in content.stripped_strings]
                        # 前言+正文等同文章主体
                        all_content = font_c + next_contents
                        data_dy = {
                            'title': title,
                            'url': url_dy,
                            'pictures': [item.get('src') for item in pictures if pictures],
                            'contents': all_content
                        }
                        return data_dy
        except IndexError:
            pass
        except ConnectionError:
            print('网络连接失败')
            info_dy(url_dy)
        except RequestException:
            print('请求失败,重试中')
            info_dy(url_dy)


# 如果跳转的是photoview页面
def info_photoview(url_photo):
    if 'photoview' in url_photo.split('/'):
        data_list = json_details(url_photo)
        if data_list:
            data_photo = {
                'dutyeditor': data_list['dutyeditor'],
                'updatetime': data_list['datetime'],
                'source': data_list['source'],
                'pictures': data_list['pictures'],
                'contents': data_list['contents']
            }
            return data_photo


# 处理源代码里面的js代码
def json_details(picture_url):
    try:
        response = requests.get(picture_url)
        if response.status_code == 200:
            pattern_pictures = re.compile(r'<textarea.*?>(.*?)</textarea>', re.S)
            results = re.search(pattern_pictures, response.text)
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
    except ConnectionError:
        print('网络连接失败')
        json_details(picture_url)
    except RequestException:
        print('请求失败,重试中')
        json_details(picture_url)
