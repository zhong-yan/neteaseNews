# 数读标签
from neteasenews.spider.datablogSpider import datablogspider
# 国内,国际,社会,军事,航空,无人机标签
# from neteasenews.spider.mainSpider import managerspider
# 图片标签
# from neteasenews.spider.photoSpider import photospider
# 首页,排行,新闻学院,政务,公益,媒体标签
# from neteasenews.spider.moreSpider import indexspider, rankspider, collegespider, govspider, gongyispider, mediaspider

# 部署爬虫唯一出入口main()方法

if __name__ == "__main__":
    datablogspider()
