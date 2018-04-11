BASE_URL = 'http://news.163.com/'
# 首页ajax内容,无人机ajax,其实后面?callback=data_callback'可以省略
# 如何快速找到json链接?现在只能手工完成..添加每一个json文档
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
    # 无人机标签
    'http://news.163.com/uav/special/000189N0/uav_index.js?callback=data_callback',
    # 体育
    'http://sports.163.com/special/000587PR/newsdata_n_index.js?callback=data_callback',
    'http://sports.163.com/special/000587PR/newsdata_n_world.js?callback=data_callback',
    'http://sports.163.com/special/000587PR/newsdata_n_china.js?callback=data_callback',
    'http://sports.163.com/special/000587PR/newsdata_n_cba.js?callback=data_callback',
    'http://sports.163.com/special/000587PR/newsdata_n_allsports.js?callback=data_callback',
    # NBA
    'http://sports.163.com/special/000587PK/newsdata_nba_hj.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_qsh.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_ysh.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_ketr.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_okc.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_huren.js?callback=data_callback',
    'http://sports.163.com/special/000587PK/newsdata_nba_mc.js?callback=data_callback',
    # 娱乐
    'http://ent.163.com/special/000380VU/newsdata_index.js?callback=data_callback',
    'http://ent.163.com/special/000380VU/newsdata_music.js?callback=data_callback',
    'http://ent.163.com/special/000380VU/newsdata_star.js?callback=data_callback',
    'http://ent.163.com/special/000380VU/newsdata_movie.js?callback=data_callback',
    'http://ent.163.com/special/000380VU/newsdata_tv.js?callback=data_callback',
    'http://ent.163.com/special/000380VU/newsdata_show.js?callback=data_callback',
    # 财经
    'http://money.163.com/special/002557S5/newsdata_idx_index.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_stock.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_finance.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_fund.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_licai.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_biz.js?callback=data_callback',
    'http://money.163.com/special/002557S5/newsdata_idx_bitcoin.js?callback=data_callback',
    # 股票
    'http://money.163.com/special/002557S6/newsdata_gp_index.js?callback=data_callback',
    'http://money.163.com/special/002557S6/newsdata_gp_hkstock.js?callback=data_callback',
    'http://money.163.com/special/002557S6/newsdata_gp_usstock.js?callback=data_callback',
    'http://money.163.com/special/002557S6/newsdata_gp_ipo.js?callback=data_callback',
    'http://money.163.com/special/002557S6/newsdata_gp_bitcoin.js?callback=data_callback',
    'http://money.163.com/special/002557S6/newsdata_gp_dy.js?callback=data_callback',
    # 科技
    'http://tech.163.com/special/00097UHL/tech_datalist.js?callback=data_callback',
    # 全国,找不到规律,不想copy了 烦
    'http://bendi.news.163.com/beijing/special/04388GGG/bjxinxiliu.js',
    'http://bendi.news.163.com/shanghai/special/04188GP4/shxinxiliu.js',
    'http://tj.news.163.com/special/04208F5D/tjxxl.js',
    'http://bendi.news.163.com/jiangsu/special/04248H8U/njxxl.js',
    'http://bendi.news.163.com/zhejiang/special/04098FBT/xinxiliu.js',
    'http://sc.news.163.com/special/04268EVT/xinxiliu.js',
    'http://bendi.news.163.com/heilongjiang/special/04238DR5/haerbin.js',
    'http://bendi.news.163.com/jilin/special/04118E6D/center_news_cc.js',
    'http://bendi.news.163.com/liaoning/special/04228EED/xinxiliu.js',
    'http://bendi.news.163.com/neimengu/special/04138EHT/nmgxxl.js'
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



