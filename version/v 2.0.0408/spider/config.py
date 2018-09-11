import pymongo
from selenium import webdriver


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

# 排行榜里面的分类
# 进程所需的迭代参数.
RANK_URL = ['http://news.163.com/special/0001386F/rank_news.html',
            'http://news.163.com/special/0001386F/rank_ent.html',
            'http://news.163.com/special/0001386F/rank_sports.html',
            'http://money.163.com/special/002526BH/rank.html',
            'http://news.163.com/special/0001386F/rank_tech.html',
            'http://news.163.com/special/0001386F/rank_auto.html',
            'http://news.163.com/special/0001386F/rank_lady.html',
            'http://news.163.com/special/0001386F/rank_house.html',
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

# 网易新闻首页
MONGODB_TABLE_0 = 'index'
# 排行
MONGODB_TABLE_1 = 'rank'
# 图片
MONGODB_TABLE_2 = 'pictures'
# 国内
MONGODB_TABLE_3 = 'domestic'
# 国际
MONGODB_TABLE_4 = 'world'
# 社会
MONGODB_TABLE_5 = 'sociology'
# 数读
MONGODB_TABLE_6 = 'datablog'
# 军事
MONGODB_TABLE_7 = 'military'
# 航空
MONGODB_TABLE_8 = 'aviation'
# 无人机
MONGODB_TABLE_9 = 'uav'
# 新闻学院
MONGODB_TABLE_10 = 'college'
# 政务
MONGODB_TABLE_11 = 'government'
# 公益
MONGODB_TABLE_12 = 'gongyi'
# 媒体
MONGODB_TABLE_13 = 'media'

client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
neteasenews = client[MONGODB_DBNAME]


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

