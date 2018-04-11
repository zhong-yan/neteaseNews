BASE_URL = 'http://news.163.com/'
# 首页ajax内容,无人机ajax,其实后面?callback=data_callback'可以省略
JSON_INDEX_URLS = [
    'http://temp.163.com/special/00804KVA/cm_yaowen.js?callback=data_callback',
    'http://house.163.com/special/00078GU7/guangzhou_xw_news_v1.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_shehui.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_dujia.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_war.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_money.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_tech.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_sports.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_ent.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_lady.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_auto.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_houseguangzhou.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_hangkong.js?callback=data_callback',
    'http://temp.163.com/special/00804KVA/cm_jiankang.js?callback=data_callback',
    # 新增无人机标签
    'http://news.163.com/uav/special/000189N0/uav_index.js?callback=data_callback'
]
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

# config mongoDB
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'neteasenews'
# 存储热更新的内容, 即更新频率快的
MONGODB_TABLE_1 = 'article'
# 存储新闻排行榜内容, 即更新频率中等
MONGODB_TABLE_2 = 'newsrank'
# 存储冷更新的内容,即更新时间长的
MONGODB_TABLE_3 = 'coldpage'
# 存储图片数据
MONGODB_TABLE_4 = 'picture'



