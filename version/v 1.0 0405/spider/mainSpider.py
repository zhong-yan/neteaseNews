import re
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from multiprocessing import Pool
# 开启startmap方法库
# from itertools import *
from .config import options, systemtime, neteasenews, URLs, MONGODB_TABLE_3, MONGODB_TABLE_7, \
    MONGODB_TABLE_4, MONGODB_TABLE_8, MONGODB_TABLE_5, MONGODB_TABLE_9


def chrome_driver(_url):
    timeout = 0
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(_url)
    response = requests.get(_url)
    try:
        if response.status_code == 200:
            wait = WebDriverWait(browser, 10)
            if wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.post_addmore'))):
                actions = ActionChains(browser)
                btn = browser.find_element_by_css_selector('.load_more_btn')
                if btn:
                    actions.move_to_element(btn).double_click(btn).perform()
                while True:
                    # 模拟JS下拉保证所有内容加载
                    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    timeout += 1
                    # 控制下拉程度的,一般100以上,200以内即可,不过也是挺随便的嘛
                    if timeout == 500:
                        break
            return browser.page_source
        print('wifi网络出现错误,或者其他网络问题')
    except ConnectionAbortedError:
        print('本地连接出现问题')
        pass
    except ConnectionError:
        print('连接失败,重试中')
        pass
    except WebDriverException:
        print('chrome驱动程序出现问题,不关我的事')
        pass


def mainspider(links_world, table):
    htmlpage = chrome_driver(links_world)
    page = BeautifulSoup(htmlpage, 'lxml')
    titles = page.select('.news_title > h3 > a')
    tags = page.select('.keywords')
    newstimes = page.select('.time')
    comments = page.select('.post_recommend_tie_icon.icons')
    for title, tag, newstime, comment in zip(titles, tags, newstimes, comments):
        urls = title.get('href')
        detail = details(urls)
        if detail:
            datalist = {
                'title': title.get_text(),
                'url': title.get('href'),
                'source': detail['source'],
                'author': detail['author'],
                'comments': comment.get_text(),
                'publishTime': detail['publishTime'],
                'lastTime': systemtime + '--' + newstime.get_text(),
                'tag': [n_tag for n_tag in tag.stripped_strings],
                'tag_pics': detail['tag_pics'],
                'pictures': detail['pictures'],
                'desc_pictures': detail['desc_pictures'],
                'contents': detail['contents'],
            }
            updatedata(datalist, table)
        if detail is None:
            print('获取详情网页失败', urls)
            details(urls)


