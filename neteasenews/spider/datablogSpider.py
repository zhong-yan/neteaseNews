import requests
from bs4 import BeautifulSoup
from neteasenews.spider.config import *
from neteasenews.spider.mainSpider import savedata
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
    # infos = page.select('.post-list > li > a > img')
    links = page.select('.post-list > li > a')
    # for info, link in zip(infos, links):
    for link in links:
        art_urls = link.get('href')
        details_blog = datablog_details(art_urls)
        if details_blog:
            data = {
                'articleUrl': link.get('href'),
                # bug
                'title': info.get('alt'),
                'author': details_blog['author'],
                'source': details_blog['source'],
                'publishtime_blog': details_blog['publishtime_blog'],
                'publishtime_wangyi': details_blog['publishtime_wangyi'],
                'imgUrl_blog': details_blog['imgUrl_blog'],
                'imgUrl_wangyi': details_blog['imgUrl_wangyi'],
                # 'imgUrl': info.get('src'),
                'content': details_blog['content']
            }
            savedata(data, MONGODB_TABLE_6)
        if datablog is None:
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
                'publishtime_wangyi': None,
                'publishtime_blog': publishtime.get_text(),
                'imgUrl_blog': [pic.get('src') for pic in pics_in_blog],
                'imgUrl_wangyi': None,
                'content': [item for item in content.stripped_strings]
            }
            return data
    for art, so, au, ptime in zip(article, source, author, publishtime):
        # 格式化时间,记得group(0),不然返回的是<_sre.SRE_Match object; span=(12, 32), match=' 2018-04-04 08:38:46' 苦逼的废物
        format_time = re.search(r'(\d+-\d+-\d+\s\d+:\d+:\d+)', ptime.get_text()).group(0)
        data = {
            # 如果需要删除多余的空白或者换行符,stripped_strings,切片处理多余的来源和作者信息
            'author': au.get_text().split('：')[1],
            'source': so.get_text(),
            'publishtime_blog': None,
            'publishtime_wangyi': format_time,
            'imgUrl_blog': None,
            'imgUrl_wangyi': [pic.get('src') for pic in pics_in_wangyi],
            'content': [page for page in art.stripped_strings][:-2]
        }
        return data


if __name__ == '__main__':
    datablogspider()
'''
仔细观察page_source,发现文档就才在js代码里,可以通过正则找出来
放弃正则,json.loads根本就格式不了,采用传统选择器手法,传统根本做不了
pattern = re.compile('var ohnofuchlist=\[\n(.*?)"a"\];', re.S)
result = re.search(pattern, response.text)
if result:
解决非法字符串无法loads为json格式,非法,'a'和一对[],我日呀
r_json = result.group(1).replace('[', '{').replace(']', '}')
r_json = result.group(1)
print(r_json)
'''