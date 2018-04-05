import re


from bs4 import BeautifulSoup
from neteasenews.spider.config import pattern, MONGODB_TABLE_0
from neteasenews.spider.mainSpider import chrome_driver, details, savedata


# http://news.163.com/
def get_urls():
    html = chrome_driver('http://news.163.com/')
    pagecontent = BeautifulSoup(html, 'lxml')
    links = pagecontent.findAll('a')
    links_list = []
    for link in links:
        if link.get('href'):
            if re.search(pattern, link.get('href')):
                re_links = re.search(pattern, link.get('href')).group(0)
                links_list.append(re_links)
    return links_list


def indexspider():
    all_urls = get_urls()
    for item in all_urls:
        data = details(item)
        if data:
            savedata(data, MONGODB_TABLE_0)


if __name__ == '__main__':
    indexspider()

