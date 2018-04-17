import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from neteasenews.spider.config import options


# 如何书写剔除带有视频信息的内容,保留正文,这是个值得思考的方法
# def video():


# 如果跳转页面为网易正文
def info_news(url_news):
    # 有些正文,比如说政务的是http://gov.163.com开头
    # 公益http://gongyi.163.com
    # 媒体http://media.163.com,所以需要判断or
    if 'news.163.com' or 'gov.163.com' or 'gongyi.163.com' or 'media.163.com' in url_news.split('/'):
        page = requests.get(url_news)
        response = BeautifulSoup(page.text, 'lxml')
        # 选择器
        article = response.select('.post_text')
        source = response.select('#ne_article_source')
        author = response.select('.ep-editor')
        pics = response.select('#endText > p.f_center > img')
        # 正文含有图片
        # 如果.f_center存在 代表文中有图片
        if pics:
            for art, sou, au, in zip(article, source, author):
                data_news = {
                    'dutyeditor': au.get_text().split('：')[1],
                    'source': sou.get_text(),
                    'pictures': [pic.get('src') for pic in pics],
                    'contents': [page for page in art.stripped_strings][:-2]
                }
                return data_news
        else:
            # 正文没有图片
            # 图片什么的都没有,只有空白的文字,如同冰冷的暮色,这么苍凉无助
            for art, sou, au, in zip(article, source, author):
                data_nopic = {
                    'dutyeditor': au.get_text().split('：')[1],
                    'source': sou.get_text(),
                    'pictures': None,
                    'contents': [page for page in art.stripped_strings][:-2]
                }
                return data_nopic


# 如果跳转的是photoview页面
def info_photoview(url_photo):
    if 'photoview' in url_photo.split('/'):
        data_list = json_details(url_photo)
        if data_list:
            data_photo = {
                'dutyeditor': data_list['dutyeditor'],
                'datetime': data_list['datetime'],
                'source': data_list['source'],
                'pictures': data_list['pictures'],
                'contents': data_list['contents']
            }
            return data_photo


# 如果跳转的是datalog页面
def info_datalog(url_blog):
    if 'data.163.com' in url_blog.split('/'):
        page = requests.get(url_blog)
        response = BeautifulSoup(page.text, 'lxml')
        #
        pics = response.select('#endText > p > a.gallery.f_center > img')
        contents = response.select('.main-content')
        publishtimes_blog = response.select('#ptime')
        comments = response.select('#endpageUrl1 > a > span.js-tiejoincount')
        for content, publishtime, comment in zip(contents, publishtimes_blog, comments):
            data_blog = {
                'source': '数读',
                'comments': comment.get_text(),
                'publishTime': publishtime.get_text(),
                'pictures': [pic.get('src') for pic in pics],
                'contents': [item for item in content.stripped_strings]
            }
            return data_blog


# 如果跳转的是网易号页面
def info_dy(url_dy):
    if 'dy.163.com' in url_dy:
        html = requests.get(url_dy)
        if html.status_code == 200:
            page_college = BeautifulSoup(html.text, 'lxml')
            try:
                # 标题
                title = page_college.select('title')[0].get_text()
                # 前言
                font_contents = page_college.select('.intro')
                # 内容
                contents = page_college.select('#content')
                if title:
                    for font_content, content in zip(font_contents, contents):
                        data_dy = {
                            'title': title,
                            'url': url_dy,
                            'font-contents': font_content.get_text().replace('\n', ''),
                            'contents': [page for page in content.stripped_strings]
                        }
                        return data_dy
                else:
                    for font_content, content in zip(font_contents, contents):
                        data_dy_2 = {
                            'url': url_dy,
                            'font-contents': font_content.get_text().replace('\n', ''),
                            'contents': [page for page in content.stripped_strings]
                        }
                        return data_dy_2
            except IndexError:
                pass


# 处理源代码里面的js代码
def json_details(picture_url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(picture_url)
    response = requests.get(picture_url)
    if response.status_code == 200:
        html = browser.page_source
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
