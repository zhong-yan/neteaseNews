import requests
import re
from bs4 import BeautifulSoup
from neteasenews.spider.config import RANK_URL
from neteasenews.spider.db import MONGODB_TABLE_2, updatedata
from neteasenews.spider.contents import info_photoview, info_datalog, info_news
from multiprocessing.pool import Pool


# Rank_url里面包含许多links,可以用map()方法建立进程,否则可以遍历赋予url
# http://news.163.com/rank/
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
        # 标题
        title = page.select('title')[0].get_text()
        data_blog = info_datalog(item)
        data_news = info_news(item)
        data_photo = info_photoview(item)
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


def rankspider():
    pool = Pool(10)
    pool.map(parse_rank, RANK_URL)

