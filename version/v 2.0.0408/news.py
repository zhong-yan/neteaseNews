import time
# 数读标签
from .spider.datablogSpider import datablogspider
# 国内,国际,社会,军事,航空,无人机标签
from .spider.mainSpider import managerspider
# 图片标签
from .spider.photoSpider import photospider
# 首页,排行,新闻学院,政务,公益,媒体标签
from .spider.moreSpider import indexspider, rankspider, collegespider, govspider, gongyispider, mediaspider
from .spider.config import *


# 考虑加入downloads()方法,分类下载到本地?
def newsSpider():
    print('============================================================\n')
    print('neteasenews Spider is working now, give me some patience,ok?\n')
    print('============================================================\n')
    print('现在进行的标签:"首页",爬虫运行中.....\n')
    indexspider()
    print('爬取"首页"成功\t\t大吉大利\t\t今晚吃鸡!')
    print('------------------------------------------------------------\n')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"排行",爬虫运行中.....\n')
    rankspider()
    print('爬取"排行"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"图片",爬虫运行中.....\n')
    photospider()
    print('爬取"图片"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"数读",爬虫运行中.....\n')
    datablogspider()
    print('爬取"数读"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')
    print('现在进行的标签:"国内",爬虫运行中.....\n')
    print('现在进行的标签:"国际",爬虫运行中.....\n')
    print('现在进行的标签:"社会",爬虫运行中.....\n')
    print('现在进行的标签:"军事",爬虫运行中.....\n')
    print('现在进行的标签:"航空",爬虫运行中.....\n')
    print('现在进行的标签:"无人机",爬虫运行中.....\n')
    managerspider()
    print('6个标签页内容爬取成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"新闻学院",爬虫运行中.....\n')
    collegespider()
    print('爬取"新闻学院"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"政务",爬虫运行中.....\n')
    govspider()
    print('爬取"政务"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"公益",爬虫运行中.....\n')
    gongyispider()
    print('爬取"公益"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')

    print('现在进行的标签:"媒体",爬虫运行中.....\n')
    mediaspider()
    print('爬取"媒体"成功\t\t大吉大利\t\t今晚吃鸡!')
    for i in range(5, 0, -1):
        time.sleep(1)
        print('Please wait for {}s, we will go to next step!'.format(i))
        print('------------------------------------------------------------\n')
    print('============================================================\n')
    print('neteasenews Spider is off, next step, i will show you the data what have crawled\n')
    print('============================================================\n')
    print('\n\n')
    print('首页(index)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_0].find().count()))
    print('------------------------------------------------------------\n')
    print('排行(rank)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_1].find().count()))
    print('------------------------------------------------------------\n')
    print('图片(pictures)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_2].find().count()))
    print('------------------------------------------------------------\n')
    print('国内(domestic)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_3].find().count()))
    print('------------------------------------------------------------\n')
    print('国际(world)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_4].find().count()))
    print('------------------------------------------------------------\n')
    print('社会(sociology)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_5].find().count()))
    print('------------------------------------------------------------\n')
    print('数读(datablog)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_6].find().count()))
    print('------------------------------------------------------------\n')
    print('军事(military)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_7].find().count()))
    print('------------------------------------------------------------\n')
    print('航空(aviation)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_8].find().count()))
    print('------------------------------------------------------------\n')
    print('无人机(uav)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_9].find().count()))
    print('------------------------------------------------------------\n')
    print('新闻学院(college)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_10].find().count()))
    print('------------------------------------------------------------\n')
    print('政务(government)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_11].find().count()))
    print('------------------------------------------------------------\n')
    print('公益(gongyi)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_12].find().count()))
    print('------------------------------------------------------------\n')
    print('媒体(media)文档数:\t{0}'.format(neteasenews[MONGODB_TABLE_13].find().count()))


# 部署爬虫唯一出入口main()方法
if __name__ == '__main__':
    newsSpider()
    print('============================================================\n')
    keybords = int(input('是否再次运行爬虫?(1 means yes and 0 means no)'))
    print('============================================================\n')
    if keybords == 1:
        newsSpider()
    elif keybords == 0:
        print('爬虫完毕!\t大吉大利\t今晚吃鸡')
        print('********************************************************\n')
