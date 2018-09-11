import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from .config import options, MONGODB_TABLE_6
from .mainSpider import updatedata
import re


# http://data.163.com/special/datablog/
# 这才是真实运用selenium的力量,本来已对正则无望了.
def get_page_source():
    timeout = 0
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('http://data.163.com/special/datablog/')
    response = requests.get('http://data.163.com/special/datablog/')
    if response.status_code == 200:
        while True:
            # 模拟JS下拉保证所有内容加载
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            timeout += 1
            # 控制下拉程度的,一般100以上,200以内即可,不过也是挺随便的嘛
            if timeout == 200:
                break
    return browser.page_source


def datablogspider():
    html = get_page_source()
    page = BeautifulSoup(html, 'lxml')
    infos = page.select('title')[0].get_text().split('_')[0]
    links = page.select('.post-list > li > a')
    for link in links:
        art_urls = link.get('href')
        details_blog = datablog_details(art_urls)
        if details_blog:
            data = {
                'title': infos,
                'url': link.get('href'),
                'author': details_blog['author'],
                'source': details_blog['source'],
                'publishTime_blog': details_blog['publishTime_blog'],
                'publishTime_news': details_blog['publishTime_news'],
                'pictures_blog': details_blog['pictures_blog'],
                'pictures_news': details_blog['pictures_news'],
                'contents': details_blog['contents']
            }
            updatedata(data, MONGODB_TABLE_6)
        if details_blog is None:
            datablog_details(art_urls)
            print('请求链接可能不具备可以爬取条件')
            pass


# 先获取文本内容先,图片再说(已解决图片链接,下一步是利用mongodb存储图片:18-04-05-09:22:24)
def datablog_details(url):
    details_html = requests.get(url)
    details_page = BeautifulSoup(details_html.text, 'lxml')
    # 数读1页面,网易新闻架构
    article = details_page.select('.post_text')
    source = details_page.select('#ne_article_source')
    author = details_page.select('.ep-editor')
    # 图片有一个bug: 有一些图片不在选择器里面.只有部分图片(待解决0405-10:15:50)
    pics_in_wangyi = details_page.select('#endText > p.f_center > a')
    publishtime = details_page.select('.post_time_source')
    # 数读2页面:blog(未解决博客里面图片链接,暂时设置为None)
    pics_in_blog = details_page.select('#endText > p > a.gallery.f_center > img')
    contents = details_page.select('.main-content')
    publishtimes_blog = details_page.select('#ptime')
    if publishtimes_blog and contents:
        for content, publishtime in zip(contents, publishtimes_blog):
            data = {
                'author': None,
                'source': None,
                'publishTime_blog': None,
                'publishTime_news': publishtime.get_text(),
                'pictures_blog': [pic.get('src') for pic in pics_in_blog],
                'pictures_news': None,
                'contents': [item for item in content.stripped_strings]
            }
            return data
    for art, so, au, ptime in zip(article, source, author, publishtime):
        # 格式化时间,记得group(0),不然返回的是<_sre.SRE_Match object; span=(12, 32), match=' 2018-04-04 08:38:46' 苦逼的废物
        format_time = re.search(r'(\d+-\d+-\d+\s\d+:\d+:\d+)', ptime.get_text()).group(0)
        data = {
            # 如果需要删除多余的空白或者换行符,stripped_strings,切片处理多余的来源和作者信息
            'author': au.get_text().split('：')[1],
            'source': so.get_text(),
            'publishTime_blog': None,
            'publishTime_news': format_time,
            'pictures_blog': None,
            'pictures_news': [pic.get('src') for pic in pics_in_wangyi],
            'contents': [page for page in art.stripped_strings][:-2]
        }
        return data


if __name__ == '__main__':
    datablogspider()
