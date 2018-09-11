import time
from neteasenews.spider.coldspider import datablogspider, collegespider, govspider, gongyispider, mediaspider
from neteasenews.spider.hotspider import hotspider, spider
from neteasenews.spider.rankspider import rankspider
# from neteasenews.spider.photospider import photospider
from neteasenews.spider.config import JSON_INDEX_URLS
from multiprocessing.pool import Pool


# 考虑加入downloads()方法,分类下载到本地?
# def downloads()

# 部署爬虫唯一出入口main()方法
if __name__ == '__main__':
    print('neteasenews Spider is working now, give me some patience,ok?\n')
    print('爬取排行标签:')
    rankspider()
    time.sleep(5)
    try:
        print('爬取国内,国际,社会,军事,航空,无人机')
        managerspider()
    except None:
        pass
    print('开启冷更新,这些标签更新频率不大')
    photospider()
    list_spider = [indexspider, datablogspider, collegespider, govspider, gongyispider, mediaspider]
    pools = Pool(7)
    pools.map(newsSpider, list_spider)
    print('============================================================\n')
    keybords = int(input('是否再次运行爬虫?(1 means yes and 0 means no)\n'))
    print('============================================================\n')
    if keybords == 1:
        print('neteasenews Spider is working now, give me some patience,ok?\n')
        print('爬取排行标签:')
        rankspider()
        try:
            print('爬取国内,国际,社会,军事,航空,无人机')
            managerspider()
        except None:
            pass
        print('开启冷更新,这些标签更新频率不大')
        list_spider = [indexspider, photospider, datablogspider, collegespider, govspider, gongyispider, mediaspider]
        pools = Pool(7)
        pools.map(newsSpider, list_spider)
    elif keybords == 0:
        print('爬虫完毕!\t大吉大利\t今晚吃鸡')
        print('********************************************************\n')
