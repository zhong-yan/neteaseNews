import pymongo
import datetime
from selenium import webdriver
import re


BASE_URL = 'http://news.163.com/'

URLs = ['http://news.163.com/',
        'http://news.163.com/rank/',
        'http://news.163.com/photo/#Current',
        'http://news.163.com/domestic/',
        'http://news.163.com/world/',
        'http://news.163.com/shehui/',
        'http://data.163.com/special/datablog/',
        'http://war.163.com/',
        'http://news.163.com/air/',
        'http://news.163.com/uav/',
        'http://news.163.com/college',
        'http://gov.163.com/',
        'http://gongyi.163.com/',
        'http://media.163.com/']

pattern = re.compile(r'^http:\/\/[\w]+\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_news = re.compile(r'^http:\/\/news\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_money = re.compile(r'^http:\/\/money\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_auto = re.compile(r'^http:\/\/auto\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_tech = re.compile(r'^http:\/\/news\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_ent = re.compile(r'^http:\/\/tech\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_sports = re.compile(r'^http:\/\/sports\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_mobile = re.compile(r'^http:\/\/mobile\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_digi = re.compile(r'^http:\/\/digi\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_gz_house = re.compile(r'^http:\/\/gz\.house\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_home = re.compile(r'^http:\/\/home\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_edu = re.compile(r'^http:\/\/edu\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_bendi_news = re.compile(r'^http:\/\/bendi\.news\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_jiankang = re.compile(r'^http:\/\/jiankang\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_art = re.compile(r'^http:\/\/art\.163\.com\/18\/\d+\/\d+\/\w+.html')

pattern_dy = re.compile(r'^http:\/\/dy\.163\.com\/18\/\d+\/\d+\/\w+.html')

RANK_URL = ['http://news.163.com/special/0001386F/rank_news.html',
            'http://news.163.com/special/0001386F/rank_ent.html',
            'http://news.163.com/special/0001386F/rank_sports.html',
            'http://money.163.com/special/002526BH/rank.html',
            'http://news.163.com/special/0001386F/rank_tech.html',
            'http://news.163.com/special/0001386F/rank_auto.html',
            'http://news.163.com/special/0001386F/rank_lady.html',
            'http://news.163.com/special/0001386F/rank_house.html',
            # 读书的文章结构不符合我的需要,就是我不想在写方法,咋的啦
            # 视频也是..麻烦.url我都不想看到
            # 图集排行榜也是一样的,吐了
            'http://news.163.com/special/0001386F/game_rank.html',
            'http://news.163.com/special/0001386F/rank_travel.html',
            'http://news.163.com/special/0001386F/rank_edu.html',
            'http://news.163.com/special/0001386F/rank_gongyi.html',
            'http://news.163.com/special/0001386F/rank_campus.html',
            'http://news.163.com/special/0001386F/rank_media.html',
            'http://news.163.com/special/rank_m/',
            'http://news.163.com/special/0001386F/rank_whole.html']
# config mongoDB
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'neteasenews'
# 网易新闻首页,非网易首页,具体可观察url
MONGODB_TABLE_0 = 'index'
# 排行
MONGODB_TABLE_1 = 'rank'
# 图片
MONGODB_TABLE_2 = 'current'
# 国内
MONGODB_TABLE_3 = 'domestic'
# 国际
MONGODB_TABLE_4 = 'world'
# 社会
MONGODB_TABLE_5 = 'shehui'
# 数读
MONGODB_TABLE_6 = 'datablog'
# 军事
MONGODB_TABLE_7 = 'war'
# 航空
MONGODB_TABLE_8 = 'air'
# 无人机
MONGODB_TABLE_9 = 'uav'
# 新闻学院
MONGODB_TABLE_10 = 'college'
# 政务
MONGODB_TABLE_11 = 'gov'
# 公益
MONGODB_TABLE_12 = 'gongyi'
# 媒体
MONGODB_TABLE_13 = 'media'
"""

"""
client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
neteasenews = client[MONGODB_DBNAME]
# 建表
index = neteasenews[MONGODB_TABLE_0]
rank = neteasenews[MONGODB_TABLE_1]
domestic = neteasenews[MONGODB_TABLE_3]
world = neteasenews[MONGODB_TABLE_4]
shehui = neteasenews[MONGODB_TABLE_5]
datablog = neteasenews[MONGODB_TABLE_6]
war = neteasenews[MONGODB_TABLE_7]
air = neteasenews[MONGODB_TABLE_8]
uav = neteasenews[MONGODB_TABLE_9]
college = neteasenews[MONGODB_TABLE_10]
gov = neteasenews[MONGODB_TABLE_11]
gongyi = neteasenews[MONGODB_TABLE_12]
media = neteasenews[MONGODB_TABLE_13]
# 创建索引.
index.create_index('articleUrl')
rank.create_index('articleUrl')
world.create_index('articleUrl')
domestic.create_index('articleUrl')
shehui.create_index('articleUrl')
datablog.create_index('articleUrl')
college.create_index('articleUrl')
gov.create_index('articleUrl')
gongyi.create_index('articleUrl')
media.create_index('articleUrl')
# config chromedriver:
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        # 'javascript': 2
        # 'User-Agent': ua
    }
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_argument('--headless')

# 现在时间:
systemtime = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")