def details(url):
    page = requests.get(url)
    response = BeautifulSoup(page.text, 'lxml')
    # 处理bug1,如果文章内有视频,正文就显示为None,尽管在其他标签里面,但是每次都试图去改,收益不大.(留作记录)
    try:
        title_more = response.select('title')[0].get_text().split('_')[0]
        article = response.select('.post_text')
        source = response.select('#ne_article_source')
        author = response.select('.ep-editor')
        pics = response.select('#endText > p.f_center > img')
        # js控制的轮播图star
        is_imgs = response.select('.main')
        img_tags = response.select('.tag')
        img_overviews = response.select('.overview > p')
        # js控制的轮播图end
        publishtime = response.select('.post_time_source')
        # 开始处理图片,现在只要url,因为是js控制,现在无法找齐全url,暂时不做处理....
        # 博客架构:
        pics_in_blog = response.select('#endText > p > a.gallery.f_center > img')
        contents = response.select('.main-content')
        publishtimes_blog = response.select('#ptime')
        comments = response.select('#endpageUrl1 > a > span.js-tiejoincount')
        #
        # 如果存在这个.main 代表是图集,分析网页而来的
        if is_imgs:
            for img_tag, img_overview in zip(img_tags, img_overviews):
                data = {
                    # 如果需要删除多余的空白或者换行符,stripped_strings,切片处理多余的来源和作者信息
                    'title': title_more,
                    'url': url,
                    'author': None,
                    'publishTime': None,
                    'source': None,
                    'tag_pics': [pic for pic in img_tag.stripped_strings][:0],
                    'pictures': None,
                    'desc_pictures': img_overview.get_text(),
                    'contents': None
                }
                return data
        # 正文含有图片
        # 如果.f_center存在 代表文中有图片
        if pics:
            for art, sou, au, ptime in zip(article, source, author, publishtime):
                # 格式化时间,记得group(0),不然返回的是<_sre.SRE_Match object; span=(12, 32), match=' 2018-04-04 08:38:46' 苦逼的废物
                format_time = re.search(r'(\d+-\d+-\d+\s\d+:\d+:\d+)', ptime.get_text()).group(0)
                data = {
                    # 如果需要删除多余的空白或者换行符,stripped_strings,切片处理多余的来源和作者信息
                    'title': title_more,
                    'url': url,
                    'author': au.get_text().split('：')[1],
                    'publishTime': format_time,
                    'source': sou.get_text(),
                    'tag_pics': None,
                    'pictures': [pic.get('src') for pic in pics],
                    'desc_pictures': None,
                    'contents': [page for page in art.stripped_strings][:-2]
                }
                return data
        # 正文没有图片
        # 图片什么的都没有,只有空白的文字,如同冰冷的暮色,这么苍凉无助
        for art, sou, au, ptime in zip(article, source, author, publishtime):
            format_time = re.search(r'(\d+-\d+-\d+\s\d+:\d+:\d+)', ptime.get_text()).group(0)
            data = {
                # 如果需要删除多余的空白或者换行符,stripped_strings,切片处理多余的来源和作者信息
                'title': title_more,
                'url': url,
                'author': au.get_text().split('：')[1],
                'publishTime': format_time,
                'source': sou.get_text(),
                'tag_pics': None,
                'pictures': None,
                'desc_pictures': None,
                'contents': [page for page in art.stripped_strings][:-2]
            }
            return data
        if publishtimes_blog and contents:
            for content, publishtime, comment in zip(contents, publishtimes_blog, comments):
                data = {
                    'title': title_more,
                    'url': url,
                    'author': None,
                    'source': None,
                    'comments': comment.get_text(),
                    'publishTime_blog': None,
                    'publishTime_news': publishtime.get_text(),
                    'pictures': [pic.get('src') for pic in pics_in_blog],
                    'contents': [item for item in content.stripped_strings]
                }
                return data
    except IndexError:
        print('该文章源代码head标签里没有title标签,暂时没找到很好的方法.')
        pass


'''
1. details_world中,使用字典的某个键值时出错：TypeError: ‘NoneType’ object is not subscriptable
原因: 生成了空字典
解决方法: 判断非空字典
2. 如何处理详情页的视频问题?
解决方法: 
'''


def updatedata(data, tablename):
    if neteasenews[tablename].update({'url': data['url']}, {'$set': data}, True):
        print('--------------------------------------------------------------------------------------\n')
        print('更新存储到mongodb数据库成功,目前文档数:{0}\t\n\n数据展示:{1}'.format(neteasenews[tablename].find().count(), data))
        return True


def savedata(data, tablename):
    if neteasenews[tablename].insert(data):
        print('--------------------------------------------------------------------------------------\n')
        print('更新存储到mongodb数据库成功,目前文档数:{0}\t\n\n数据展示:{1}'.format(neteasenews[tablename].find().count(), data))
        return True


if __name__ == '__main__':
    # 国内, 社会, 国际:
    # 军事, 无人机, 航空
    while True:
        list_table = [(URLs[3], MONGODB_TABLE_3), (URLs[4], MONGODB_TABLE_4), (URLs[5], MONGODB_TABLE_5),
                      (URLs[7], MONGODB_TABLE_7), (URLs[8], MONGODB_TABLE_8), (URLs[9], MONGODB_TABLE_9)]
        pool = Pool(6)
        # 为什么会有7个chrome,原因是因为运行了config文件,解决方案,在mainspider里面写浏览器对象
        pool.starmap(mainspider, [item for item in list_table])
        pool.close()

        print('数据爬取成功,并且成功存储到数据库中')
