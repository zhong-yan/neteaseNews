from neteasenews.spider.mainSpider import *
from neteasenews.spider.config import *
from multiprocessing import Pool


# css选择器难用,这个架构就设置为一下data所示吧,过几天再完善
# 具体思路为,正则筛选出url,然后请求url再组合成文档.
# http://news.163.com/rank/
def rankspider(url):
    links_list = []
    patterns = re.compile(r'^http:\/\/[\w]+\.163\.com\/18\/\d+\/\d+\/\w+.html')
    html = requests.get(url)
    htmlpage = BeautifulSoup(html.text, 'lxml')
    # 这是一个很好提取文章标题的方法,我咋忘记了,卧槽
    title = htmlpage.select('title')[0].get_text().split('_')[0]
    links = htmlpage.findAll('a')
    # 通过链接找到属性?
    for link in links:
        if link.get('href'):
            if re.search(pattern, link.get('href')):
                re_links = re.search(patterns, link.get('href')).group(0)
                links_list.append(re_links)
    for link in links_list:
        if details(link):
            detail = details(link)
            if detail:
                #
                if detail['content']:
                    data = {
                        'title': title,
                        # url
                        'articleUrl': link,
                        # 来源
                        'source': detail['source'],
                        # 作者
                        'author': detail['author'],
                        # 发表时间
                        'publishtime': detail['publishtime'],
                        # 正文
                        'content': detail['content']
                    }
                    savedata(data, MONGODB_TABLE_1)
                #
                return False
            if detail is None:
                print('获取详情网页失败', urls)
                details(link)


if __name__ == '__main__':
    pool = Pool(2)
    pool.map(rankspider, RANK_URL)
    pool.close()
    # rank 表里还缺些数据,比如tag, 点击数等等
