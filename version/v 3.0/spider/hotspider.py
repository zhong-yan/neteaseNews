import json
import requests
from requests.exceptions import RequestException
from .config import JSON_INDEX_URLS
from .contents import info_news, info_datalog, info_dy
from multiprocessing.pool import Pool
from .db import updatedata, MONGODB_TABLE_1


# 爬取首页要闻,广州,社会,国内,国际,独家,军事,财经,科技,体育,娱乐,时尚,汽车,房产,航空,健康,无人机
# 现在这个方法可以所有json
def parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 解析json,运用replace()使得该字符串符合json语法,否则会出现编码解码异常,即无法loads()
            response_json = json.loads(response.text.replace('data_callback(', '').replace(')', ''))
            for item in response_json:
                # 网易正文
                data_news = info_news(item.get('docurl'))
                # 数读平台
                data_datablog = info_datalog(item.get('docurl'))
                # 网易号:
                data_dy = info_dy(item.get('docurl'))
                if data_news:
                    infomation_news = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_news
                    }
                    updatedata(infomation_news, MONGODB_TABLE_1)
                elif data_datablog:
                    infomation_datalog = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_datablog
                    }
                    updatedata(infomation_datalog, MONGODB_TABLE_1)
                elif data_dy:
                    infomation_dy = {
                        'title': item.get('title'),
                        'label': item.get('label'),
                        'comments': item.get('tienum'),
                        'updatetime': item.get('time'),
                        'keywords': [key.get('keyname') for key in item.get('keywords')],
                        'url': item.get('docurl'),
                        'info': data_dy
                    }
                    updatedata(infomation_dy, MONGODB_TABLE_1)
    except RequestException:
        pass
    except ConnectionError:
        print('连接失败,请重试!')
        pass


# 在广东有两个callback.js,默认广东,这个是根据请求头里面IP来判断的
# http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE
def gd_city_infos():
    # 存储指定城市的json
    news_city = []
    citys = []
    response = requests.get('http://house.163.com/special/00078GU8/guangdong_xw_news_v1.js?callback=XW_NEWS_PROVINCE')
    if response.status_code == 200:
        response_city = json.loads(response.text.replace('XW_NEWS_PROVINCE(', '').replace(')', ''))
        for k in response_city.values():
            if k.get('inc'):
                # 存储到最初的列表
                citys.append(k.get('inc'))
    city_domain = 'http://house.163.com/special/00078GU7/'
    # ajax变化规律在foshan_xw_news_v1.js,v1那里,修改并递进
    for a_city in citys:
        city_name = a_city.split('/')[5]
        for num in range(2, 6):
            next_city = city_domain + city_name.split('.')[-2] + '_0{}'.format(num) + '.js'
            # 存储变化的列表
            news_city.append(next_city)
    gd_city = citys + news_city
    return gd_city
# 返回所有关于广东各城市的新闻文档


# 处理所有json文档的下一步,即js渲染的ajax内容
def get_next_urls():
    link = []
    for item in JSON_INDEX_URLS:
        for num in range(2, 11):
            new_item = item.split('.js')[0] + '_0{}'.format(num) + '.js'
            link.append(new_item)
    links = link + JSON_INDEX_URLS + gd_city_infos()
    return links


def hotspider():
    pool = Pool(5)
    pool.map(parse, JSON_INDEX_URLS)


def spider():
    url_data = get_next_urls()
    pool = Pool(5)
    pool.map(parse, url_data)


if __name__ == '__main__':
    spider()
