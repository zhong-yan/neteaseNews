# import requests
# from bs4 import BeautifulSoup
# import datetime as d

# print(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
#
# # 2017.12.17-09:51:07
#
# url = ['http://data.163.com/18/0401/00/DE91E1I8000181IU.html',
#        'http://news.163.com/18/0404/05/DEHARGVR0001899N.html',
#        'http://news.163.com/18/0404/05/DEHA3K280001899N.html',
#        'http://news.163.com/18/0404/04/DEH7CGLR0001899N.html']
#
# page = requests.get(url[3])
# response = BeautifulSoup(page.text, 'lxml')
# article = response.select('.post_text')
# source = response.select('#ne_article_source')
# author = response.select('.ep-editor')
# comments = response.select('.js-tiejoincount.js-tielink')
# # print(source)
# for art, sou, au, co in zip(article, source, author, comments):
#     data = {
#         'content': art.strings,
#         'source': sou.get_text(),
#         'author': au.get_text(),
#         'comments': co.get_text()
#     }
#     print(data)
#
#
# def p():
#     print('我操你妈逼的 贱货,老子跟你有仇,非要老子清考,我操你全家')
#
#
# nowtime = d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
# nexttime = d.datetime.timedelta(minutes=1)+nowtime
# print(nexttime)
# if nowtime == nexttime:
#     p()
