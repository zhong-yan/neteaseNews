import re
import requests
from bs4 import BeautifulSoup
from neteasenews.spider.mainSpider import details, savedata
from neteasenews.spider.config import RANK_URL, MONGODB_TABLE_1
from multiprocessing import Pool


# css选择器难用,这个架构就设置为一下data所示吧,过几天再完善
# 具体思路为,正则筛选出url,然后请求url再组合成文档.
# http://news.163.com/rank/
def rankspider(url):
    links_list = []
    patterns = re.compile(r'^http:\/\/[\w]+\.163\.com\/\d+\/\d+\/\d+\/\w+.html')
    html = requests.get(url)
    htmlpage = BeautifulSoup(html.text, 'lxml')
    links = htmlpage.findAll('a')
    for link in links:
        if link.get('href'):
            if re.search(patterns, link.get('href')):
                re_links = re.search(patterns, link.get('href')).group(0)
                links_list.append(re_links)
    for item in links_list:
        data = details(item)
        if data:
            savedata(data, MONGODB_TABLE_1)


if __name__ == '__main__':
    pool = Pool(2)
    pool.map(rankspider, RANK_URL)
    pool.close()
